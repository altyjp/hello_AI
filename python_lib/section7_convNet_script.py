import pickle
import numpy as np
import sys
from section7_NN import convNet
from dataset.mnist import load_mnist


#(訓練画像,訓練用教師データ),(テスト用画像, テスト用教師データ)
#(x_train, t_train),(x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)
(x_train, t_train), (x_test, t_test) = load_mnist(flatten=False, one_hot_label=True)

train_loss_list = []

iters_num = 10000 #何回学習するか？
train_size = x_train.shape[0]
batch_size = 100 #1回の学習で利用する、画像の枚数
learning_rate = 0.1

train_acc_list = []
test_acc_list = []
iter_per_epoch = max(train_size / batch_size, 1)


network = convNet()

for i in range(iters_num):

    print(str(i) + "truns start.")
    
    #ミニバッチの取得
    batch_mask = np.random.choice(train_size, batch_size)
    x_batch = x_train[batch_mask]
    t_batch = t_train[batch_mask]

    # 微分
    grad = network.gradient(x_batch, t_batch)

    #重みの更新
    for key in ('W1','b1','W2','b2','W3','b3'):
        network.params[key] -= learning_rate * grad[key]

    #学習課程の記憶
    loss = network.loss(x_batch, t_batch)
    train_loss_list.append(loss)


train_acc = network.accuracy(x_train, t_train)
test_acc = network.accuracy(x_test, t_test)
train_acc_list.append(train_acc)
test_acc_list.append(test_acc)
print("train acc and test acc | " + str(train_acc) + " , " + str(test_acc))

#人工知能の保存を行う
#暇だったので名前について真剣に考えた結果、マーキュリーと決定しました。
with open('Mercury.pickle', 'wb') as f:
    pickle.dump(network, f)