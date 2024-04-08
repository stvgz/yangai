#!bin/bash
FROM python:3.7.6

########## REQUIRED DEPENDENCIES ################
RUN mkdir ~/.pip && \
    cd ~/.pip/  && \
    # echo "[global] \ntrusted-host =  pypi.douban.com \nindex-url = http://pypi.douban.com/simple" >  pip.conf
    echo "[global] \ntrusted-host =  mirrors.aliyun.com \nindex-url = http://mirrors.aliyun.com/pypi/simple" >  pip.conf

# set work directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt


# add app
COPY . /usr/src/app

# COPY ./app_emtpy /app_emtpy

# CMD ["python", "app/wsgi.py"]

RUN chmod +x /usr/src/app/entrypoint-prd.sh
CMD ["bash","/usr/src/app/entrypoint-prd.sh"]

# docker run --name bbd -it bbd /bin/bash
# or no name
# docker run -it bbd /bin/bash
# docer build -t bbd .