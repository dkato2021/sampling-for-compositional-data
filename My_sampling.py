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
    def __init__(self, num_col = None, num_sample = None):
        self.num_col = num_col
        self.num_sample = num_sample
        self.dfW = pd.DataFrame()
        self.dfN = pd.DataFrame()
        
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
    
    def get_X(self, norm = None): #単体空間への写像
        if norm:
            W = self.get_N()
        else:
            W = self.get_W()  
        _df = pd.DataFrame()
        for i in range(self.num_sample):
            tmp = [W.iloc[i,j]/sum(W.loc[i,:]) for j in range(self.num_col)]
            _df = pd.concat([_df, pd.DataFrame(tmp).T], axis = 0)
        _df.index = range(self.num_sample) ;_df.columns = [f"x{i}" for i in range(self.num_col)]
        return _df
    
def plot(df, x = None, y = None):
    fig, ax = plt.subplots(figsize=(5, 5))
    sns.scatterplot(data=df, x=df.columns[x], y=df.columns[y]) ;plt.show()
    
if __name__ == "__main__":
    instance = My_sampling(num_col = 3, num_sample = 300)
    W, N = instance.get_W(), instance.get_N()
    X = instance.get_X(norm = True)

    plot(N, x =0, y = 2)
    plot(N, x =1, y = 2)
    plot(N, x =0, y = 2)
