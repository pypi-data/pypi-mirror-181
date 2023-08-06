import os
os.environ['TOKENIZERS_PARALLELISM'] = "false"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from xxnlp import Args
from xxnlp.utils import ojoin, set_directory
from pytorch_lightning import seed_everything, Trainer
from transformers import AutoTokenizer
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from pytorch_lightning.loggers import TensorBoardLogger
with set_directory():
    from constant import ERISK_PATH as DATA_PATH
    from data import EriskDataModule
    from model import EriskModel

args = Args(
    # --------------- something you must explicitly specify ---
    exp_name = 'TEST',
    optim_metric = 'val_f1',
    optim_direction = 'maximize',
    # --------------- train ---
    seed = 2021,
    batch_sz = 4,
    lr = 2e-5,
    data_mode = 'together', #choice(depress, last, together, question)
    topk = 16,
    num_epochs = 100,
    # --------------- model ---
    # model_name = 'bert-base-uncased',
    model_name = 'mental/mental-bert-base-uncased',
    num_layers = 4,
    user_mode = 'absolute', #choice(absolute, raw, average, han, simple)
    # --------------- extra ---
    max_len = 128,
    accumulate = 1,
    grad_clip = 0.1,
    find_lr = True,
    patience = 4
)

def main():
    seed_everything(args.seed, workers=True)
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    args.update(
        datapath = ojoin(DATA_PATH, f'{args.data_mode}_top{args.topk}')
    )
    m_args = Args(
        threshold=0.5, lr=args.lr, model_name=args.model_name, user_mode=args.user_mode, num_heads=8, num_layers=args.num_layers, freeze_word_level=False, pool_mode="first", 
    )
    model = EriskModel(**m_args)
    d_args = Args(
        batch_size=args.batch_sz,
        input_dir=args.datapath,
        tokenizer=tokenizer,
        max_len=args.max_len
    )
    data_module = EriskDataModule(**d_args)
    callbacks = [
        EarlyStopping(args.optim_metric, patience=args.patience, mode='max'),
        ModelCheckpoint(monitor=args.optim_metric, mode='max')
    ]
    logger = TensorBoardLogger(
        save_dir='tb_logs', name=args.exp_name, version=0
    )
    trainer = Trainer(
        accelerator='gpu', devices=1,
        callbacks=callbacks, 
        val_check_interval=1.0, 
        logger=logger,
        max_epochs=args.num_epochs, 
        min_epochs=1, 
        accumulate_grad_batches=args.accumulate, 
        gradient_clip_val=args.grad_clip, 
        deterministic=True, 
        log_every_n_steps=10
    )
    trainer.fit(model, data_module)



if __name__ == '__main__':
    main()






