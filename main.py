import os
import mysql.connector
import boto3
from datetime import datetime

# MySQL数据库连接信息
mysql_host = os.getenv("MYSQL_HOST")
mysql_port = os.getenv("MYSQL_PORT")
mysql_username = os.getenv("MYSQL_USERNAME")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_database = os.getenv("MYSQL_DATABASE")


# AWS S3配置信息
aws_region = os.getenv("AWS_REGION")
s3_bucket = os.getenv("S3_BUCKET_NAME")
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
s3_endpoint = os.getenv("S3_ENDPOINT")

def get_current_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted_time

def backup_and_upload_to_s3():
    try:
        # 连接到MySQL数据库
        conn = mysql.connector.connect(
            host=mysql_host,
            port=mysql_port,
            user=mysql_username,
            password=mysql_password,
            database=mysql_database
        )

        # 创建MySQL游标对象
        cursor = conn.cursor()

        # 获取数据库中所有表名
        cursor.execute("SHOW TABLES;")
        tables = [table[0] for table in cursor]
        time_with_underscore = get_current_time()
        backup_filename = f"{time_with_underscore}_backup.sql"
        # 执行查询，将结果写入备份文件
        with open(backup_file, 'w') as f:
            for table in tables:
                cursor.execute(f"SELECT * FROM {table};")
                rows = cursor.fetchall()

                # 写入表名和数据
                f.write(f"TABLE: {table}\n")
                for row in rows:
                    row_str = ', '.join(str(col) for col in row)
                    f.write(f"{row_str}\n")
                f.write("\n")

        print("数据库备份成功！")

        # 上传备份文件到S3
        s3_client = boto3.client('s3', region_name=aws_region,
                                 aws_access_key_id=aws_access_key,
                                 aws_secret_access_key=aws_secret_key,
                                 endpoint_url=s3_endpoint)

        time_with_underscore = get_current_time()
        s3_object_key = f"{time_with_underscore}_backup.sql"

        with open(backup_file, 'rb') as file:
            s3_client.upload_fileobj(file, s3_bucket, s3_object_key)

        print("备份文件上传到S3成功！")
    except Exception as e:
        print(f"出现错误：{e}")
    finally:
        # 关闭数据库连接
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    try:
        while True:
            print("开始上传")
            sleep(3600)  # 备份间隔时间，单位为秒
            backup_and_upload_to_s3()
            print("上传结束")
    except KeyboardInterrupt:
        print("脚本已手动停止")


