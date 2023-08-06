from typing import Callable, Dict
import torch
import torch.nn as nn
from ignite.engine import Engine, EventEnum
from ignite.contrib.handlers import ProgressBar
from xxnlp.utils import xmove, get_logger
from .metrics import METRICS
from .callback import CALLBACKS, BackpropEvents


def create_engine(
    model: nn.Module, 
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: str,
    metrics: Dict[str, dict], 
    callbacks: Dict[str, dict],
    train_fn: Callable = None,
    test_fn: Callable = None
    ) -> Engine:
    """
    Combines the .... into an engine
    """
    device = torch.device(device)
    criterion.to(device)
    
    # Training ============================================================
    def train_step(engine, batch):
        model.train()
        x, y = batch
        xmove(x, device)
        y_pred = model(**x)
        loss = criterion(y_pred, y.to(device))
        optimizer.zero_grad()
        engine.fire_event(BackpropEvents.BACKWARD_STARTED)
        loss.backward()
        engine.fire_event(BackpropEvents.BACKWARD_COMPLETED)
        optimizer.step()
        engine.fire_event(BackpropEvents.OPTIM_STEP_COMPLETED)
        return loss.item()

    # Define trainer engine and keep track of criterion/optimizer
    engine = Engine(train_fn or train_step)
    engine.register_events(*BackpropEvents)
    # anything you'd be using in callback by adding engine.state.xx = xx
    engine.state.model = model
    for name, kwargs in callbacks.items():
        CALLBACKS.get(name, engine='ignite')(**kwargs).attach(engine)

    ProgressBar(
        bar_format='{desc}[{n_fmt}/{total_fmt}]{percentage:3.0f}%{postfix}',
        persist=True
    ).attach(
        engine, 
        output_transform=lambda x: {'loss': x},
        state_attributes=['lr']
    )
    
    # Evaluation ========================================================
    @torch.no_grad()
    def test_step(engine, batch):
        model.eval()
        x, y = batch
        xmove(x, device)
        y_pred = model(**x).argmax(axis=1)
        return y_pred.cpu().numpy(), y.numpy()
    
    evaluator = Engine(test_fn or test_step)
    for name, kwargs in metrics.items():
        METRICS.get(name, engine='ignite')(**kwargs).attach(evaluator, name)
    evaluator.state.performance = {}  # used to evaluate and save model per epoch
    engine.state.evaluator = evaluator
        
    # change ignite logging level (disable INFO level logging)
    get_logger('ignite.engine.engine.Engine', level='WARNING')

    return engine






     

