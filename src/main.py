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
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)


@app.command()
def create_bucket(bucket_name: str, region: str = None):
    """
    创建桶
    :param bucket_name: 桶
    :param region: 区域
    :return:
    """
    print(S3_CLIENT["create_bucket"](oss_resource, bucket_name, region))


@app.command()
def delete_bucket(bucket_name: str, force: bool = False):
    """
    删除桶
    :param bucket_name: 桶
    :param force: 强制
    :return:
    """
    print(S3_CLIENT["delete_bucket"](oss_resource, bucket_name, force))


@app.command()
def exists_bucket(bucket_name: str) -> bool:
    """
    桶是否存在
    :param bucket_name: 桶
    :return:
    """
    print(S3_CLIENT["exists_bucket"](oss_resource, bucket_name))


@app.command()
def list_objects(bucket_name: str = settings.oss_bucket,
                 prefix: str = '',
                 start_after: str = ''):
    """
    对象列表
    :param bucket_name: 桶
    :param prefix: 前缀
    :param start_after: 起始对象名称
    :return:
    """
    obj_list = S3_CLIENT["list_objects"](oss_resource, bucket_name, prefix, start_after)
    for obj in obj_list:
        print(obj.key)


@app.command()
def exists_object(object_name: str,
                  bucket_name: str = settings.oss_bucket):
    """
    查询对象状态
    :param bucket_name: 桶
    :param object_name: 对象名称
    :return:
    """
    print(S3_CLIENT["exists_object"](oss_resource, bucket_name, object_name))


@app.command()
def remove_objects(obj1: str,
                   obj2: str = None,
                   obj3: str = None,
                   obj4: str = None,
                   obj5: str = None,
                   bucket_name: str = settings.oss_bucket, ):
    """
    删除对象
    :param bucket_name: 桶
    :param obj1: 对象名称
    :param obj2: 对象名称
    :param obj3: 对象名称
    :param obj4: 对象名称
    :param obj5: 对象名称
    :return:
    """
    print(S3_CLIENT["remove_objects"](oss_resource, bucket_name, obj1, obj2, obj3, obj4, obj5))


@app.command()
def get_data(object_name: str,
             bucket_name: str = settings.oss_bucket,
             offset: int = 0, length: int = 0):
    """
    获取对象数据
    :param bucket_name: 桶
    :param object_name: 对象名称
    :param offset: 起始位置
    :param length: 长度
    :return:
    """
    data = S3_CLIENT["get_data"](oss_resource, bucket_name, object_name, offset, length)
    if not data:
        print('Object Not Found')
    print(data.decode('utf-8'))


@app.command()
def get_json(object_name: str,
             bucket_name: str = settings.oss_bucket):
    """
    获取json数据
    :param bucket_name: 桶
    :param object_name: 对象名称
    :return:
    """
    print(S3_CLIENT["get_json"](oss_resource, bucket_name, object_name))


@app.command()
def upload_file(object_name: str,
                file_path: str,
                bucket_name: str = settings.oss_bucket,
                content_type: str = typer.Option("application/octet-stream"), ):
    """
    上传文件
    :param bucket_name: 桶
    :param object_name: 对象名称
    :param file_path: 文件路径
    :param content_type: 类型
    :return:
    """
    print(S3_CLIENT["upload_file"](oss_resource, bucket_name, object_name, file_path, content_type))


@app.command()
def download_file(object_name: str,
                  file_path: str = None,
                  bucket_name: str = settings.oss_bucket, ):
    """
    下载文件
    :param bucket_name: 桶
    :param object_name: 对象名称
    :param file_path: 文件路径
    :return:
    """
    print(S3_CLIENT["download_file"](oss_resource, bucket_name, object_name, file_path))


@app.command()
def get_upload_url(object_name: str,
                   bucket_name: str = settings.oss_bucket,
                   seconds: int = 3600):
    """
    获取上传文件的URL
    :param bucket_name: 桶
    :param object_name: 对象名称
    :param seconds: 有效时长(秒)
    :return:
    """
    print(S3_CLIENT["get_upload_url"](oss_resource, bucket_name, object_name, seconds))


@app.command()
def get_download_url(object_name: str,
                     bucket_name: str = settings.oss_bucket,
                     seconds: int = 3600):
    """
    获取下载文件的URL
    :param bucket_name: 桶
    :param object_name: 对象名称
    :param seconds: 有效时长(秒)
    :return:
    """
    print(S3_CLIENT["get_download_url"](oss_resource, bucket_name, object_name, seconds))


@app.command()
def upload_folder(from_path: str,
                  bucket_name: str = settings.oss_bucket,
                  target: str = None):
    """
    上传文件夹
    :param bucket_name: 桶
    :param from_path: 本地文件夹路径
    :param target: 目标文件夹名称
    :return:
    """
    print(S3_CLIENT["upload_folder"](oss_resource, bucket_name, from_path, target))


if __name__ == '__main__':
    app()
