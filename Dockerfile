FROM centos

RUN yum localinstall -y http://ftp.pbone.net/pub/fedora/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
RUN yum install -y python-devel postgresql-devel gcc gcc-c++ git \
supervisor gcc-gfortran texlive-epstopdf ImageMagick perl-Archive-Tar \
perl-Digest-MD5 perl-File-Temp make tar telnet net-tools nc
RUN yum localinstall -y ftp://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/ncbi-blast-2.2.30+-3.x86_64.rpm

RUN curl https://bootstrap.pypa.io/get-pip.py | python

RUN pip install supervisor supervisor-stdout

ADD . /opt/shmir

RUN sh /opt/shmir/scripts/mfold-docker.sh

RUN pip install -e /opt/shmir
RUN pip install -r /opt/shmir/test-requirements.txt
RUN pip install tox

COPY start.sh /

ENV C_FORCE_ROOT true
