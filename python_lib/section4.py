import numpy as np
#損失関数について。
#損失関数とは、人工知能の計算誤差(AI)を示すための関数
#この値が高いと誤検知が多い＝悪いAIと言うことになる。

#損失関数その１:2乗和誤差
def mean_squared_error(y,t):
    return 0.5 * no.sum((y - t) ** 2 )

#その２交差エントロピー誤差
"""
#旧式。バッチ学習非対応
def cross_entropy_error(y,t):
    delta = 1e-7
    return -np.sum(t * np.log(y + delta))
"""
#バッチ学習対応版！やったね！
def cross_entropy_error(y, t):

    #前提条件のチェック
    #次元数が1([a, b, c])のとき、2次元にする。([[a, b, c]])
    if y.ndim == 1: 
        t = t.reshape(1, t.size)
        y = y.reshape(1, y.size)
        
    # 教師データがone-hot-vectorの場合、正解ラベルのインデックスに変換
    if t.size == y.size:
        t = t.argmax(axis=1) # 横方向の軸
             
    batch_size = y.shape[0]
    return -np.sum(np.log(y[np.arange(batch_size), t] + 1e-7)) / batch_size


#微分。
#損失関数を微分する事によって、学習の変化率を求める。
#変化率が0の部分がゴールとなる。
#NOTE:認識率では感度が低く、重みを変更してもほぼ値が変化しないため学習の指標には適さない。
def numerical_diff(f,x):
    h = 1e-4
    return (f(x + h) - f(x-h) / (2*h) )

#偏微分 指定した関数の指定した地点(任意の次元配列(x,y...等))を微分し、傾きを求める。
# fは関数,xは微分したい点の配列(x=3, y=4→[3,4])
# ※ただし、xは一次元の配列のみ利用可能(EX:[0,・・・,0])のみ
def numerical_gradient(f,x):
    h = 1e-4
    grad = np.zeros_like(x)

    for idx in range(x.size):

        tmp_val = x[idx]

        x[idx] = tmp_val + h
        fxh1 = f(x)

        x[idx] = tmp_val - h
        fxh2 = f(x)

        grad[idx] = (fxh1 - fxh2) / (2 * h)
        x[idx] = tmp_val

    return grad

# xが多次元配列でも傾きを求める事ができるようになったバージョン。
def numerical_gradient_for_array(f, x):
    h = 1e-4 # 0.0001
    grad = np.zeros_like(x)
    
    it = np.nditer(x, flags=['multi_index'], op_flags=['readwrite'])
    while not it.finished:
        idx = it.multi_index
        tmp_val = x[idx]
        x[idx] = float(tmp_val) + h
        fxh1 = f(x) # f(x+h)
        
        x[idx] = tmp_val - h 
        fxh2 = f(x) # f(x-h)
        grad[idx] = (fxh1 - fxh2) / (2*h)
        
        x[idx] = tmp_val # 値を元に戻す
        it.iternext()   
        
    return grad