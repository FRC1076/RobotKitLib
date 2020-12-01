import os
import subprocess

cmd = "python testing.py"



a = subprocess.check_output("pwd").decode("utf8")
b = a[0:len(a)-1] + "/" + "testing.py"
r = subprocess.Popen(b, shell=True)
rc = r.returncode
print("a")
print("Code = " + str(rc))