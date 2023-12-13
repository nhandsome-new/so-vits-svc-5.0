python svc_inference_content_aug.py \
 --config configs/base.yaml  \
 --model /home/mluser/so-vits-5/ckpt/sovits_data_big_with_song/sovits_data_big_with_song_0050.pt \
 --spk /data/fusic/vc_noutomi/spkemb/noutomi1-18_DeepFilterNet3.g.pt \
 --vec /data/sing/tmp/content/yoasobi.c.pt \
 --pit /data/sing/tmp/f0uv/yoasobi.f0.npy \
 --shift -14
# /data/karanovc_min/jvs001/wav/BASIC5000_0025.wav
# RKB
# /data/rkb_select/tabata/wav/
# rkb-01.wav  rkb-03.wav  rkb-05.wav  rkb-07.wav  rkb-09.wav  rkb-11.wav  rkb-13.wav  rkb-15.wav  rkb-17.wav  rkb-19.wav
# rkb-02.wav  rkb-04.wav  rkb-06.wav  rkb-08.wav  rkb-10.wav  rkb-12.wav  rkb-14.wav  rkb-16.wav  rkb-18.wav

# --vec /data/sing/tmp/content/aka.c.pt \
# /data/fusic/han/wav/0759_DeepFilterNet3.wav
# MODEL
#  /data/karano_nhk_first_finetune_batch_2_accum_4_content_loss_3_0012.pt
# /home/mluser/so-vits-5/ckpt/fusic3_finetune_freeze/fusic3_finetune_freeze_9999.pt
# /home/mluser/so-vits-5/ckpt/karanovc_min_lr_1e4_sraug/karanovc_min_lr_1e4_sraug_0012.pt
# /home/mluser/so-vits-5/ckpt/karanovc_min_lr_1e4_sraug_song_fusic/karanovc_min_lr_1e4_sraug_song_fusic_0001.pt

# SPEAKER
# /data/fusic_ref/minna/spkemb/hirosawa_DeepFilterNet3.g.pt
# --spk /data/fusic/han/spkemb/0142_DeepFilterNet3.g.pt
# --spk /data/add_fusic_1200/c_nogami/spkemb/EMOTION100_011.g.pt
# --spk /data/fusic/hama/spkemb/hamasaki-03_DeepFilterNet3.g.pt \ 160 3
#  /data/fusic/hamasaki/spkemb/006_DeepFilterNet3.g.pt
# --spk /data/fusic/vc_noutomi/spkemb/noutomi1-26_DeepFilterNet3.g.pt \ \ 140 0-2
# --spk /data/fusic_ref/minna/spkemb/nogami_DeepFilterNet3.g.pt  9
# /data/karanovc_min/han/content/0424_DeepFilterNet3.c.pt \
# /data/景浦大輔2/f0uv/0002_00025_00000.f0.npy 

# MUSIC
# ネジバナ_vocal_small.wav
# ラビリンス_vocal_small.wav
# 白銀の小舟_vocal_small.wav
# happiness_vocal_small.wav
# again_vocal_small.wav
# aimyon_vocal_01.wav # aimyon_vocal_02.wav

# /data/tmp2/tmp/spkemb/
# fusic_oda_test.g.pt         fusic_sakuragawa_test.g.pt  fusic_shinkawa_test.g.pt    fusic_sugimoto_test.g.pt    fusic_yoshino_test.g.pt 

# CONTENT
# /data/fusic_introduce/minna/f0uv/han_normal_vc.f0.npy 
# /data/fusic_introduce/minna/f0uv/nogami_vc.f0.npy

# TEST
# /data/sing/tmp/wav/
# Fusic_en_indian.wav  fusic_en.wav  raw.wav  raw2.wav  sing_female.wav  sing_female_high.wav  sing_male.wav yoasobi.wav jp_song.wav
# kr_rap.wav   dism-02.wav   aka.wav    dryflower.wav


# /data/introduce/han/wav/han_fusic_DeepFilterNet3.wav
# /data/fusic/han/wav/0012_DeepFilterNet3.wav
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

# /data/tmp/minna/wav/
# はんくんの早口_VC音源_DeepFilterNet3.wav  ハンくん_VC音源_DeepFilterNet3.wav  野上ちゃん_VC音源_DeepFilterNet3.wav/

# /data/karanovc_min/中川翔/wav/0000_00027_00000.wav
# /data/karanovc_min/景浦大輔2/wav/0002_00025_00000.wav
# /data/karanovc_min/下山吉光1/wav/0001_00002_00016.wav
# /data/karanovc_min/李ふぁい/wav/0002_00023_00000.wav

# /data/fusic/vc_noutomi/wav/noutomi1-4_DeepFilterNet3.wav
# --vec /data/fusic_han/han/content/han_test_DeepFilterNet3.c.pt \
# /data/karanovc_min/han/wav/0142_DeepFilterNet3.wav

# /data/fusic_ref/minna/spkemb/
# funagosi_DeepFilterNet3.g.pt  hirosawa_DeepFilterNet3.g.pt  nogami_DeepFilterNet3.g.pt  yuki_DeepFilterNet3.g.pt
# fusic_oda_test.g.pt           fusic_sakuragawa_test.g.pt    fusic_shinkawa_test.g.pt      fusic_sugimoto_test.g.pt      fusic_yoshino_test.g.pt
# /data/fusic_ref/funakoshi/wav/funakoshi_long_DeepFilterNet3.wav

# /data/fusic/hama/wav/hamasaki-03_DeepFilterNet3.wav

# /data/tmp/minna/
# fusic_hamasaki_test.wav    fusic_noutomi_test.wav     fusic_oda_test.wav         
# fusic_sakuragawa_test.wav  fusic_shinkawa_test.wav    fusic_sugimoto_test.wav    fusic_yoshino_test.wav

# /data/tmp/tmp/spkemb/
# /data/tmp/tmp/spkemb/dog-barking-70772.g.pt       train-crossing-bell-01.g.pt  train-pass-by-01.g.pt