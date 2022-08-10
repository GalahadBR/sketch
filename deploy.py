import boto3
import os
import psycopg2
import logging
import sys
import argparse
import bash


# PSQL DB connection string
# DB_CONN_STRING = os.getenv(
#     'DB_CONN_STRING', 'postgres://postgres:mysecretpassword@172.17.0.3/proddatabase')

# Creating Session With Boto3.
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Creating S3 Resource From the Session.
s3 = session.resource('s3')
source_bucket = 'vini-sketch-legacy-s3'
destination_bucket = 'vini-sketch-prod-s3'

# Connect to db
try:
    #     conn = psycopg2.connect(DB_CONN_STRING)
    # except Exception as e:
    #     logging.error(f"Error while connecting to the database: {e}")
    #     sys.exit(1)
    #     cursor = connection.cursor()

    # Create a Source Dictionary That Specifies Bucket Name and Key Name of the Object to Be Copied

    connection = psycopg2.connect(user="postgres",
                                  password="mysecretpassword",
                                  host="172.17.0.3",
                                  port="5432",
                                  database="proddatabase")
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from avatars"

    cursor.execute(postgreSQL_select_Query)
    print("Selecting AWS S3 paths from table avatars")
    s3_path = cursor.fetchall()

    print("Print each row and it's columns values")
    for row in s3_path:
        copy_source = {
            'Bucket': source_bucket,
            'Key': row[1]
        }

        bucket = s3.Bucket(destination_bucket)

        bucket.copy(copy_source, row[1])

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)


# def insert_db_row(connection, path):
#     try:
#         cur = conn.cursor()
#         cur.execute("INSERT INTO avatars (path) VALUES (%s)", (path,))
#         conn.commit()
#     except Exception as e:
#         logging.error(f"Error inserting to the database: {e}")
#         sys.exit(1)


# # Creating S3 Resource From the Session.
# s3 = session.resource('s3')

# # Create a Soucre Dictionary That Specifies Bucket Name and Key Name of the Object to Be Copied
# copy_source = {
#     'Bucket': 'vini-sketch-legacy-s3',
#     'Key': 'job_done.jpg'
# }

# bucket = s3.Bucket('vini-sketch-prod-s3')

# bucket.copy(copy_source, 'job_done.jpg')

# # Printing the Information That the File Is Copied.
# print('Single File is copied')
