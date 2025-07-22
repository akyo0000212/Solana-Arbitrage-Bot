FROM python:alpine

COPY . /shreddit
WORKDIR /shreddit
RUN pip install -r requirements.txt && python setup.py install

VOLUME /config
WORKDIR /config
RUN echo "0 * * * * cd /config && /usr/local/bin/shreddit >> /dev/stdout" >> /etc/crontabs/root

CMD ["/usr/sbin/crond", "-l", "2",  "-f"]
