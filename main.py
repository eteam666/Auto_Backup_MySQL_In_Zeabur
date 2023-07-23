import os
import mysql.connector
import boto3
from datetime import datetime
import time

# MySQL数据库连接信息
mysql_host = "infra.zeabur.com"
mysql_port = "30326"
mysql_username = "root"
mysql_password = "2cQ84R1g6G7C"
mysql_database = "zhuanxian"

# AWS S3配置信息
aws_region = os.getenv("AWS_REGION")
s3_bucket = os.getenv("S3_BUCKET_NAME")
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
s3_endpoint = os.getenv("S3_ENDPOINT")

seconds = "10"
seconds = int(seconds)

def get_current_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted_time

def backup_and_upload_to_s3():
    conn = None
    try:
        # 连接到MySQL数据库
        conn = mysql.connector.connect(
            host=mysql_host,
            port=mysql_port,
            user=mysql_username,
            password=mysql_password,
            database=mysql_database,
            auth_plugin='mysql_native_password'  # 使用mysql_native_password认证插件
        )

        # 创建MySQL游标对象
        cursor = conn.cursor()
        print("导出文件中.....")
        # 获取数据库中所有表名
        cursor.execute("SHOW TABLES;")
        tables = [table[0] for table in cursor]
        time_with_underscore = get_current_time()
        backup_filename = f"{time_with_underscore}_backup.sql"
        # 执行查询，将结果写入备份文件
        with open(backup_filename, 'w') as f:
            for table in tables:
                # 获取表的创建语句
                cursor.execute(f"SHOW CREATE TABLE {table};")
                create_table_statement = cursor.fetchone()[1]
                f.write(f"{create_table_statement};\n")

                # 获取表的数据
                cursor.execute(f"SELECT * FROM {table};")
                rows = cursor.fetchall()

                # 写入表的数据
                for row in rows:
                    row_str = ', '.join(str(col) for col in row)
                    f.write(f"INSERT INTO {table} VALUES ({row_str});\n")
                f.write("\n")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"出现错误：{e}")
        # 记录错误日志
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"出现错误：{e}\n")
    finally:
        if conn:
            conn.close()
        print("数据库备份成功！")

        # 上传备份文件到S3
        s3_client = boto3.client('s3', region_name=aws_region,
                                 aws_access_key_id=aws_access_key,
                                 aws_secret_access_key=aws_secret_key,
                                 endpoint_url=s3_endpoint)

        time_with_underscore = get_current_time()
        s3_object_key = f"{time_with_underscore}_backup.sql"

        with open(backup_filename, 'rb') as file:
            s3_client.upload_fileobj(file, s3_bucket, s3_object_key)

        print("备份文件上传到S3成功！")

if __name__ == "__main__":
    try:
        while True:
            time.sleep(seconds)  # 备份间隔时间，单位为秒
            backup_and_upload_to_s3()
    except KeyboardInterrupt:
        print("脚本已手动停止")


