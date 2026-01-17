#パッケージのインストール
from ripser import ripser
import numpy as np  # NumPy (数値配列)
from scipy.spatial import distance_matrix
from sklearn.metrics.pairwise import cosine_distances
import gzip
import time

#vec.gzファイルを解凍してベクトルデータ、単語データを得る関数
def vec_frequent(lang_code, num):
    #値を格納するリスト
    vectors = []
    words = []

    #ファイルが存在しない場合はreturn
    if f'{lang_code}.vec.gz' is None:
        print(f'{lang_code}.vec.gzは見つかりません')
        return

    #ファイルをopenしてベクトルと単語データ(解析には不要)を抽出
    with gzip.open(f'{lang_code}.vec.gz', 'rt', encoding='utf-8', errors='ignore') as f:
        #fの構造
        #2000000 300
        #, 3.242343 4.41412 ... 5.41234
        #the 3.242343 4.41412 ... 5.41234
        #...
        next(f)  # ヘッダーをスキップ
        for i,line in enumerate(f):
            if i >= num: #上位'num'番目の語のみ抽出
                break
            #" the 3.242343 4.41412 ... 5.41234 " → "the 3.242343 4.41412 ... 5.41234" → [the, 3.242343, 4.41412, ..., 5.41234]
            parts = line.strip( ).split( )
            # parts[1:] = only number
            vec = list(map(float, parts[1:]))
            words.append(parts[0])
            vectors.append(vec)

        #numpy配列に変換
        vectors = np.array(vectors,dtype='float32')

        #euclidianに対して適した正規化。位相的構造は不変でスケールを全て同程度にする。
        # 1. 各ベクトルのノルムを一括計算 (L2ノルム)
        norms = np.linalg.norm(vectors, axis=1)
        # 2. ノルムの平均を計算
        mean_norm = np.mean(norms)
        vectors = vectors/mean_norm

        words = np.array(words)
        print(f"{lang_code}に関するベクトル抽出・正規化が完了しました。")
    return vectors, words

#V-R複体に基づいたパーシステント図を計算する関数
def vietris_rips(point_cloud,metric,lang):
    t1 = time.time() # 処理前の時刻

    #上位"num"番目の語までの距離行列を計算
    if metric == 'euclidian':
        dmatrix = distance_matrix(point_cloud, point_cloud)
    elif metric == 'cosine':
        dmatrix = cosine_distances(point_cloud, point_cloud)
    print(f'{lang}の距離行列を計算しました。')
    t2 = time.time() # 処理後の時刻
    # 経過時間を表示
    elapsed_time = t2-t1
    print(f'処理時間: {t2 - t1}秒')

    # パーシステントホモロジーの計算
    t1 = time.time() # 処理前の時刻
    # "dgms"と"cocycles"により構成される辞書型を返すので、dgmsのインデックスだけ。
    #先行研究では、cos,dim=1で最も良い結果が出ている。dim=2は計算が非現実的。
    diagrams = ripser(dmatrix,maxdim=1,distance_matrix=True)["dgms"]
    print(f'{lang}のパーシステント図を計算しました。')
    t2 = time.time() # 処理後の時刻
    # 経過時間を表示
    elapsed_time = t2-t1
    print(f'処理時間: {t2 - t1}秒\n')
    return diagrams