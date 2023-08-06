import numpy as np
from .led import LED
from .room import Room
from ..error import VLPSequenceLenError

class PD:
    def __init__(self,
                n=1.5,
                fov=60,
                Ar=1e-4,
                Ts=1,
                pos:tuple=(0,0,0),
                alpha=0, 
                beta=0,
                *args,
                **kwargs) -> None:
        """ 
        n: 透镜的折射率
        fov: 接收视场角 (单位: 度)
        Ar: PD检测器的接收面积(单位:平方米)
        Ts: 光学滤波器的增益
        pos: PD参考位置(注意:self._pos为参考位置,self.pos为相对位置) 
        alpha: PD方位角(单位: 度)
        beta: PD倾斜角(单位: 度)
        """
        self.n = n
        self.fov = fov
        self.Ar = Ar
        self.Ts = Ts

        self.pos = pos
        self.origin = (0,0,0) #原点位置

        self.alpha = alpha
        self.beta = beta
    
    @staticmethod
    def tilt_pd_surface(r, l, alpha, center_tp_pos:tuple):
        """头盔曲球面:倾斜PD和中心参考点位置关系
        Params
            r: 曲球面半径(单位:米)
            l: 倾斜PD到顶部中心(参考点)的弧长(单位:米)   
            alpha:倾斜PD方位角(单位:度) 
            center_tp_pos: 测试点位置 
        Return
            (xr,yr,zr): 倾斜PD位置
            (alpha,beta): 倾斜PD的方位角和倾斜角(单位:度)
        """
        # 倾斜PD的方位角和倾斜角
        alpha_rad = alpha*np.pi/180 # 角度制转弧度制
        beta_rad = l/r   # PD倾斜角

        assert 0 <= beta_rad <= np.pi/2 # 限定
        [x0, y0, z0] = np.array(center_tp_pos, dtype=np.float) #测试点位置

        L = r * np.tan(beta_rad/2) * (1 + np.cos(beta_rad)) # 倾斜PD到顶部中心的水平距离
        H = r * np.tan(beta_rad/2) * np.sin(beta_rad)  # 倾斜PD到顶部中心的垂直距离
        # 倾斜PD位置
        xr = x0 + L * np.cos(alpha_rad) 
        yr = y0 + L * np.sin(alpha_rad) 
        zr = z0 - H

        beta = np.degrees(beta_rad) # 弧度制转角度制
        return (xr,yr,zr), (alpha,beta) 

    @staticmethod
    def tilt_pd_frame(l, alpha, beta, center_tp_pos:tuple):
        """PD支架:倾斜PD和中心参考点位置关系
        Params
            l: 倾斜PD到中心水平PD(参考点)的长度(单位:米)
            alpha: 倾斜PD方位角(单位:度)
            beta: 倾斜PD倾斜角(单位:度)
            center_tp_pos: 水平中心测试点位置
        Return
            (xr,yr,zr): 倾斜PD位置
            (alpha,beta): 倾斜PD的方位角和倾斜角(单位:度)
        """
        [x0, y0, z0] = np.array(center_tp_pos, dtype=np.float)  #水平中心测试点位置
        # 倾斜PD的方位角和倾斜角,角度制转弧度制
        alpha_rad = alpha*np.pi/180
        beta_rad = beta*np.pi/180

        xr = x0 + l * np.cos(alpha_rad) * np.cos(beta_rad) 
        yr = y0 + l * np.sin(alpha_rad) * np.cos(beta_rad)
        zr = z0 + l * np.sin(beta_rad)
        return (xr,yr,zr), (alpha,beta) 

    def recv_led_radiation_intensity(self, led:LED):
        """计算LED辐射强度(LOS链路):
        Parameters
            led: LED实例化
        Return 
            LOS链路LED辐射强度
        """
        pd_pos = np.array(self.pos,dtype=np.float) # PD相对位置
        led_pos = np.array(led.pos,dtype=np.float) # LED相对位置
        
        [xr, yr, zr] = pd_pos  # PD位置坐标矩阵
        [xt, yt, zt] = led_pos # led位置

        d = np.sqrt((xt-xr)**2 + (yt-yr)**2 + (zt-zr)**2) # LED灯到PD接收器的距离 (l,w,h) 
        cos_led_t_angle_rad_rad = np.abs(zt - zr) / d # LED发射角的余弦值 (l,w,h)  

        R0 = ((led.m + 1)  / (2 * np.pi)) * cos_led_t_angle_rad_rad**led.m  # 辐射强度模型 (l,w,h)

        # 如果LED发送的是直流信号
        if led.is_dc:
            return R0 * led.send_signal  # LED辐射强度 (l,w,h)

        # LED发送的是交流信号
        """
        H0 = H0.flatten() #打平 (l,w) -> (l*w,)
        return np.array([np.convolve(h,led.send_signal) for h in H0])  #卷积 (l*w,npt)
              <=> np.array([h * led.send_signal for h in H0])          #相乘 (l*w,npt) 
        """
        R0 = np.expand_dims(R0,-1) # 在最后一维扩充一个维度 (l,w,h) -> (l,w,h,1)  <=> H0.reshape(l,w,h,1) <=> H0[...,np.newaxis]
        radiation_intensity = R0 * led.send_signal # LED辐射强度[广播机制 (l,w,h,1) * (npt) -> (l,w,h,npt) * (l,w,h,npt) = (l,w,h,npt)]
        return np.squeeze(radiation_intensity)  # (l,w,h,npt).如果npt==1,则返回形状为(l,w,h)

    def recv_los_led_signal(self, led:LED):
        """计算PD接收LED信号(LOS链路):
        Parameters
            led: LED实例化
        Return 
            LOS链路中PD探测器接收LED信号
        """
        pd_pos = np.array(self.pos,dtype=np.float) # PD相对位置
        led_pos = np.array(led.pos,dtype=np.float) # LED相对位置
        
        [xr, yr, zr] = pd_pos  # PD位置坐标矩阵
        [xt, yt, zt] = led_pos # led位置

        # PD方位角和倾斜角,角度制转弧度制
        alpha_rad = self.alpha*np.pi/180
        beta_rad = self.beta*np.pi/180

        d = np.sqrt((xt-xr)**2 + (yt-yr)**2 + (zt-zr)**2) # LED灯到PD接收器的距离 (l,w,h) 
        cos_led_t_angle_rad_rad = np.abs(zt - zr) / d # LED发射角的余弦值 (l,w,h)
        h = (xt-xr) * np.cos(alpha_rad) * np.sin(beta_rad) + \
            (yt-yr) * np.sin(alpha_rad) * np.sin(beta_rad) + \
            (zt-zr) * np.cos(beta_rad) # PD到LED方向向量在PD接收面法向量上的投影 (l,w,h) 
        cos_pd_r_angle_rad = h / d # PD接收器入射角的余弦值 (l,w,h)   
          
        pd_r_angle_rad = np.arccos(cos_pd_r_angle_rad) # PD接收器入射角的大小(弧度制) (l,w,h)
        pd_r_angle = np.degrees(pd_r_angle_rad) # 弧度制转为角度制 (l,w,h)
  
        H0 = (((led.m + 1) * self.Ar) / (2 * np.pi * d**2)) * cos_led_t_angle_rad_rad**led.m * cos_pd_r_angle_rad * self.Ts * self.G_Con # 信道增益 (l,w,h)
        H0 = np.where((pd_r_angle>=0) & (pd_r_angle<=self.fov), H0, 0)  # 视场内信道增益 (l,w,h) <=> np.place(H0,(phi>=0)&(phi<=pd.fov),0)

        # 以下是为了兼容交直流信号
        """
        H0 = H0.flatten() #打平 (l,w) -> (l*w,)
        return np.array([np.convolve(h,led.send_signal) for h in H0])  #卷积 (l*w,npt)
              <=> np.array([h * led.send_signal for h in H0])          #相乘 (l*w,npt) 
        """
        H0 = np.expand_dims(H0,-1) # 在最后一维扩充一个维度 (l,w,h) -> (l,w,h,1)  <=> H0.reshape(l,w,h,1) <=> H0[...,np.newaxis]
        recv_signal = H0 * led.signal # PD接收信号 [广播机制 (l,w,h,1) * (npt) -> (l,w,h,npt) * (l,w,h,npt) = (l,w,h,npt)]
        return np.squeeze(recv_signal) # (l,w,h,npt).如果npt==1,则返回形状为(l,w,h)

    
    def recv_nlos_led_signal(self, led:LED, room:Room):
        """计算PD接收LED一次反射信号(NLOS链路):
        Params
            led: LED实例化
            room: Room实例化
        Return 
            NLOS链路中PD探测器接收LED一次反射信号
        """
        pd_pos = np.array(self.pos,dtype=np.float) # PD相对位置
        led_pos = np.array(led.pos,dtype=np.float) # LED相对位置
        
        # 
        [xr, yr, zr] = pd_pos  # PD位置坐标矩阵[测试点位于空间区域内:(l,w,h), 测试点位于一个平面区域:(l,w)]
        [xt, yt, zt] = led_pos # led位置
        
        # 对PD坐标张量扩充两个维度,以便使用广播
        xr = xr[...,np.newaxis,np.newaxis]  # (l,w,h,1,1) 
        yr = yr[...,np.newaxis,np.newaxis]  # (l,w,h,1,1)
        zr = zr[...,np.newaxis,np.newaxis]  # (l,w,h,1,1)

        H0 = 0  #反射（LOS）链路信道增益
        # 遍历每一面反射墙壁参数:((l1,w1),(l1,w1),(l1,w1)), ((l1,w1),(l1,w1))
        for i, ((xw, yw, zw), (w_alpha, w_beta)) in enumerate(room.get_reflect_wall_args()):
            # 墙壁反射单元的方向角和倾斜角,角度制转弧度制
            w_alpha_rad = w_alpha*np.pi/180
            w_beta_rad = w_beta*np.pi/180

            # LED -> 墙壁反射单元
            d1 = np.sqrt((xt-xw)**2 + (yt-yw)**2 + (zt-zw)**2)  # LED灯到墙壁反射单元的距离 (l1,w1)
            cos_led_t_angle_rad = np.abs(zt - zw) / d1 # LED发射角的余弦值 (l1,w1)
            h1 = (xt-xw) * np.cos(w_alpha_rad) * np.sin(w_beta_rad) + \
                 (yt-yw) * np.sin(w_alpha_rad) * np.sin(w_beta_rad) + \
                 (zt-zw) * np.cos(w_beta_rad)  # 墙壁反射单元到LED方向向量在墙壁反射单元法向量上的投影 (l1,w1)
            cos_wall_r_angle_rad = h1 / d1 # 墙壁反射单元入射角 (l1,w1)
            
            # 墙壁反射单元 -> PD
            d2 = np.sqrt((xw-xr)**2 + (yw-yr)**2 + (zw-zr)**2)  # 墙壁反射单元到PD之间的距离 (l,w,h,l1,w1)
            h2 = (xr-xw) * np.cos(w_alpha_rad) * np.sin(w_beta_rad) + \
                 (yr-yw) * np.sin(w_alpha_rad) * np.sin(w_beta_rad) + \
                 (zr-zw) * np.cos(w_beta_rad)  # 墙壁反射面到PD方向向量在墙壁反射单元法向量上的投影  (l,w,h,l1,w1)

            # 1.限定d2(除数)不为0 (去掉墙壁反射单元和参考点重合)  2.限定cos_wall_t_angle_rad不小于0 
            h2 = np.where((d2>0) & (h2>0), h2, 0) # 限定cos_wall_t_angle_rad不小于0，并使得d2中为0的元素（反射点与测试点重合）对应位置上h2元素为0
            d2 = np.where((d2>0), d2, 1)  # 使得d2中为0的元素等于一个不为0的数,且h2为0,从而cos_wall_t_angle_rad为0
            cos_wall_t_angle_rad = h2 / d2    # 墙壁反射单元发射角  (l,w,h,l1,w1)

            # PD的方向角和倾斜角,角度制转弧度制
            alpha_rad = self.alpha*np.pi/180
            beta_rad = self.beta*np.pi/180
            h = (xw-xr) * np.cos(alpha_rad) * np.sin(beta_rad) + \
                (yw-yr) * np.sin(alpha_rad) * np.sin(beta_rad) + \
                (zw-zr) * np.cos(beta_rad) # PD到墙壁反射单元方向向量在PD接收面法向量上的投影 (l,w,h,l1,w1)

            h = np.where((d2>0) & (h>0), h, 0) # 限定cos_pd_r_angle不小于0，并使得d2中为0的元素（反射点与测试点重合）对应位置上h元素为0    
            cos_pd_r_angle_rad = h / d2 # PD接收角的余弦值   (l,w,h,l1,w1)

            pd_r_angle_rad = np.arccos(cos_pd_r_angle_rad) # PD接收器入射角(弧度制) (l,w,h,l1,w1)
            pd_r_angle = np.degrees(pd_r_angle_rad) # 弧度制转为角度制 (l,w,h,l1,w1)

            rho = room.rho[i]   #墙壁反射率
            Aw = room.Aw[i]     #墙壁反射单元面积

            # 反射(NLOS)链路信道增益 (l,w,h,l1,w1)
            Hw = (((led.m + 1) * self.Ar) / (2 * np.pi**2 * d1**2 * d2**2)) * rho * Aw * cos_led_t_angle_rad**led.m * cos_wall_r_angle_rad * cos_wall_t_angle_rad *  cos_pd_r_angle_rad * self.Ts * self.G_Con  # 信道增益 
            Hw = np.where((pd_r_angle>=0) & (pd_r_angle<=self.fov), Hw, 0)  # 视场内信道增益 (l,w,h,l1,w1)

            pd_pos_shape = Hw.shape[:-2] # pd坐标矩阵形状【测试点位于空间区域内:(l,w,h), 测试点位于一个平面区域:(l,w)】
            l1, w1 = Hw.shape[-2:]    # 墙壁反射单元坐标形状 (l1,w1)
            Hw = Hw.reshape(*pd_pos_shape, l1*w1)  # 重塑形状 (l,w,h,l1*w1)
            Hw = np.sum(Hw, axis=-1)     # 墙壁反射面增益 (l,w,h)
            H0 += Hw  # 墙壁反射(NLOS)链路信道增益(l,w,h)
        
        H0 = np.expand_dims(H0,-1) # 在最后一维扩充一个维度 (l,w,h) -> (l,w,h,1)  <=> H0.reshape(l,w,h,1) <=> H0[...,np.newaxis]
        recv_signal = H0 * led.signal # PD接收信号[广播机制 (l,w,h,1) * (npt) -> (l,w,h,npt) * (l,w,h,npt) = (l,w,h,npt)]
        return np.squeeze(recv_signal)
    
    def recv_led_signal(self, led:LED, room:Room):
        """计算PD接收LED信号(LOS+NLOS链路):
        Params
            led: LED实例化
            room: Room实例化
        Return 
            LOS+NLOS链路中PD探测器接收LED信号
        """
        recv_los_signal = self.recv_los_led_signal(led=led)  # PD接收直射链路信号
        recv_nlos_signal = self.recv_nlos_led_signal(led=led, room=room) # PD接收一次反射链路信号
        return recv_los_signal + recv_nlos_signal

    def shot_noise(self,P,R=0.4,Ibg=5,I2=0.562,B=100,*argv,**kwargv):
        """获取PD散粒噪声功率
        Params
            P: PD接收功率(W)
            R: PD响应度(A/W)
            Ibg: 暗电流(uA)
            I2: 噪声带宽系数
            B: 噪声带宽(MHz)
        Return 
            PD散粒噪声功率
        """
        q = 1.6e-19  # 电子电荷量(C)
        # Ibg *= 1e-6  # 单位换算 （1 A = 1e6 uA）
        # B *= 1e6  
        return 2*q*R*P + 2*q*Ibg*I2*B
    
    def thermal_noise(self,Tk=300,G=10,eta=112,B=100,I2=0.562,I3=0.0868,gamma=1.5,gm=30,*argv,**kwargv):
        """获取PD热噪声功率
        Params
            Tk: 热力学温度:Tk = T + 273.15°C(K)
            G: 开环电压增益
            eta: PD每单位面积上固定电容(pF/cm2)
            B: 噪声带宽(MHz)
            I2: 噪声带宽系数 
            I3: 噪声带宽系数 
            gamma: 信道噪声系数
            gm: 跨导(m/S)
        Return
            PD热噪声功率
        """
        k = 1.38e-23  # 玻尔兹曼常数
        eta *= 1e-8 # 单位换算（1pF/cm2 = 1e-8F/m2）
        B *= 1e6
        gm *= 1e-3
        return 8*np.pi*k*Tk/G*eta*self.Ar*I2*B**2 + \
            16*np.pi**2*k*Tk*gamma/gm*eta**2*self.Ar**2*I3*B**3

    def recv_noise_signal(self, *argv,**kwargv):
        """接收噪声信号功率
        """
        return self.shot_noise(*argv, **kwargv) + self.thermal_noise(*argv, **kwargv)

    @property
    def origin(self) -> tuple:
        """设置原点位置
        """
        return self._origin

    @origin.setter
    def origin(self,o):
        """获取原点位置
        """
        if not len(o) == 3:
            raise VLPSequenceLenError(o,3)
        self._origin = tuple(o) 

    @property
    def pos(self) -> tuple:
        """获取相对位置(参考位置相对与原点的相对位置)
        """
        return tuple(i+j for i,j in zip(self._pos,self.origin))
    
    @pos.setter
    def pos(self,pos:tuple):
        """设置参考位置
        """
        if not len(pos) == 3:
            raise VLPSequenceLenError(pos,3)
        self._pos = tuple(pos)
    
    @property
    def alpha(self):
        """获取PD方位角(单位: 度)
        """
        return self._alpha
    
    @alpha.setter
    def alpha(self,alpha):
        """设置PD方位角(单位: 度)
        """
        self._alpha = alpha 

    @property
    def beta(self):
        """获取PD倾斜角(单位: 度)
        """
        return self._beta
    
    @beta.setter
    def beta(self,beta):
        """设置PD倾斜角(单位: 度)
        """
        self._beta = beta 

    @property
    def fov(self):
        """获取接收视场角 (单位: 度)
        """    
        return self._fov

    @fov.setter
    def fov(self,fov): 
        """设置接收视场角 (单位: 度)
        """
        assert 0 <= fov <= 90
        self._fov = fov

    @property
    def Ar(self):   
        """获取PD检测器的接收面积(单位:平方米)
        """ 
        return self._Ar

    @Ar.setter
    def Ar(self,a): 
        """设置PD检测器的接收面积(单位:平方米)
        """
        self._Ar = a

    @property
    def Ts(self):   
        """获取光学滤波器的增益 
        """ 
        return self._Ts

    @Ts.setter
    def Ts(self,ts): 
        """设置光学滤波器的增益 
        """
        self._Ts = ts

    @property
    def n(self): 
        """获取透镜的折射率
        """   
        return self._n

    @n.setter
    def n(self,n): 
        """设置透镜的折射率
        """
        self._n = n

    @property
    def G_Con(self):
        """获取聚光器增益
        """
        fov_rad = self.fov * np.pi/180
        return self.n**2 / np.sin(fov_rad)**2  

