"""
API References: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
"""
import base64
import json
import os.path
from hashlib import md5
from pathlib import Path
from typing import Iterator, Any, List

import boto3
from boto3.resources.base import ServiceResource
from boto3.resources.model import Collection
from boto3.s3.transfer import TransferConfig
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from botocore.response import StreamingBody

from config import settings

PART_SIZE_DEFAULT = 8 * 1024 * 1024  # 8MiB
DEFAULT_CHUNK_SIZE = 4 * 1024  # 4iB


def get_resource(endpoint: str,
                 access_key: str,
                 secret_key: str,
                 secure: bool = False,
                 region: str = None, ) -> ServiceResource:
    """
    获取链接
    """
    return boto3.resource(service_name='s3',
                          region_name=region,
                          verify=secure,
                          endpoint_url=endpoint,
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key, )


def get_client(endpoint: str,
               access_key: str,
               secret_key: str,
               secure: bool = False,
               region: str = None, ) -> BaseClient:
    """
    获取链接
    """
    return boto3.client(service_name='s3',
                        region_name=region,
                        verify=secure,
                        endpoint_url=endpoint,
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key, )


def create_bucket(client: ServiceResource, bucket_name: str, region: str = None) -> dict:
    """
    创建桶
    """
    config = {}
    if region:
        config.update(LocationConstraint=region)
    return client.Bucket(bucket_name).create(ACL='private', CreateBucketConfiguration=config)


def delete_bucket(client: ServiceResource, bucket_name: str, force: bool = False) -> List[dict]:
    """
    删除桶

    """
    if not exists_bucket(client=client, bucket_name=bucket_name):
        return []
    # delete object
    if force:
        res = client.Bucket(bucket_name).objects.delete()
        if res and 'Errors' in res[0]:
            return res[0]["Errors"]
    client.Bucket(bucket_name).delete()


def exists_bucket(client: ServiceResource, bucket_name: str) -> bool:
    """
    桶是否存在
    """
    try:
        client.meta.client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == '404':
            return False
        raise


def list_objects(client: ServiceResource, bucket_name: str,
                 prefix: str = '', start_after: str = '', **kwargs) -> Collection:
    """
    对象列表
    """
    return client.Bucket(bucket_name).objects.filter(Prefix=prefix, Marker=start_after)


def put_object(client: ServiceResource, bucket_name: str, object_name: str,
               data=None, length: int = 0, content_type: str = '', content_md5: str = '',
               **kwargs):
    """
    上传对象
    """
    params = {}
    if content_md5:
        params.update(ContentMD5=content_md5)
    if length:
        params.update(ContentLength=length)
    if data:
        params.update(Body=data)
    if content_type:
        params.update(ContentType=content_type)
    return client.Bucket(bucket_name).put_object(Key=object_name, **params)


def exists_object(client: ServiceResource, bucket_name: str, object_name: str, **kwargs) -> bool:
    """
    对象状态
    """
    try:
        client.meta.client.head_object(Bucket=bucket_name, Key=object_name)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == '404':
            return False
        raise


def remove_objects(client: ServiceResource, bucket_name: str, objects: list) -> dict:
    """
    删除对象
    """
    obj_list = list(map(lambda x: {"Key": x}, filter(lambda o: o, objects)))
    return client.Bucket(bucket_name).delete_objects(Delete={"Objects": obj_list, "Quiet": True})


def get_object(client: ServiceResource, bucket_name: str, object_name: str,
               offset: int = 0, length: int = 0, content_type: str = '', **kwargs) -> dict:
    """
    获取对象
    """
    params = {}
    # range
    rang = f'bytes={offset}-'
    if length:
        rang += f'{offset + length - 1}'
    params.update(Range=rang)
    if content_type:
        params.update(ResponseContentType=content_type)
    return client.Bucket(bucket_name).Object(object_name).get(**params)


def get_stream(client: ServiceResource, bucket_name: str, object_name: str,
               offset: int = 0, length: int = 0, amt: int = DEFAULT_CHUNK_SIZE, **kwargs) -> Iterator[bytes]:
    """
    获取对象流
    """
    resp_body: StreamingBody = None
    try:
        resp = get_object(client=client, bucket_name=bucket_name, object_name=object_name,
                          offset=offset, length=length)
        resp_body = resp["Body"]
        resp_data = resp_body.iter_chunks(chunk_size=amt)
        for data in resp_data:
            yield data
    finally:
        if resp_body:
            resp_body.close()


def get_data(client: ServiceResource, bucket_name: str, object_name: str,
             offset: int = 0, length: int = 0, **kwargs) -> bytes:
    """
    获取对象数据
    """
    resp_body: StreamingBody = None
    try:
        resp = get_object(client=client, bucket_name=bucket_name, object_name=object_name,
                          offset=offset, length=length)
        resp_body = resp["Body"]
        return resp_body.read()
    finally:
        if resp_body:
            resp_body.close()


def get_json(client: ServiceResource, bucket_name: str, object_name: str, **kwargs) -> Any:
    """
    获取json数据
    """
    data = get_data(client=client, bucket_name=bucket_name, object_name=object_name, )
    if not data:
        return None
    return json.loads(data.decode('utf-8'))


def upload_file(client: ServiceResource, bucket_name: str, object_name: str, file_path: str,
                content_type: str = "application/octet-stream",
                part_size: int = PART_SIZE_DEFAULT, **kwargs):
    """
    上传文件
    """
    extra = {}
    if content_type:
        extra.update(ContentType=content_type)
    config = TransferConfig()
    if part_size:
        config.multipart_chunksize = part_size
    client.Bucket(bucket_name).Object(object_name).upload_file(Filename=file_path, ExtraArgs=extra, Config=config)


def download_file(client: ServiceResource, bucket_name: str, object_name: str, file_path: str = None,
                  part_size: int = PART_SIZE_DEFAULT, **kwargs):
    """
    下载文件
    """
    if not file_path:
        file_path = Path(object_name).name
    config = TransferConfig()
    if part_size:
        config.multipart_chunksize = part_size
    client.Bucket(bucket_name).Object(object_name).download_file(Filename=file_path, Config=config)


def get_upload_url(client: ServiceResource, bucket_name: str, object_name: str, seconds: int = 3600, **kwargs) -> dict:
    """
    获取上传文件的URL
    """
    return client.meta.client.generate_presigned_post(Bucket=bucket_name, Key=object_name, ExpiresIn=seconds, )


def get_download_url(client: ServiceResource, bucket_name: str, object_name: str, seconds: int = 3600, **kwargs) -> str:
    """
    获取下载文件的URL
    """
    return client.meta.client.generate_presigned_url(ClientMethod='get_object',
                                                     Params={"Bucket": bucket_name, "Key": object_name},
                                                     ExpiresIn=seconds,
                                                     HttpMethod='GET', )


def upload_folder(client: ServiceResource, bucket_name: str, from_path: str, target: str = None, **kwargs):
    """
    上传文件
    """
    if not os.path.isdir(from_path):
        raise RuntimeError(f"Folder Path is Invalid: {from_path}")
    # 创建目录
    folder_name = target
    if not folder_name:
        folder_name = Path(from_path).name
    to_root = folder_name in ['.', '/', './']
    if not to_root:
        put_object(client=client, bucket_name=bucket_name, object_name=folder_name + '/')
    # 遍历目录
    for chd in os.listdir(from_path):
        chd_path = os.path.join(from_path, chd)
        object_name = chd if to_root else f'{folder_name}/{chd}'
        if os.path.isdir(chd_path):
            upload_folder(client=client, bucket_name=bucket_name, from_path=chd_path, target=object_name)
        else:
            upload_file(client=client, bucket_name=bucket_name, object_name=object_name, file_path=chd_path)


def object_md5(obj) -> str:
    """
    计算md5值
    """
    data_hash = md5()
    if hasattr(obj, 'read'):
        while True:
            data = obj.read(4096)
            if not data:
                break
            data_hash.update(data)
    else:
        data_hash.update(obj)
    return base64.b64encode(data_hash.digest()).decode('utf-8')


def object_len(obj) -> int:
    """
    计算内容长度
    """
    length = 0
    if hasattr(obj, 'read'):
        while True:
            data = obj.read(4096)
            if not data:
                break
            length += len(data)
    else:
        length = len(obj)
    return length


def __is_success__(resp: dict):
    if resp and 'ResponseMetadata' in resp:
        return resp["ResponseMetadata"]["HTTPStatusCode"] == 200
    return False


oss_resource = get_resource(endpoint=settings.oss_endpoint,
                            access_key=settings.oss_access_key,
                            secret_key=settings.oss_secret_key,
                            region=settings.oss_region,
                            secure=settings.oss_secure)

oss_client = get_client(endpoint=settings.oss_endpoint,
                        access_key=settings.oss_access_key,
                        secret_key=settings.oss_secret_key,
                        region=settings.oss_region,
                        secure=settings.oss_secure)

S3_CLIENT = {
    "create_bucket": create_bucket,
    "delete_bucket": delete_bucket,
    "download_file": download_file,
    "exists_bucket": exists_bucket,
    "exists_object": exists_object,
    "get_data": get_data,
    "get_download_url": get_download_url,
    "get_json": get_json,
    "get_object": get_object,
    "get_stream": get_stream,
    "get_upload_url": get_upload_url,
    "list_objects": list_objects,
    "remove_objects": remove_objects,
    "upload_file": upload_file,
    "upload_folder": upload_folder,
}
