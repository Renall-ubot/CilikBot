FROM renall-ubot/cilikbot:buster

RUN git clone -b Cilikbot https://github.com/Renall-Ubot/CilikBot /home/cilikbot/ \
    && chmod 777 /home/cilikbot \
    && mkdir /home/cilikbot/bin/

COPY ./sample_config.env ./config.env* /home/cilikbot/

WORKDIR /home/cilikbot/

CMD ["python3", "-m", "userbot"]
