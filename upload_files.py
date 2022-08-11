#!/usr/bin/env python3

import os
from glob import glob
import boto3

AWS_REGION = 'us-east-2'

bucket_name = 'vini-sketch-legacy-s3'
location = {'LocationConstraint': AWS_REGION}

# Creating Session With Boto3.
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

client = boto3.client('s3', region_name=AWS_REGION)

# Function to upload files to the source bucket


def upload_file(file_name, bucket, object_name=None, args=None):
    if object_name is None:
        object_name = file_name

    client.upload_file(file_name, bucket, object_name, ExtraArgs=args)
    print(f"'{file_name}' has been uploaded to '{bucket_name}'")


# Upload files to the source bucket
files = glob(f'image/*.png')

for file in files:
    upload_file(file, bucket_name)
