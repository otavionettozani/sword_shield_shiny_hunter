from os import listdir, getcwd
import xml.etree.ElementTree as ET
from math import floor, ceil

images_dir = f"{getcwd()}/models_training/images/train"
files = [element for element in listdir(images_dir) if element.endswith(".xml")]


print("filename,width,height,class,xmin,ymin,xmax,ymax")
for file in files:
  full_path = f"{images_dir}/{file}"
  parsed = ET.parse(full_path)
  root = parsed.getroot()
  image_name = root.find("filename").text
  image_path = root.find("path").text

  obj = root.find("object")
  class_label = obj.find("name").text

  bounds = obj.find("bndbox")
  minx = bounds.find("xmin").text
  miny = bounds.find("ymin").text
  maxx = bounds.find("xmax").text
  maxy = bounds.find("ymax").text

  size = root.find("size")
  height = size.find("height").text
  width = size.find("width").text
  print(f"{image_name},{width},{height},{class_label},{minx},{miny},{maxx},{maxy}")