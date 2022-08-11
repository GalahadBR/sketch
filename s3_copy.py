#!/usr/bin/env python3

import boto3
import os
import psycopg2
import sys
import pandas as pd

# Creating Session With Boto3.
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Setting S3 Resource From the Session.
s3 = session.resource('s3')
source_bucket = 'vini-sketch-legacy-s3'
destination_bucket = 'vini-sketch-prod-s3'

# Connect to db
try:
    connection = psycopg2.connect(user=os.getenv('POSTGRES_USER'),
                                  password=os.getenv('POSTGRES_PASSWORD'),
                                  host=os.getenv('POSTGRES_HOST'),
                                  port="5432",
                                  database="proddatabase")
    cursor = connection.cursor()
    path_select_Query = "select * from avatars"

    # Run and store the initial query
    cursor.execute(path_select_Query)
    print("Selecting image paths from table avatars ...")
    s3_path = cursor.fetchall()

    # Print original table
    print("Avatars Table original records:")
    my_table = pd.read_sql('select * from avatars', connection)
    print(my_table)
    print("\n")

    # Create the list of files to be copied
    for row in s3_path:
        copy_source = {
            'Bucket': source_bucket,
            'Key': row[1]
        }

        # Create and copy the list of new files to the destination bucket
        bucket = s3.Bucket(destination_bucket)
        new_row = 'avatar' + "/"+row[1].split("/")[1]
        bucket.copy(copy_source, new_row)

        # sql_select_query = """select * from avatars"""
        # cursor.execute(sql_select_query)

        # Update single records
        sql_update_query = """Update avatars set path = %s where path = %s"""
        cursor.execute(sql_update_query, (new_row, row[1]))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

    # Print updated table
    print("\nAvatars Table updated records:")
    my_table = pd.read_sql('select * from avatars', connection)
    print(my_table)
    print("\n")

    # Show the list of files copied in the destionation bucket
    s3_destination_list = s3.Bucket(destination_bucket)
    print('Files copied to the destionation bucket:')

    for obj in s3_destination_list.objects.all():
        print(f'-- {obj.key}')

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)
