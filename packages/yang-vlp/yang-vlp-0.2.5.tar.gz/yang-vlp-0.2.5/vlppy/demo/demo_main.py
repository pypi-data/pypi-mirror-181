import numpy as np
from ..setting import Settings
from ..io import IO
from .vlp_model import VLP_Model

Args = Settings() #加载settings.json文件

save_excel_path = f'vlp_data.xlsx'
save_npz_path = f'vlp_data.npz'

def main():

    # 训练集
    cm = VLP_Model(**Args.items)
    (P1,P2,P3,P4,X,Y,Z) = cm.get_data()

    # P_SUM = P1 + P2 + P3 + P4
    # P = P_SUM
    # cm.show(P)
    train_p = np.stack([P1,P2,P3,P4],axis=1)
    train_x = X
    train_y = Y
    train_z = Z
    
    train_dataset = {
        "P1": P1,
        "P2": P2,
        "P3": P3,
        "P4": P4,
        "X": X,
        "Y": Y,
        "Z": Z
    }

    # 训练集
    Args.items['Room']["test_plane"]["gap"] = 0.24  
    cm = VLP_Model(**Args.items)  
    (P1,P2,P3,P4,X,Y,Z) = cm.get_data()  
    test_p = np.stack([P1,P2,P3,P4],axis=1)
    test_x = X
    test_y = Y
    test_z = Z
    test_dataset = {
        "P1": P1,
        "P2": P2,
        "P3": P3,
        "P4": P4,
        "X": X,
        "Y": Y,
        "Z": Z
    } 

    io = IO() 
    io.user_save_npz_3d(save_npz_path,train_p=train_p,train_x=train_x,train_y=train_y,train_z=train_z,
                                    test_p=test_p,test_x=test_x,test_y=test_y,test_z=test_z)

    io.save_excel(save_excel_path, train_dataset, test_dataset)   

if __name__ == '__main__':
    io = IO()
    for a in range(0,2):
        if a == 0:   # 产生数据
            main()
        elif a == 1: # 加载数据 验证数据集
            with io.load_npz(save_npz_path) as f:
                print(f.files)
                train_p, train_x, train_y, train_z = f['train_p'], f['train_x'], f['train_y'], f['train_z']
                test_p, test_x, test_y, test_z = f['test_p'], f['test_x'], f['test_y'], f['test_z']
            data = (train_p,train_x,train_y,train_z), (test_p,test_x,test_y,test_z)
            [print(j.shape,end=", ") for i in data for j in i]
            print()
            [[print(j[:2])for j in i] for i in data]
            print("train_p max:",np.max(data[0][0]))
            print("test_p max:",np.max(data[1][0]))

