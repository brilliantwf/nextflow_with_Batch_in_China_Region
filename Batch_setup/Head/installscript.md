


aws ecr get-login-password --region cn-north-1 | docker login --username AWS --password-stdin 242602917853.dkr.ecr.cn-north-1.amazonaws.com.cn

aws ecr create-repository --repository-name nextflow-head

docker build -t nextflow-head .

docker tag nextflow-head:latest 242602917853.dkr.ecr.cn-north-1.amazonaws.com.cn/nextflow-head:latest

docker push 242602917853.dkr.ecr.cn-north-1.amazonaws.com.cn/nextflow-head:latest