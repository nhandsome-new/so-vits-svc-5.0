python svc_inference.py \
 --config configs/base.yaml  \
 --model /home/mluser/so-vits-5/ckpt/big_data_d_lr_2e-3_perturbation_change_lr/big_data_d_lr_2e-3_perturbation_change_lr_0025.pt \
 --spk /home/mluser/so-vits-5/tmp/noutomi.pt \
 --vec /data/木澤智之/content/0000_00037_00000.c.pt \
 --pit /data/木澤智之/f0uv/0000_00037_00000.f0.npy \
 --shift 3

# --pit /data/jvs001/f0uv/BASIC5000_0025.f0.npy \
# --pit /data/jvs002/f0uv/BASIC5000_0104.f0.npy \
# --pit /data/木澤智之/f0uv/0000_00037_00000.f0.npy \
# --pit /data/k小田切優衣1/f0uv/0000_00097_00000.f0.npy \
# --pit /data/k小田切優衣1/f0uv/0000_00097_00000.f0.npy \