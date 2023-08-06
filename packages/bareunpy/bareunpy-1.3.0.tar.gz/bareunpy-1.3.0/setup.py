# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bareunpy']

package_data = \
{'': ['*']}

install_requires = \
['bareun-apis>=0.10.1,<0.11.0',
 'googleapis-common-protos>=1.56.0,<2.0.0',
 'grpcio>=1.46.0,<2.0.0',
 'protobuf>=3.19.4,<4.0.0']

setup_kwargs = {
    'name': 'bareunpy',
    'version': '1.3.0',
    'description': 'The bareun python library using grpc',
    'long_description': '# What is this?\n\n`bareunpy` is the python 3 library for bareun.\n\nBareun is a Korean NLP,\nwhich provides tokenizing, POS tagging for Korean.\n\n## How to install\n\n```shell\npip3 install bareunpy\n```\n\n## How to get bareun\n- Go to https://bareun.ai/.\n  - With registration, for the first time, you can get a free license for 3 months.\n  - If you are a student or a researcher, you can get also a free license for 1 year,\n    which is able to renew after 1 year.\n- Or use docker image.\n```shell\ndocker pull bareunai/bareun:latest\n```\n\n## How to use\n\n```python\nimport sys\nimport google.protobuf.text_format as tf\nfrom bareunpy import Tagger\n\n# If you have your own localhost bareun.\nmy_tagger = Tagger(\'localhost\')\n# or if you have your own bareun which is running on 10.8.3.211:15656.\nmy_tagger = Tagger(\'10.8.3.211\', 15656)\n# or with smaller public cloud instance, it may be slow. It is free.\ntagger = Tagger()\n\n# print results. \nres = tagger.tags(["안녕하세요.", "반가워요!"])\n\n# get protobuf message.\nm = res.msg()\ntf.PrintMessage(m, out=sys.stdout, as_utf8=True)\nprint(tf.MessageToString(m, as_utf8=True))\nprint(f\'length of sentences is {len(m.sentences)}\')\n## output : 2\nprint(f\'length of tokens in sentences[0] is {len(m.sentences[0].tokens)}\')\nprint(f\'length of morphemes of first token in sentences[0] is {len(m.sentences[0].tokens[0].morphemes)}\')\nprint(f\'lemma of first token in sentences[0] is {m.sentences[0].tokens[0].lemma}\')\nprint(f\'first morph of first token in sentences[0] is {m.sentences[0].tokens[0].morphemes[0]}\')\nprint(f\'tag of first morph of first token in sentences[0] is {m.sentences[0].tokens[0].morphemes[0].tag}\')\n\n## Advanced usage.\nfor sent in m.sentences:\n    for token in sent.tokens:\n        for m in token.morphemes:\n            print(f\'{m.text.content}/{m.tag}:{m.probability}:{m.out_of_vocab})\n\n# get json object\njo = res.as_json()\nprint(jo)\n\n# get tuple of pos tagging.\npa = res.pos()\nprint(pa)\n# another methods\nma = res.morphs()\nprint(ma)\nna = res.nouns()\nprint(na)\nva = res.verbs()\nprint(va)\n\n# custom dictionary\ncust_dic = tagger.custom_dict("my")\ncust_dic.copy_np_set({\'내고유명사\', \'우리집고유명사\'})\ncust_dic.copy_cp_set({\'코로나19\'})\ncust_dic.copy_cp_caret_set({\'코로나^백신\', \'"독감^백신\'})\ncust_dic.update()\n\n# laod prev custom dict\ncust_dict2 = tagger.custom_dict("my")\ncust_dict2.load()\n\ntagger.set_domain(\'my\')\ntagger.pos(\'코로나19는 언제 끝날까요?\')\n```\n',
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
