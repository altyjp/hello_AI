import numpy as np

#活性化関数
#中間層で使用。前の層のノード（シナプス）からの入力の総和を元に出力値を決定する関数
#ステップ関数
def step_function(x):
    return np.array( x > 0, dtype=np.int)

#シグモイド関数
def sigmoid(x):
    return 1 / (1+ np.exp(-x))

#出力層で使用する関数達
#softmax関数（分類問題の出力で利用する）
"""
def softmax(a):
    c = np.max(a)
    exp_a = np.exp(a - c)
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    return y
"""
#バッチ学習対応版
def softmax(x):
    if x.ndim == 2:
        x = x.T
        x = x - np.max(x, axis=0)
        y = np.exp(x) / np.sum(np.exp(x), axis=0)
        return y.T 

    x = x - np.max(x) # オーバーフロー対策
    return np.exp(x) / np.sum(np.exp(x))