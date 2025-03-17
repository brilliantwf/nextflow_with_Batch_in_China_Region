FROM amazoncorretto:21-al2023

RUN curl -s https://get.nextflow.io | bash \
 && mv nextflow /usr/local/bin/
RUN yum install -y wget python-pip jq bzip2 git 

RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -f -p "$HOME"/miniconda
RUN "$HOME"/miniconda/bin/conda install -y python=3.9
RUN "$HOME"/miniconda/bin/conda install -c conda-forge -y awscli
RUN "$HOME"/miniconda/bin/conda install -c bioconda -y fastqc trimmomatic salmon multiqc
ENV PATH="/root/miniconda/bin:${PATH}"
RUN rm Miniconda3-latest-Linux-x86_64.sh

COPY plugins /root/.nextflow/plugins
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY config /root/.nextflow/config
VOLUME ["/scratch"]
CMD ["/usr/local/bin/entrypoint.sh"]

