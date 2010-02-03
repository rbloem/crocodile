import classtools
import time

reload(classtools)

y=classtools.ClassTools()
y.test = "check2"
y.time = time.localtime()

print y  