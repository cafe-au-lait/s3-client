import os
import sys

import typer

from config import settings
from sss import S3_CLIENT, oss_resource

app = typer.Typer()

# Remove '' and current working directory from the first entry
# of sys.path, if present to avoid using current directory
# in pip commands check, freeze, install, list and show,
# when invoked as python -m pip <command>
if sys.path[0] in ("", os.getcwd()):
    sys.path.pop(0)

# If we are running from a wheel, add the wheel to sys.path
# This allows the usage python pip-*.whl/pip install pip-*.whl
if __package__ == "":
    # __file__ is pip-*.whl/pip/__main__.py
    # first dirname call strips of '/__main__.py', second strips off '/pip'
    # Resulting path is the name of the wheel itself
    # Add that to sys.path so we can import pip
    _path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, _path)


@app.command()
def create_bucket(bucket: str, region: str = None):
    """
    创建桶
    :param bucket: 桶
    :param region: 区域
    :return:
    """
    print(S3_CLIENT["create_bucket"](client=oss_resource, bucket_name=bucket, region=region))


@app.command()
def delete_bucket(bucket: str, force: bool = False):
    """
    删除桶
    :param bucket: 桶
    :param force: 强制
    :return:
    """
    print(S3_CLIENT["delete_bucket"](client=oss_resource, bucket_name=bucket, force=force))


@app.command()
def exists_bucket(bucket: str) -> bool:
    """
    桶是否存在
    :param bucket: 桶
    :return:
    """
    print(S3_CLIENT["exists_bucket"](client=oss_resource, bucket_name=bucket))


@app.command()
def list_objects(bucket: str = settings.oss_bucket, prefix: str = '', start: str = ''):
    """
    对象列表
    :param bucket: 桶
    :param prefix: 前缀
    :param start: 起始对象名称
    :return:
    """
    obj_list = S3_CLIENT["list_objects"](client=oss_resource, bucket_name=bucket,
                                         prefix=prefix, start_after=start)
    for obj in obj_list:
        print(obj.key)


@app.command()
def exists_object(object_name: str, bucket: str = settings.oss_bucket):
    """
    查询对象状态
    :param bucket: 桶
    :param object_name: 对象名称
    :return:
    """
    print(S3_CLIENT["exists_object"](client=oss_resource, bucket_name=bucket, object_name=object_name))


@app.command()
def remove_object(object_name: str, bucket: str = settings.oss_bucket, ):
    """
    删除对象
    :param bucket: 桶
    :param object_name: 对象名称
    :return:
    """
    print(S3_CLIENT["remove_objects"](client=oss_resource, bucket_name=bucket, objects=[object_name]))


@app.command()
def get_data(object_name: str, bucket: str = settings.oss_bucket, offset: int = 0, length: int = 0):
    """
    获取对象数据
    :param bucket: 桶
    :param object_name: 对象名称
    :param offset: 起始位置
    :param length: 长度
    :return:
    """
    data = S3_CLIENT["get_data"](client=oss_resource, bucket_name=bucket, object_name=object_name,
                                 offset=offset, length=length)
    if not data:
        print('Object Not Found')
    print(data.decode('utf-8'))


@app.command()
def get_json(object_name: str, bucket: str = settings.oss_bucket):
    """
    获取json数据
    :param bucket: 桶
    :param object_name: 对象名称
    :return:
    """
    print(S3_CLIENT["get_json"](client=oss_resource, bucket_name=bucket, object_name=object_name))


@app.command()
def upload_file(object_name: str, path: str,
                bucket: str = settings.oss_bucket,
                content_type: str = typer.Option("application/octet-stream"), ):
    """
    上传文件
    :param bucket: 桶
    :param object_name: 对象名称
    :param path: 文件路径
    :param content_type: 类型
    :return:
    """
    print(S3_CLIENT["upload_file"](client=oss_resource, bucket_name=bucket,
                                   object_name=object_name, file_path=path, content_type=content_type))


@app.command()
def download_file(object_name: str, path: str = None, bucket: str = settings.oss_bucket, ):
    """
    下载文件
    :param bucket: 桶
    :param object_name: 对象名称
    :param path: 文件路径
    :return:
    """
    print(S3_CLIENT["download_file"](client=oss_resource, bucket_name=bucket,
                                     object_name=object_name, file_path=path))


@app.command()
def get_upload_url(object_name: str, bucket: str = settings.oss_bucket, seconds: int = 3600):
    """
    获取上传文件的URL
    :param bucket: 桶
    :param object_name: 对象名称
    :param seconds: 有效时长(秒)
    :return:
    """
    print(S3_CLIENT["get_upload_url"](client=oss_resource, bucket_name=bucket,
                                      object_name=object_name, seconds=seconds))


@app.command()
def get_download_url(object_name: str, bucket: str = settings.oss_bucket, seconds: int = 3600):
    """
    获取下载文件的URL
    :param bucket: 桶
    :param object_name: 对象名称
    :param seconds: 有效时长(秒)
    :return:
    """
    print(S3_CLIENT["get_download_url"](client=oss_resource, bucket_name=bucket,
                                        object_name=object_name, seconds=seconds))


@app.command()
def upload_folder(path: str, bucket: str = settings.oss_bucket, target: str = None):
    """
    上传文件夹
    :param bucket: 桶
    :param path: 本地文件夹路径
    :param target: 目标文件夹名称
    :return:
    """
    print(S3_CLIENT["upload_folder"](client=oss_resource, bucket_name=bucket,
                                     from_path=path, target=target))


if __name__ == '__main__':
    app()
