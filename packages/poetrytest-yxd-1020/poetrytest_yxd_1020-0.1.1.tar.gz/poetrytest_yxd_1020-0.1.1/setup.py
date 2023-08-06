# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyraisdk', 'pyraisdk.dynbatch', 'pyraisdk.rlog']

package_data = \
{'': ['*']}

install_requires = \
['azure-eventhub>=5.10.1,<6.0.0',
 'azure-identity>=1.7.0,<2.0.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'gputil>=1.4.0,<2.0.0',
 'psutil>=5.6.3,<6.0.0',
 'typeguard>=2.13.3,<3.0.0']

setup_kwargs = {
    'name': 'poetrytest-yxd-1020',
    'version': '0.1.1',
    'description': '',
    'long_description': "# pyraisdk\n\n## Dynamic Batching\n\n### Description\nWhen we deploy a model in AML with GPU instance to provide inference service, if it occupies GPU for inferencing in each request separately, it will be quite inefficient. This is a shared module helping to collect data items from different requests, and inferencing batchly in a backend thread. This will considerably improve usage efficiency of GPU.\n\n### Usage Examples\n\nBuild `YourModel` class inherited from `pyraisdk.dynbatch.BaseModel`.\n\n```python\nfrom typing import List\nfrom pyraisdk.dynbatch import BaseModel\n\nclass SimpleModel(BaseModel):\n    def predict(self, items: List[str]) -> List[int]:\n        rs = []\n        for item in items:\n            rs.append(len(item))\n        return rs\n            \n    def preprocess(self, items: List[str]) -> List[str]:\n        rs = []\n        for item in items:\n            rs.append(f'[{item}]')\n        return rs\n```\n\nInitialize a `pyraisdk.dynbatch.DynamicBatchModel` with `YourModel` instance, and call `predict / predict_one` for inferencing.\n\n```python\nfrom pyraisdk.dynbatch import DynamicBatchModel\n\n# prepare model\nsimple_model = SimpleModel()\nbatch_model = DynamicBatchModel(simple_model)\n\n# predict\nitems = ['abc', '123456', 'xyzcccffaffaaa']\npredictions = batch_model.predict(items)\nassert predictions == [5, 8, 16]\n\n# predict_one\nitem = 'abc'\nprediction = batch_model.predict_one(item)\nassert prediction == 5\n```\n\nConcurrent requests to `predict / predict_one`, in different threads.\n\n```python\nfrom threading import Thread\nfrom pyraisdk.dynbatch import DynamicBatchModel\n\n# prepare model\nsimple_model = SimpleModel()\nbatch_model = DynamicBatchModel(simple_model)\n\n# thread run function\ndef run(name, num):\n    for step in range(num):\n        item = f'{name}-{step}'\n        prediction = batch_model.predict_one(item)\n        assert prediction == len(item) + 2\n\n# start concurrent inference\nthreads = [Thread(target=run, args=(f'{tid}', 100)) for tid in range(20)]\nfor t in threads:\n    t.start()\nfor t in threads:\n    t.join()\n```\n\n\n## Loging & Events\n\n### Description\nThis module is for logging and event tracing.\n\n### interface\n\n```python\n\ndef initialize(\n    eh_hostname: Optional[str] = None,\n    client_id: Optional[str] = None,\n    eh_conn_str: Optional[str] = None,\n    eh_structured: Optional[str] = None,\n    eh_unstructured: Optional[str] = None,\n    role: Optional[str] = None,\n    instance: Optional[str] = None,\n)\n```\n\nParameter description for `initialize`:\n- **eh_hostname**: Fully Qualified Namespace aka EH Endpoint URL (*.servicebus.windows.net). Default, read $EVENTHUB_NAMESPACE\n- **client_id**: client_id of service principal. Default, read $UAI_CLIENT_ID\n- **eh_conn_str**: connection string of eventhub namespace. Default, read $EVENTHUB_CONN_STRING\n- **eh_structured**: structured eventhub name. Default, read $EVENTHUB_AUX_STRUCTURED\n- **eh_unstructured**: unstructured eventhub name. Default, read $EVENTHUB_AUX_UNSTRUCTURED\n- **role**: role, Default: `RemoteModel`\n- **instance**: instance, Default: `${ENDPOINT_NAME}|${ENDPOINT_VERSION}|{hostname}` or `${ENDPOINT_NAME}|${ENDPOINT_VERSION}|{_probably_unique_id()}`\n- **sys_metrics_enable**: Whether to enable auto metrics reporting periodically for system info like gpu, memory and gpu. Default: True\n- **sys_metrics_interval**: Interval in seconds of auo metrics reporting. Default: 60\n\n```python\n\ndef event(self, key: str, code: str, numeric: float, detail: str='', corr_id: str='', elem: int=-1)\ndef infof(self, format: str, *args: Any)\ndef infocf(self, corr_id: str, elem: int, format: str, *args: Any)\ndef warnf(self, format: str, *args: Any)\ndef warncf(self, corr_id: str, elem: int, format: str, *args: Any)\ndef errorf(self, format: str, *args: Any)\ndef errorcf(self, corr_id: str, elem: int, ex: Optional[Exception], format: str, *args: Any)\ndef fatalf(self, format: str, *args: Any)\ndef fatalcf(self, corr_id: str, elem: int, ex: Optional[Exception], format: str, *args: Any)\n\n```\n\n### examples\n\n```python\n# export EVENTHUB_AUX_UNSTRUCTURED='ehunstruct'\n# export EVENTHUB_AUX_STRUCTURED='ehstruct'\n# export UAI_CLIENT_ID='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'\n# export EVENTHUB_NAMESPACE='xxx.servicebus.windows.net'\n\nfrom pyraisdk import rlog\nrlog.initialize()\n\nrlog.infof('this is a info message %s', 123)\nrlog.event('LifetimeEvent', 'STOP_GRACEFUL_SIGNAL', 0, 'detail info')\n\n```\n\n```python\n# export EVENTHUB_AUX_UNSTRUCTURED='ehunstruct'\n# export EVENTHUB_AUX_STRUCTURED='ehstruct'\n# export EVENTHUB_CONN_STRING='<connection string>'\n\nfrom pyraisdk import rlog\nrlog.initialize()\n\nrlog.infocf('corrid', -1, 'this is a info message: %s', 123)\nrlog.event('RequestDuration', '200', 0.01, 'this is duration in seconds')\n\n```\n\n```python\nfrom pyraisdk import rlog\nrlog.initialize(eh_structured='ehstruct', eh_unstructured='ehunstruct', eh_conn_str='<eventhub-conn-str>')\n\nrlog.errorcf('corrid', -1, Exception('error msg'), 'error message: %s %s', 1,2)\nrlog.event('CpuUsage', '', 0.314, detail='cpu usage', corr_id='corrid', elem=-1)\n\n```\n",
    'author': 'Xiaodong Yang',
    'author_email': 'xiaoyan@microsoft.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
