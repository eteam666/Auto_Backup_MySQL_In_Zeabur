import os
import subprocess
import boto3
from time import sleep
from datetime import datetime 

seconds = os.getenv("TIME")
seconds = int(seconds)

def get_current_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted_time

def backup_and_upload_to_s3():
    mysql_host = os.getenv("MYSQL_HOST")
    mysql_port = os.getenv("MYSQL_PORT")
    mysql_username = os.getenv("MYSQL_USERNAME")
    mysql_password = os.getenv("MYSQL_PASSWORD")
    mysql_database = os.getenv("MYSQL_DATABASE")
    aws_region = os.getenv("AWS_REGION")
    s3_bucket = os.getenv("S3_BUCKET_NAME")
    s3_object_key = "backup.sql"
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    s3_endpoint = os.getenv("S3_ENDPOINT")

    time_with_underscore = get_current_time()
    backup_filename = f"{time_with_underscore}_backup.sql"

    try:
        # Backup database to a local file
        cmd = f"mysqldump -h {mysql_host} -P {mysql_port} -u {mysql_username} -p{mysql_password} {mysql_database} > {backup_filename}"
        subprocess.run(cmd, shell=True, check=True)

        # Upload the backup file to S3
        s3_client = boto3.client('s3', region_name=aws_region,
                                 aws_access_key_id=aws_access_key,
                                 aws_secret_access_key=aws_secret_key,
                                 endpoint_url=s3_endpoint)
        with open(backup_filename, 'rb') as file:
            s3_client.upload_fileobj(file, s3_bucket, s3_object_key)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        cmd = ("sudo apt-get update")
        subprocess.run(cmd, shell=True, check=True)
        cmd = ("sudo apt-get install mysql-client")
        subprocess.run(cmd, shell=True, check=True)
        while True:
            print("开始上传")
            sleep(seconds)
            backup_and_upload_to_s3()
            print("上传结束")
    except KeyboardInterrupt:
        print("脚本已手动停止")

