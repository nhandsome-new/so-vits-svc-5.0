from torch.utils.tensorboard import SummaryWriter
import numpy as np
import librosa

from .plotting import plot_waveform_to_numpy, plot_spectrogram_to_numpy

class MyWriter(SummaryWriter):
    def __init__(self, hp, logdir):
        super(MyWriter, self).__init__(logdir)
        self.sample_rate = hp.data.sampling_rate

    def log_training(self, g_loss, d_loss, mel_loss, stft_loss, k_loss, r_loss, score_loss, loss_f, loss_i, loss_c, step):
        self.add_scalar('train/g_loss', g_loss, step)
        if d_loss != 0:
            self.add_scalar('train/d_loss', d_loss, step)
        
        self.add_scalar('train/score_loss', score_loss, step)
        self.add_scalar('train/stft_loss', stft_loss, step)
        self.add_scalar('train/mel_loss', mel_loss, step)
        self.add_scalar('train/kl_f_loss', k_loss, step)
        self.add_scalar('train/kl_r_loss', r_loss, step)
        self.add_scalar('train/feature_loss', loss_f, step)
        self.add_scalar('train/speaker_loss', loss_i, step)
        self.add_scalar('train/contents_loss', loss_c, step)
    
    def log_training_disc(self, d_loss_real, d_loss_fake, loss_d_real_rev, step):
        self.add_scalar('train/d_loss_real', d_loss_real, step)
        self.add_scalar('train/loss_d_real_rev', loss_d_real_rev, step)
        self.add_scalar('train/d_loss_fake', d_loss_fake, step)
        
    def log_lr(self, lr_g, lr_d, step):
        self.add_scalar('lr_g', lr_g, step)
        self.add_scalar('lr_d', lr_d, step)

    def log_validation(self, mel_loss, generator, discriminator, step):
        self.add_scalar('validation/mel_loss', mel_loss, step)

    def log_fig_audio(self, real, fake, spec_fake, spec_real, idx, step):
        if idx == 0:
            spec_fake = librosa.amplitude_to_db(spec_fake, ref=np.max,top_db=80.)
            spec_real = librosa.amplitude_to_db(spec_real, ref=np.max,top_db=80.)
            self.add_image(f'spec_fake/{step}', plot_spectrogram_to_numpy(spec_fake), step)
            self.add_image(f'wave_fake/{step}', plot_waveform_to_numpy(fake), step)
            self.add_image(f'spec_real/{step}', plot_spectrogram_to_numpy(spec_real), step)
            self.add_image(f'wave_real/{step}', plot_waveform_to_numpy(real), step)

            self.add_audio(f'fake/{step}', fake, step, self.sample_rate)
            self.add_audio(f'real/{step}', real, step, self.sample_rate)

    def log_histogram(self, model, step):
        for tag, value in model.named_parameters():
            self.add_histogram(tag.replace('.', '/'), value.cpu().detach().numpy(), step)
