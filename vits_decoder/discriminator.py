# import sys
# sys.path.append("/home/mluser/so-vits-5/vits_decoder")
# print(sys.path)
import torch
import torch.nn as nn

from omegaconf import OmegaConf
from .msd import ScaleDiscriminator
from .mpd import MultiPeriodDiscriminator
from .mrd import MultiResolutionDiscriminator


class Discriminator(nn.Module):
    def __init__(self, hp):
        super(Discriminator, self).__init__()
        self.MRD = MultiResolutionDiscriminator(hp)
        self.MPD = MultiPeriodDiscriminator(hp)
        self.MSD = ScaleDiscriminator()

    def forward(self, x):
        r = self.MRD(x)
        p = self.MPD(x)
        s = self.MSD(x)
        return r + p + s


if __name__ == '__main__':
    hp = OmegaConf.load('/home/mluser/so-vits-5/configs/base.yaml')
    model = Discriminator(hp)

    x = torch.randn(3, 1, 16384)
    print("x", "-"*100)
    print(x.shape)
    print("-"*100)
    output = model(x)
    for features, score in output:
        print("-"*100)
        for feat in features:
            print("f",feat.shape)
        print("s",score.shape)

    pytorch_total_params = sum(p.numel()
                               for p in model.parameters() if p.requires_grad)
    print(pytorch_total_params)
