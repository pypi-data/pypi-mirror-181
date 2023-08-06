# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_sg_backup']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.25,<2.0.0']

setup_kwargs = {
    'name': 'aws-sg-backup',
    'version': '0.1.0',
    'description': 'Backup and restore AWS security groups as local files or to S3',
    'long_description': "# AWS Security Group Backup\n\nAWS Security Group Backup is a tiny library that allows to backup and restore AWS security groups. It may be useful \nif you want to delete security groups that are not used, but you want to have a backup in case you need to restore them.\n\nIf security group references other security groups, then they will be also backed up.\nOn restore, if some referenced security group is not found, then it will be restored.\n\nLibrary doesn't restore security group IDs, so you need to update your environment to use new security group IDs.\n\n## Installation\n\n`pip install aws-sg-backup`\n\n## Required IAM permissions\n\nTo use this library, you need to have the following IAM permissions:\n* `ec2:DescribeSecurityGroups`\n* `ec2:CreateSecurityGroup`\n* `ec2:AuthorizeSecurityGroupIngress`\n* `ec2:AuthorizeSecurityGroupEgress`\n* `ec2:RevokeSecurityGroupEgress`\n* `s3:PutObject`\n* `s3:GetObject\n\n## Usage\n\nLibrary provides two functions: `backup_security_group` and `restore_security_group`. Both functions take the following arguments:\n * `security_group_id` - ID of the security group to backup or restore\n * `backup_path` - local file path or S3 bucket path (e.g. bucket_name/path/to/dir). Depends on `backup_target` argument.\n * `backup_target` - backup target. Can be either `Backup.S3` or `Backup.LOCAL`. If `Backup.S3` is specified, \n    backup will be created in S3 bucket. If `Backup.LOCAL` is specified, backup will be stored in the local file system.",
    'author': 'Vassili Gorshkov',
    'author_email': 'vassili.gorshkov@atlasgurus.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
