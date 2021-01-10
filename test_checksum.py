import os
import hashlib
import pathlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    
def getChecksumOfDir(path):
    checksums = []
    for filename in os.listdir(path):
        checksums.append(md5(path + filename))
    return checksums
local_path = os.fspath(pathlib.Path().absolute())
local_checksum  =  getChecksumOfDir(os.fspath(pathlib.Path(__file__).parent.absolute()) + "/RobotCode/") 

x = ""
for i in local_checksum:
    x += i[:2]

print(x)
print(pathlib.Path(__file__).parent.absolute())