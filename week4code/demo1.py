import re
txt =" The rain in Spain"
pattern = r"\s"
x = re.search(pattern,txt)
print("The first char is located in position:", x.start())
print("The last char is located in position:", x.end())
