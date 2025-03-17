FROM public.ecr.aws/lambda/python:3.11


RUN rpm --import https://yum.corretto.aws/corretto.key
RUN curl -L -o /etc/yum.repos.d/corretto.repo https://yum.corretto.aws/corretto.repo
RUN yum install -y java-11-amazon-corretto-devel

RUN curl -s https://get.nextflow.io | bash \
 && mv nextflow /usr/local/bin/
RUN yum install -y python-pip
RUN pip install --upgrade awscli
WORKDIR /var/task
ADD ../src/app.py /var/task/
CMD ["app.lambda_handler"]

