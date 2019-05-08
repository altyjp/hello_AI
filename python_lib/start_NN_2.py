import sys, os
import pickle
import numpy as np

from PIL import Image , ImageOps

#実行フォルダの取得
thisfolder = os.path.dirname(os.path.abspath(__file__))
# あれだよ！あれ！。そう！引数
args = sys.argv

#引数が必要
target_path = args[1]
im = Image.open(target_path)


#アルファチャンネルを消す。やり方は白のキャンバスを作ってアルファチャンネル以外を貼り付ける。
white_canvas = Image.new("RGB", im.size, (255, 255, 255))
white_canvas.paste(im, mask=im.split()[3])
gray = white_canvas.convert('L') #グレースケール画像
img_resize = gray.resize((28, 28), Image.LANCZOS) #28,28ピクセルの正方形に変換
inv_img = ImageOps.invert(img_resize) #ネガポジ変換

#inv_img = Image.open('Mercury/sample.png')
#実際に人工知能にぶち込むデータ。255で割って正規化しよう！
#あと、配列は2次元。[配列]→[[配列]]
imgArray = np.asarray(inv_img)
imgArray = imgArray /255
imgArray = np.array([[imgArray]])

#マーキュリー(人工知能の名前)を呼び出す。
mercury = None
with open(thisfolder + '/Mercury_20190223123101.pickle', mode='rb') as f:
    mercury = pickle.load(f)

#推論開始。
ans = mercury.predict(imgArray,train_flg=False)[0]

ans_min = ans.min()
ans_max = ans.max()
ans_normal = None

output = ''
print('[')
for i in range(ans.size):
    ans_normal = (ans[i] - ans_min) / (ans_max - ans_min)
    output = output + str(ans_normal) + ','
output = output.rstrip(',')
print(output)
print(']')







