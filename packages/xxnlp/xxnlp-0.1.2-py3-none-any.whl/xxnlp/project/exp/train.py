from xxnlp import Args
from xxnlp.utils import seed_all
from ignite.engine import Engine

AVAILABLE_MODELS = ['bert-base-cased', 'google/electra-small-discriminator', 'roberta-base', 'xlnet-base-cased']

def run_train(args: Args, logger=None):
    seed_all(args.seed)

    def get_train_step(mode, model, optimizer):
        """Get the appropriate train step for the model, which is specified by name."""
        def train(engine: Engine, batch):
            model.train()
            optimizer.zero_grad()