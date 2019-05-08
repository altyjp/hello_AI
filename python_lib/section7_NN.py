import numpy as np
from collections import OrderedDict
from section5 import Relu,Affine,SoftmaxWithLoss
from section6 import Dropout,BatchNormalization
from section7 import Convolution,Pooling

class convNet:

    #初期化。パラメータは
    #imput_dim:(チャンネル・高さ・幅)
    #hidden_size:中間層の数
    #output_size:出力層の数
    def __init__(self,input_dim=(1,28,28),conv_param={'filter_num':30,'filter_size':5,'pad':0,'stride':1},
                  hidden_size=100,hidden_size2=100, output_size=10, weight_init_std=0.01):
        #
        filter_num = conv_param['filter_num']
        filter_size = conv_param['filter_size']
        filter_pad = conv_param['pad']
        filter_stride = conv_param['stride']
        input_size = input_dim[1]

        #アウトプットのサイズ。
        conv_output_size = (input_size - filter_size + 2*filter_pad) / filter_stride + 1
        pool_output_size = int(filter_num * (conv_output_size/2) * (conv_output_size/2))
        
        
        #重みの初期化
        self.params = {}
        self.params = {}
        self.params['W1'] = weight_init_std * \
                            np.random.randn(filter_num, input_dim[0], filter_size, filter_size)
        self.params['b1'] = np.zeros(filter_num)
        
        #バッチノーマライゼーション
        self.params['gamma'] = np.ones(filter_num * int(conv_output_size) * int(conv_output_size)) 
        self.params['beta'] = np.zeros(filter_num * int(conv_output_size) * int(conv_output_size))

        self.params['W2'] = weight_init_std * \
                            np.random.randn(pool_output_size, hidden_size)
        self.params['b2'] = np.zeros(hidden_size)
        self.params['W3'] = weight_init_std * \
                            np.random.randn(hidden_size, output_size)
        self.params['b3'] = np.zeros(output_size)

        # レイヤの生成
        self.layers = OrderedDict()
        self.layers['conv1'] = Convolution(self.params['W1'],self.params['b1'],
                                                conv_param['stride'],conv_param['pad'])
        
        self.layers['bnorm1'] = BatchNormalization(gamma= self.params['gamma'],beta=self.params['beta'])

        self.layers['Relu1'] = Relu()

        self.layers['Pool1']= Pooling(pool_h=2, pool_w=2, stride=2)

        self.layers['Affine1'] = Affine(self.params['W2'],self.params['b2'])

        self.layers['Relu2'] = Relu()

        self.layers['Affine2'] = Affine(self.params['W3'],self.params['b3'])

        #self.layers['Dropout']= Dropout(dropout_ratio=0.1)

        self.lastLayer = SoftmaxWithLoss()

    #推論を行う。
    def predict(self, x, train_flg=True):
        
        for key,layer in self.layers.items():
            if key == 'bnorm1':
                x = layer.forward(x, train_flg)
            else:
                x = layer.forward(x)
        return x
    
    def loss(self, x, t):
        y = self.predict(x)
        return self.lastLayer.forward(y,t)

    #複数のデータを提示して正解である確率を求める
    # x 全入力データ(画像だったら全枚数)
    # t 全教師データ
    def accuracy(self, x, t, batch_size=100):
        if t.ndim != 1 : t = np.argmax(t, axis=1)
        
        acc = 0.0

        for i in range(int(x.shape[0] / batch_size)):
            
            print("calculate accuracy: " + str(i) + "/" + str((x.shape[0] / batch_size)))

            tx = x[i*batch_size:(i+1)*batch_size]
            tt = t[i*batch_size:(i+1)*batch_size]
            y = self.predict(tx)
            y = np.argmax(y, axis=1)
            acc += np.sum(y == tt) 

            


        return acc / x.shape[0]

    # [英]Backpropagation.誤差逆伝播法（ごさぎゃくでんぱほう）を使った微分（笑）
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
        # 設定
        grads = {}
        grads['W1'], grads['b1'] = self.layers['conv1'].dW, self.layers['conv1'].db
        grads['W2'], grads['b2'] = self.layers['Affine1'].dW, self.layers['Affine1'].db
        grads['W3'], grads['b3'] = self.layers['Affine2'].dW, self.layers['Affine2'].db
        grads['gamma'] = self.layers['bnorm1'].dgamma
        grads['beta'] = self.layers['bnorm1'].dbeta

        return grads