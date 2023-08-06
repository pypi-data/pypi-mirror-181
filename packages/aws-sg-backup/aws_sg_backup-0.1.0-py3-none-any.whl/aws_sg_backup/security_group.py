import json
from enum import Enum

import boto3

ec2 = boto3.resource("ec2")
ec2client = boto3.client("ec2")
s3 = boto3.client("s3")


class Backup(Enum):
    LOCAL = 1
    S3 = 2


def backup_security_group(security_group_id, backup_path, backup_type=Backup.LOCAL):
    """
    Backup security group in JSON format to local file or S3 bucket.

    :param security_group_id: security group id
    :param backup_type: Backup.LOCAL or Backup.S3
    :param backup_path: local file path or S3 bucket path (e.g. bucket_name/path/to/dir)
    """
    if not security_group_id:
        raise ValueError("security_group_id is required")
    if not backup_path:
        raise ValueError("backup_path is required")
    if not backup_type or backup_type not in Backup:
        raise ValueError(
            f"backup_type is required and must be one of {Backup.LOCAL} or {Backup.S3}"
        )

    stored_sgs = set()
    return _backup_security_group(
        security_group_id, backup_type, backup_path, stored_sgs
    )


def restore_security_group(security_group_id, backup_path, backup_type=Backup.LOCAL):
    """
    Restore security group from JSON backup located in local file or S3 bucket.

    :param security_group_id: security group id
    :param backup_type: Backup.LOCAL or Backup.S3
    :param backup_path: local file path or S3 bucket path (e.g. bucket_name/path/to/dir)
    """
    if not security_group_id:
        raise ValueError("security_group_id is required")
    if not backup_path:
        raise ValueError("backup_path is required")
    if not backup_type or backup_type not in Backup:
        raise ValueError(
            f"backup_type is required and must be one of {Backup.LOCAL} or {Backup.S3}"
        )

    restored_sgs = {}
    return _restore_security_group(
        backup_type, backup_path, security_group_id, restored_sgs
    )


def _backup_security_group(security_group_id, backup_type, backup_path, stored_sgs):
    if security_group_id in stored_sgs:
        return None
    stored_sgs.add(security_group_id)
    security_group = _describe_security_group(security_group_id)
    for sg in security_group["inbound_rules"]:
        for user_id_group_pair in sg["UserIdGroupPairs"]:
            if (
                "GroupId" in user_id_group_pair
                and user_id_group_pair["GroupId"] != "SELF_REFERENCE"
            ):
                _backup_security_group(
                    user_id_group_pair["GroupId"], backup_type, backup_path, stored_sgs
                )
    for sg in security_group["outbound_rules"]:
        for user_id_group_pair in sg["UserIdGroupPairs"]:
            if (
                "GroupId" in user_id_group_pair
                and user_id_group_pair["GroupId"] != "SELF_REFERENCE"
            ):
                _backup_security_group(
                    user_id_group_pair["GroupId"], backup_type, backup_path, stored_sgs
                )
    sg_description = json.dumps(security_group, indent=2)
    if backup_type == Backup.LOCAL:
        path = f"{backup_path}/{security_group_id}.json"
        with open(path, "w") as f:
            f.write(sg_description)
    elif backup_type == Backup.S3:
        path = f"s3://{backup_path}/{security_group_id}.json"
        bucket_name = backup_path.split("/")[0]
        key = backup_path[len(bucket_name) + 1 :]
        s3.put_object(
            Body=sg_description,
            Bucket=bucket_name,
            Key=f"{key}/{security_group_id}.json",
        )
    return path


def _restore_security_group(backup_type, backup_dir, security_group_id, restored_sgs):
    sg_description = _load_security_group_description(
        backup_type, backup_dir, security_group_id
    )
    security_group = ec2.create_security_group(
        GroupName=sg_description["name"],
        Description=sg_description["description"],
        VpcId=sg_description["vpc_id"],
    )
    restored_sgs[security_group_id] = security_group.id
    security_group.revoke_egress(IpPermissions=security_group.ip_permissions_egress)
    ingress_rules = _verify_and_restore_ip_permissions(
        sg_description["inbound_rules"],
        security_group.id,
        backup_type,
        backup_dir,
        restored_sgs,
    )
    if ingress_rules:
        security_group.authorize_ingress(IpPermissions=ingress_rules)
    egress_rules = _verify_and_restore_ip_permissions(
        sg_description["outbound_rules"],
        security_group.id,
        backup_type,
        backup_dir,
        restored_sgs,
    )
    if egress_rules:
        security_group.authorize_egress(IpPermissions=egress_rules)
    if sg_description["tags"] is not None:
        security_group.create_tags(Tags=sg_description["tags"])
    return security_group


def _is_security_group_exists(security_group_id):
    try:
        resp = ec2client.describe_security_groups(GroupIds=[security_group_id])
        return len(resp["SecurityGroups"]) > 0
    except Exception:
        return False


def _verify_and_restore_ip_permissions(
    ip_permissions, security_group_id, backup_type, backup_dir, restored_sgs
):
    verified = []
    for ip_permission in ip_permissions:
        include_permission = True
        if "UserIdGroupPairs" in ip_permission:
            for user_id_group_pair in ip_permission["UserIdGroupPairs"]:
                if "GroupId" in user_id_group_pair:
                    group_id = user_id_group_pair["GroupId"]
                    if group_id in restored_sgs:
                        user_id_group_pair["GroupId"] = restored_sgs[group_id]
                    elif not _is_security_group_exists(group_id):
                        print(
                            f"WARNING: Security group {group_id} referenced by {security_group_id} "
                            f"no longer exists. Trying to restore it from backup..."
                        )
                        try:
                            restored_sg = _restore_security_group(
                                backup_type, backup_dir, group_id, restored_sgs
                            )
                            user_id_group_pair["GroupId"] = restored_sg.id
                            print(
                                f"Security group {group_id} successfully restored with new id {restored_sg.id}"
                            )
                        except Exception as e:
                            print(
                                f"ERROR: Failed to restore security group {group_id} referenced by {security_group_id}: {e}. "
                                f"Corresponding rule will be skipped."
                            )
                            include_permission = False
                            continue
        if include_permission:
            verified.append(ip_permission)

    return verified


def _describe_security_group(security_group_id):
    security_group = ec2.SecurityGroup(security_group_id)
    return {
        "id": security_group.id,
        "name": security_group.group_name,
        "description": security_group.description,
        "vpc_id": security_group.vpc_id,
        "inbound_rules": security_group.ip_permissions,
        "outbound_rules": security_group.ip_permissions_egress,
        "tags": security_group.tags,
    }


def _load_security_group_description(backup_type, backup_dir, security_group_id):
    if backup_type == Backup.LOCAL:
        backup_path = f"{backup_dir}/{security_group_id}.json"
        with open(backup_path, "r") as f:
            sg_description = json.loads(f.read())
    elif backup_type == Backup.S3:
        bucket = backup_dir.split("/")[0]
        key = f"{backup_dir[len(bucket) + 1:]}/{security_group_id}.json"
        sg_description = json.loads(
            s3.get_object(Bucket=bucket, Key=key)["Body"].read()
        )
    return sg_description
