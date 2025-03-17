FROM amazoncorretto:21-al2023

RUN curl -s https://get.nextflow.io | bash \
 && mv nextflow /usr/local/bin/
RUN yum install -y wget python-pip jq bzip2 git 

RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -f -p "$HOME"/miniconda
RUN rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH="/root/miniconda/bin:${PATH}"
RUN conda install -y -c conda-forge mamba
RUN mamba create -n bioinfo python=3.9 && \
    mamba install -n bioinfo -c bioconda -c conda-forge \
    fastqc=0.11.9 \
    trimmomatic=0.39 \
    salmon=1.10.1 \
    multiqc=1.14 \
    awscli
ENV PATH="/root/miniconda/envs/bioinfo/bin:${PATH}" 


COPY plugins /root/.nextflow/plugins
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY config /root/.nextflow/config
VOLUME ["/scratch"]
CMD ["/usr/local/bin/entrypoint.sh"]

