import tensorflow
import cv2
from os import getcwd
import csv
import io
from object_detection.utils import dataset_util

images_dir = f"{getcwd()}/models_training/images/train"
writer = tensorflow.io.TFRecordWriter("./tf_record.record")
csv_file = open("./train_data.csv")
data = list(csv.DictReader(csv_file))

classes = sorted(set(map(lambda x: x["class"], data)))

for record in data:
  height = int(record["height"])
  width = int(record["width"])
  filename = record["filename"]
  source_id = filename
  image_format = b"jpg"
  xmin = int(record["xmin"])/width
  xmax = int(record["xmax"])/width
  ymin = int(record["ymin"])/height
  ymax = int(record["ymax"])/height
  class_text = record["class"]
  class_label = classes.index(class_text)

  image_location = f"{images_dir}/{filename}"
  image_data = tensorflow.io.gfile.GFile(image_location, "rb").read()

  tf_example = tensorflow.train.Example(features=tensorflow.train.Features(feature={
    'image/height': dataset_util.int64_feature(height),
    'image/width': dataset_util.int64_feature(width),
    'image/filename': dataset_util.bytes_feature(filename.encode("utf8")),
    'image/source_id': dataset_util.bytes_feature(filename.encode("utf8")),
    'image/encoded': dataset_util.bytes_feature(image_data),
    'image/format': dataset_util.bytes_feature(image_format),
    'image/object/bbox/xmin': dataset_util.float_list_feature([xmin]),
    'image/object/bbox/xmax': dataset_util.float_list_feature([xmax]),
    'image/object/bbox/ymin': dataset_util.float_list_feature([ymin]),
    'image/object/bbox/ymax': dataset_util.float_list_feature([ymax]),
    'image/object/class/text': dataset_util.bytes_list_feature([class_text.encode("utf8")]),
    'image/object/class/label': dataset_util.int64_list_feature([class_label]),
  }))
  writer.write(tf_example.SerializeToString())

writer.close()