from picarx_improved import Picarx
import time

px = Picarx()
px.forward(50)
time.sleep(2)
px.backward(50)
time.sleep(2)
px.stop()