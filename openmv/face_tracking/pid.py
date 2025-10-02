'''
Compony: NUC
Date: 2025-10-01 11:59:42
LastEditors: Loong2525
LastEditTime: 2025-10-02 19:58:31
'''
from pyb import millis
from math import pi, isnan

class PID:
    _kp = _ki = _kd = _integrator = _imax = 0
    _last_error = _last_derivative = _last_t = 0
    _RC = 1/(2 * pi * 20)

    def __init__(self, p=0, i=0, d=0, imax=0):
        self._kp = float(p)
        self._ki = float(i)
        self._kd = float(d)
        self._imax = abs(imax)                  # 积分限幅
        self._last_derivative = float('nan')

    def get_pid(self, error, scaler):
        tnow = millis()
        dt = tnow - self._last_t
        output = 0
        if self._last_t == 0 or dt > 1000:      # 超过一定时间（1000）则积分项归0
            dt = 0
            self.reset_I()
        self._last_t = tnow # 时间递推

        delta_time = float(dt) / float(1000)    # t的单位从ms变为s

        output += error * self._kp              # 比例项输出

        if abs(self._kd) > 0 and dt > 0:
            if isnan(self._last_derivative):
                derivative = 0
                self._last_derivative = 0
            else:   
                #deltaerror/delttime，微分公式
                derivative = (error - self._last_error) / delta_time
                
            # 对微分项滤波
            derivative = self._last_derivative + \
                                     ((delta_time / (self._RC + delta_time)) * \
                                        (derivative - self._last_derivative))
            
            self._last_error = error #误差递推
            self._last_derivative = derivative # 微分项递推

            output += self._kd * derivative
        output *= scaler                  # 微分项输出
        
        if abs(self._ki) > 0 and dt > 0:
            self._integrator += (error * self._ki) * scaler * delta_time
            if self._integrator < -self._imax: self._integrator = -self._imax
            elif self._integrator > self._imax: self._integrator = self._imax
            output += self._integrator# 积分项输出
        return output
    
    def reset_I(self):
        self._integrator = 0
        self._last_derivative = float('nan')