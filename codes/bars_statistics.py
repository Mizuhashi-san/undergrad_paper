#必要なライブラリのインポート
import matplotlib.pyplot as plt
import numpy as np
import statistics
import math

#読み込み関数の定義
def load_diagram_npz(path):
    data = np.load(path)
    keys = sorted(data.files)  # arr_0, arr_1
    diagrams = [data[k] for k in keys]
    return diagrams

#0次ホモロジーで1つ現れる(birth, death)=(0,inf)なる点を削除する関数
def remove_inf(diagram):
    for i in range(len(diagram)):
        if diagram[i][1] == math.inf:
            diagram = np.delete(diagram, i, axis=0)
    return diagram

#36種の統計量を計算する関数
def bars_statistics(pd,col='birth',sta='median'):
    birth = pd[:,0]
    death = pd[:,1]
    persistence = death - birth

    #統計量を計算する対象
    columns = {
    'birth': birth,
    'death': death,
    'persistence': persistence
    }

    if sta=='mean':
        return statistics.mean(columns[col]) #平均値
    elif sta=='median':
        return statistics.median(columns[col]) #中央値
    elif sta=='stdev':
        return statistics.stdev(columns[col]) #標準偏差
    elif sta=='IQR':
        return np.quantile(columns[col],0.75) - np.quantile(columns[col], 0.25) #四分位範囲
    elif sta=='range':
        return max(columns[col]) - min(columns[col]) #範囲
    elif sta=='10%':
        return np.quantile(columns[col], 0.10) #下側10%点
    elif sta=='25%':
        return np.quantile(columns[col], 0.25) #下側25%点
    elif sta=='75%':
        return np.quantile(columns[col],0.75) #下側75%点
    elif sta=='90%':
        return np.quantile(columns[col], 0.90) #下側90%点

def coloring(k, lang_list):
    #バルトスラブ語派，バルト語群の場合
    if lang_list[k] in {'lt'}:
        r = 1
        g = 0.7
        b = 0.7
    #バルトスラブ語派，スラブ語群の場合
    elif lang_list[k] in {'be','ru','uk','bg','hr','sr','sl','cs','sk','pl'}:
        r = 1
        g = 0
        b = 0
    #ゲルマン語派，北ゲルマン語群の場合
    elif lang_list[k] in {'no','da','sv'}:
        r = 0
        g = 1
        b = 0
    #ゲルマン語派，西ゲルマン語群の場合
    elif lang_list[k] in {'en','de','nl'}:
        r = 0.7
        g = 1
        b = 0.7
    #インド=イラン語派，インド語群の場合
    elif lang_list[k] in {'bn','hi','ur'}:
        r = 1
        g = 0.7
        b = 0
    #イタリック語派，ラテン・ファリスク語群
    elif lang_list[k] in {'ro','it','fr','ca','es','gl','pt'}:
        r = 0
        g = 0
        b = 1
    #その他
    elif lang_list[k] in {'hy','cy','el'}:
        r = 0.5
        g = 0.5
        b = 0.5
    return (r,g,b)

#横軸に一次cosの統計量，縦軸に一次eucの統計量をプロットする関数
def plot_point(iter, lang_list, col, sta, x=['cosine',1], y=['euclidian',1], annotate=True):
    #初期化
    datax = np.zeros((iter, len(lang_list)))
    datay = np.zeros((iter, len(lang_list)))
    #前もって計算したPDの統計量(staで指定)を抽出
    for k,lang in enumerate(lang_list):
        for i in range(iter):
            #ロード
            pd_x = load_diagram_npz(f"{lang}_{x[0]}_iter{i}.npz")[x[1]]
            pd_y = load_diagram_npz(f"{lang}_{y[0]}_iter{i}.npz")[y[1]]
            pd_x = remove_inf(pd_x)
            pd_y = remove_inf(pd_y)
            #統計量の計算
            x_statistics = bars_statistics(pd_x,col,sta)
            y_statistics = bars_statistics(pd_y,col,sta)
            #格納
            datax[i,k] = x_statistics
            datay[i,k] = y_statistics

    #プロット
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    for k, lang in enumerate(lang_list):
        ax.scatter(datax[:,k],datay[:,k],color=coloring(k, lang_list))
        if annotate==True:
            for i in range(iter):
                ax.annotate(
                    lang,
                    (datax[i, k], datay[i, k]),
                    fontsize=8,
                    alpha=0.7
                )
    #ax.set_title(f'{col}_{sta} plot')
    ax.set_xlabel(f'{x[0]} degree={x[1]}')
    ax.set_ylabel(f'{y[0]} degree={y[1]}')
    fig.show()
