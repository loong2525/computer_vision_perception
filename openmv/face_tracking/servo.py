'''
Compony: NUC
Date: 2025-10-01 19:45:14
LastEditors: Loong2525
LastEditTime: 2025-10-02 10:31:02
'''
from pyb import Servo
import math , time

class PTZ :
    def __init__(self):
        self.pan=Servo(1)           #舵机1控制水平转动 270（PB7）
        self.tilt=Servo(2)          #舵机2控制竖直转动 180（PB8）
        '''
        '''
        self.pan_value=0            #水平角度 10 value/角度
        self.tilt_value=0           #数值角度 10 value/角度


    def tanslation(angle):    # 将角度值变为pwm值
        pwm = 1500+angle*10
        if pwm > 2420 :
            pwm = 2420
        if pwm < 640 :
            pwm=640
        return pwm

    def set_pan(self,angle):
        self.pan.pulse_width(self.tanslation(angle))

    def set_tilt(self,angle):
        self.tilt.pulse_width(self.tanslation(angle))


# 使用示例
if __name__ == "__main__":
    # 创建云台控制器实例
    ptz = PTZ()

    ptz.set_pan(0)
    time.sleep(2)
    print(ptz.tilt.angle())
    ptz.set_pan(0)
    time.sleep(2)
    ptz.set_pan(0)
    time.sleep(2)
    print(ptz.tilt.angle())

    print("finish")

