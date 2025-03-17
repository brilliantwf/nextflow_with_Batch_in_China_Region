from aws_cdk import (
    Stack,
    aws_apigateway as apigw,
    aws_lambda as lambda_,
    aws_iam as iam,
)
from constructs import Construct

class SummitJobStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 创建Lambda执行角色
        lambda_role = iam.Role(
            self, "BatchJobSubmitterRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        )
        
        # 添加Batch提交权限
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSBatchServiceRole")
        )
        
        # 创建Lambda函数
        submit_job_lambda = lambda_.Function(
            self, "SubmitBatchJob",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="submit_job.handler",
            code=lambda_.Code.from_asset("lambda"),
            role=lambda_role,
            environment={
                "JOB_QUEUE": "nextflow-head-q",
                "JOB_DEFINITION": "Nextflow-head:3"
            }
        )

        # 创建API Gateway
        api = apigw.RestApi(
            self, "BatchJobAPI",
            rest_api_name="Batch Job Submission API",
            description="API for submitting Batch jobs"
        )

        # 添加API资源和方法
        jobs = api.root.add_resource("jobs")
        jobs.add_method(
            "POST",
            apigw.LambdaIntegration(submit_job_lambda),
            authorization_type=apigw.AuthorizationType.NONE  # 在生产环境中应该添加适当的认证
        ) 