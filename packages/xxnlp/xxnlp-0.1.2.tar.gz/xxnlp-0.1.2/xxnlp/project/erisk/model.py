from typing import Tuple
from pytorch_lightning import LightningModule
import torch.nn as nn
import torch, numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score
from argparse import ArgumentParser
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoModel

def mean_pooling(token_embeddings, attention_mask):
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

class Model(LightningModule):

    @staticmethod
    def add_model_specific_args(parent_parser: ArgumentParser):
        parser = ArgumentParser(parents=[parent_parser], add_help=False)
        return parser
    
    def __init__(self, threshold=0.5, **kwargs):
        super(Model, self).__init__()
        self.best_f1 = 0.
        self.threshold = threshold
        self.criterion = nn.BCEWithLogitsLoss()

    def process_batch(self, batch):
        x, y_true = batch
        y_pred = self(x)
        if isinstance(y_pred, Tuple):
            y_pred, attn_scores = y_pred
        loss = self.criterion(y_pred, y_true)
        return y_pred, y_true, loss

    def training_step(self, batch, batch_idx):
        y_pred, y_true, loss = self.process_batch(batch)
        return {
            'loss': loss, 
            'log': {'train_loss': loss}
        }
    
    def validation_step(self, batch, batch_idx):
        y_pred, y_true, loss = self.process_batch(batch)
        return {
            'val_loss': loss, 
            "labels": y_true.cpu().numpy(), 
            "probs":  y_pred.sigmoid().cpu().numpy()
        }

    def validation_epoch_end(self, outputs):
        avg_loss = torch.stack([x['val_loss'] for x in outputs]).mean()
        all_labels = np.concatenate([x['labels'] for x in outputs])
        all_probs = np.concatenate([x['probs'] for x in outputs])
        all_preds = (all_probs > self.threshold).astype(float)
        acc = np.mean(all_labels == all_preds)
        p = precision_score(all_labels, all_preds)
        r = recall_score(all_labels, all_preds)
        f1 = f1_score(all_labels, all_preds)
        self.best_f1 = max(self.best_f1, f1)
        if self.current_epoch == 0:  # prevent the initial check modifying it
            self.best_f1 = 0.
        tensorboard_logs = {'val_loss': avg_loss, 'val_acc': acc, 'val_p': p, 'val_r': r, 'val_f1': f1, 'hp_metric': self.best_f1}
        self.log_dict(tensorboard_logs)
        self.log("best_f1", self.best_f1, prog_bar=True, on_epoch=True)
        return {'val_loss': avg_loss, 'log': tensorboard_logs}


    def test_step(self, batch, batch_idx):
        y_pred, y_true, loss = self.process_batch(batch)
        return {
            'test_loss': loss, 
            "labels": y_true.cpu().numpy(), 
            "probs":  y_pred.sigmoid().cpu().numpy()
        }

    def test_epoch_end(self, outputs):
        avg_loss = torch.stack([x['test_loss'] for x in outputs]).mean()
        all_labels = np.concatenate([x['labels'] for x in outputs])
        all_probs = np.concatenate([x['probs'] for x in outputs])
        all_preds = (all_probs > self.threshold).astype(float)
        acc = np.mean(all_labels == all_preds)
        p = precision_score(all_labels, all_preds)
        r = recall_score(all_labels, all_preds)
        f1 = f1_score(all_labels, all_preds)
        return {'test_loss': avg_loss, 'test_acc': acc, 'test_p': p, 'test_r': r, 'test_f1': f1}

    def on_after_backward(self):
        pass

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.lr)
        return optimizer

class BERTHierClassifierTransAbs(nn.Module):
    def __init__(self, model_name, num_heads=8, num_layers=6, max_posts=64, freeze=False, pool_mode="first"):
        super(BERTHierClassifierTransAbs, self).__init__()
        self.model_name = model_name
        self.num_heads = num_heads
        self.num_trans_layers = num_layers
        self.pool_type = pool_mode
        self.post_encoder = AutoModel.from_pretrained(model_name)
        if freeze:
            for name, param in self.post_encoder.named_parameters():
                param.requires_grad = False
        self.hidden_dim = self.post_encoder.config.hidden_size
        self.max_posts = max_posts
        self.pos_emb = nn.Parameter(torch.Tensor(max_posts, self.hidden_dim))
        nn.init.xavier_uniform_(self.pos_emb)
        encoder_layer = nn.TransformerEncoderLayer(d_model=self.hidden_dim, dim_feedforward=self.hidden_dim, nhead=num_heads, activation='gelu')
        self.user_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.attn_ff = nn.Linear(self.hidden_dim, 1)
        self.dropout = nn.Dropout(self.post_encoder.config.hidden_dropout_prob)
        self.clf = nn.Linear(self.hidden_dim, 1)

    def forward(self, batch, **kwargs):
        """
        $ all raw text input is first tokenized in datamodule (with pretrained `model_name`)
        @input_ids          token id per each document? [topk, max_len], note every token is prepended with <cls> (id=101)
        @attention_mask     valid token padding [topk, max_len]

        $ first post_encoder (with pretrained `model_name`) process input tokens
        @last_hidden_state  last layer hidden states [topk, max_len, embed-size]
        @pooler_output      last layer hidden-state of the first token of the sequence (cls token), with further post-processing, + ffn? [topk, embed-size]

        $ since all these {topk} posts are sequential data, we position embedding it
        @user_encoder       a nn.TransformerEncoder (3layer+768emb)
        @attn_score         attention score [topk] paid to each {topk} instance
        @feat               final feature (of this subject), (topk)attn-weighted [embed-size=768]
        """
        feats, attn = [], []
        for user_feats in batch:
            post_outputs = self.post_encoder(user_feats["input_ids"], user_feats["attention_mask"], user_feats["token_type_ids"])
            # [num_posts, seq_len, hidden_size] -> [num_posts, 1, hidden_size]
            if self.pool_type == "first":
                x = post_outputs.last_hidden_state[:, 0:1, :]
            elif self.pool_type == 'mean':
                x = mean_pooling(post_outputs.last_hidden_state, user_feats["attention_mask"]).unsqueeze(1)
            # positional embedding for posts
            x = x + self.pos_emb[:x.shape[0], :].unsqueeze(1)
            x = self.user_encoder(x).squeeze(1) # [num_posts, hidden_size]
            attn_score = torch.softmax(self.attn_ff(x).squeeze(-1), -1) 
            feat = attn_score @ x
            feats.append(feat); attn.append(attn_score)
        x = self.dropout(torch.stack(feats))
        logits = self.clf(x).squeeze(-1)  # [bs, num_posts]
        return logits, attn


class EriskModel(Model):

    def __init__(
        self, threshold=0.5, lr=5e-5, model_name="prajjwal1/bert-tiny", user_mode="simple", num_heads=8, num_layers=2, freeze_word_level=False, pool_mode="first", **kwargs
    ):
        super(EriskModel, self).__init__(threshold=threshold, **kwargs)
        self.model_name = model_name
        if user_mode == 'absolute':
            self.model = BERTHierClassifierTransAbs(model_name, num_heads, num_layers, freeze=freeze_word_level, pool_mode=pool_mode)
        self.lr = lr
        self.save_hyperparameters()

    def forward(self, x):
        x = self.model(x)
        return x


