import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

class MyLoss(nn.Module):
    def __init__(self, samples_per_cls=[10,1], no_of_classes=2, loss_type='focal'):
        super(MyLoss, self).__init__()
        self.loss_type = loss_type
        beta, self.gamma = 0.9999, 2.0
        if not samples_per_cls:
            samples_per_cls = [1] * no_of_classes
        samples_per_cls = torch.tensor(samples_per_cls)
        effective_num = 1.0 - torch.pow(beta, samples_per_cls)
        weights = (1.0 - beta) / effective_num
        self.weights = nn.Parameter(weights.softmax(-1) * no_of_classes, requires_grad=False)
        self.n_cls = no_of_classes

    def forward(self, pred, target, seq_len=None, is_training=True):
        n = len(pred)
        # 1. prepare weight: weight_ (batch-size, n-class)
        weight_ = self.weights.expand(n, self.n_cls)       
        weight_ = weight_[torch.arange(n), target]
        weight_ = weight_[:,None].repeat(1, self.n_cls)
        # 2. prepare inputs (label has to be fload!)
        target_ = F.one_hot(target, self.n_cls).float()
        loss_type, gamma = self.loss_type, self.gamma
        if loss_type == "focal":
            loss = focal_loss(target_, pred, weight_, gamma)
        elif loss_type == "sigmoid":
            loss = F.binary_cross_entropy_with_logits(pred,target_,weight_)
        elif loss_type == "softmax":
            pred = pred.softmax(dim = 1)
            loss = F.binary_cross_entropy(pred, target_, weight_)
        return loss



def focal_loss(labels, logits, alpha, gamma):
    """Compute the focal loss between `logits` and `labels`
    """    
    BCLoss = F.binary_cross_entropy_with_logits(logits, labels, reduction = "none")

    if gamma == 0.0:
        modulator = 1.0
    else:
        modulator = torch.exp(-gamma * labels * logits - gamma * torch.log(1 + 
            torch.exp(-1.0 * logits)))
             
    weighted_loss = alpha * modulator * BCLoss
    focal_loss = weighted_loss.sum()/labels.sum()
    return focal_loss


def f1_loss(y_true:torch.Tensor, y_pred:torch.Tensor, is_training=False, epsilon=1e-7) -> torch.Tensor:
    """Compute the f1 loss between `logits` and `labels`
    """
    if y_pred.ndim == 2: y_pred = y_pred.argmax(dim=1)
    tp = (y_true * y_pred).sum().to(torch.float32)
    fp = ((1 - y_true) * y_pred).sum().to(torch.float32)
    fn = (y_true * (1 - y_pred)).sum().to(torch.float32)
    precision = tp / (tp + fp + epsilon)
    recall = tp / (tp + fn + epsilon)
    f1 = 2* (precision*recall) / (precision + recall + epsilon)
    f1.requires_grad = is_training
    return f1