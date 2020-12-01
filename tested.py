import os
import subprocess

cmd = "python testing.py"



a = subprocess.check_output("pwd").decode("utf8")
b = a[0:len(a)-1] + "/" + "testing.py"
r = subprocess.call(b, shell=True)

print("a")
print("Code = " + str(r))