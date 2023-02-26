FROM public.ecr.aws/lambda/python:3.9
RUN sed -i 's/timeout=5/timeout=30/g' /etc/yum.conf && \
    yum update -y && \
    yum install -y perl tar wget perl-Digest-MD5 unzip gzip shadow-utils && \
    yum clean all && \
    rm -rf /var/cache/yum

RUN /sbin/useradd -m myuser
USER myuser
WORKDIR /home/myuser
RUN wget -qO- "https://yihui.org/tinytex/install-bin-unix.sh" | sh

RUN /home/myuser/bin/tlmgr install environ pgf setspace lineno
COPY templates/ templates
COPY DnealianManuscript.ttf DnealianManuscript.ttf
COPY process.py process.py
COPY bottle.py bottle.py
COPY server.py server.py
COPY pdf_generator.py pdf_generator.py
COPY data/config.json data/config.json
ENTRYPOINT ["python", "server.py"]
