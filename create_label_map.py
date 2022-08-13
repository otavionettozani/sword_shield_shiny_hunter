import csv

csv_file = open("./train_data.csv")
data = list(csv.DictReader(csv_file))

classes = sorted(set(map(lambda x: x["class"], data)))


i = 1

for klass in classes:
  print("item {")
  print(f"\tid: {i}")
  print(f"\tname: \"{klass}\"")
  print("}")
  i+=1