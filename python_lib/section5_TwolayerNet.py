# [英]Backpropagation.誤差逆伝播法（ごさぎゃくでんぱほう）
# Section4の微分がより高速に行えるようになった。
import numpy as np
from collections import OrderedDict
from section4 import numerical_gradient_for_array
from section5 import *

class TwoLayerNet_section5:

    #初期化。パラメータは
    #input_size:入力層の数
    #hidden_size:中間層の数
    #output_size:出力層の数
    def __init__(self, input_size, hidden_size, output_size, weight_init_std=0.01):
        #重みの初期化
        self.params = {}
        self.params['W1'] = weight_init_std * np.random.randn(input_size, hidden_size)
        self.params['b1'] = np.zeros(hidden_size)
        self.params['W2'] = weight_init_std * np.random.randn(hidden_size, output_size)
        self.params['b2'] = np.zeros(output_size)

        # レイヤの生成
        self.layers = OrderedDict()
        self.layers['Affine1'] = Affine(self.params['W1'],self.params['b1'])
        self.layers['Relu1'] = Relu()
        self.layers['Affine2'] = Affine(self.params['W2'],self.params['b2'])

        self.lastLayer = SoftmaxWithLoss()

    #推論を行う。
    def predict(self, x):
        
        for layer in self.layers.values():
            x = layer.forward(x)

        return x
    
    def loss(self, x, t):
        y = self.predict(x)
        return self.lastLayer.forward(y,t)

    #複数のデータを提示して正解である確率を求める
    # x 全入力データ(画像だったら全枚数)
    # t 全教師データ
    def accuracy(self, x, t):
        y = self.predict(x)
        y = np.argmax(y, axis=1)
        t = np.argmax(t, axis=1)

        accuracy = np.sum(y == t)/ float( x.shape[0] )

        return accuracy
    
    #旧式の微分関数
    #確認用に残してあるだけ。
    def numerical_gradient(self, x, t):
        loss_W = lambda W : self.loss(x, t)
        grads = {}

        grads['W1'] = numerical_gradient_for_array(loss_W, self.params['W1'])
        grads['b1'] = numerical_gradient_for_array(loss_W, self.params['b1'])
        grads['W2'] = numerical_gradient_for_array(loss_W, self.params['W2'])
        grads['b2'] = numerical_gradient_for_array(loss_W, self.params['b2'])

        return grads

    # [英]Backpropagation.誤差逆伝播法（ごさぎゃくでんぱほう）を使った微分（笑）
    # なんでこんな日本語難しいんですかね？誰かおしえてください.
    def gradient(self, x, t):
        #forward
        self.loss(x, t)

        #backward
        dout = 1
        dout = self.lastLayer.backward(dout)

        layers = list(self.layers.values())
        layers.reverse()

        for layer in layers:
            dout = layer.backward(dout)

        grads = {}
        grads['W1'] = self.layers['Affine1'].dW
        grads['b1'] = self.layers['Affine1'].db
        grads['W2'] = self.layers['Affine2'].dW
        grads['b2'] = self.layers['Affine2'].db

        return grads