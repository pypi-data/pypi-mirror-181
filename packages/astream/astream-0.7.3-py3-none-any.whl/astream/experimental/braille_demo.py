import time
import math
from random import randint
from collections import deque
from braille import sparkline

t = 0
data = deque(maxlen=120)
import os
w = os.get_terminal_size().lines
while True:
    t += 0.5
    data.append(math.sin(t) * 3 + randint(-1, 4))
    spark = sparkline(data, max_val=6, min_val=-2, width=w)

    clear = len(spark)//2 * " " + "\r "
    print(clear + spark, end="\r")
    time.sleep(0.05)
