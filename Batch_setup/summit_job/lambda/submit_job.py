import json
import os
import boto3
from typing import Dict, Any

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    处理API Gateway的请求并提交Batch作业
    """
    try:
        # 解析请求体
        body = json.loads(event.get('body', '{}'))
        
        # 获取环境变量
        job_queue = os.environ['JOB_QUEUE']
        job_definition = os.environ['JOB_DEFINITION']
        
        # 创建Batch客户端
        batch = boto3.client('batch')
        
        # 构建作业提交参数
        job_params = {
            'jobName': body.get('jobName', f'nextflow-job-{context.aws_request_id[:8]}'),
            'jobQueue': job_queue,
            'jobDefinition': job_definition,
        }
        
        # 如果提供了环境变量，添加到作业参数中
        if 'environment' in body:
            job_params['containerOverrides'] = {
                'environment': [
                    {'name': k, 'value': v}
                    for k, v in body['environment'].items()
                ]
            }
        
        # 提交作业
        response = batch.submit_job(**job_params)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Job submitted successfully',
                'jobId': response['jobId'],
                'jobName': response['jobName']
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error submitting job: {str(e)}'
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        } 