# We start this script by important the module boto3
import boto3
import json

#If the file ~/.aws/credentials is not properly configured, insert the credentials here
#Since the session is established using the credentials, get a S3 resouce
s3 = boto3.resource('s3')

# Set a bucket name
bucket_name = "stc.web.com"

# Create a new S3 bucket, using the bucket name declared as a variable
s3.create_bucket(Bucket=bucket_name)


# We need to set an S3 policy for our bucket to
# allow anyone read access to our bucket and files.
# If we do not set this policy, people will not be
# able to view our S3 static web site.
bucket_policy = s3.BucketPolicy(bucket_name)
access = {
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "Allow Public Access to All Objects",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::stc.web.com/*"
  }
  ]
}

# Add the policy to the bucket
apply_policy = bucket_policy.put(Policy=json.dumps(access))


# Next we'll set a basic configuration for the static
# website.
website_config = {
    'ErrorDocument': {
        'Key': 'error.html'
    },
    'IndexDocument': {
        'Suffix': 'index.html'
    }
}

# Make our new S3 bucket a static website
bucket_website = s3.BucketWebsite(bucket_name)

# And configure the static website with our desired index.html
# and error.html configuration.
bucket_website.put(WebsiteConfiguration=website_config)

# Adding the contents for the index.html file
content = ("<html><head><title>Automation for people</title></head>"
           "<body><h1>Automation for people</h1></body></html>")

# Create the index.html page in S3
s3.Object(bucket_name, 'index.html').put(Body=content, ContentType='text/html')

# Adding the contents for the error.html file
content_error = ("<html><head><title>Automation for people</title></head>"
           "<body><h1>Automation for people</h1><h2>ERROR!!</h2></body></html>")

# Create the index.html page in S3
s3.Object(bucket_name, 'error.html').put(Body=content_error, ContentType='text/html')
