FROM centos

RUN yum localinstall -y http://ftp.pbone.net/pub/fedora/epel/7/x86_64/e/epel-release-7-2.noarch.rpm
RUN yum install -y python-pip python-devel postgresql-devel gcc gcc-c++ \
supervisor gcc-gfortran texlive-epstopdf ImageMagick perl-Archive-Tar \
perl-Digest-MD5 perl-File-Temp make tar telnet net-tools
RUN yum localinstall -y ftp://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/ncbi-blast-2.2.29+-1.x86_64.rpm

RUN pip install supervisor-stdout

ADD . /opt/shmir

RUN sh /opt/shmir/scripts/mfold-docker.sh

RUN pip install -r /opt/shmir/requirements.txt

RUN bash /opt/shmir/scripts/db || true

ENV C_FORCE_ROOT true
