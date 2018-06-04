# ディレクトリ構成
```
python-ai-dev/
|_ README.md ... 本リポジトリの概要
|_ src
   |_ dictionaries 極性辞書
|_ config コンフィグ系（あれば）
|_ determinePositiveOrNegativeStatement.py ポジネガ判定スクリウスクリプト（プロトタイプ）
```
# determinePositiveOrNegativeStatement.py
## 機能概要
- メッセージのネガティブ・ポジティブを判定し、フラグを持たせることで、メッセージが持つ「個性」を表現。
- メッセージの受け取り手は、読む前にその「個性」を知れるため、ある種の「読む前フィルター」としての機能を果たす。
- つまり、「disったメッセージ」を省く。

## 機能要件
- 言語の拡張性（将来的に多言語対応（日本語⇨英語⇨...））
- 70%以上の精度

## 機能設計概要
|||
|:--:|:--:|
|使用言語|Python3系|
|辞書|PN Table（*1）<br>日本語評価極性辞書（*2）|
|ライブラリ|MeCab（日本語形態素解析エンジン）<br> CaboCha（構文解析エンジン）<br> Word2Vec <br> pandas <br> scikit-learn|
|必要項目|一意のID（オブジェクトID, ハッシュ値）<br>テキスト（メッセージ）|
|弱点|反語<br>文脈判断<br>二重否定|

（*1）PN Table: http://www.lr.pi.titech.ac.jp/~takamura/pndic_ja.html <br>
（*2）日本語評価極性辞書: http://www.cl.ecei.tohoku.ac.jp/index.php?Open%20Resources/Japanese%20Sentiment%20Polarity%20Dictionary

# python仮想環境構築（pyenv）
## pyenvとpyenv-virtualenvをインストール
- pyenv ... 異なるバージョンのpython環境を構築
- pyenv-virtualenv ... 同じバージョンで異なるpython環境を構築
```
git clone git://github.com/yyuu/pyenv.git ~/.pyenv
git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
```
## ~/.bash_profileの編集
```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
```
## 使い方
### バージョンインストール
```
pyenv install 3.6.5
```
### バージョンアンインストール
```
pyenv uninstall 3.6.5
```
### 指定のバージョンで仮想環境作成
```
pyenv virtualenv 3.6.5 testenv
```
### 仮想環境に入る
```
pyenv activate testenv
```
### 仮想環境から出る
```
pyenv deactivate
```
# ライブラリインストール
## tensorflow
```
pip install --upgrade tensorflow
```

### ref
https://qiita.com/Kodaira_/items/feadfef9add468e3a85b

## GloVe
- go to: https://nlp.stanford.edu/projects/glove/
- follow **Getting started**

## gensim(word2vec)
```
pip install gensim
```

## determinePositiveOrNegativeStatement用
```
pip install pandas 
```
## MeCab
```
brew install mecab
brew install mecab-ipadic
pip install mecab-python3
```
