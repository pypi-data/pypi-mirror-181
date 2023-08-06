'''
Date         : 2022-12-18 12:33:46
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2022-12-18 14:02:30
LastEditors  : BDFD
Description  : 
FilePath     : \WES_Calculation\windspeed.py
Copyright (c) 2022 by BDFD, All Rights Reserved. 
'''
# Calculations
import numpy as np
import math
import matplotlib.pyplot as plt

import io
import base64
from datetime import datetime as dt
import time


def windspeed(o2, zw, Xlat, X, Rg, U, atm, Ta, zt, Tw, TaaC, wdu, zu):
    if o2==3:
        X=42 # distance from an overwater loaction to the shore, or fetch length (km)
    if o2==4 or o2==3:    
        Xlat=-44 # average latitude of fetch (+: for the Northern hemisphere, -: for the Southern hemisphere); required when o2 = 4 or 3   
    if o2==4: 
        Rg=.7 # Rg=U10/Ug, read from Figure II-2-13 in CEM 2015
    
    # Secondary (default)
    tol=0.0001 # Iteration tolerance
    z0l=0.03# overland z0 (m)  
    z0=0.003# initial value of z0 (m) 
    z02=z0 # for B-D
    k=0.4 # von Karman Constant (approximately 0.4)
    c1=.11# a coefficient in estimating z0 for wind profile  
    c2=.0185# a coefficient in estimating z0 for wind profile  
    c3=0# a coefficient in estimating z0 for wind profile  
    gammap=18
    phi1u=5  
    phi1l=0.0
    va=1.4607/100000# kinematic viscosity of air at 280 K degrees  
    Cdlc=0.00255 # an coefficient in Cdland
    dU=0.001 # a step applied for the numerical derivative in the Newton-Raphson method solving 1-h U10 for API RP 2A-WSD (m/s)
    zcsy=120 # height of constant-stress later
    Uu=50 # the maximum windspeed for profile illustration (m/s)

    #legend_font = {'family' : 'Times New Roman'}
    plt.rc('legend', fontsize='small')# medium

    # Functions 
    def phi1f(z,x): # a function of solving phi (phi^4-gammap*phi^3*z/L'=1), in which x=L'.
        le=phi1l # the upper end of phi range
        ue=phi1u # the lower end of phi range
        mp=0.5*(le+ue) # the mid point between both ends
        while abs(mp**4-gammap*mp**3*z/x-1)>tol:   
            if mp**4-gammap*mp**3*z/x-1>0:
                ue=mp 
            else:
                le=mp
            mp=0.5*(le+ue)
        return mp

    def psi1f(x): # the psi function in terms of phi (for KEYPS Model) 
        y=1-x-3*math.log(x)+2*math.log(0.5+0.5*x)+2*math.atan(x)-0.5*math.pi+math.log(0.5+0.5*x**2)
        return y

    def psi2f(x): # the psi function in terms of phi (for B-D Model) 
        y=math.log((1+x)**2*(1+x**2)/8)-2*math.atan(x)+0.5*math.pi 
        return y

    def A(x): # A function in the ABL resistance law
        if x<=0:
            Af = 1.1+3.7241*math.log(1-0.02*x)
        else:
            Af = 1.1-6.364*math.log(1+0.02*x)			 
        return Af

    def B(x): # B function in the ABL resistance law
        if x<=0:
            Bf = 4.3-(4.3-0.23)*(1-math.exp(0.03*x))         
        else:
            Bf = 4.3+0.7*x**0.5			 
        return Bf

    def att(u1,t1,t2): # a function transforming widnspeeds between different averaging times (AT) by the CEM method
    # u1: windspeed (m/s) at AT t1 (min), u2: windspeed (m/s) at AT t2 (min)
        if 1/60<t1<=60:
            if 1/60<t2<=60:
                if t2==60:                
                    u2=np.array(u1)/(1.277+0.296*math.tanh(0.9*math.log10(45/t1/60)))*(t1!=60)+np.array(u1)*(t1==60)
                else:
                    u2=(1.277+0.296*math.tanh(0.9*math.log10(45/t2/60)))*np.array(u1)/(1.277+0.296*math.tanh(0.9*math.log10(45/t1/60)))*(t1!=60)+(1.277+0.296*math.tanh(0.9*math.log10(45/t2/60)))*np.array(u1)*(t1==60)
            if 60<t2<600:
                u2=(1.5334-0.15*math.log10(t2*60))*np.array(u1)/(1.277+0.296*math.tanh(0.9*math.log10(45/t1/60)))*(t1!=60)+(1.5334-0.15*math.log10(t2*60))*np.array(u1)*(t1==60)       
        if 60<t1<600:
            if 1/60<t2<=60:
                if t2==60:
                    u2=np.array(u1)/(1.5334-0.15*math.log10(t1*60))
                else:
                    u2=(1.277+0.296*math.tanh(0.9*math.log10(45/t2/60)))*np.array(u1)/(1.5334-0.15*math.log10(t1*60))
            if 60<t2<600:
                Up1=(1.5334-0.15*math.log10(t2*60))*np.array(u1)/(1.5334-0.15*math.log10(t1*60))
        return u2


    # 1. Basic Windspeed Calculations
    if TaaC==None:
        TaaC=Ta
    Taa=TaaC+273.15 # known mean air temperature of the constant-stress layer (K)

    dT=Ta+zt*9.8/1000-Tw # air-sea potential temperature difference at C Degrees (= air temeprature - water surface temperature)
    if abs(dT)<tol*10:
        dT=0
    plt.scatter(Ta,zt,marker="x",s=40,color="black",label='已知气温及对应高度')
    plt.scatter(Tw,0,marker="x",s=40,color="black")
    plt.axvline(TaaC,ls=":",color="black",linewidth=2,label='大气表面层的平均气温')

    section1 = []
    heading = ' '
    section1.extend(['---总说明---'])
    section1.extend(['. 图中的风速廓线均指水上风速。水面以上10 m处风速(U\u2081\u2080)的数值结果见下表。'])
            
    if dT==0:
        section1.extend(['. 大气表面层的稳定性状态：中性'])
    if dT>0:
        section1.extend(['. 大气表面层的稳定性状态：稳定'])
    if dT<0:
        section1.extend(['. 大气表面层的稳定性状态：不稳定'])

    section2 = []
    section2.extend(['---滨水工的风速计算方法---'])
    nn=0 # order number of notes
    ssBD1=0 # for B-D

    zp1=[j for j in range(0,zu+1)] # z values for KEYPS profile
    zp2=[j for j in range(0,zu+1)] # z values for B-D profile
    Up1=[1 for j in range(0,zu+1)] # windspeeds on KEYPS profile
    Up2=[1 for j in range(0,zu+1)] # windspeeds on B-D profile

    # KEYPS和B-D风速廓线及大气层阻力定律

    # various initial values
    if o2==1 or o2==2:
        if o2==1:
            plt.scatter(U,zw,c="blue",marker="*",s=70,edgecolors="blue",label='已知的'+str(round(atm))+'-min水上风速及对应高度')
        if o2==2:
            section2.ex(['. 本例中的已知陆上风速可视为水上风速。'])
        
        Uf0=k*U/math.log(zw/z0) # the initial value of friction velocity
        Uf20=Uf0# for B-D
        if dT!=0:
            Lp0=Taa/k**2/9.81*Uf0**2*math.log(zt/z0)/dT      
            
        z0=c1*va/Uf0+c2*Uf0**2/9.81+c3
        z02=c1*va/Uf20+c2*Uf20**2/9.81+c3

        if dT==0: # neutral
            Uf=k*U/math.log(zw/z0)
            
        if dT>0: # stable
            Uf=k*U/(math.log(zw/z0)+7*zw/Lp0)
            Lp=Taa/k**2/9.81*Uf**2*(math.log(zt/z0)+7*zt/Lp0-7*z0/Lp0)/dT

            Ri2=min(0.199,9.81*k**2*(zt-z02)*dT*0.95/Taa/Uf20**2/math.log(zt/z02)) # for B-D  
            L0=(1-5*Ri2)*(zt-z02)/Ri2
            Uf2=k*U/(math.log(zw/z02)+6*zw/L0-6*z02/L0) 
            Ri2=min(0.199,9.81*k**2*(zt-z02)*dT*(0.95+7.8*(zt-z02)/L0)/Taa/Uf2**2/(math.log(zt/z02)+7.8*zt/L0-7.8*z02/L0)/(1+6*(zt-z02)/L0)**2) # for B-D
            L=(1-5*Ri2)*(zt-z02)/Ri2
            
        if dT<0: # unstable
            phi1=phi1f(zw,Lp0)
            psi1=psi1f(phi1)
            Uf=k*U/(math.log(zw/z0)-psi1+psi1f(phi1f(z0,Lp0)))
            Lp=Taa/k**2/9.81*Uf**2*(math.log(zt/z0)-psi1f(phi1f(zt,Lp0))+psi1f(phi1f(z0,Lp0)))/dT

            Ri2=9.81*k**2*(zt-z02)*dT*0.95/Taa/Uf20**2/math.log(zt/z02) # for B-D  
            L0=(zt-z02)/Ri2
            psi2=psi2f((1-19.3*zw/L0)**0.25)
            Uf2=k*U/(math.log(zw/z02)-psi2+psi2f((1-19.3*z02/L0)**0.25))
            Ri2=9.81*k**2*(zt-z02)*dT*(0.95*(1-11.6*(zt-z02)/L0))**(-0.5)/Taa/Uf2**2/(math.log(zt/z02)-psi2f((1-19.3*zt/L0)**0.25)+psi2f((1-19.3*z02/L0)**0.25))/(1-19.3*(zt-z02)/L0)**(-0.5)  # for B-D
            L=(zt-z02)/Ri2

    if o2==4 or o2==3:

        fCo=1.45*math.sin(Xlat*math.pi/180)/10000 # original Coriolis parameter
        fC=abs(fCo) # the absolute value of fCo which will be used in various calculations
        
        if o2==3: 
            Ufl=k*U/math.log(zw/z0l) # friction velocity for overland wind       
            Ug=Ufl*((math.log(Ufl/fC/z0l)-A(0))**2+B(0)**2)**0.5/k # estimated geostrophic windspeed
            #Ug=Ufl/.0275
            plt.axvline(Ug,ls="--",color="blue",linewidth=0.5,label='推算的'+str(round(atm))+'-min $U_g$ (自由大气中)')
            # nn=nn+1
            section2.extend(['. 陆域风速对数分布律参数： 摩擦风速U*=',round(Ufl,3),'m/s'])
            # nn=nn+1
            section2.extend(['. 根据已知陆域风推算的地转风速Ug=',round(Ug,3),'m/s'])            
        if o2==4:
            Ug=U # geostrophic windspeed (measured)
            plt.axvline(Ug,ls="--",color="blue",linewidth=0.5,label='已知的'+str(round(atm))+'-min $U_{g}$ (自由大气中)')
        plt.text(Ug-1.,2,'$U_{g}$',fontdict=None)    

        #overwater    
        Uf0=1 # initial value
        Uf20=Uf0# for B-D
        if dT!=0:
            Lp0=Taa/k**2/9.81*Uf0**2*math.log(zt/z0)/dT

        Uf=k*Ug/((math.log(Uf0/fC/z0)-A(0))**2+B(0)**2)**0.5    
        theta=math.asin(B(0)*Uf/k/Ug)*(Xlat<=0)+math.asin(-B(0)*Uf/k/Ug)*(Xlat>0)

        Uf2=k*Ug/((math.log(Uf20/fC/z02)-A(0))**2+B(0)**2)**0.5    
        theta2=math.asin(B(0)*Uf2/k/Ug)*(Xlat<=0)+math.asin(-B(0)*Uf2/k/Ug)*(Xlat>0)
        
        if dT>0:
            Lp=Taa/k**2/9.81*Uf**2*(math.log(zt/z0)+7*zt/Lp0-7*z0/Lp0)/dT

            Ri2=min(0.199,9.81*k**2*(zt-z02)*dT*0.95/Taa/Uf20**2/math.log(zt/z02)) # for B-D  
            L0=(1-5*Ri2)*(zt-z02)/Ri2
            Ri2=min(0.199,9.81*k**2*(zt-z02)*dT*(0.95+7.8*(zt-z02)/L0)/Taa/Uf2**2/(math.log(zt/z02)+7.8*zt/L0-7.8*z02/L0)/(1+6*(zt-z02)/L0)**2) # for B-D
            L=(1-5*Ri2)*(zt-z02)/Ri2
            
        if dT<0:
            Lp=Taa/k**2/9.81*Uf**2*math.log(zt/z0)/dT

            Ri2=9.81*k**2*(zt-z02)*dT*0.95/Taa/Uf20**2/math.log(zt/z02) # for B-D  
            L0=(zt-z02)/Ri2
            psi2=psi2f((1-19.3*zt/L0)**0.25)
            Ri2=9.81*k**2*(zt-z02)*dT*(0.95*(1-11.6*(zt-z02)/L0))**(-0.5)/Taa/Uf2**2/(math.log(zt/z02)-psi2+psi2f((1-19.3*z02/L0)**0.25))/(1-19.3*(zt-z02)/L0)**(-0.5)  # for B-D
            L=(zt-z02)/Ri2

    # various iterations

    if dT==0:
        if o2==1 or o2==2:
            while abs(Uf-Uf0)>tol: 
                z0=c1*va/Uf+c2*Uf**2/9.81+c3    
                Uf0=Uf
                Uf=k*U/math.log(zw/z0)
        else:
            miu=0
            while abs(Uf-Uf0)>tol:         
                z0=c1*va/Uf+c2*Uf**2/9.81+c3
                Uf0=Uf               
                Uf=k*Ug*math.cos(theta)/(math.log(Uf/fC/z0)-A(0))
                theta=math.asin(B(0)*Uf/k/Ug)*(Xlat<=0)+math.asin(-B(0)*Uf/k/Ug)*(Xlat>0)

        zp1[0]=z0
        Up1=Uf*(np.log(zp1)-np.log(z0))/k
        Up2=Up1
        
    if dT!=0:
        z0=c1*va/Uf+c2*Uf**2/9.81+c3
        z02=c1*va/Uf2+c2*Uf2**2/9.81+c3
        
        if o2==1 or o2==2:    
            while max(abs(Uf-Uf0),abs(Lp-Lp0))>tol:# KEYPS
                z0=c1*va/Uf+c2*Uf**2/9.81+c3    
                Uf0=Uf
                Lp0=Lp

                if dT>0: # stable
                    Uf=k*U/(math.log(zw/z0)+7*(zw-z0)/Lp0)
                    Lp=Taa/k**2/9.81*Uf**2*(math.log(zt/z0)+7*(zt-z0)/Lp0)/dT # initial value of L'
                    
                if dT<0: # unstable
                    Uf=k*U/(math.log(zw/z0)-psi1f(phi1f(zw,Lp0))+psi1f(phi1f(z0,Lp0)))
                    Lp=Taa/k**2/9.81*Uf**2*(math.log(zt/z0)-psi1f(phi1f(zt,Lp0))+psi1f(phi1f(z0,Lp0)))/dT

            while max(abs(Uf2-Uf20),abs(L-L0))>tol:# B-D
                z02=c1*va/Uf2+c2*Uf2**2/9.81+c3
                Uf20=Uf2
                L0=L

                if dT>0: # stable
                    Ri2=9.81*k**2*(zt-z02)*dT*(0.95+7.8*(zt-z02)/L0)/Taa/Uf2**2/(math.log(zt/z02)+7.8*(zt-z02)/L0)/(1+6*(zt-z02)/L0)**2 # for B-D
                    if Ri2>0.199:
                        ssBD1=1
                        Ri2=0.199
                        L=(1-5*Ri2)*(zt-z02)/Ri2
                        Uf2=k*U/(math.log(zw/z02)+6*(zw-z02)/L) 
                        L0=L
                        Uf20=Uf2
                        z02=c1*va/Uf2+c2*Uf2**2/9.81+c3
                    else:
                        L=(1-5*Ri2)*(zt-z02)/Ri2
                        Uf2=k*U/(math.log(zw/z02)+6*(zw-z02)/L)

                if dT<0:
                    Ri2=9.81*k**2*(zt-z02)*dT*(0.95*(1-11.6*(zt-z02)/L0))**(-0.5)/Taa/Uf2**2/(math.log(zt/z02)-psi2+psi2f((1-19.3*z02/L)**0.25))/(1-19.3*(zt-z02)/L0)**(-0.5) 
                    L=(zt-z02)/Ri2
                    psi2=psi2f((1-19.3*zw/L)**0.25)
                    Uf2=k*U/(math.log(zw/z02)-psi2+psi2f((1-19.3*z02/L)**0.25))
                    
            if dT>0:
                z0=c1*va/Uf+c2*Uf**2/9.81+c3   
                Uf=k*U/(math.log(zw/z0)+7*(zw-z0)/Lp) # a final update
                Uzw1=Uf*(math.log(zw/z0)+7*(zw-z0)/Lp)/k # at the measurement elevation for checking
                zp1[0]=z0
                Up1=Uf*(np.log(np.array(zp1)/z0)+7*(np.array(zp1)-z0)/Lp)/k
                Up1n=Uf*np.log(np.array(zp1)/z0)/k # a nuetral profile based on KEYPS model for comparison 

                z02=c1*va/Uf2+c2*Uf2**2/9.81+c3 
                Uf2=k*U/(math.log(zw/z02)+6*(zw-z02)/L)
                Uzw2=Uf2*(math.log(zw/z02)+6*(zw-z02)/L)/k # at the measurement elevation for checking
                zp2[0]=z02
                Up2=Uf2*(np.log(np.array(zp2)/z02)+6*(np.array(zp2)-z02)/L)/k
                Up2n=Uf2*np.log(np.array(zp2)/z02)/k # a nuetral profile based on B-D model for comparison 
                            
            if dT<0:
                z0=c1*va/Uf+c2*Uf**2/9.81+c3   
                Uf=k*U/(math.log(zw/z0)-psi1f(phi1f(zw,Lp))+psi1f(phi1f(z0,Lp)))# a final update
                
                phi1zw=phi1f(zw,Lp)         
                psi1zw=psi1f(phi1zw)
                Uzw1=Uf*(math.log(zw/z0)-psi1zw+psi1f(phi1f(z0,Lp)))/k # at the measurement elevation for checking

                zp1[0]=z0
                for i in range(0,zu+1):
                    phi1z=phi1f(zp1[i],Lp)  
                    psi1z=psi1f(phi1z) 
                    Up1[i]=Uf*(np.log(zp1[i]/z0)-psi1z+psi1f(phi1f(z0,Lp)))/k
                    if Up1[i]<0:
                        Up1[i]=0
                Up1n=Uf*np.log(np.array(zp1)/z0)/k # a nuetral profile based on KEYPS model for comparison 
                
                z02=c1*va/Uf2+c2*Uf2**2/9.81+c3 
                Ri2=9.81*k**2*(zt-z02)*dT*(0.95*(1-11.6*(zt-z02)/L0))**(-0.5)/Taa/Uf2**2/(math.log(zt/z02)-psi2+psi2f((1-19.3*z02/L)**0.25))/(1-19.3*(zt-z02)/L0)**(-0.5)
                L=(zt-z02)/Ri2
                
                psi2zw=psi2f((1-19.3*zw/L)**0.25)
                Uzw2=Uf2*(math.log(zw/z02)-psi2zw+psi2f((1-19.3*z02/L)**0.25))/k
                
                zp2[0]=z02
                for i in range(0,zu+1):
                    psi2z=psi2f((1-19.3*zp2[i]/L)**0.25)
                    Up2[i]=Uf2*(math.log(zp2[i]/z02)-psi2z+psi2f((1-19.3*z02/L)**0.25))/k
                    if Up2[i]<0:
                        Up2[i]=0
                Up2n=Uf2*np.log(np.array(zp2)/z02)/k # a nuetral profile based on B-D model for comparison 
                
        if o2==3 or o2==4:
            
            while max(abs(Uf-Uf0),abs(Lp-Lp0))>tol:# KEYPS    
                z0=c1*va/Uf+c2*Uf**2/9.81+c3    
                Uf0=Uf
                Lp0=Lp
                
                miu=k*Uf/fC/Lp
                Uf=k*Ug*math.cos(theta)/(math.log(Uf/fC/z0)-A(miu))
                theta=math.asin(B(miu)*Uf/k/Ug)*(Xlat<=0)+math.asin(-B(miu)*Uf/k/Ug)*(Xlat>0)
                                
                if dT>0: # stable
                    Lp=Taa/k**2/9.81*Uf**2*(math.log(zt/z0)+7*(zt-z0)/Lp0)/dT
                
                if dT<0: # unstable
                    phi1=phi1f(zt,Lp0)
                    psi1=psi1f(phi1)
                    Lp=Taa/k**2/9.81*Uf**2*(math.log(zt/z0)-psi1+psi1f(phi1f(z0,Lp0)))/dT
    
            miu=k*Uf/fC/Lp
            Uf=k*Ug*math.cos(theta)/(math.log(Uf/fC/z0)-A(miu))

            while max(abs(Uf2-Uf20),abs(L-L0))>tol:# B-D
                z02=c1*va/Uf2+c2*Uf2**2/9.81+c3
                Uf20=Uf2
                L0=L
                            
                miu2=k*Uf2/fC/L
                Uf2=k*Ug*math.cos(theta2)/(math.log(Uf2/fC/z02)-A(miu2))
                theta2=math.asin(B(miu2)*Uf2/k/Ug)*(Xlat<=0)+math.asin(-B(miu2)*Uf2/k/Ug)*(Xlat>0)
                    
                if dT>0: # stable
                    Ri2=9.81*k**2*(zt-z02)*dT*(0.95+7.8*(zt-z02)/L0)/Taa/Uf2**2/(math.log(zt/z02)+7.8*(zt-z02)/L0)/(1+6*(zt-z02)/L0)**2 # for B-D
                    L=(1-5*Ri2)*(zt-z02)/Ri2
                    if Ri2>0.199:
                        ssBD1=1
                        Ri2=0.199                    
                        miu2=200
                        L=k*Uf2/miu2/fC
                        theta2i=math.asin(B(miu2)*Uf2/k/Ug)*(Xlat<=0)+math.asin(-B(miu2)*Uf2/k/Ug)*(Xlat>0)
                        Uf2i=Uf2
                        z02i=z02
                        while max(abs(theta2i-theta2),abs(Uf2i-Uf2),abs(z02i-z02))>tol:
                            theta2=theta2i
                            Uf2=Uf2i
                            z02=z02i

                            z02i=c1*va/Uf2i+c2*Uf2i**2/9.81+c3
                            Uf2i=k*Ug*math.cos(theta2)/(math.log(Uf2/fC/z02)-A(miu2))                    
                            theta2i=math.asin(B(miu2)*Uf2/k/Ug)*(Xlat<=0)+math.asin(-B(miu2)*Uf2/k/Ug)*(Xlat>0)
                            L=k*Uf2/miu2/fC
                            
                        theta2=theta2i
                        Uf2=Uf2i
                        L0=L
                        Uf20=Uf2
                        z02=c1*va/Uf2+c2*Uf2**2/9.81+c3                    
                
                if dT<0: # unstable
                    Ri2=9.81*k**2*(zt-z02)*dT*(0.95*(1-11.6*(zt-z02)/L0))**(-0.5)/Taa/Uf2**2/(math.log(zt/z02)-psi2+psi2f((1-19.3*z02/L)**0.25))/(1-19.3*(zt-z02)/L0)**(-0.5) #???????
                    L=zt/Ri2
                    psi2=psi2f((1-19.3*zt/L)**0.25)
                
            Uf2=k*Ug*math.cos(theta2)/(math.log(Uf2/fC/z02)-A(miu2))# a final update
            
            if dT>0:
                Uzw1=Uf*(math.log(zw/z0)+7*(zw-z0)/Lp)/k # at the measurement elevation for checking  
                zp1[0]=z0
                Up1=Uf*(np.log(np.array(zp1)/z0)+(7*np.array(zp1)-z0)/Lp)/k
                Up1n=Uf*np.log(np.array(zp1)/z0)/k # a nuetral profile based on KEYPS model for comparison 

                Uzw2=Uf2*(math.log(zw/z02)+6*(zw-z02)/L)/k # at the measurement elevation for checking
                zp2[0]=z02
                Up2=Uf2*(np.log(np.array(zp2)/z02)+(6*np.array(zp2)-z02)/L)/k
                Up2n=Uf2*np.log(np.array(zp2)/z02)/k # a nuetral profile based on B-D model for comparison 
            if dT<0:
                phi1zw=phi1f(zw,Lp)         
                psi1zw=psi1f(phi1zw)
                Uzw1=Uf*(math.log(zw/z0)-psi1zw+psi1f(phi1f(z0,Lp)))/k # at the measurement elevation for checking

                zp1[0]=z0
                for i in range(0,zu+1):
                    phi1z=phi1f(zp1[i],Lp)  
                    psi1z=psi1f(phi1z) 
                    Up1[i]=Uf*(np.log(zp1[i]/z0)-psi1z+psi1f(phi1f(z0,Lp)))/k
                    if Up1[i]<0:
                        Up1[i]=0
                Up1n=Uf*np.log(np.array(zp1)/z0)/k # a nuetral profile based on KEYPS model for comparison
                
                psi2zw=psi2f((1-19.3*zw/L)**0.25)
                Uzw2=Uf2*(math.log(zw/z02)-psi2zw+psi2f((1-19.3*z02/L)**0.25))/k
                
                zp2[0]=z02
                for i in range(0,zu+1):
                    psi2z=psi2f((1-19.3*zp2[i]/L)**0.25)
                    Up2[i]=Uf2*(math.log(zp2[i]/z02)-psi2z+psi2f((1-19.3*z02/L)**0.25))/k
                    if Up2[i]<0:
                        Up2[i]=0
                Up2n=Uf2*np.log(np.array(zp2)/z02)/k # a nuetral profile based on B-D model for comparison
                
    if o2==3:
        if X<2:
            RF=1.0
        if 2<=X<30:
            RF=0.5*(1.1+1.14)
        if 30<=X<50:
            RF=0.5*(1.14+1.23)
        if 50<=X<100:
            RF=0.5*(1.23+1.3)
        if X>=100:
            RF==1.3 # assumed
        Up1=RF*np.array(Up1)
        Up2=RF*np.array(Up2)
        if dT!=0:
            Up1n=RF*np.array(Up1n) 
            Up2n=RF*np.array(Up2n)    
        # nn=nn+1
        section2.extend(['. 陆上风进入水域后随风距的增大系数RF=',round(RF,2),'. 最终的KEYPS和B-D结果均已考虑RF。'])    

    if o2==2 or o2==3:
        plt.scatter(U,zw,c="blue",marker="*",s=50,edgecolors="blue",label='已知的'+str(round(atm))+'-min陆上风速及对应高度')
        # nn=nn+1
        section2.extend(['. 图中已知陆上风速的位置按地面以上的高度绘出。（注意：地面和水面的标高可能不同。）'])    
        
    # Duration adjustment for required averaging time
    if atm!=wdu:
        Up1=att(Up1,atm,wdu)
        Up2=att(Up2,atm,wdu)
        if dT!=0:                    
            Up1n=att(Up1n,atm,wdu)   
            Up2n=att(Up2n,atm,wdu)    
            
    # nn=nn+1
    if dT==0:
        section2.extend(['. 水域风速廓线参数： 粗糙度z0=',round(z0*1000,2),'mm, 摩擦风速U*=',round(Uf,3),'m/s'])
    else:
        section2.extend(['. 水域风速KEYPS廓线参数： 粗糙度z0=',round(z0*1000,2),'mm, 摩擦风速U*=',round(Uf,3),'m/s, 修改后的Obukhov稳定长度L\u2032=',round(Lp,3),'m'])
        # nn=nn+1
        section2.extend(['. 水域风速B-D廓线参数： z0=',round(z02*1000,2),'mm, U*=',round(Uf2,3),'m/s, Obukhov稳定长度L=',round(L,3),'m,','梯度Richardson数Ri=',round(Ri2,3)])
        if ssBD1==1:
            # nn=nn+1
            if o2==1 or o2==2:  
                section2.extend(['. 在迭代求解B-D廓线时，由于求得的Ri出现了一个大于0.2的值，计算程序令Ri=0.199, 据此求得其它参数，并终止迭代。'])
            if o2==3 or o2==4:
                section2.extend(['. 在迭代求解B-D廓线时，由于求得的Ri出现了一个大于0.2的值，计算程序令Ri=0.199, 令大气边界层阻力定律中的稳定性参数\u03BC=',round(miu2,1),', 据此求得其它参数，并终止迭代。'])            

    if o2==4 or o2==3:
        # nn=nn+1
        section2.extend(['. 大气边界层阻力定律参数'])    
        section2.extend(['     Coriolis参数=',round(fCo,7),'rad/s'])
        if dT==0:
            section2.extend(['     地转风与近水面风之间的夹角\u03B8=',round(180*theta/math.pi,2),'\u00B0, 稳定性参数\u03BC=',round(miu,1),', A(\u03BC)=',round(A(miu),2),', B(\u03BC)=',round(B(miu),2)])
        else:        
            section2.extend(['     结合KEYPS廓线： 地转风与近水面风之间的夹角\u03B8=',round(180*theta/math.pi,2),'\u00B0, 稳定性参数\u03BC=',round(miu,1),', A(\u03BC)=',round(A(miu),2),', B(\u03BC)=',round(B(miu),2)])
            section2.extend(['     结合B-D廓线： \u03B8=',round(180*theta2/math.pi,2),'\u00B0, \u03BC=',round(miu2,1),', A(\u03BC)=',round(A(miu2),2),', B(\u03BC)=',round(B(miu2),2)])

    plt.plot([min(0,TaaC-0.5),Uu],[10,10],color='grey',linestyle='--',linewidth=0.5)
    plt.scatter(Up1[10],10,c="None",marker="o",s=50,edgecolors="red",label=str(round(wdu))+'-min $U_{10}$（滨水工）')

    if dT==0:
        plt.plot(Up1,zp1,label=str(round(wdu))+'-min风速对数分布律',color='red',linewidth=1)
    else: 
        plt.plot(Up1,zp1,label=str(round(wdu))+'-min风速KEYPS廓线',color='red',linewidth=1)    
        plt.plot(Up2,zp2,label=str(round(wdu))+'-min风速B-D廓线',color='red',linestyle='--',linewidth=1.5)
        plt.plot(Up1n,zp1,label=str(round(wdu))+'-min风速对数分布律(按KEYPS参数)',color='grey',linewidth=1)    
        plt.plot(Up2n,zp2,label=str(round(wdu))+'-min风速对数分布律(按B-D参数)',color='black',linestyle='--',linewidth=1.5)
        plt.scatter(Up2[10],10,c="None",marker="o",s=50,edgecolors="red")
        
    # 2. 港口与航道水文规范 (JTS 145-2015)
    section3 = []
    section3.extend(['---港口与航道水文规范 (JTS 145-2015)---'])
    # nn=0 # order number of notes
    ss1=None

    if wdu!=atm: 
        # nn=nn+1  
        section3.extend(['. JTS 145-2015未提供不同时距风速之间的转换方法。U\u2081\u2080只能通过其它方法获取。'])    
        ss1=1 

    if dT!=0: 
        # nn=nn+1  
        section3.extend(['. JTS 145-2015未提供在稳定或不稳定大气条件下推算U\u2081\u2080的方法。U\u2081\u2080只能通过其它方法获取。'])    
        ss1=1 

    if dT==0 and wdu==atm:
        
        if o2==3:
            # nn=nn+1
            section3.extend(['. JTS 145-2015未提供风速从陆域到水域的转换方法。U\u2081\u2080只能通过其它方法获取。']) 
            ss1=1 
            
        if o2==1 or o2==2:
            Ua1=U*math.log10(10/.03)/math.log10(zw/.03)
            if zw!=10:
                # nn=nn+1
                section3.extend(['. 按第7.1.2.2条求得',str(round(atm,1))+'-min时距的U\u2081\u2080=',round(Ua1,3),'m/s'])   
                
        if o2==4:
            Ua1=(.7-0.01*dT)*U  
            # nn=nn+1
            section3.extend(['. 按图7.1.3估计海面风速=',round(Ua1,3),'m/s。在此假设该图中的"海面风速"系指U\u2081\u2080。图7.1.3适用于海域。对于大湖和大型水库，建议采用相关有效方法，JTS 145-2015的结果在此仅作参考。'])
                
    if ss1!=1:  
        plt.scatter(Ua1,10,c="None",edgecolor='purple',marker="p",s=60,label=str(round(wdu))+'-min $U_{10}$ (JTS 145-2015)')
                    
    # 3. Shore Protection Manual (1984)
    section4 = []
    section4.extend(['---Shore Protection Manual (SPM 1984)---'])
    # nn=0
                    
    if o2!=4:    
        Ue2=U*(10/zw)**(1/7) # at 10 m elevation
        if zw!=10:
            # nn=nn+1
            if o2==3:
               section4.extend(['. 按公式(3-26)求得地面以上10m处的风速：',round(Ue2,3),'m/s'])
            else:
                section4.extend(['. 按公式(3-26)求得',str(round(atm,1))+'-min时距的U\u2081\u2080=',round(Ue2,3),'m/s'])        
            if zw>=20:
                # nn=nn+1
                section4.extend(['. 警告：SPM 1984建议在风速高度低于20 m时使用公式(3-26)，但本例中已知风速的高度并不低于20 m。'])
        if o2==1 or o2==2:  
            Uel2=Ue2 #(locational effect)
        if o2==3: #(locational effect)    
            if X<16:
                Uel2=1.2*Ue2
                # nn=nn+1
                section4.extend(['. 按第3-IV-3-(c)条,陆-水转换系数RL=1.2,由陆上风估计的U\u2081\u2080=',round(Uel2,3),'m/s。'])                      
            else:
                RL=(0.04*0.0357*Ue2**2-0.2*0.3423*Ue2+1.724)*(Ue2<=18.5)+0.9*(Ue2>18.5)
                Uel2=Ue2*RL
                # nn=nn+1
                section4.extend(['. 按图3-15，陆-水转换系数RL=',round(RL,2),'，对应的U\u2081\u2080=',round(Uel2,3),'(m/s)'])                       
    else:
        Uel2=U*0.89/U**0.192 # at 10 m elevation (by Figure 3-19)
        # nn=nn+1
        section4.extend(['. 按图3-19，Rg=',round(0.89/U**0.192,2),'，由Ug估计的U\u2081\u2080=',round(Uel2,3),'m/s。'])

    if dT==0:
        RT=1.0
    else:
        RT=1-dT*(abs(dT)/1900)**(1/3)/abs(dT) # stability ((by Figure 3-14)   
    Uels2=Uel2*RT    
    # nn=nn+1
    section4.extend(['. 按图3-14，RT=',round(RT,2),'，考虑大气稳定性以后的U\u2081\u2080=',round(Uels2,3),'m/s'])

    # Duration adjustment for required averaging time
    if atm!=wdu:
        U1021h=att(Uels2,atm,60)
        U102=att(Uels2,atm,wdu)   
        # nn=nn+1
        section4.extend(['. 按图3-13，1-h时距的U\u2081\u2080=',round(U1021h,3),'m/s，而',str(round(wdu,1))+'-min时距的U\u2081\u2080=', round(U102,3),'m/s。'])        
    else:
        U102=Uels2

    plt.scatter(U102,10,c="None",marker="s",s=50,edgecolors="darkblue",label=str(round(wdu))+'-min $U_{10}$ (SPM 1984)')    
    Ua2=0.71*U102**1.23
        
    # 4. Coastal Engineering Manual  (CEM 2015)
    section5 = []
    section5.extend(['---Coastal Engineering Manual (CEM)---'])
    # nn=0
    ss3=None

    # nn=nn+1
    section5.extend(['. 对于风速计算，CEM 2015提供了一套简易方法，也建议采用ACES软件。在此仅采用其推荐的简易方法进行风速计算。'])
        
    if o2==4 and Rg==None:
        ss3=1
        # nn=nn+1
        section5.extend(['. 图II-2-13中的Rg值未提供，故无法按Rg直接估算U\u2081\u2080。'])

    if ss3==None:
                        
        if o2!=4:    
            Ue3=U*(10/zw)**(1/7) # at 10 m elevation
            if zw!=10:
                # nn=nn+1
                if o2==3:
                    section5.extend(['. 按公式(II-2-28)求得地面以上10m处的风速：',round(Ue3,3),'m/s'])
                else:
                    section5.extend(['. 按公式(II-2-28)求得',str(round(atm,1))+'-min时距的U\u2081\u2080=',round(Ue3,3),'m/s'])        
                if zw<8 or zw>12:
                    # nn=nn+1
                    section5.extend(['. 警告：CEM 2015建议当风速高度在8~12 m之间时使用公式(II-2-28)，但本例中已知风速的高度并未在这一范围。'])
            if o2==1 or o2==2:  
                Uel3=Ue3 #(locational effect)
            if o2==3: #(locational effect)    
                if X<16:
                    Uel3=1.2*Ue3
                    # nn=nn+1
                    section5.extend(['. 按图II-2-20，陆-水转换系数RL=1.2,由陆上风估计的U\u2081\u2080=',round(Uel3,3),'m/s。'])                      
                else:
                    RL=(0.04*0.0357*Ue3**2-0.2*0.3423*Ue3+1.724)*(Ue3<=18.5)+0.9*(Ue3>18.5)
                    Uel3=Ue3*RL
                    # nn=nn+1
                    section5.extend(['. 按图II-2-20和图II-2-7，陆-水转换系数RL=',round(RL,2),'，对应的U\u2081\u2080=',round(Uel3,3),'(m/s)'])                       
        else:
            Uel3=Rg*Ug # at 10 m elevation (by Figure II-2-13)
            # nn=nn+1
            section5.extend(['. 按图II-2-13，由Ug估计的U\u2081\u2080=',round(Uel3,3),'m/s。'])

        if dT==0:
            RT=1.0
        if dT>0:
            RT=0.9  
        if dT<0:
            RT=1.1
            
        if o2!=4 or (o2==4 and  Rg!=None):   
            U103=Uel3*RT
            # nn=nn+1
            section5.extend(['. 按图II-2-20，RT=',round(RT,2),'，考虑大气稳定性以后的U\u2081\u2080=',round(U103,3),'m/s。\
                            (RT可按气水温差\u0394T在图II-2-8中读取，该图由ACES软件生成。然而，该图未明确说明气温的高度，且该软件中某些参数的取值有待进一步核实。故在此RT采用图II-2-20中建议的简易取值。）'])
                            # Duration adjustment for required averaging time
            if atm!=wdu:
                U1031h=att(U103,atm,60)
                Ua3=att(U103,atm,wdu) 
                # nn=nn+1
                section5.extend(['. 按图II-2-1，1-h时距的U\u2081\u2080=',round(U1031h,3),'m/s，而',str(round(wdu,1))+'-min时距的U\u2081\u2080=', round(Ua3,3),'m/s。'])        
            else:
                Ua3=U103
        plt.scatter(Ua3,10,c="None",marker="v",s=50,edgecolors="limegreen",label=str(round(wdu))+'-min $U_{10}$ (CEM)')

    # 5. API RP 2A-WSD
    section6 = []
    section6.extend(['---API RP 2A-WSD---'])
    # nn=0
    ss6=None

    # nn=nn+1
    section6.extend(['. 严格来说，API RP 2A-WSD的方法仅适用于外海环境。对于沿海、大湖、大型水库等水域，建议采用相关有效方法，API RP 2A-WSD的结果在此仅作参考。'])  
        
    if o2==4:
        # nn=nn+1
        section6.extend(['. API RP 2A-WSD未提供根据地转风推算U\u2081\u2080的方法。U\u2081\u2080只能通过其它方法获取。']) 
        ss6=1 

    if o2==3:
        # nn=nn+1
        section6.extend(['. API RP 2A-WSD未提供风速从陆域到水域的转换方法。U\u2081\u2080只能通过其它方法获取。']) 
        ss6=1 
    
    if o2==1 or o2==2:
        if dT==0:
            aU10=U # assumed U10 (m/s)
            if1=aU10*(1+0.0573*(1+0.15*aU10)**0.5*math.log(0.1*zw))*(1-0.41*0.06*(1+0.043*aU10)*math.log(atm*60/3600)/(0.1*zw)**0.22)-U # an iteration function 
            while (abs(if1)>tol):
                if1u=(aU10+dU)*(1+0.0573*(1+0.15*(aU10+dU))**0.5*math.log(0.1*zw))*(1-0.41*0.06*(1+0.043*(aU10+dU))*math.log(atm*60/3600)/(0.1*zw)**0.22)-U # updated wave length (m)
                if1l=(aU10-dU)*(1+0.0573*(1+0.15*(aU10-dU))**0.5*math.log(0.1*zw))*(1-0.41*0.06*(1+0.043*(aU10-dU))*math.log(atm*60/3600)/(0.1*zw)**0.22)-U # updated wave length (m)
                if abs(if1u-if1l)>tol:
                    aU10=aU10-2*dU*if1/(if1u-if1l)
                    if1=aU10*(1+0.0573*(1+0.15*aU10)**0.5*math.log(0.1*zw))*(1-0.41*0.06*(1+0.043*aU10)*math.log(atm*60/3600)/(0.1*zw)**0.22)-U # an iteration function 
                else:
                    if1=aU10*(1+0.0573*(1+0.15*aU10)**0.5*math.log(0.1*zw))*(1-0.41*0.06*(1+0.043*aU10)*math.log(atm*60/3600)/(0.1*zw)**0.22)-U # an iteration function 
                    if abs(if1)>tol:
                        if1=0
                        ss6=1
            if ss6==None:        
                U1061h=aU10
                Ua6=U1061h*(1+0.0573*(1+0.15*U1061h)**0.5*math.log(0.1*10))*(1-0.41*0.06*(1+0.043*U1061h)*math.log(wdu*60/3600)/(0.1*10)**0.22) # updated wave length (m)
                # nn=nn+1
                section6.extend(['. 根据已知风速按公式(5.3)求得一小时时距的U\u2081\u2080，再按该公式求得指定时距的U\u2081\u2080']) 
                plt.scatter(Ua6,10,marker="P",s=50,color="brown",label=str(round(wdu))+'-min $U_{10}$ (API RP 2A-WSD)')
            else:
                # nn=nn+1
                section6.extend(['. 公式(5.3)无解，无法求得一小时时距的U\u2081\u2080。']) 
        else:
            ss6=1
            # nn=nn+1
            section6.extend(['. API RP 2A-WSD未提供在稳定或不稳定大气条件下推算U\u2081\u2080的方法。U\u2081\u2080只能通过其它方法获取。']) 

    # More outputs 
    section7 = []
    section7.extend(['---结果汇总：',str(round(wdu,1))+'-min时距U\u2081\u2080(m/s)---'])

    if dT==0:#20221211
        section7.extend(['滨水工',round(Up1[10],3)])
    else:
        section7.extend(['滨水工',str(round(Up1[10],3))+'(KEYPS)',str(round(Up2[10],3))+'(B-D)'])

    if ss1==None:
        section7.extend(['JTS 145-2015',round(Ua1,3)])
    else:
        section7.extend(['JTS 145-2015','无有效方法'])
    
    section7.extend(['SPM 1984',round(U102,3)])

    if ss3==None:
        section7.extend(['CEM',round(Ua3,3)])
    else:
        section7.extend(['CEM','信息不足'])

    if ss6==None:
        section7.extend(['API RP 2A-WSD',round(Ua6,3)])
    else:
        section7.extend(['API RP 2A-WSD','无有效方法'])

    ending = '---结果展示结束---'

    plt.xlabel('风速 (m/s) 或 气温（摄氏度）')
    plt.ylabel('距水面的高度 (m)')
    plt.xlim(min(0,TaaC-0.5),Uu)
    plt.ylim(0,zu)
    plt.legend()
    # plt.rcParams['font.sans-serif'] = ['Kaiti'] 
    # plt.show()
    plt.rcParams["font.family"]="sans-serif"
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    todayis = dt.utcnow()
    d1 = todayis.strftime("%Y%m%d%H%M%S")
    # plt.savefig(f'pichistory/{d1}-wavespectra.png',dpi = 300)
    # plt.savefig(f'var/www/flaskapp/pichistory/{d1}-wavespectra.png',dpi = 300)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_stream = base64.b64encode(img.getvalue()).decode()
    plt.close("all")

    return img_stream, heading, section1, section2, section3, section4, section5, section6, section7, ending