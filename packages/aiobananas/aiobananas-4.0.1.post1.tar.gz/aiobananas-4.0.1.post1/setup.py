# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aiobananas']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'charset-normalizer>=2.0.7,<3.0.0',
 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'aiobananas',
    'version': '4.0.1.post1',
    'description': 'aiobananas is an async version of banana-dev',
    'long_description': '# Banana Python SDK\n\n### Getting Started\n\nInstall via pip\n`pip3 install aiobananas`\n\nGet your API Key\n- [Sign in / log in here](https://app.banana.dev)\n\nRun:\n```python\nimport aiobananas\n\napi_key = "demo" # "YOUR_API_KEY"\nmodel_key = "carrot" # "YOUR_MODEL_KEY"\nmodel_inputs = {\n    # a json specific to your model. For example:\n    "imageURL":  "https://demo-images-banana.s3.us-west-1.amazonaws.com/image2.jpg"\n}\n\nasync with aiobananas.Session(api_key) as banana:\n    out = await banana.run(model_key, model_inputs)\n\n\n\nout = banana.run(api_key, model_key, model_inputs)\nprint(out)\n```\n\nReturn type:\n```python\n{\n    "id": "12345678-1234-1234-1234-123456789012", \n    "message": "success", \n    "created": 1649712752, \n    "apiVersion": "26 Nov 2021", \n    "modelOutputs": [\n        {\n            # a json specific to your model. In this example, the caption of the image\n            "caption": "a baseball player throwing a ball"\n        }\n    ]\n}\n```\n\nParse the server output:\n```python\nmodel_out = out["modelOutputs"][0]\n```',
    'author': 'Bennett Hoffman',
    'author_email': 'benn.hoffman@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
