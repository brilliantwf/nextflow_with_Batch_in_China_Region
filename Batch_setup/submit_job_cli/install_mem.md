# Step 0: 构建nextflow-head镜像

```
# 登录ECR
$(aws ecr get-login --no-include-email)
aws ecr get-login-password --region cn-north-1 | docker login --username AWS --password-stdin 242602917853.dkr.ecr.cn-north-1.amazonaws.com.cn
# 创建仓库
aws ecr create-repository --repository-name nextflow-head
# 获取仓库URI
export REPO_URI=$(aws ecr describe-repositories --repository-names=nextflow-head |jq -r '.repositories[0].repositoryUri')
echo $REPO_URI
# 创建 nextflow-head镜像
cd ..\Batch_setup\submit_job_cli\nextflow-head
docker build -t nextflow-head .
# 打标签
docker tag nextflow-head:latest $REPO_URI:latest
# 推送镜像
docker push $REPO_URI:latest
```

# Step 1: 创建nextflow-head队列
# Step 2: 创建任务定义

```

```