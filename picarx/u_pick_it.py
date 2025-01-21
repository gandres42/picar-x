from picarx_improved import Picarx
import time

px = Picarx()
try:
    while True:
        cmd = input("select one of the following using 1/2/3:\n  1. forward/backward\n  2. parallel parking\n  3. three point turn\n")
        if cmd == '1':
            print("running forward/backward")
            px.forward(50)
            time.sleep(2)
            px.backward(50)
            time.sleep(2)
            px.stop()
        elif cmd == '2':
            print("running parallel park")
            px.set_dir_servo_angle(-60)
            px.backward(40)
            time.sleep(1.5)
            px.set_dir_servo_angle(0)
            time.sleep(1)
            px.set_dir_servo_angle(60)
            time.sleep(2.15)
            px.set_dir_servo_angle(0)
            px.forward(40)
            time.sleep(1)
            px.stop()
        elif cmd == '3':
            print("running three point turn")
            px.set_dir_servo_angle(-60)
            px.forward(30)
            time.sleep(1)
            px.set_dir_servo_angle(60)
            px.backward(30)
            time.sleep(1)
            px.set_dir_servo_angle(-60)
            px.forward(30)
            time.sleep(1)
            px.set_dir_servo_angle(0)
            time.sleep(1)
            px.stop()
        else:
            print("invalid selection,", end=" ")
except KeyboardInterrupt():
    px.stop()