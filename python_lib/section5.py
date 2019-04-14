import numpy as np
from section3 import softmax
from section4 import cross_entropy_error
#from common.functions import *

#乗算レイヤー
#forward : xとyを乗算する。
#backward : 逆伝播する。doutは順w伝播時の出力変数に対する微分結果
#このようにコーディングする事で、効率よく微分を行う事が出来る。
class MulLayer:

    def __init__(self):
        self.x = None
        self.y = None

    def forward(self, x, y):
        self.x = x
        self.y = y
        out = x * y
        return out

    def backward(self, dout):
        dx = dout * self.y
        dy = dout * self.x
        return dx, dy

#可算レイヤー
#forward : xとyを可算する。
#backward : 逆伝播する。doutは順伝播時の出力変数に対する微分結果
class addLayer:

    def __init__(self):
        pass

    def forward(self, x, y):
        out = x + y
        return out

    def backward(self, dout):
        dx = dout * 1
        dy = dout * 1
        return dx, dy

#ReLuレイヤー
#活性化関数の一つ、ReLu関数
class Relu:
    def __init__(self):
        self.mask = None
    
    def forward(self, x):
        self.mask = (x <= 0)
        out = x.copy()
        out[self.mask] = 0 # xが0以下のものに0を設定する。
        return out

    def backward(self, dout):
        dout[self.mask] = 0 # xが0以下のものに0を設定する。
        dx = dout
        return dx

#お馴染みシグモイド関数
class Sigmoid:
    def __init__(self):
        self.out = None

    def forward(self, x):
        out = 1 / (1 + np.exp(-x) )
        self.out = out
        return out

    def backward(self, dout):
        dx = dout * (1.0 - self.out) * self.out
        return dx

# 重みWと入力Xのドット積とバイアスBの足し算
class Affine:
    def __init__(self, W, b):
        self.W = W
        self.b = b
        self.x = None
        self.original_x_shape = None
        self.dW = None
        self.db = None

    def forward(self, x):
        # テンソル(3次元以上の配列)対応
        self.original_x_shape = x.shape
        x = x.reshape(x.shape[0], -1)
        self.x = x
        out = np.dot(self.x, self.W) + self.b
        return out
    
    def backward(self, dout):
        dx = np.dot(dout, self.W.T) #Tは転置行列にするメソッド 行列のサイズを(2,3)→(3,2)にする。
        self.dW = np.dot(self.x.T, dout)
        self.db = np.sum(dout, axis=0)
        dx = dx.reshape(*self.original_x_shape)  # 入力データの形状に戻す（テンソル対応）
        return dx

#Softmax関数と損失関数
class SoftmaxWithLoss:
    def __init__(self):
        self.loss = None #損失関数
        self.y = None #softmaxの出力
        self.t = None #教師データ（one hot）

    def forward(self, x, t):
        self.t = t
        self.y = softmax(x)
        self.loss = cross_entropy_error(self.y, self.t)

        return self.loss

    #doutは最終層なので初期値。1になる。
    def backward(self, dout = 1):
        batch_size = self.t.shape[0]
        dx = (self.y - self.t) / batch_size
        return dx
