# Sketch Challenge

This solution was created using the tools below:

- Python3
- Python3 Libraries
- Docker
- Docker image for postgre
- AWS s3 bucket

# Installing dependencies

In order to execute the solution, you'll need to set the environment as follow:

NOTE: This was all set in a Linux Ubuntu Based distro

Install the following packages:

- postgresql-client-12
- python3
- python3-pandas
- python3-psycopg2
- docker
- aws-cli

Make sure your aws credentials are already created and set for your local user.
Assuming that you have python, docker and aws-cli already installed, run the command below for the other dependencies:

```bash
sudo apt install postgresql-client-12 python3-pandas python3-psycopg2
```

## Setting the environment

NOTE: This environment was already set so the local user would be able to execute any docker command, if this is not your case, make sure to add *sudo* before any docker command from here on.

Download the docker image for postgresql with the command below:

```bash
docker pull postgres
```

Start the docker container with the commands below:

```bash
docker run -d --name sketch -e POSTGRES_PASSWORD=mysecretpassword postgres
```

```bash
docker start sketch
```
## Set environment variables

I find it easier when dealing with local labs to use environment variables to help you set it up.
Export the variables below to help you set up the environment:

```bash
export AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCES_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<YOUR_AWS_ACCESS_KEY>
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=mysecretpassword
export POSTGRES_HOST=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' sketch)

```
NOTE:
I am using the default user *postgres* but any user with the proper read and write access to the DB should work fine.

## Create the S3 Buckets
```bash
python3 create_buckets.py
```
NOTE:
I am creating the s3 buckets with the default parameters here but I assume since we are using an *API key*, it will work as long as the API key used have the proper rights to do that (In this case, admin access).

## Upload sample images to the S3 bucket
```bash
python3 upload_files.py
```

## Create and Populate the postgresql database

```bash
psql -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -c 'create database proddatabase'       
psql -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -d proddatabase < proddatabase.txt

```
## Upload the sample images to prod-s3 bucket and update the DB
```bash
python3 s3_copy.py
```

The script should show you the list of files copied to the S3, the old and new DataBase entries as well.

## Deleting S3 Buckets

Once you done, don't forget to delete the resources to avoid unwanted billing

```bash
aws s3 rb s3://vini-sketch-legacy-s3 --force
aws s3 rb s3://vini-sketch-prod-s3 --force
```

## Removing Docker Image and Container

```bash
docker stop sketch
docker rm <DOCKER_CONTAINER_ID>
docker rmi -f postgres
```