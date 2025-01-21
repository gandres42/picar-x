from picarx_improved import Picarx
import time

px = Picarx()
px.set_dir_servo_angle(-60)
px.backward(30)
time.sleep(1.5)
px.set_dir_servo_angle(0)
time.sleep(1)
px.set_dir_servo_angle(60)
time.sleep(1.5)
px.set_dir_servo_angle(0)
px.forward(30)
time.sleep(1.5)
px.stop()