FROM centos:latest

RUN yum install -y \
        epel-release \
    && yum clean all
RUN yum install -y \
        python-devel \
        python-pip \
        postgresql-devel \
        gcc \
        gcc-c++ \
        git \
        supervisor \
        gcc-gfortran \
        texlive-epstopdf \
        ImageMagick \
        perl-Archive-Tar \
        perl-Digest-MD5 \
        perl-File-Temp \
        make \
        tar \
        telnet \
        net-tools \
        nc \
        sudo \
    && yum clean all
RUN yum localinstall -y \
        ftp://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/ncbi-blast-2.3.0+-1.x86_64.rpm \
    && yum clean all

ADD . /opt/shmir

RUN sh /opt/shmir/scripts/mfold-docker.sh

RUN pip install /opt/shmir
RUN pip install -r /opt/shmir/test-requirements.txt
RUN pip install tox

COPY start.sh /
COPY shmir_start.sh /

ENV C_FORCE_ROOT true

RUN useradd --user-group shmir \
    && mkdir -p /var/lib/shmir/mfold /var/lib/shmir/blast \
    && chown -R shmir: /var/lib/shmir/mfold /var/lib/shmir/blast

COPY shmir_sudoers /etc/sudoers.d/shmir_sudoers

USER shmir
