import os
import subprocess
import boto3
from time import sleep
seconds = os.getenv("TIME")

def get_current_time():
    # 获取当前时间
    current_time = datetime.now()

    # 将空格替换为下划线
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
    s3_object_key = "backup.sql"  # 在S3中保存的对象键
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    s3_endpoint = os.getenv("S3_ENDPOINT")  # 如果使用非AWS S3服务，需要提供自定义Endpoint
    time_with_underscore = get_current_time()
    # 备份数据库到本地文件
    backup_filename = f"{time_with_underscore}_backup.sql"
    cmd = f"mysqldump -h {mysql_host} -P {mysql_port} -u {mysql_username} -p{mysql_password} {mysql_database} > {backup_filename}"
    subprocess.run(cmd, shell=True)

    # 将备份文件上传到S3
    s3_client = boto3.client('s3', region_name=aws_region,
                             aws_access_key_id=aws_access_key,
                             aws_secret_access_key=aws_secret_key,
                             endpoint_url=s3_endpoint)  # 如果使用非AWS S3服务，需要提供自定义Endpoint
    with open(backup_filename, 'rb') as file:
        s3_client.upload_fileobj(file, s3_bucket, s3_object_key)
if __name__ == "__main__":
    while True:
        print("开始上传")
        sleep(seconds)
        backup_and_upload_to_s3()
        print("上传结束")

