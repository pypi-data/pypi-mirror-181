import torch
import torchvision
import albumentations as A
from albumentations.pytorch import ToTensorV2
import torch.nn as nn
import pytorch_lightning as pl
import numpy as np
from cv2 import imread

class SkewSimilarity(nn.Module):
    def __init__(self, embedding_dim):
        super(SkewSimilarity, self).__init__()
        std = np.sqrt(2.0 / embedding_dim)
        self.J = nn.Parameter(std * torch.randn(embedding_dim, embedding_dim))

    def forward(self, x, y):
        J_ = 0.5 * (self.J - self.J.transpose(1, 0))
        return torch.sum(torch.matmul(x, J_) * y, dim=-1, keepdim=True)

class L2Normalize(nn.Module):
    def __init__(self, eps=1e-5):
        super(L2Normalize, self).__init__()
        self.eps = eps

    def forward(self, x):
        return x / (torch.norm(x, dim=-1, keepdim=True) + self.eps)

class ScoreModel(pl.LightningModule):
    def __init__(self):

        backbone_model = getattr(torchvision.models, 'inception_v3')(pretrained=True)
        backbone_model.aux_logits = False
        backbone_model.fc = nn.Linear(2048, 2048)

        embedding_dim=2048*2

        super(ScoreModel, self).__init__()

        self.features = backbone_model
        self.norm = L2Normalize()
        self.similarity = SkewSimilarity(embedding_dim=embedding_dim)

    def forward(self, x):

        B, _, C, H, W = x.shape

        x = x.reshape(-1, C, H, W)
        f = self.features(x)
        f = f.view(B, 3, -1)
        f1, f2, f3 = f[:, 0, :], f[:, 1, :], f[:, 2, :]

        f1 = self.norm(f1)
        f2 = self.norm(f2)
        f3 = self.norm(f3)

        d = self.similarity(torch.cat((f1,f3),1), torch.cat((f2,f3),1))

        return d

def get_model(ckpt_path):
    score_model =  ScoreModel.load_from_checkpoint(ckpt_path)
    score_model.eval()
    return score_model.cuda()

def get_score(input_path, reference_path, gt_path, model):
    val_transform = A.Compose(
        [
            A.Resize(299, 299),
            A.Normalize(),
            ToTensorV2()
        ],
    )

    input=imread(input_path)
    reference=imread(reference_path)
    gt=imread(gt_path)
    input = torch.unsqueeze(val_transform(image=input)["image"], 0)
    reference = torch.unsqueeze(val_transform(image=reference)["image"], 0)
    gt=  torch.unsqueeze(val_transform(image=gt)["image"], 0)

    tensors=torch.stack([reference, input,
                            gt], 1)

    tensors=tensors.cuda()

    with torch.no_grad():
        return float(torch.sigmoid(model.forward(tensors)))
