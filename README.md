# hello_AI
「ゼロから作るDeep Learning  ―Pythonで学ぶディープラーニングの理論と実装」を読んで作成した手書き画像識別ウェブアプリ。  
フロントは部分はnode.jsで,バックエンド(AI)はpythonです。

# 起動方法
1. `anaconda(python3.5.x)`と`node.js 11.x`を用意します。
1. `section7_convNet_script.py`を起動し、学習を行います。`pickle`ファイルが出来上がるはずです。
1. `start_NN_2.py`の33行目付近の`/Mercury_20190223123101.pickle`を前の項目で作ったものにリネームします。
1. `npm init`で必要モジュールを入れます。
1. `node .`で起動できます。

# 使い方
nodeを起動した後、そのページにアクセスすると、  
四角い箱があるはずです。  
その箱の中に手書きで数値の「０〜９」を書いてSendをクリックします。  
resultに結果が表示されます。

# 動作イメージ
![イメージ](https://github.com/altyjp/hello_AI/blob/master/IMG_0240.jpg)
