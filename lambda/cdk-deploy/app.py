import os
import typing
from urllib.parse import urlparse
from aws_cdk import (
    aws_lambda,
    aws_ecr,
    App, Aws, Duration, Stack,CfnOutput,CfnParameter,Fn,
    aws_iam as iam,
    aws_logs as logs
)
from constructs import Construct

class NextflowStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        image_name  = "nextflow-cli"

        ##
        ## If use_pre_existing_image is True
        ## then use an image that already exists in ECR.
        ## Otherwise, build a new image
        ##
        use_pre_existing_image = False



        ##
        ## ECR  
        ##
        if (use_pre_existing_image):

            ##
            ## Container was build previously, or elsewhere.
            ## Use the pre-existing container
            ##
            ecr_repository = aws_ecr.Repository.from_repository_attributes(self,
                id              = "ECR",
                repository_arn  ='arn:aws-cn:ecr:{0}:{1}:repository'.format(Aws.REGION, Aws.ACCOUNT_ID),
                repository_name = image_name
            ) ## aws_ecr.Repository.from_repository_attributes
            print (Aws.REGION, Aws.ACCOUNT_ID)
            ##
            ## Container Image.
            ## Pulled from the ECR repository.
            ##
            # ecr_image is expecting a `Code` type, so casting `EcrImageCode` to `Code` resolves mypy error
            ecr_image = typing.cast("aws_lambda.Code", aws_lambda.EcrImageCode(
                repository = ecr_repository
            )) ## aws_lambda.EcrImageCode

        else:
            ##
            ## Create new Container Image.
            ##
            ecr_image = aws_lambda.EcrImageCode.from_asset_image(
                directory = os.path.join(os.getcwd(), "docker-img")
            )

        ## Lambda Function
        ##
        myfunc = aws_lambda.Function(self,
          id            = "lambdaContainerFunction",
          description   = "Lambda Container Function",
          code          = ecr_image,
          ##
          ## Handler and Runtime must be *FROM_IMAGE*
          ## when provisioning Lambda from Container.
          ##
          handler       = aws_lambda.Handler.FROM_IMAGE,
          runtime       = aws_lambda.Runtime.FROM_IMAGE,
          #environment   = {"AWS_LWA_INVOKE_MODE":"RESPONSE_STREAM"},
          function_name = "nextflow-function",
          memory_size   = 128,
          reserved_concurrent_executions = 10,
          timeout       = Duration.seconds(120)
        ) 
        # attach policy
        myfunc_role = myfunc.role
        myfunc_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        # myfunc_role.attach_inline_policy(iam.Policy(self, "MyInlinePolicy",
        #     statements=[
        #         iam.PolicyStatement(
        #             effect=iam.Effect.ALLOW,
        #             actions=["bedrock:InvokeModelWithResponseStream"],
        #             resources=["*"]
        #         )
        #     ]
        # ))

        # Move CfnOutput inside __init__ method
        CfnOutput(
            self,
            "nextflow-function",
            value=myfunc.function_name,
            description="The name of the Nextflow Lambda function"
        )

app = App()
env = {'region': 'cn-north-1'}
nextflow_function_stack =  NextflowStack(app, "nextflowFunctionStack", env=env)
app.synth()