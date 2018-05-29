import os

from background_task import background
import time

@background (schedule = 1)
def test_background():
    print("donedone")
    dirname = kkktestbackground
    if not os.path.exists("userImg/" + dirname):
        os.mkdir("userImg/" + dirname)
    for i in range(3):
        time.sleep(2)
        print("test i "+str(i))