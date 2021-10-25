import  os, sys
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
def fix_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
   
class My_sampling(object):
    def __init__(self, num_col = None, num_sample = None, dist = None):
        self.num_col = num_col
        self.num_sample = num_sample
        self.dist = dist
        self.dfW = pd.DataFrame()
        self.dfN = pd.DataFrame()
        self.dfP = pd.DataFrame()
        
    def get_W(self): #実空間からランダムサンプリング
        for i in range(self.num_col):
            fix_seed(i) ;tmp = pd.DataFrame([random.uniform(0, 1) for j in range(self.num_sample)], columns =[f"w{i}"])
            self.dfW = pd.concat([self.dfW, tmp], axis = 1)
        return self.dfW
    
    def get_N(self): #実空間から正規分布に従ったサンプリング
        for i in range(self.num_col):
            fix_seed(i) ;tmp = pd.DataFrame([np.random.normal(0, 1) for j in range(self.num_sample)], columns =[f"n{i}"])
            self.dfN = pd.concat([self.dfN, tmp], axis = 1)
        return self.dfN
    
    def get_P(self): #実空間からポアソン分布に従ったサンプリング
        for i in range(self.num_col):
            fix_seed(i) ;tmp = pd.DataFrame([np.random.poisson(lam=50) for j in range(self.num_sample)], columns =[f"p{i}"])
            self.dfP = pd.concat([self.dfP, tmp], axis = 1)
        return self.dfP

    def get_R(self):
        if self.dist == 0:
            return self.get_W()
        elif self.dist == 1:
            return self.get_N()
        elif self.dist == 2:
            return self.get_P()
        
    def get_X(self):#単体空間への写像
        R = self.get_R()
        _df = pd.DataFrame()
        for i in range(self.num_sample):
            tmp = [R.iloc[i,j]/sum(R.loc[i,:]) for j in range(self.num_col)]
            _df = pd.concat([_df, pd.DataFrame(tmp).T], axis = 0)
        _df.index = range(self.num_sample) ;_df.columns = [f"x{i}" for i in range(self.num_col)]
        return _df
    
def plot(df):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15,5))
    sns.scatterplot(data=df, x=df.columns[0], y = df.columns[1], ax = ax1)
    sns.scatterplot(data=df, x=df.columns[0], y = df.columns[2], ax = ax2)
    sns.scatterplot(data=df, x=df.columns[1], y = df.columns[2], ax = ax3);plt.show()
    
if __name__ == "__main__":
    instance = My_sampling(num_col = 5, num_sample = 300, dist = 2)
    R = instance.get_R()
    X = instance.get_X()#単体空間への写像

    plot(R) ;plot(X)
