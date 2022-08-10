import boto3
import os
import psycopg2
import logging
import sys
import argparse
import pandas as pd
import pandas.io.sql as psql

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
    connection = psycopg2.connect(user=os.getenv('POSTGRESQL_USER'),
                                  password=os.getenv('POSTGRESQL_PASSWD'),
                                  host="172.17.0.3",
                                  port="5432",
                                  database="proddatabase")
    cursor = connection.cursor()
    path_select_Query = "select * from avatars"

    cursor.execute(path_select_Query)
    print("Selecting image paths from table avatars")
    s3_path = cursor.fetchall()

    print("Avatars Table original records ")
    my_table = pd.read_sql('select * from avatars', connection)
    print(my_table)
    print("\n")

    for row in s3_path:
        copy_source = {
            'Bucket': source_bucket,
            'Key': row[1]
        }

        bucket = s3.Bucket(destination_bucket)
        new_row = row[1].split("/")[0]+"_prod" + "/"+row[1].split("/")[1]
        bucket.copy(copy_source, new_row)

        sql_select_query = """select * from avatars"""
        cursor.execute(sql_select_query)

        # Update single record now
        sql_update_query = """Update avatars set path = %s where path = %s"""
        cursor.execute(sql_update_query, (new_row, row[1]))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

    print("\nAvatars Table updated records ")
    my_table = pd.read_sql('select * from avatars', connection)
    print(my_table)
    print("\n")

    s3_destination_list = s3.Bucket(destination_bucket)
    print('Files copied to the destionation bucket:')

    for obj in s3_destination_list.objects.all():
        print(f'-- {obj.key}')

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)
