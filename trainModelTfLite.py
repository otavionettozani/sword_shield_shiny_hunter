import numpy as np
import os

from tflite_model_maker.config import ExportFormat, QuantizationConfig
from tflite_model_maker import model_spec
from tflite_model_maker import object_detector

from tflite_support import metadata

import tensorflow as tf
assert tf.__version__.startswith('2')

tf.get_logger().setLevel('ERROR')
from absl import logging
logging.set_verbosity(logging.ERROR)

labels = ["box_arrow","change_user","close_button","dialog_hint","dialog_hint_inverted","menu_arrow","r_to_boxes","shiny_hint","user_box","woman_egg","woman_no_egg"]

train_data = object_detector.DataLoader.from_pascal_voc(
  './models_training/images/train',
  './models_training/images/train',
  labels
)

val_data = object_detector.DataLoader.from_pascal_voc(
  './models_training/images/train',
  './models_training/images/train',
  labels
)

spec = model_spec.get('efficientdet_lite0')
model = object_detector.create(train_data, model_spec=spec, batch_size=4, train_whole_model=True, epochs=20, validation_data=val_data)

model.export(export_dir='.', tflite_filename='pkmn_swsh.tflite')

