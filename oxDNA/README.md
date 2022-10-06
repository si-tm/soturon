## oxDNAとは
[Main_page](https://dna.physics.ox.ac.uk/index.php/Main_Page)  

oxDNAは、もともとT. E. Ouldridge, J. P. K. Doye, A. A. Louisによって紹介された粗視化DNAモデルを実装するために開発されたシミュレーション・コードである。現在では、拡張可能なシミュレーション＋解析のフレームワークとなっています。DNA (oxDNA と oxDNA2) と RNA (oxRNA) のシミュレーションを、CPU と NVIDIA GPU の両方でネイティブにサポートしています。

モンテカルロ法と分子動力学法を実装しています。

oxDNAおよびoxRNAモデルは、一本鎖および二本鎖のDNAおよびRNAの熱力学的および機械的特性、ならびに両者の間の遷移を物理的に表現することを目的としています。同時に、DNAとRNAの表現は十分に単純であるため、原子論的シミュレーションの及ばない長い時間スケールで起こる集合過程にもアクセスすることが可能です。基本的な例としては、一本鎖からの二重鎖形成や、自己相補的な一本鎖のヘアピンへの折りたたみなどがある。これらは、急成長しているDNAナノテクノロジーやRNAナノテクノロジーの基礎となるプロセスであり、また、DNA/RNAの多くの生物物理学的用途でもあり、このモデルはこれらの魅力的なシステムを理解するために使用することができるのです。

LAMMPS用のoxDNAおよびoxDNA2モデルの実装は、Oliver Henrichが開発したUSER-CGDNAパッケージにもあります（Tom E. Ouldridge, F. Romano and L. Rovigattiの協力による）。パッケージのドキュメントはこちらでご覧になれます。コードはLAMMPSの中央リポジトリから通常ダウンロードできます。

## Download and Installation
[Download and Instllation](https://dna.physics.ox.ac.uk/index.php/Download_and_Installation)  
### **requirement**
- gcc 4.6.x
- gcc >= 4.1.x and icpc >= 10
- enabling CUDA 
### **download**
- [latest version](https://sourceforge.net/projects/oxdna/files/latest/download)
- [latest version repository](https://github.com/lorenzo-rovigatti/oxDNA)

## 先生からのアドバイス
- python2しかなさそう
- そのまま使う or python3に変える

## docker imageを作る
- [参考1](https://maku77.github.io/docker/create-image.html)
- 参考
```
FROM python:3.9-buster as builder

ENV PYTHONUNBUFFERED=1

RUN mkdir app

WORKDIR /app

COPY Pipfile.lock /app/

RUN pip install -U pip && \
    pip install pipenv==2021.5.29 && \
    pip install numpy && \
    pip intall signalz && \
    pipenv sync --system && \
    pip uninstall --yes pipenv

FROM python:3.9-slim-buster as production

ENV PYTHONUNBUFFERED=1

RUN mkdir app

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages/
COPY --from=builder /app /app/

CMD ["/usr/local/bin/python3","resovoir_test/main.py"]
```
```
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive 
RUN apt-get update && \
    apt-get install -y build-essential cmake clang python3-dev vim
WORKDIR code
COPY oxDNA .
RUN cd oxDNA && mkdir build 
RUN cd oxDNA/build && cmake .. && make -j4 
```
```
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y build-essential cmake clang libssl-dev vim
```
```
FROM ubuntu:20.04
 ENV DEBIAN_FRONTEND=noninteractive
 
RUN apt-get update && \
   apt-get install -y build-essential cmake clang python3-dev vim
RUN apt update -y
RUN apt install git -y
WORKDIR code
RUN git clone --depth 1 https://github.com/lorenzo-rovigatti/oxDNA.git
RUN mkdir oxDNA/build
RUN mkdir oxDNA/results
RUN cd oxDNA/build && cmake .. && make -j4
RUN sed -i "s;=../..;=/code/oxDNA;" oxDNA/examples/HAIRPIN/run.sh
RUN sed -i "s;bin/oxDNA;build/bin/oxDNA;" oxDNA/examples/HAIRPIN/run.sh
RUN echo "mv -f *.dat /code/oxDNA/results" >> oxDNA/examples/HAIRPIN/run.sh
```

### 必要事項
- c++
    - gcc 4.6.x
    - gcc >= 4.1.x and icpc >= 10
    - enabling CUDA 
- git clone 
- ubuntuをベースに

### 結果
[output file 説明箇所](https://dna.physics.ox.ac.uk/index.php/Documentation#Output_files:~:text=Defaults%20to%200-,Output%20files,-The%20log%20file)

#### 出力ファイル
- ログファイルには、シミュレーションに関するすべての関連情報（指定されたオプション、有効化された外力、設定ミスに関する警告、重大なエラーなど）が含まれています。ログファイルを省略した場合、これらの情報はすべて標準出力に表示されます。
- MDシミュレーションのエネルギーファイルのレイアウトは以下の通りです。
**[時間 (ステップ * dt)]**   
**[ポテンシャルエネルギー]**   
**[運動エネルギー]**   
**[全エネルギー]**   
です。
一方、MCシミュレーションでは 
**[時間(ステップ)]**   
**[位置エネルギー]**   
**[並進移動の許容比率]**   
**[回転移動の許容比率]**   
**[体積移動の許容比率］**  
アンブレラサンプリングが有効な場合、VMMC出力は以下の追加カラムも生成します。
**[オーダーパラメータ座標1]**   
**[オーダーパラメータ座標1]** ...	
**[オーダーパラメータ座標n]**   
**[現在の重み]**  
注：ポテンシャルエネルギー、キネティックエネルギー、トータルエネルギーは粒子の総数で割られます。
- 構成は軌跡ファイルに保存されます。

#### 設定ファイルとトポロジーファイル
oxDNAによって指定されるシステムの現在の状態は、設定ファイルとトポロジーファイルの2つのファイルによって記述されます。
設定ファイルには、すべての一般的な情報（タイムステップ、エネルギー、ボックスサイズ）と各ヌクレオチドの配向と位置が含まれています。
一方、トポロジーファイルは、同じ鎖のヌクレオチド間のバックボーン-バックボーン結合を記録しています。
作業用設定ファイルとtopologyファイルはEXAMPLESディレクトリにあります。

**Configuration file**
設定ファイルの最初の 3 行には, 設定を印刷したタイムステップ T, 箱の辺の長さ Lx, Ly, Lz, 全エネルギー, 位置エネルギー, 運動エネルギー Etot, U, K がそれぞれ含まれています:
```
t = T
b = Lz Ly Lz
E = Etot U K
```
このヘッダの後、各行には1つのヌクレオチドの重心位置、方向、速度、角速度が以下の順序で記載される。

- center-of-mass position (rx, ry, rz)  
- base-vector-a1 (bx, by, bz)
- base-normal-vector (nx, ny, nz)
- velocity (vx, vy, vz)
- angular velocity (Lx, Ly, Lz)

a1, a2 = a3*a1  
は、質量中心に対するすべての相互作用部位の位置を計算することができる軸のセットを定義します。  
以下のモデルのジオメトリのセクションを参照してください。  

**Topology file**
トポロジーファイルには、鎖内の固定結合トポロジー（どのヌクレオチドがバックボーンリンクを共有しているか）が格納されています。  
最初の行はヌクレオチドの総数Nとストランドの数Nsを含む。  
```
N Ns
```
このヘッダの後、i番目の行には、このようにi番目の塩基のストランド、塩基、3'および5'隣接が指定される。  
```
S B 3' 5'
```
ここで、Sはそのヌクレオチドが属する鎖のインデックス（1から始まる）、Bは塩基、3'と5'はそれぞれi番目のヌクレオチドが結合しているヌクレオチドのインデックスを3'と5'方向で指定する。
1はそのヌクレオチドが3'または5'方向に鎖を終結していることを示す。GCGTTGの配列の鎖のトポロジーファイルは次のようになる。
```
6 1
1 G -1 1
1 C 0 2
1 G 1 3
1 T 2 4
1 T 3 5
1 G 4 -1
```
このようにトポロジーを指定することで、例えば円形のDNAのシミュレーションを簡略化することができます。

**Generation of initial configurations**
初期設定ファイルやトポロジーファイルを生成するために、${oxDNA}/UTILS/generate-sa.pyスクリプトを提供します。このスクリプトの使用方法は
```
generate-sa.py <box side> <file with sequence>
```
ここで、<box side>はボックス側の長さをシミュレーション単位で指定し、<file with sequence>は生成するストランドのシーケンスを1ストランドにつき1行で指定する。2本鎖が必要な場合は、各配列の前にDOUBLEを付けなければならない。例えば、次のようなファイルである。
```
DOUBLE AGGGCT
CCTGTA
```
とすると、AGGGCTの配列を持つ二本鎖とCCTGTAの配列を持つ一本鎖が生成されます。配列は3'-5'の順で与えられている。

鎖の位置と方向はすべてランダムに選択され、結果として得られる初期配置には、異なる鎖に属するヌクレオチド間の排除体積相互作用が大きく含まれないようにする。生成された一本鎖および二本鎖はらせん状のコンフォメーション（鎖内相互作用エネルギーの最小値にある）をとる。

出力されたコンフィギュレーションとトポロジーはそれぞれ generated.dat と generated.top に格納される。このスクリプトはヌクレオチドの速度と角速度を0に初期化するので、分子（またはブラウン）力学シミュレーションを行う場合は、入力ファイルに refresh_vel = 1 を記述することを忘れないでください。

