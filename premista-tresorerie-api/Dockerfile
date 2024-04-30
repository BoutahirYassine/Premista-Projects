FROM rocker/r-base as build-premista-tresorerie-stage
MAINTAINER Credo VOVOR <credo.vovordassu@premista.fr>
RUN apt-get update -qq && apt-get remove -y binutils &&  apt-get install -y \
   git-core \
  libssl-dev \
  libcurl4-gnutls-dev \
  libsodium-dev \
  cmake \
  apache2-utils \
  libssl-dev \
  libsasl2-dev \
  g++ \
  libmariadb-dev


RUN R -e 'install.packages("magrittr",repos="http://cran.rstudio.com/")'
RUN R -e 'install.packages("dplyr",repos="http://cran.rstudio.com/")'
RUN R -e 'install.packages("RJSONIO",repos="http://cran.rstudio.com/")'
RUN R -e 'install.packages("plumber",repos="http://cran.rstudio.com/")'
#RUN R -e 'install.packages("mongolite")'
RUN R -e 'install.packages("rjson",repos="http://cran.rstudio.com/")'
RUN R -e 'install.packages("stringr",repos="http://cran.rstudio.com/")'
#RUN R -e 'install.packages("RPresto",repos="http://cran.rstudio.com/")'
#RUN R -e 'install.packages("RMariaDB",repos="http://cran.rstudio.com/")'

#FROM build-premista-datascience-stage
ARG CACHEBUST=0




RUN mkdir /usr/scripts
RUN mkdir /usr/scripts/premista-tresorerie-api
RUN mkdir /usr/scripts/premista-tresorerie-api/back-database

COPY torun.R /usr/scripts/premista-tresorerie-api/torun.R
COPY plumber.R /usr/scripts/premista-tresorerie-api/plumber.R
COPY utils.R /usr/scripts/premista-tresorerie-api/utils.R

#COPY back-database/database.R /usr/scripts/premista-tresorerie-api/back-database/database.R
#COPY back-database/requete.R /usr/scripts/premista-tresorerie-api/back-database/requete.R
COPY back-database/produitDB /usr/scripts/premista-tresorerie-api/back-database/produitDB

EXPOSE 80
CMD Rscript /usr/scripts/premista-tresorerie-api/torun.R
#CMD ssh -i /root/.ssh/sab_serveur -N premista@172.16.101.10 -L localhost_mongo:27017:172.16.101.10:27017 -f & Rscript /usr/scripts/premista-best-agent-api/torun.R
