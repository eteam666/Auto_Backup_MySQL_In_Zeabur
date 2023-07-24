# 在Zeabur上临时的MySQL自动备份工具
# 在Zeabur中部署
[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://dash.zeabur.com/templates/FNGH21)
## 安全起见，所有数据需要**添加到变量**
## 变量们
* MYSQL_DATABASE：数据库名称
* AWS_ACCESS_KEY_ID:访问密钥 ID(Access Key ID)
* AWS_SECRET_ACCESS_KEY：秘密访问密钥（秘密访问密钥）
* AWS_REGION：CloudFlare R2如果是自动的写"auto"，自己选择的请参考[文档的Hint](https://developers.cloudflare.com/r2/buckets/data-location/#location-hints)
* S3_BUCKET_NAME：存储桶名称
* S3_ENDPOINT:存储桶端点
* SECONDS:自动备份的时间（单位：秒）
## **填写完后记得Redeploy**
