'''
Compony: NUC
Date: 2025-10-01 22:10:00
LastEditors: Loong2525
LastEditTime: 2025-10-02 21:10:25
'''
'''
@ description: 代码适用于openmvM4，舵机云台（pan为270°，tilt为180°）
        其他角度云台需要重写servo.py中tanslation方法
@ readme：https://www.cnblogs.com/loong2525/articles/19108654
'''
import sensor, image, time
from pid import PID
from servo import PTZ



#pan_pid = PID(p=0.07, i=0, imax=90)    #脱机运行或者禁用图像传输，使用这个PID
#tilt_pid = PID(p=0.05, i=0, imax=90)   #脱机运行或者禁用图像传输，使用这个PID
pan_pid = PID(p=0.08, i=0.01, imax=90)  #在线调试使用这个PID
tilt_pid = PID(p=0.05, i=0.02, imax=90)#在线调试使用这个PID

sensor.reset()                          # Initialize the camera sensor.
sensor.set_contrast(3)                  # 增强对比度，便于特征检测
sensor.set_gainceiling(16)              # 限制增益，减少噪声
sensor.set_pixformat(sensor.GRAYSCALE)  # use RGB565.
sensor.set_framesize(sensor.QVGA)       # use QQVGA for speed.
sensor.set_vflip(False)       
sensor.skip_frames(10)                  # Let new settings take affect.
sensor.set_auto_whitebal(False)         # 关闭自动白平衡，保持一致性
clock = time.clock() # Tracks FPS.
face_cascade = image.HaarCascade("frontalface", stages=25)

def find_max(blobs):
    max_size = 0
    for blob in blobs :
        if blob[2]*blob[3] > max_size:
            max_blob = blob
            max_size = blob[2]*blob[3]
    return max_blob
    '''
    blob[0]：矩形左上角的x坐标
    blob[1]：矩形左上角的y坐标
    blob[2]：矩形的宽度（width）
    blob[3]：矩形的高度（height）
    '''
ptz = PTZ()
ptz.set_pan(0)
ptz.set_tilt(0)

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.

    faces = img.find_features(face_cascade, threshold=0.75, scale=1.25)
    
    if faces:
        face = find_max(faces)
        cx = int(face[0]+face[2]/2)
        cy = int(face[1]+face[3]/2)
        pan_error = cx-img.width()/2
        tilt_error = cy-img.height()/2

        print("pan_error: ", pan_error)

        img.draw_rectangle(face) # rect
        img.draw_cross(cx, cy) # cx, cy

        pan_output=pan_pid.get_pid(pan_error,1)
        tilt_output=tilt_pid.get_pid(tilt_error,1)
        print("pan_output",pan_output)
        ptz.set_pan(int(ptz.pan.angle()-pan_output))
        ptz.set_tilt(int(ptz.tilt.angle()-tilt_output))
