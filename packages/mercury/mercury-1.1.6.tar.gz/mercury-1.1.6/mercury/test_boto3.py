import boto3
#s3 = boto3.resource('s3')
#for bucket in s3.buckets.all():
#    print(bucket.name)

s3 = boto3.client("s3")
s3.upload_file("index.html", "mercury-public-bucket", "index.html",
            ExtraArgs={
                #'ACL': 'public-read', 
                "ContentType": "text/html"
            })

