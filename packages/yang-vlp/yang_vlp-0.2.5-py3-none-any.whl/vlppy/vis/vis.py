import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def draw_position_contrast(pred,true,title="",savepath=...,showfig=True):
    """预测位置和真实位置对比图
    Params
        pred: 预测位置
        true: 真实位置
        title: 标题
        savepath: 保存路径
        showfig: 是否显示图例
    """
    assert len(pred) == len(true) 
    if len(pred) == 2:
        plt.plot(*pred,'ro') 
        plt.plot(*true,'b*') 
    elif len(pred) == 3:
        ax = plt.axes(projection='3d')
        ax.scatter3D(*pred, c='r',marker="o")
        ax.scatter3D(*true, c='b',marker="*")
    else:
        plt.plot(pred,'ro')
        plt.plot(true,'b*')
    plt.title(title)
    plt.legend(['pred','true'])
    if savepath != ...:
        plt.savefig(savepath)
    if showfig:
        plt.show()

def draw_history(history,title="history",savepath=...,showfig=True):
    """绘制网络模型训练过程参数变换图
    Params
        history: 历史值
        title: 标题
        savepath: 保存路径
        showfig: 是否显示图例
    """
    data = pd.DataFrame(history)
    data.plot(figsize=(8,5))
    plt.grid(True)
    plt.title(title)
    plt.xlabel("iter")
    if savepath != ...:
        plt.savefig(savepath)
    if showfig:
        plt.show()

def cdfplot(error,title="",savepath=...,showfig=True):
    """绘制误差积累分布图CDF
    Params 
        error: 误差数组
        title: 标题
        savepath: 保存路径
        showfig: 是否显示图例
    """
    x = np.array(error)
    x = x[~np.isnan(x)]     #去除nan
    x = np.sort(x)          #排序
    n = len(x)              
    y = np.arange(1,n+1)/n  #返回1/n步进到1
    notdup = [x[i]-x[i-1]>0 for i in range(1,len(x))]  #返回梯度布尔值
    notdup.append(True) 
    xx = x[notdup]             #去除重复元素
    yy = np.array([0,*y[notdup]])  #在第一位置上插入一个0
    m = np.repeat(np.arange(1,len(xx)+1),2)  #在第0轴上复制元素
    xCDF = np.array([-np.inf,*xx[m-1],np.inf]) #前后延申
    yCDF = np.array([0,0,*yy[m]]) #在第一位置上插入两个0

    plt.plot(xCDF,yCDF)  #绘图
    plt.title(title)
    plt.xlabel("position error")
    plt.ylabel("CDF")

    if savepath != ...:
        plt.savefig(savepath)
    if showfig:
        plt.show()
    return xCDF,yCDF

