import argparse
import os

import model

import tensorflow as tf
from tensorflow.contrib.learn.python.learn import learn_runner
from tensorflow.contrib.learn.python.learn.estimators import run_config
from tensorflow.contrib.learn.python.learn.utils import (
    saved_model_export_utils)
from tensorflow.contrib.training.python.training import hparam


def generate_experiment_fn(**experiment_args):
    """Create an experiment function.

    See command line help text for description of args.
    Args:
    experiment_args: keyword arguments to be passed through to experiment
      See `tf.contrib.learn.Experiment` for full args.
    Returns:
    A function:
      (tf.contrib.learn.RunConfig, tf.contrib.training.HParams) -> Experiment

    This function is used by learn_runner to create an Experiment which
    executes model code provided in the form of an Estimator and
    input functions.
    """
    def _experiment_fn(run_config, hparams):
        # num_epochs can control duration if train_steps isn't
        # passed to Experiment
        train_input = lambda: model.generate_input_fn(
            hparams.train_files,
            num_epochs=hparams.num_epochs,
            batch_size=hparams.train_batch_size,
        )
        # Don't shuffle evaluation data
        eval_input = lambda: model.generate_input_fn(
            hparams.eval_files,
            batch_size=hparams.eval_batch_size,
            shuffle=False
        )

        return tf.contrib.learn.Experiment(
            model.build_estimator(
                embedding_size=hparams.embedding_size,
                # Construct layers sizes with exponetial decay
                hidden_units=[
                    max(2, int(hparams.first_layer_size *
                               hparams.scale_factor**i))
                    for i in range(hparams.num_layers)
                ],
                config=run_config
            ),
            train_input_fn=train_input,
            eval_input_fn=eval_input,
            **experiment_args
        )
    return _experiment_fn

