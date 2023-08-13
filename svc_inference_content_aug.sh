python svc_inference_content_aug.py \
 --config configs/base.yaml  \
 --model /home/mluser/so-vits-5/ckpt/big_data_d_lr_2e-3_perturbation_change_lr_no_spkloss_smalldata_2_with_many_kor_with_contents_loss/big_data_d_lr_2e-3_perturbation_change_lr_no_spkloss_smalldata_2_with_many_kor_with_contents_loss_0152.pt \
 --spk /data/karanovc_min/han/spkemb/0424_DeepFilterNet3.g.pt \
 --vec /data/karanovc_min/景浦大輔2/content/0002_00025_00000.c.pt \
 --pit /data/karanovc_min/景浦大輔2/f0uv/0002_00025_00000.f0.npy \
 --shift 3 \
 --device cpu

# /data/karanovc_min/jvs001/content/BASIC5000_0025.c.pt
# --vec /data/karanovc_min/han/content/0424_DeepFilterNet3.c.pt \
# --spk /data/karanovc_min/菅沢公平/spkemb//0001_00044_00000.g.pt \
# --pit /data/jvs001/f0uv/BASIC5000_0025.f0.npy \
# --pit /data/jvs002/f0uv/BASIC5000_0104.f0.npy \
# --pit /data/景浦大輔2/f0uv/0002_00025_00000.f0.npy \
# --pit /data/k小田切優衣1/f0uv/0000_00097_00000.f0.npy \
# --pit /data/k小田切優衣1/f0uv/0000_00097_00000.f0.npy \
# --spk /data/karanovc_min/vウマ娘_カレン/spkemb/0007_00000_00000.g.pt \
# 0010_00016_00000.wav 朴璐美2

# /data/karanovc_min/中川翔/wav/0000_00027_00000.wav
# /data/karanovc_min/景浦大輔2/wav/0002_00025_00000.wav
# /data/karanovc_min/下山吉光1/wav/0001_00002_00016.wav
# /data/karanovc_min/李ふぁい/wav/0002_00023_00000.wav
