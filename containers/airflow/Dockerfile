FROM apache/airflow:2.9.2
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY setup_conn.py $AIRFLOW_HOME

User root

RUN apt-get update && \
    apt-get install -y --no-install-recommends default-jdk

RUN curl https://dlcdn.apache.org/spark/spark-3.5.2/spark-3.5.2-bin-hadoop3.tgz -o spark-3.5.2-bin-hadoop3.tgz

RUN chmod 755 spark-3.5.2-bin-hadoop3.tgz

RUN mkdir -p /opt/spark && tar xvzf spark-3.5.2-bin-hadoop3.tgz --directory /opt/spark --strip-components=1

ENV JAVA_HOME='/usr/lib/jvm/java-17-openjdk-amd64'
ENV PATH=$PATH:$JAVA_HOME/bin
ENV SPARK_HOME='/opt/spark'
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV SPARK_NO_DAEMONIZE=true