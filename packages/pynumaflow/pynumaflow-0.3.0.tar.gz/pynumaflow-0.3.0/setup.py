# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynumaflow',
 'pynumaflow.function',
 'pynumaflow.function.generated',
 'pynumaflow.sink',
 'pynumaflow.sink.generated',
 'pynumaflow.tests',
 'pynumaflow.tests.function',
 'pynumaflow.tests.sink']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-tools>=1.48.1,<2.0.0', 'grpcio>=1.48.1,<2.0.0']

setup_kwargs = {
    'name': 'pynumaflow',
    'version': '0.3.0',
    'description': 'Provides the interfaces of writing Python User Defined Functions and Sinks for NumaFlow.',
    'long_description': '# Python SDK for Numaflow\n\nThis SDK provides the interface for writing [UDFs](https://numaflow.numaproj.io/user-guide/user-defined-functions/) \nand [UDSinks](https://numaflow.numaproj.io/user-guide/sinks/user-defined-sinks/) in Python.\n\n## Implement a User Defined Function (UDF)\n\n```python\n\nfrom pynumaflow.function import Messages, Message, Datum, UserDefinedFunctionServicer\n\n\ndef function_handler(key: str, datum: Datum) -> Messages:\n    """\n    Simple UDF that relays an incoming message.\n    """\n    val = datum.value\n    _ = datum.event_time\n    _ = datum.watermark\n    messages = Messages(Message(key=key, value=val))\n    return messages\n\n\nif __name__ == "__main__":\n    grpc_server = UserDefinedFunctionServicer(function_handler)\n    grpc_server.start()\n```\n\n### Sample Image (TODO)\n\n## Implement a User Defined Sink (UDSink)\n\n```python\nfrom typing import List\nfrom pynumaflow.sink import Datum, Responses, Response, UserDefinedSinkServicer\n\n\ndef udsink_handler(datums: List[Datum]) -> Responses:\n    responses = Responses()\n    for msg in datums:\n        print("User Defined Sink", msg)\n        responses.append(Response.as_success(msg.id))\n    return responses\n\n\nif __name__ == "__main__":\n    grpc_server = UserDefinedSinkServicer(udsink_handler)\n    grpc_server.start()\n```\n\n### Sample Image\n\nA sample UDSink [Dockerfile](examples/sink/simplesink/Dockerfile) is provided \nunder [examples](examples/sink/simplesink).\n',
    'author': 'NumaFlow Developers',
    'author_email': 'None',
    'maintainer': 'Avik Basu',
    'maintainer_email': 'avikbasu93@gmail.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
