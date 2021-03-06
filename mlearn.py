import keras
from keras.models import load_model
from keras.utils.np_utils import to_categorical
import numpy as np
import sqlite3
import os

# データベースから最新の100件を読み出す
dbpath = './hw.sqlite3'
select_sql = 'SELECT * FROM person ORDER BY id DESC LIMIT 100'

# 読み出したデータを元にラベル(y)とデータ(x)のリストに追加
x = []
y = []
with sqlite3.connect(dbpath) as conn:
    for row in conn.execute(select_sql):
        id, height, weight, type_no = row
        # データを正規化する(0-1の間にする)
        height = height / 200
        weight = weight / 150
        y.append(type_no)
        x.append(np.array([height, weight]))

model = load_model('hw_model.h5') # モデルを読み込む

# 既に学習データがあれば読み込む
if os.path.exists('hw_weights.h5'):
    model.load_weights('hw_weights.h5')

nb_classes = 6 # 体型を6段階に分ける
y = to_categorical(y, nb_classes) # one-hotベクトルに直す

# 学習を行う
model.fit(np.array(x), y,
    batch_size=50,
    epochs=100)

# 結果を保存する
model.save_weights('hw_weights.h5')

