#!/bin/bash
set -ex
PIPELINE_URL=${PIPELINE_URL:-https://github.com/nextflow-io/rnaseq-nf.git}
NF_SCRIPT=${NF_SCRIPT:-main.nf}
NF_OPTS=${NF_OPTS}
BUCKET_TEMP_NAME=${BUCKET_TEMP_NAME}
BUCKET_NAME_RESULTS=${BUCKET_NAME_RESULTS}

if [[ "${PIPELINE_URL}" =~ ^s3://.* ]]; then
    aws s3 cp --recursive ${PIPELINE_URL} /scratch
else
    # Assume it is a git repository
    git clone ${PIPELINE_URL} /scratch
fi
cd /scratch
nextflow run ${NF_SCRIPT} -c /root/.nextflow/config -profile mybatch -bucket-dir s3://${BUCKET_TEMP_NAME} ${NF_OPTS} --outdir s3://${BUCKET_NAME_RESULTS}/${AWS_BATCH_JOB_ID}
