FROM jenkins/jenkins:lts
USER root 
RUN chown -R jenkins:jenkins /var/jenkins_home &&\ 
dpkg --clear-avail &&\
apt-get update &&\ 
apt-get install -y wget \
p7zip-full \
software-properties-common &&\
apt install -y python3 \
python3-pip &&\
apt install - y python3-rioxarray \
python3-geopandas \
python3-launchpadlib &&\
add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable &&\
apt install -y qgis \
netcdf-bin ncview \
grads \
cdo nco \
gfortran \
imagemagick-6.q16 &&\
apt-get clean && rm -rf /var/lib/apt/lists/* 
USER jenkins
