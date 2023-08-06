# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bareun']

package_data = \
{'': ['*']}

install_requires = \
['googleapis-common-protos>=1.56.0,<2.0.0',
 'grpcio>=1.46.0,<2.0.0',
 'protobuf>=3.19.4,<4.0.0']

setup_kwargs = {
    'name': 'bareun-apis',
    'version': '0.10.1',
    'description': 'bareunai-apis contains the python classes generated from the bareun ai APIs, which includes tagger, and so on.',
    'long_description': '# What is this?\n\n`bareun-apis` is the generated python classes of GRPC API for bareun.ai.\n\nThe bareun.ai provides several service for deep learning NLP features.\nThis api has all of main features, which provides tokenizing, POS tagging for Korean.\nIt has also customized dictionary service.\n\n## How to install\n\n```shell\npip3 install bareun-apis\n```\n\n## How to use\n- You can create your own baikal language service client.\n- It is used for `bareunlpy`, the official bareun package for python.\n\n\n```python\nfrom google.protobuf.json_format import MessageToDict\n\nimport bareun.language_service_pb2 as pb\nimport bareun.language_service_pb2_grpc as ls\n\nMAX_MESSAGE_LENGTH = 100*1024*1024\n\nclass BareunLanguageServiceClient:\n    stub = None\n\n    def __init__(self, remote):\n        channel = grpc.insecure_channel(\n            remote,\n            options=[\n                (\'grpc.max_send_message_length\', MAX_MESSAGE_LENGTH),\n                (\'grpc.max_receive_message_length\', MAX_MESSAGE_LENGTH),\n            ])\n\n        self.stub = ls.LanguageServiceStub(channel)\n\n    def analyze_syntax(self, document, auto_split=False):\n        req = pb.AnalyzeSyntaxRequest()\n        req.document.content = document\n        req.document.language = "ko_KR"\n        req.encoding_type = pb.EncodingType.UTF32\n        req.auto_split_sentence = auto_split\n\n        res = self.stub.AnalyzeSyntax(req)\n        # print_syntax_as_json(res)\n        return res\n\n\ndef print_syntax_as_json(res: pb.AnalyzeSyntaxResponse, logf=sys.stdout):\n    d = MessageToDict(res)\n    import json\n    json_str = json.dumps(d, ensure_ascii=False, indent=2)\n    logf.write(json_str)\n    logf.write(\'\\n\')\n```\n',
    'author': 'Gihyun YUN',
    'author_email': 'gih2yun@baikal.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://bareun.ai/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
