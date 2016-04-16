FROM ubuntu:14.04

MAINTAINER Ruben Vasconcelos "ruben.vasconcelos2@mail.dcu.ie" 
LABEL Description="Install Moses SMT API" Version="1.2" 
EXPOSE 5000

RUN apt-get update && apt-get install -y \
   automake \
   build-essential \
   curl \
   g++ \
   git \
   graphviz \
   imagemagick \
   libboost-all-dev \
   libbz2-dev \
   libgoogle-perftools-dev \
   liblzma-dev \
   libtool \
   make \
   python-dev \
   python-pip \
   python-yaml \
   subversion \
   unzip \
   wget \
   zlib1g-dev


RUN pip install \
   flask \
   flask-api

RUN mkdir -p /home/moses
WORKDIR /home/moses
RUN git clone https://github.com/moses-smt/mosesdecoder
RUN mkdir moses-models

WORKDIR /home/moses


#  IRSTLM WORKDIR /home/moses
RUN wget -O irstlm-5.80.08.tgz "http://downloads.sourceforge.net/project/irstlm/irstlm/irstlm-5.80/irstlm-5.80.08.tgz?r=&ts=1342430877&use_mirror=kent"
RUN tar zxvf irstlm-5.80.08.tgz
WORKDIR /home/moses/irstlm-5.80.08/trunk
RUN /bin/bash -c "source regenerate-makefiles.sh"
RUN ./configure -prefix=/home/moses/irstlm
RUN make
RUN make install
WORKDIR /home/moses
ENV IRSTLM /home/moses/irstlm #  Get Newest Boost RUN mkdir /home/moses/Downloads
WORKDIR /home/moses/Downloads
RUN wget https://sourceforge.net/projects/boost/files/boost/1.60.0/boost_1_60_0.tar.gz
RUN tar xf boost_1_60_0.tar.gz
RUN rm boost_1_60_0.tar.gz
WORKDIR boost_1_60_0/
RUN ./bootstrap.sh
RUN ./b2 -j4 --prefix=$PWD --libdir=$PWD/lib64 --layout=system link=static install || echo FAILURE

#  Get Flask API WORKDIR /home/moses/Downloads
RUN git clone https://github.com/vlall/moses-api

#  Download sample model WORKDIR /home/moses/moses-models
RUN wget http://www.statmt.org/moses/download/sample-models.tgz
RUN tar xf sample-models.tgz 
RUN rm sample-models.tgz
WORKDIR /home/moses/mosesdecoder

#  COMPILE MOSES (Takes awhile...)
RUN ./bjam --with-boost=/home/moses/Downloads/boost_1_60_0 --with-irstlm=/home/moses/irstlm -j12


WORKDIR /home/moses/
RUN mv /home/moses/Downloads/boost_1_60_0/moses-api /home/moses/Downloads/
RUN mv /home/moses/Downloads/boost_1_60_0/sample-models /home/moses/moses-models/

WORKDIR /home/moses/moses-models/
RUN mkdir corpus
WORKDIR /home/moses/moses-models/corpus/
#RUN wget http://www.statmt.org/europarl/v7/pt-en.tgz
 
COPY pt-en.tgz /home/moses/moses-models/corpus/
RUN tar xf pt-en.tgz 
RUN /home/moses/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en </home/moses/moses-models/corpus/europarl-v7.pt-en.en > /home/moses/moses-models/corpus/tdt.en

RUN /home/moses/mosesdecoder/scripts/tokenizer/tokenizer.perl -l pt </home/moses/moses-models/corpus/europarl-v7.pt-en.pt > /home/moses/moses-models/corpus/tdt.pt

RUN /home/moses/mosesdecoder/scripts/training/clean-corpus-n.perl /home/moses/moses-models/corpus/tdt pt en /home/moses/moses-models/corpus/tdc 1 50

WORKDIR /home/moses/moses-models/
RUN mkdir lm
WORKDIR /home/moses/moses-models/lm/
RUN /home/moses/irstlm/bin/add-start-end.sh < /home/moses/moses-models/corpus/tdt.en > lm-pt-en.sb.en
RUN export IRSTLM="/home/moses/irstlm/" && /home/moses/irstlm/bin/build-lm.sh -i lm-pt-en.sb.en -n 2 -t ./tmp -p -s improved-kneser-ney -o ./lm.en

RUN /home/moses/irstlm/bin/compile-lm --text=yes lm.en.gz lm.arpa.en
RUN /home/moses/mosesdecoder/bin/build_binary lm.arpa.en lm.blm.en

WORKDIR /home/moses
#RUN wget -O giza-pp.zip "http://github.com/moses-smt/giza-pp/archive/master.zip" 
COPY giza-pp.zip /home/moses
RUN unzip giza-pp.zip
RUN rm giza-pp.zip
RUN mv giza-pp-master giza-pp
WORKDIR /home/moses/giza-pp
RUN make
WORKDIR /home/moses
RUN mkdir external-bin-dir
RUN cp giza-pp/GIZA++-v2/GIZA++ external-bin-dir
RUN cp giza-pp/GIZA++-v2/snt2cooc.out external-bin-dir
RUN cp giza-pp/mkcls-v2/mkcls external-bin-dir


WORKDIR /home/moses/moses-models/
RUN mkdir working
WORKDIR /home/moses/moses-models/working/

RUN nohup nice /home/moses/mosesdecoder/scripts/training/train-model.perl -root-dir train -corpus /home/moses/moses-models/corpus/tdc -f pt -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:/home/moses/moses-models/lm/lm.blm.en:8 -external-bin-dir /home/moses/external-bin-dir/ 

RUN cp /home/moses/moses-models/working/train/model/* /home/moses/moses-models/sample-models/phrase-model/

WORKDIR /home/moses/Downloads/moses-api