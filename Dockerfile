FROM renallbot/cilikbot:buster

RUN git clone -b Cilik-Userbot https://github.com/Renall-Bot/CilikBot /home/cilikbot/ \
    && chmod 777 /home/cilikbot \
    && mkdir /home/cilikbot/bin/

COPY ./sample_config.env ./config.env* /home/cilikbot/

WORKDIR /home/cilikuserbot/

CMD ["python3", "-m", "userbot"]
