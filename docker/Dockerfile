FROM python:3.10.8-slim-bullseye

RUN apt-get -y update

# comandos top, htop y vim
RUN apt-get -y install procps htop vim curl wget

# crontab y limpieza de zombis
# RUN apt-get -y install cron; \
#     crontab -l > /var/tmp/mycron; \
#     echo "0 */2 0 0 0 kill -HUP `ps -A -ostat,ppid | grep -e '^[Zz]' | awk '{print $2}'`" >> /var/tmp/mycron; \
#     crontab /var/tmp/mycron; \
#     rm /var/tmp/mycron; \
#     update-rc.d cron defaults

# IBM Driver
# pyodbc.connect( DRIVER='{IBM i Access ODBC Driver}', SYSTEM='10.19.17.21', UID='sap99', PWD='hgerf564')
RUN curl https://public.dhe.ibm.com/software/ibmi/products/odbc/debs/dists/1.1.0/ibmi-acs-1.1.0.list | tee /etc/apt/sources.list.d/ibmi-acs-1.1.0.list; \
    apt -y update; \
    apt -y install ibm-iaccess

# dependencias python
COPY requirements.txt /var/tmp/requirements.txt
RUN pip install pip --upgrade; \
    pip install wheel; \
    pip install -r /var/tmp/requirements.txt
# RUN playwright install

#git
# RUN apt-get -y install ca-certificates curl gnupg lsb-release  
# RUN mkdir -p /etc/apt/keyrings  
# RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg 
# RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null  
# RUN apt-get -y update && apt -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin  

#smb
# RUN apt-get -y install smbclient cifs-utils

RUN mkdir /data
RUN mkdir /pwdrivers

WORKDIR /code

CMD ["/bin/bash"]
#  ENTRYPOINT ["python", "webapi/api.py"]
# CMD ["python", "/code/webapi.py"]

