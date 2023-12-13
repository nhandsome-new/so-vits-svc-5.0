python svc_inference_content_aug_from_wav.py \
 --config configs/base.yaml  \
 --model /home/mluser/so-vits-5/ckpt/fusic3_finetune_freeze/fusic3_finetune_freeze_7318.pt \
 --spk /data/fusic/hama/spkemb/hamasaki-03_DeepFilterNet3.g.pt \
 --wav /data/tmp/minna/wav/fusic_shinkawa_test.wav \
 --shift 0\ 
# --spk /data/fusic/hama/spkemb/hamasaki-03_DeepFilterNet3.g.pt \ 160 3
# --spk /data/vc_noutomi/vc_noutomi/spkemb/noutomi1-26_DeepFilterNet3.g.pt \ 140 0-2
# --spk /data/fusic_ref/minna/spkemb/nogami_DeepFilterNet3.g.pt  9
#  --device cpu
# /data/introduce/han/wav/han_fusic_DeepFilterNet3.wav
# /data/tmp/tmp/f0uv/han_fusic_DeepFilterNet3.f0.npy
# /data/karano_nhk_first_finetune_batch_2_accum_4_content_loss_3_0012.pt

# /data/karano_nhk_first_finetune_batch_2_accum_4_content_loss_3_0012.pt
# /data/fusic_ref/minna/spkemb/nogami_DeepFilterNet3.g.pt
# /data/fusic/vc_noutomi/spkemb/noutomi1-26_DeepFilterNet3.g.pt
# /data/fusic_han/han/wav/han_test_DeepFilterNet3.wav // 0020_DeepFilterNet3.wav
# /data/karanovc_min/jvs001/content/BASIC5000_0025.c.pt
# --vec /data/karanovc_min/han/content/0424_DeepFilterNet3.c.pt \
# --spk /data/karanovc_min/菅沢公平/spkemb//0001_00044_00000.g.pt \
# --pit /data/jvs001/f0uv/BASIC5000_0025.f0.npy \
# --pit /data/jvs002/f0uv/BASIC5000_0104.f0.npy \
# --pit /data/jvs010/f0uv/VOICEACTRESS100_002.f0.npy
# --pit /data/景浦大輔2/f0uv/0002_00025_00000.f0.npy \
# --pit /data/k小田切優衣1/f0uv/0000_00097_00000.f0.npy \
# --pit /data/k小田切優衣1/f0uv/0000_00097_00000.f0.npy \
# --spk /data/karanovc_min/vウマ娘_カレン/spkemb/0007_00000_00000.g.pt \
# 0010_00016_00000.wav 朴璐美2

# /data/karanovc_min/中川翔/wav/0000_00027_00000.wav
# /data/karanovc_min/景浦大輔2/wav/0002_00025_00000.wav
# /data/karanovc_min/下山吉光1/wav/0001_00002_00016.wav
# /data/karanovc_min/李ふぁい/wav/0002_00023_00000.wav

# /data/fusic/vc_noutomi/wav/noutomi1-4_DeepFilterNet3.wav
# --vec /data/fusic_han/han/content/han_test_DeepFilterNet3.c.pt \
# /data/karanovc_min/han/wav/0142_DeepFilterNet3.wav

# /data/fusic_ref/minna/spkemb/
# funagosi_DeepFilterNet3.g.pt  hirosawa_DeepFilterNet3.g.pt  nogami_DeepFilterNet3.g.pt  yuki_DeepFilterNet3.g.pt
# /data/fusic_ref/funakoshi/wav/funakoshi_long_DeepFilterNet3.wav

# /data/fusic/hama/wav/hamasaki-03_DeepFilterNet3.wav

# /data/tmp/minna/
# fusic_hamasaki_test.wav    fusic_noutomi_test.wav     fusic_oda_test.wav         
# fusic_sakuragawa_test.wav  fusic_shinkawa_test.wav    fusic_sugimoto_test.wav    fusic_yoshino_test.wav

