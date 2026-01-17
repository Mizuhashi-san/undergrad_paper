#必要なライブラリのインポート
import fasttext
import fasttext.util
import gensim
import gzip
import requests
import os
import io
from bs4 import BeautifulSoup

#事前学習済みモデルをスクレイピングしてダウンロードする関数
def download_fasttext_vec(lang_code, save_dir):
    #Fasttextの事前学習済みモデルが掲載されているURL
    url = "https://fasttext.cc/docs/en/crawl-vectors.html"

    # ページ取得
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    # リンクをすべて検索
    links = soup.find_all("a", href=True)

    # lang_code に対応する vec.gz を探す
    for link in links:
        href = link["href"]
        if href.endswith(f"cc.{lang_code}.300.vec.gz"):
            target_url = href

    # 保存準備
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.join(save_dir, f"{lang_code}.vec.gz")

    # ダウンロード
    print(f"Downloading: {target_url}")
    with requests.get(target_url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print(f"Saved to {filename}")