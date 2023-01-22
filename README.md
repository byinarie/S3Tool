# S3Tool
Checks for common misconfigurations in AWS S3.

## Get AWS Secret + Access Key

https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html

## Installation

```bash
git clone https://github.com/byinarie/S3Tool.git
pip3 install -r requirements.txt

or

pip3 install boto3 && pip3 install botocore && pip3 install click
```

## Currently checks for
Versioning
Access Logging
Encryption
MFA Delete
Object Level Replication

## TODO
Bucket Policy
Public Access

## Usage/Examples

```

python3 S3Tool.py --access_key KEY --secret_key SECRET
Confirmed credentials are valid.
Bucket -> TestingBucket — Should have server access logging enabled.
Bucket -> TestingBucket — Should have default encryption enabled.
Bucket -> TestingBucket — Should have have object-level replication enabled.

```
