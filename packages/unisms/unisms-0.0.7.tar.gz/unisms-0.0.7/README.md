# UniSMS Python SDK

[UniSMS](https://unisms.apistd.com/) - 高可用聚合短信服务平台官方 Python SDK.

## 文档

查看完整产品介绍与 API 文档请访问 [UniSMS Documentation](https://unisms.apistd.com/docs).

## 安装

Uni Python SDK 使用 PyPI 托管，可从公共 [PyPI 仓库](https://pypi.org/project/unisms/) 中获得。

在项目中使用 pip 添加 `unisms` 作为依赖：

```bash
pip install unisms
```

## 使用示例

以下示例展示如何使用 Uni Python SDK 快速调用服务。

### 发送短信

```py

from unisdk.sms import UniSMS
from unisdk.exception import UniException

client = UniSMS("your access key id", "your access key secret")

try:
  res = client.send({
    "to": "your phone number",
    "signature": "UniSMS",
    "templateId": "login_tmpl",
    "templateData": {
      "code": 7777
    }
  })
  print(res.data)
except UniException as e:
  print(e)

```

## 相关参考

### 其他语言 SDK

- [Java](https://github.com/apistd/uni-java-sdk)
- [Go](https://github.com/apistd/uni-go-sdk)
- [Node.js](https://github.com/apistd/unisms-node-sdk)
- [PHP](https://github.com/apistd/uni-php-sdk/)
