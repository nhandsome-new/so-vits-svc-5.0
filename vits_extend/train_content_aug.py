import os
import time
import logging
import math
import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributed import init_process_group
from torch.nn.parallel import DistributedDataParallel
import itertools
import traceback

from vits_extend.dataloader_content_aug import create_dataloader_train
from vits_extend.dataloader_content_aug import create_dataloader_eval
from vits.models_content_aug import SynthesizerTrn
from vits_extend.writer import MyWriter
from vits_extend.stft import TacotronSTFT
from vits_extend.stft_loss import MultiResolutionSTFTLoss
from vits_extend.validation import validate
from vits_decoder.discriminator import Discriminator
from vits import commons
from vits.losses import kl_loss, content_emb_loss
from vits.commons import clip_grad_value_
from vits.utils import f0_to_coarse


def load_part(model, saved_state_dict):
    if hasattr(model, 'module'):
        state_dict = model.module.state_dict()
    else:
        state_dict = model.state_dict()
    new_state_dict = {}
    for k, v in state_dict.items():
        if k.startswith('TODO'):
            new_state_dict[k] = v
        else:
            new_state_dict[k] = saved_state_dict[k]
    if hasattr(model, 'module'):
        model.module.load_state_dict(new_state_dict)
    else:
        model.load_state_dict(new_state_dict)
    return model


def load_model(model, saved_state_dict, prefix=None):
    if hasattr(model, 'module'):
        state_dict = model.module.state_dict()
    else:
        state_dict = model.state_dict()
    new_state_dict = {}
    for k, v in state_dict.items():
        try:
            if prefix is not None:
                if not k.startswith(prefix):
                    continue
                k_ = k[len(prefix)+1:]
            else:
                k_ = k
            new_state_dict[k] = saved_state_dict[k_]
        except:
            print("%s is not in the checkpoint" % k_)
            print("%s is not in the model" % k)
            new_state_dict[k] = v

    if hasattr(model, 'module'):
        model.module.load_state_dict(new_state_dict)
    else:
        model.load_state_dict(new_state_dict, strict=False)
    return model


def train(rank, args, chkpt_path, hp, hp_str):

    if args.num_gpus > 1:
        init_process_group(backend=hp.dist_config.dist_backend, init_method=hp.dist_config.dist_url,
                           world_size=hp.dist_config.world_size * args.num_gpus, rank=rank)

    torch.cuda.manual_seed(hp.train.seed)
    device = torch.device('cuda:{:d}'.format(rank))

    model_g = SynthesizerTrn(
        hp.data.filter_length // 2 + 1,
        hp.data.segment_size // hp.data.hop_length,
        hp).to(device)
    model_d = Discriminator(hp).to(device)

    optim_g = torch.optim.AdamW(model_g.parameters(),
                                lr=hp.train.learning_rate_g, betas=hp.train.betas, eps=hp.train.eps)
    optim_d = torch.optim.AdamW(model_d.parameters(),
                                lr=hp.train.learning_rate_d, betas=hp.train.betas, eps=hp.train.eps)

    init_epoch = 1
    step = 0

    stft = TacotronSTFT(filter_length=hp.data.filter_length,
                        hop_length=hp.data.hop_length,
                        win_length=hp.data.win_length,
                        n_mel_channels=hp.data.mel_channels,
                        sampling_rate=hp.data.sampling_rate,
                        mel_fmin=hp.data.mel_fmin,
                        mel_fmax=hp.data.mel_fmax,
                        center=False,
                        device=device)
    # define logger, writer, valloader, stft at rank_zero
    if rank == 0:
        pth_dir = os.path.join(hp.log.pth_dir, args.name)
        log_dir = os.path.join(hp.log.log_dir, args.name)
        os.makedirs(pth_dir, exist_ok=True)
        os.makedirs(log_dir, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, '%s-%d.log' % (args.name, time.time()))),
                logging.StreamHandler()
            ]
        )
        logger = logging.getLogger()
        writer = MyWriter(hp, log_dir)
        valloader = create_dataloader_eval(hp)

    if os.path.isfile(hp.train.pretrain):
        if rank == 0:
            logger.info("Start from 32k pretrain model: %s" % hp.train.pretrain)
        checkpoint = torch.load(hp.train.pretrain, map_location='cpu')
        load_model(model_g, checkpoint['model_g'])
        load_model(model_d, checkpoint['model_d'])
        logger.info("Start from pretrain model: %s" % hp.train.pretrain)

    if chkpt_path is not None:
        if rank == 0:
            logger.info("Resuming from checkpoint: %s" % chkpt_path)
        checkpoint = torch.load(chkpt_path, map_location='cpu')
        load_model(model_g, checkpoint['model_g'])
        load_model(model_d, checkpoint['model_d'])
        optim_g.load_state_dict(checkpoint['optim_g'])
        optim_d.load_state_dict(checkpoint['optim_d'])
        init_epoch = checkpoint['epoch']
        step = checkpoint['step']

        if rank == 0:
            if hp_str != checkpoint['hp_str']:
                logger.warning("New hparams is different from checkpoint. Will use new.")
                for param_group in optim_g.param_groups:
                    param_group['lr'] = hp.train.learning_rate_g
                for param_group in optim_d.param_groups:
                    param_group['lr'] = hp.train.learning_rate_d
    else:
        if rank == 0:
            logger.info("Starting new training run.")
    
    if hp.train.pretrain_disc:
        checkpoint = torch.load(hp.train.pretrain_disc, map_location='cpu')
        load_model(model_d, checkpoint['mrd'], "MRD")
        load_model(model_d, checkpoint['mpd'], "MPD")

    if args.num_gpus > 1:
        model_g = DistributedDataParallel(model_g, device_ids=[rank])
        model_d = DistributedDataParallel(model_d, device_ids=[rank])

    # this accelerates training when the size of minibatch is always consistent.
    # if not consistent, it'll horribly slow down.
    torch.backends.cudnn.benchmark = True

    scheduler_g = torch.optim.lr_scheduler.ExponentialLR(optim_g, gamma=hp.train.lr_decay, last_epoch=init_epoch-2)
    scheduler_d = torch.optim.lr_scheduler.ExponentialLR(optim_d, gamma=hp.train.lr_decay, last_epoch=init_epoch-2)

    stft_criterion = MultiResolutionSTFTLoss(device, eval(hp.mrd.resolutions))
    spkc_criterion = nn.CosineEmbeddingLoss()

    trainloader = create_dataloader_train(hp, args.num_gpus, rank)

    for epoch in range(init_epoch, hp.train.epochs):

        trainloader.batch_sampler.set_epoch(epoch)

        if rank == 0 and epoch % hp.log.eval_interval == 0:
            with torch.no_grad():
                validate(hp, args, model_g, model_d, valloader, stft, writer, step, device)

        if rank == 0:
            loader = tqdm.tqdm(trainloader, desc='Loading train data')
        else:
            loader = trainloader

        model_g.train()
        model_d.train()

        for ppg, c1, c1_l, c2, c2_l, pit, spk, spec, spec_l, audio, audio_l in loader:

            ppg = ppg.to(device)
            c1 = c1.to(device)
            c2 = c2.to(device)
            pit = pit.to(device)
            spk = spk.to(device)
            spec = spec.to(device)
            audio = audio.to(device)
            c1_l = c1_l.to(device)
            c2_l = c2_l.to(device)
            spec_l = spec_l.to(device)
            audio_l = audio_l.to(device)
            
            # set weights update steps
            update_step = False
            if ((step + 1) % hp.train.accum_iter == 0) or (step + 1 == len(loader)):
                update_step = True
            disc_step = True if (step+1) % hp.train.disc_iter == 0 else False
            freeze_step = True if step < hp.train.freeze_step else False
            
            optim_g.zero_grad()
            optim_d.zero_grad()
            
            fake_audio, ids_slice, _, \
                (_, _, _, _, _, _, _, _, _, _), _ = model_g(
                    ppg, c1, pit, spec, spk, c1_l, spec_l)
            real_audio = commons.slice_segments(
                audio, ids_slice * hp.data.hop_length, hp.data.segment_size)  # slice
            
            # discriminator
            disc_fake = model_d(fake_audio.detach())
            disc_real = model_d(real_audio)
            
            loss_d = 0.
            loss_d_real = 0.
            loss_d_fake = 0.
            loss_d_real_rev = 0.
            
            if disc_step:
                for (_, score_fake), (_, score_real) in zip(disc_fake, disc_real):
                    # print(f"{score_real.min()=}",f"{score_real.max()=}")
                    # print(f"{score_fake.min()=}",f"{score_fake.max()=}")
                    loss_d_real += torch.mean(torch.pow(score_real - 1.0, 2))
                    loss_d_fake += torch.mean(torch.pow(score_fake, 2))
                    loss_d_real_rev += torch.mean(torch.pow(score_real, 2))
                loss_d = loss_d_real + loss_d_fake
                loss_d = loss_d / len(disc_fake)
                loss_d = loss_d * hp.train.c_dis
                
                
                loss_d_real = loss_d_real / len(disc_fake)
                loss_d_fake = loss_d_fake / len(disc_fake)
                loss_d_real_rev = loss_d_real_rev / len(disc_fake)
                
                loss_d.backward()
                clip_grad_value_(model_d.parameters(),  None)
                
                if update_step:
                    optim_d.step()
            
            
            
            
            # generator
            fake_audio, ids_slice, z_mask, \
                (z_f, z_r, z_p, m_p, logs_p, z_q, m_q, logs_q, logdet_f, logdet_r), emb_c = model_g(
                    ppg, c1, pit, spec, spk, c1_l, spec_l)
            _, _, _, _, emb_c_aug = model_g.enc_p(c2, c2_l, f0=f0_to_coarse(pit))
            real_audio = commons.slice_segments(
                audio, ids_slice * hp.data.hop_length, hp.data.segment_size)  # slice
            # Spk Loss
            spk_loss = 0
            # spkc_criterion(spk, spk_preds, torch.Tensor(spk_preds.size(0))
            #                     .to(device).fill_(1.0)) * hp.train.c_spk
            # Mel Loss
            mel_fake = stft.mel_spectrogram(fake_audio.squeeze(1))
            mel_real = stft.mel_spectrogram(real_audio.squeeze(1))
            mel_loss = F.l1_loss(mel_fake, mel_real) * hp.train.c_mel

            # Multi-Resolution STFT Loss
            sc_loss, mag_loss = stft_criterion(fake_audio.squeeze(1), real_audio.squeeze(1))
            stft_loss = (sc_loss + mag_loss) * hp.train.c_stft

            # Generator Loss
            disc_fake = model_d(fake_audio)
            score_loss = 0.0
            for (_, score_fake) in disc_fake:
                score_loss += torch.mean(torch.pow(score_fake - 1.0, 2))
            score_loss = score_loss / len(disc_fake)
            score_loss = score_loss * hp.train.c_score

            # Feature Loss
            disc_real = model_d(real_audio)
            feat_loss = 0.0
            for (feat_fake, _), (feat_real, _) in zip(disc_fake, disc_real):
                for fake, real in zip(feat_fake, feat_real):
                    feat_loss += torch.mean(torch.abs(fake - real))
            feat_loss = feat_loss / len(disc_fake)
            feat_loss = feat_loss * hp.train.c_feat
            
            # Content Loss
            loss_content_emb = (content_emb_loss(emb_c, emb_c_aug) / 2 + content_emb_loss(emb_c_aug, emb_c) / 2) * hp.train.c_cont

            # Kl Loss
            loss_kl_f = kl_loss(z_f, logs_q, m_p, logs_p, logdet_f, z_mask) * hp.train.c_kl
            loss_kl_r = kl_loss(z_r, logs_p, m_q, logs_q, logdet_r, z_mask) * hp.train.c_kl * 0.5

            # Loss
            if freeze_step:
                loss_g = mel_loss
            else:
                loss_g = score_loss + feat_loss + mel_loss + stft_loss + loss_kl_f + loss_kl_r + spk_loss + loss_content_emb
            loss_g.backward()
            clip_grad_value_(model_g.parameters(),  None)
            
            # if update_step:
            optim_g.step()
                            
            step += 1
            # logging
            loss_g = loss_g.item()
            loss_d = loss_d.item()
            loss_d_real = loss_d_real.item()
            loss_d_fake = loss_d_fake.item()
            loss_s = stft_loss.item()
            loss_m = mel_loss.item()
            loss_k = loss_kl_f.item()
            loss_r = loss_kl_r.item()
            loss_i = spk_loss
            loss_f = feat_loss.item()
            loss_c = loss_content_emb.item()
            if rank == 0 and step % hp.log.info_interval == 0:
                writer.log_training(
                    loss_g, loss_d, loss_m, loss_s, loss_k, loss_r, score_loss.item(), loss_f, loss_i, loss_c, step)
                writer.log_training_disc(
                    loss_d_real, loss_d_fake, loss_d_real_rev, step)
                writer.log_lr(
                    scheduler_g.get_last_lr()[0], scheduler_d.get_last_lr()[0], step
                )
                logger.info("epoch %d | g %.04f m %.04f s %.04f d %.04f k %.04f r %.04f i %.04f c %.04f | step %d" % (
                    epoch, loss_g, loss_m, loss_s, loss_d, loss_k, loss_r, loss_i, loss_c, step))

        if rank == 0 and epoch % hp.log.save_interval == 0:
            save_path = os.path.join(pth_dir, '%s_%04d.pt'
                                     % (args.name, epoch))
            torch.save({
                'model_g': (model_g.module if args.num_gpus > 1 else model_g).state_dict(),
                'model_d': (model_d.module if args.num_gpus > 1 else model_d).state_dict(),
                'optim_g': optim_g.state_dict(),
                'optim_d': optim_d.state_dict(),
                'step': step,
                'epoch': epoch,
                'hp_str': hp_str,
            }, save_path)
            logger.info("Saved checkpoint to: %s" % save_path)


        def clean_checkpoints(path_to_models=f'{pth_dir}', n_ckpts_to_keep=hp.log.keep_ckpts, sort_by_time=True):
            """Freeing up space by deleting saved ckpts
            Arguments:
            path_to_models    --  Path to the model directory
            n_ckpts_to_keep   --  Number of ckpts to keep, excluding sovits5.0_0.pth
                                  If n_ckpts_to_keep == 0, do not delete any ckpts
            sort_by_time      --  True -> chronologically delete ckpts
                                  False -> lexicographically delete ckpts
            """
            assert isinstance(n_ckpts_to_keep, int) and n_ckpts_to_keep >= 0
            ckpts_files = [f for f in os.listdir(path_to_models) if os.path.isfile(os.path.join(path_to_models, f))]
            name_key = (lambda _f: int(re.compile(f'{args.name}_(\d+)\.pt').match(_f).group(1)))
            time_key = (lambda _f: os.path.getmtime(os.path.join(path_to_models, _f)))
            sort_key = time_key if sort_by_time else name_key
            x_sorted = lambda _x: sorted(
                [f for f in ckpts_files if f.startswith(_x) and not f.endswith('sovits5.0_0.pth')], key=sort_key)
            if n_ckpts_to_keep == 0:
                to_del = []
            else:
                to_del = [os.path.join(path_to_models, fn) for fn in x_sorted(f'{args.name}')[:-n_ckpts_to_keep]]
            del_info = lambda fn: logger.info(f"Free up space by deleting ckpt {fn}")
            del_routine = lambda x: [os.remove(x), del_info(x)]
            rs = [del_routine(fn) for fn in to_del]

        clean_checkpoints()

        if rank == 0:
            os.makedirs(f'{pth_dir}', exist_ok=True)
            keep_ckpts = getattr(hp.log, 'keep_ckpts', 0)
            if keep_ckpts > 0:
                clean_checkpoints(path_to_models=f'{pth_dir}', n_ckpts_to_keep=hp.log.keep_ckpts, sort_by_time=True)

        scheduler_g.step()
        scheduler_d.step()
