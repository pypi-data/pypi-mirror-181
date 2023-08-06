from xxnlp.types import Callable, List, Union, Mapping, Any, Dict, Path, Optional
from xxnlp.utils import get_logger, xtable
from xxnlp import Registry

from ignite.engine import Events, Engine, EventEnum
from ignite.handlers import LRScheduler, ModelCheckpoint as MC
from functools import partial
import torch, shutil

log = get_logger(__name__)
__all__ = ['CALLBACKS', 'BackpropEvents']

class BackpropEvents(EventEnum):
    BACKWARD_STARTED = 'backward_started'
    BACKWARD_COMPLETED = 'backward_completed'
    OPTIM_STEP_COMPLETED = 'optim_step_completed'

    
def log_performance(
    engine: Engine, dirname: Union[str, Path], score_name: str, score_dir: str, n_saved: int
    ):
    def function(engine: Engine, saver: ModelCheckpoint):
        state = engine.state
        evaluator, train, val, test = state.evaluator, *state.data
        train_dict = evaluator.run(train).metrics.copy()
        val_dict = evaluator.run(val).metrics.copy()
        # save model if better validation score is achieved !
        evaluator.state.epoch = engine.state.epoch
        saver(evaluator, to_save={
            'model': evaluator.state.model, 
        })
        test_dict = evaluator.run(test).metrics.copy()
        saver.update(test_dict)
        log.info(f'Epoch {state.epoch} \n' + xtable(
            dicts=[train_dict, val_dict, test_dict], 
            index=['train','valid','test'],
            fcodes=['', '.6f', '.6f', '.6f', '.6f'], 
            pads=['<8','>10','>10', '>10', '>10']
        ))
    dirname = Path(dirname)/'models'
    try:
        dirname.mkdir()
    except OSError:
        shutil.rmtree(dirname)
    finally:
        dirname.mkdir(exist_ok=True)
    mc = ModelCheckpoint(dirname, score_name, score_dir, n_saved)
    engine.add_event_handler(Events.EPOCH_COMPLETED, function, saver=mc)

    
class ModelCheckpoint(MC):

    def __init__(self, dirname: Union[str, Path], score_name: str, score_dir: str = 'max', n_saved: int = 0, model_name: str = 'model'):
        super(ModelCheckpoint, self).__init__(
            dirname=dirname, filename_prefix='best',
            score_function=partial(self.score_fn, mode=score_dir, name=score_name), 
            global_step_transform=self.epoch_fn, n_saved=n_saved, score_name=score_name, require_empty=False,
            filename_pattern="{filename_prefix}_{name}[%s{score_name}={score}, epoch={global_step}].{ext}",
            greater_or_equal=True
        )
        self._is_better = False
        self.model_name = model_name

    def _setup_checkpoint(self) -> Dict[str, Dict[Any, Any]]:
        checkpoint = super()._setup_checkpoint()
        self._is_better = True
        return checkpoint

    def attach(self, engine):
        engine.add_event_handler(Events.EPOCH_COMPLETED, self.record_experiment)

    def record_experiment(self, engine: Optional[Engine], name: Optional[str] = None) -> None:
        state = engine.state
        evaluator, train, val, test = state.evaluator, *state.data
        # record model performance on train/val/test data
        train_dict = evaluator.run(train).metrics.copy()
        val_dict = evaluator.run(val).metrics.copy()
        # save model if better validation score is achieved !
        evaluator.state.epoch = engine.state.epoch
        self(evaluator, to_save={ self.model_name: state.model,})
        test_dict = evaluator.run(test).metrics.copy()
        self.update(test_dict)
        log.info(f'Epoch {state.epoch} \n' + xtable(
            dicts=[train_dict, val_dict, test_dict], 
            index=['train','valid','test'],
            fcodes=[''] + ['.6f']*len(train_dict), 
            pads=['<8'] + ['>10']*len(train_dict)
        ))
    
    @staticmethod
    def epoch_fn(engine, event):
        return engine.state.epoch

    def update(self, metrics):
        if self._is_better:
            name = str(self.last_checkpoint)
            score = metrics[self.score_name]
            shutil.copy(
                str(self.last_checkpoint), 
                name%(f'test_f1={score:.4f}, valid_')
            )
    
    @staticmethod
    def score_fn(engine, mode, name):
        if mode=='max': return engine.state.metrics[name]
        else: return -engine.state.metrics[name]

    def __call__(self, engine: Engine, to_save: Mapping):
        self._is_better = False
        super(ModelCheckpoint, self).__call__(engine, to_save)

        
class GradClip:
    def __init__(self, clip_value=None, max_norm=None):
        self.clip_value=clip_value
        self.max_norm=max_norm
    def clip_grad_value(self, engine: Optional[Engine], name: Optional[str] = None) -> None:
        torch.nn.utils.clip_grad_value_(engine.state.model.parameters(), self.clip_value)
    def clip_grad_norm(self, engine: Optional[Engine], name: Optional[str] = None) -> None:
        torch.nn.utils.clip_grad_norm_(engine.state.model.parameters(), self.max_norm, norm_type=2)
    def attach(self, engine):
        if self.clip_value:
            engine.add_event_handler(BackpropEvents.BACKWARD_COMPLETED, self.clip_grad_value)
        elif self.max_norm:
            engine.add_event_handler(BackpropEvents.BACKWARD_COMPLETED, self.clip_grad_norm)


class TorchLR(LRScheduler):
    def attach(self, engine):
        engine.add_event_handler(Events.ITERATION_STARTED, self)
    def __call__(self, engine: Optional[Engine], name: Optional[str] = None) -> None:
        super(TorchLR, self).__call__(engine, name)
        engine.state.lr = self.optimizer_param_groups[-1]['lr']


        
CALLBACKS = Registry('callback:torch')
for name, fn in {
    'torch_lr': TorchLR,
    'grad_clip': GradClip,
    'checkpoint': ModelCheckpoint
}.items():
    CALLBACKS(fn=fn, name=name, engine='ignite')