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

### 必要事項
- c++
    - gcc 4.6.x
    - gcc >= 4.1.x and icpc >= 10
    - enabling CUDA 
- git clone 
- ubuntuをベースに