import os

items = os.listdir(os.path.join(os.path.expanduser("~"), "Videos", "JWLibrary"))
for file in items:
    print(file)
    

