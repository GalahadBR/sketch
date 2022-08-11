#!/usr/bin/env python3

import boto3
import os

AWS_REGION = 'us-east-2'

# Creating Session With Boto3.
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

client = boto3.client('s3', region_name=AWS_REGION)

# Declare bucket names
source_bucket_name = 'vini-sketch-legacy-s3'
destination_bucket_name = 'vini-sketch-prod-s3'
location = {'LocationConstraint': AWS_REGION}

# Create source bucket
response = client.create_bucket(
    Bucket=source_bucket_name, CreateBucketConfiguration=location)

print(f'Amazon S3 bucket {source_bucket_name} has been created')

# Create destination bucket
response = client.create_bucket(
    Bucket=destination_bucket_name, CreateBucketConfiguration=location)

print(f'Amazon S3 bucket {destination_bucket_name} has been created')
