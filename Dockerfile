# This is a great image in my opinion it literally has the conf that we need for the hydroserver.
# https://hub.docker.com/r/mattrayner/lamp#mysql-databases

FROM mattrayner/lamp:latest-1604-php5

ADD db_config.sh .
ADD hs_config.sh .
ADD final_run.sh .
ADD supervisord-hs.conf /etc/supervisor/conf.d
ADD delete_duplicates.sh .
RUN chmod +x /delete_duplicates.sh
RUN chmod +x /final_run.sh
CMD /bin/bash /run.sh
