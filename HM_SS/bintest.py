from binpack import pack
from binunpack import unpack


test_item = "Script.bin"


unpack(test_item, "Script_test")
pack("Script_test", "Script_test.bin")

with open(test_item, "rb") as f1, open("Script_test_bin", "rb") as f2:
    assert f1.read() == f2.read()
print("Passed!")

# Cleanup item
import os

# Recursively remove a directory and its contents name Script_test
for root, dirs, files in os.walk("Script_test", topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
try:
    os.remove("Script_test.bin")
except:
    pass
try:
    os.rmdir("Script_test")
except:
    pass
