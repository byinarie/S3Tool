#!/usr/bin/env python3
import boto3
import botocore.exceptions
import click

@click.command()
@click.option('--access_key', prompt='AWS access key', help='Your AWS access key.')
@click.option('--secret_key', prompt='AWS secret key', help='Your AWS secret key.')
@click.option('--region', default='us-east-1', help='AWS region.')
@click.option('--help', is_flag=True, help='Displays help information.')


def check_s3_issues(access_key, secret_key, region, help):
    s3 = boto3.client('s3',
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key,
                      region_name=region)

    # Get list of buckets
    buckets = s3.list_buckets()

    if 'Buckets' in buckets and len(buckets['Buckets']) > 0:
        print("Confirmed credentials are valid.")
    else:
        print("No S3 buckets were found using given credentials.")

    if 'Buckets' in buckets and len(buckets['Buckets']) > 0:
        # Check for versioning
        for bucket in buckets['Buckets']:
            versioning = s3.get_bucket_versioning(Bucket=bucket['Name'])
            if 'Status' in versioning and versioning['Status'] != 'Enabled':
                print(f'Bucket -> {bucket["Name"]} — Should have versioning enabled.')

        # Check for access logging
        for bucket in buckets['Buckets']:
            logging = s3.get_bucket_logging(Bucket=bucket['Name'])
            if not logging or 'LoggingEnabled' not in logging:
                print(f'Bucket -> {bucket["Name"]} — Should have server access logging enabled.')

        # Check for default encryption
        for bucket in buckets['Buckets']:
            encryption = s3.get_bucket_encryption(Bucket=bucket['Name'])
            if not encryption or 'Rules' not in encryption:
                print(f'Bucket -> {bucket["Name"]} — Should have default encryption enabled.')

        # Check for MFA delete
        for bucket in buckets['Buckets']:
            mfa_delete = s3.get_bucket_versioning(Bucket=bucket['Name'])
            if 'MFADelete' in mfa_delete and mfa_delete['MFADelete'] != 'Enabled':
                print(f'Bucket -> {bucket["Name"]} — Should have MFA delete enabled.')
        try:
            for bucket in buckets['Buckets']:
        # Get the replication configuration for the object
                replication_config = s3.get_bucket_replication(Bucket=bucket['Name'])

        # Check if object-level replication is enabled
            if 'ReplicationRule' in replication_config:
                print(f'Object-level replication is enabled for object: {obj["Key"]}')
            else:
                print(f'Object-level replication is not enabled for object: {obj["Key"]}')
        except botocore.exceptions.ClientError as error:
            print(f'Bucket -> {bucket["Name"]} — Should have have object-level replication enabled.')


        # Bug in check bucket policy

        # for bucket in buckets['Buckets']:
        #     policy = s3.get_bucket_policy(Bucket=bucket['Name'])
        #     if 'Policy' in policy:
        #         print(f'Bucket {bucket["Name"]}: has a bucket-level policy.')
        #     else:
        #         print(f'Bucket {bucket["Name"]}: does not have a bucket-level policy.')

# Bug in check for public access

        # # Check for public access blocked
        # for bucket in buckets['Buckets']:
        #     public_access = s3.get_public_access_block(Bucket=bucket['Name'])
        #     if 'BlockPublicAcls' in public_access and public_access['BlockPublicAcls'] != True:
        #         print(f'Bucket {bucket["Name"]}: should have public access blocked')

    # else:
    #     print("Could not find any buckets using provided credentials.")

if __name__ == '__main__':
    check_s3_issues()
