# s3-client

[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)


---

**Documentation**: [https://github.com/cafe-au-lait/s3-client](https://github.com/cafe-au-lait/s3-client)

**Source Code**: [https://github.com/cafe-au-lait/s3-client](https://github.com/cafe-au-lait/s3-client)

**PyPI**: [https://pypi.org/project/s3-client/](https://pypi.org/project/s3-client/)

---

A short description of the project

## Installation

```sh
pip install -r requirements.txt
```

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.8+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
pytest
```

### Documentation
1. 创建环境变量配置文件.env
```properties
OSS_ENDPOINT=http://127.0.0.1:9000
OSS_ACCESS_KEY=AWS Access Key
OSS_SECRET_KEY=AWS Secret Key
```
2. Usage
```shell
Usage: s3-client [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  create-bucket     创建桶 :param bucket_name: 桶 :param region: 区域 :return:
  delete-bucket     删除桶 :param bucket_name: 桶 :param force: 强制 :return:
  download-file     下载文件 :param bucket_name: 桶 :param object_name: 对象名称...
  exists-bucket     桶是否存在 :param bucket_name: 桶 :return:
  exists-object     查询对象状态 :param bucket_name: 桶 :param object_name: 对象名称...
  get-data          获取对象数据 :param bucket_name: 桶 :param object_name: 对象名称...
  get-download-url  获取下载文件的URL :param bucket_name: 桶 :param object_name:...
  get-json          获取json数据 :param bucket_name: 桶 :param object_name:...
  get-upload-url    获取上传文件的URL :param bucket_name: 桶 :param object_name:...
  list-objects      对象列表 :param bucket_name: 桶 :param prefix: 前缀 :param...
  remove-objects    删除对象 :param bucket_name: 桶 :param obj1: 对象名称 :param...
  upload-file       上传文件 :param bucket_name: 桶 :param object_name: 对象名称...
  upload-folder     上传文件夹 :param bucket_name: 桶 :param from_path: 本地文件夹路径...
```

---

This project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.
