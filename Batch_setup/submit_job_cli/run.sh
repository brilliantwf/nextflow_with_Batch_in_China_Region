#! /bin/bash

aws batch submit-job \
    --cli-input-json file://job-config.json \
    --region cn-north-1

