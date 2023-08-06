import inspect
import warnings
from inspect import isclass
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, confloat, conint, constr, validator

from _finetuner.runner.stubs import callback
from _finetuner.runner.stubs.model import get_model_stubs_dict


class ModelConfig(BaseModel):
    name: constr(min_length=1) = Field(
        description='The name of the backbone model that will be fine-tuned.'
    )
    freeze: bool = Field(
        default=False,
        description=(
            'If set to True all layers in the backbone model except the last '
            'one will be freezed.'
        ),
    )
    output_dim: Optional[conint(gt=0)] = Field(
        default=None,
        description=(
            'The embedding model\'s output dimensionality. If set, a projection '
            'head will be attached to the backbone model.'
        ),
    )
    options: Dict[str, Any] = Field(
        default_factory=lambda: {},
        description=(
            'Additional arguments to pass to the backbone model construction. These '
            'are model specific options and are different depending on the model you '
            'choose.'
        ),
    )
    to_onnx: bool = Field(
        default=False, description='If set `True` will convert model as onnx.'
    )

    @validator('name')
    def valid_model_name(cls, v):
        stubs_dict = get_model_stubs_dict()
        if v in stubs_dict:
            return v
        else:
            raise ValueError(
                f'No pre-trained model found with name {v}, '
                'see https://finetuner.jina.ai/walkthrough/choose-backbone/ for a list '
                'of all supported models.'
            )

    class Config:
        validate_assignment = True


class DataConfig(BaseModel):
    train_data: constr(min_length=1) = Field(
        description='The training data to use for fine-tuning the model.'
    )
    eval_data: Optional[constr(min_length=1)] = Field(
        default=None,
        description=(
            'Optional evaluation data to use for the fine-tuning run. '
            'Validation loss is computed per epoch agaist this dataset.'
        ),
    )
    val_split: confloat(ge=0, lt=1) = Field(
        default=0.0,
        description=(
            'Determines which portion of the `train_data` specified in the '
            '`fit` function is held out and used for validation (and not for '
            'training). If it is set to 0, or an `eval_data` parameter is provided '
            'to the `fit` function, no training data is held out for validation.'
        ),
    )
    num_workers: conint(gt=0) = Field(
        default=8, description='Number of workers used by the dataloaders.'
    )
    num_items_per_class: conint(gt=1) = Field(
        default=4,
        description='Number of same-class items that will make it in the batch.',
    )

    class Config:
        validate_assignment = True


class CallbackConfig(BaseModel):
    name: constr(min_length=1) = Field(description='The name of the callback.')
    options: Dict[str, Any] = Field(
        default_factory=lambda: {},
        description='Arguments to pass to the callback construction.',
    )

    @validator('name')
    def valid_callback_name(cls, v):

        callbacks = [
            name
            for name, callback_cls in inspect.getmembers(callback)
            if isclass(callback_cls)
        ]
        if v in callbacks:
            return v
        else:
            raise ValueError(
                f'No callback found with name {v}, '
                'see https://finetuner.jina.ai/walkthrough/using-callbacks/ for a list '
                'of all supported callbacks.'
            )


class HyperParametersConfig(BaseModel):
    loss: constr(min_length=1) = Field(
        default='TripletMarginLoss',
        description=(
            'Name of the loss function to use for fine-tuning. See '
            'https://finetuner.jina.ai/api/finetuner/#finetuner.fit for '
            'available options.'
        ),
    )
    optimizer: constr(min_length=1) = Field(
        default='Adam',
        description=(
            'Name of the optimizer that will be used for fine-tuning. See '
            'https://pytorch.org/docs/stable/optim.html for available options.'
        ),
    )
    optimizer_options: Dict[str, Any] = Field(
        default_factory=lambda: {},
        description='Specify arguments to pass to the optimizer construction.',
    )
    miner: Optional[constr(min_length=1)] = Field(
        default=None,
        description=(
            'Specify the miner that will be used for fine-tuning. See '
            'https://kevinmusgrave.github.io/pytorch-metric-learning/miners/ for '
            'available options.'
        ),
    )
    miner_options: Dict[str, Any] = Field(
        default_factory=lambda: {},
        description=(
            'Specify arguments to pass to the miner construction. See '
            'https://kevinmusgrave.github.io/pytorch-metric-learning/miners/ for '
            'detailed information about all possible attributes.'
        ),
    )
    batch_size: conint(gt=0) = Field(
        default=128, description='The training batch size.'
    )
    learning_rate: Optional[confloat(ge=0, lt=1)] = Field(
        default=None,
        description=(
            'The learning rate to use during training. If given, this argument '
            'overwrites the optimizer default learning rate or the learning rate '
            'specified in the optimizer options.'
        ),
    )
    epochs: conint(ge=0, lt=50) = Field(
        default=10, description='Number of fine-tuning epochs.'
    )
    scheduler_step: str = Field(
        default='batch',
        description=(
            'At which interval should the learning rate scheduler\'s '
            'step function be called. Valid options are `batch` and `epoch`.'
        ),
    )

    @validator('batch_size')
    def batch_size_warning(cls, v):
        if v >= 256:
            warnings.warn('batch_size >= 256 may result in out of memory errors.')
        return v

    @validator('scheduler_step')
    def validate_scheduler_step(cls, v):
        if v not in ['batch', 'epoch']:
            raise ValueError(
                f'Invalid scheduler step value \'{v}\', '
                'choose between \'batch\' and \'epoch\''
            )
        return v

    class Config:
        validate_assignment = True


class RunConfig(BaseModel):
    model: ModelConfig = Field(description='Model configuration.')
    data: DataConfig = Field(description='Data configuration.')
    callbacks: List[CallbackConfig] = Field(
        default_factory=lambda: [],
        description='List of callbacks that will be used during fine-tuning.',
    )
    hyper_parameters: HyperParametersConfig = Field(
        default=HyperParametersConfig(), description='Hyper-parameter configuration.'
    )
    public: bool = Field(
        default=False,
        description=('If set to True artifact will be set as public artifact.'),
    )
    run_name: Optional[constr(min_length=1)] = Field(
        default=None, description='Specify a run name.'
    )
    experiment_name: Optional[constr(min_length=1)] = Field(
        default=None, description='Specify an experiment name.'
    )
