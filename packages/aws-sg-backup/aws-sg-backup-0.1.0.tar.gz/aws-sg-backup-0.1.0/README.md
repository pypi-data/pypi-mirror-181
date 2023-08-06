# AWS Security Group Backup

AWS Security Group Backup is a tiny library that allows to backup and restore AWS security groups. It may be useful 
if you want to delete security groups that are not used, but you want to have a backup in case you need to restore them.

If security group references other security groups, then they will be also backed up.
On restore, if some referenced security group is not found, then it will be restored.

Library doesn't restore security group IDs, so you need to update your environment to use new security group IDs.

## Installation

`pip install aws-sg-backup`

## Required IAM permissions

To use this library, you need to have the following IAM permissions:
* `ec2:DescribeSecurityGroups`
* `ec2:CreateSecurityGroup`
* `ec2:AuthorizeSecurityGroupIngress`
* `ec2:AuthorizeSecurityGroupEgress`
* `ec2:RevokeSecurityGroupEgress`
* `s3:PutObject`
* `s3:GetObject

## Usage

Library provides two functions: `backup_security_group` and `restore_security_group`. Both functions take the following arguments:
 * `security_group_id` - ID of the security group to backup or restore
 * `backup_path` - local file path or S3 bucket path (e.g. bucket_name/path/to/dir). Depends on `backup_target` argument.
 * `backup_target` - backup target. Can be either `Backup.S3` or `Backup.LOCAL`. If `Backup.S3` is specified, 
    backup will be created in S3 bucket. If `Backup.LOCAL` is specified, backup will be stored in the local file system.