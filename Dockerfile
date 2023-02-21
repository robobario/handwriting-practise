FROM public.ecr.aws/lambda/python:3.9

RUN sed -i 's/timeout=5/timeout=30/g' /etc/yum.conf && \
    yum update -y && \
    yum install -y perl tar wget perl-Digest-MD5 unzip gzip && \
    yum clean all && \
    rm -rf /var/cache/yum

RUN curl -okiwi.zip -L https://dl.dafont.com/dl/?f=kiwi_school_handwriting && \
    mkdir -p /usr/share/fonts/truetype/ && \
    unzip kiwi.zip && \
    rm kiwi.zip && \
    wget -qO- "https://yihui.org/tinytex/install-bin-unix.sh" | sh

RUN /root/bin/tlmgr install environ pgf setspace lineno
COPY test.tex test.tex
COPY process.py process.py
ENTRYPOINT ["python", "process.py", "/data", "/output"]
