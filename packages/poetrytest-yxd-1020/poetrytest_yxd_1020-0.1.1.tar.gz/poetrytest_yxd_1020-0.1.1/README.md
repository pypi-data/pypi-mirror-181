# pyraisdk

## Dynamic Batching

### Description
When we deploy a model in AML with GPU instance to provide inference service, if it occupies GPU for inferencing in each request separately, it will be quite inefficient. This is a shared module helping to collect data items from different requests, and inferencing batchly in a backend thread. This will considerably improve usage efficiency of GPU.

### Usage Examples

Build `YourModel` class inherited from `pyraisdk.dynbatch.BaseModel`.

```python
from typing import List
from pyraisdk.dynbatch import BaseModel

class SimpleModel(BaseModel):
    def predict(self, items: List[str]) -> List[int]:
        rs = []
        for item in items:
            rs.append(len(item))
        return rs
            
    def preprocess(self, items: List[str]) -> List[str]:
        rs = []
        for item in items:
            rs.append(f'[{item}]')
        return rs
```

Initialize a `pyraisdk.dynbatch.DynamicBatchModel` with `YourModel` instance, and call `predict / predict_one` for inferencing.

```python
from pyraisdk.dynbatch import DynamicBatchModel

# prepare model
simple_model = SimpleModel()
batch_model = DynamicBatchModel(simple_model)

# predict
items = ['abc', '123456', 'xyzcccffaffaaa']
predictions = batch_model.predict(items)
assert predictions == [5, 8, 16]

# predict_one
item = 'abc'
prediction = batch_model.predict_one(item)
assert prediction == 5
```

Concurrent requests to `predict / predict_one`, in different threads.

```python
from threading import Thread
from pyraisdk.dynbatch import DynamicBatchModel

# prepare model
simple_model = SimpleModel()
batch_model = DynamicBatchModel(simple_model)

# thread run function
def run(name, num):
    for step in range(num):
        item = f'{name}-{step}'
        prediction = batch_model.predict_one(item)
        assert prediction == len(item) + 2

# start concurrent inference
threads = [Thread(target=run, args=(f'{tid}', 100)) for tid in range(20)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```


## Loging & Events

### Description
This module is for logging and event tracing.

### interface

```python

def initialize(
    eh_hostname: Optional[str] = None,
    client_id: Optional[str] = None,
    eh_conn_str: Optional[str] = None,
    eh_structured: Optional[str] = None,
    eh_unstructured: Optional[str] = None,
    role: Optional[str] = None,
    instance: Optional[str] = None,
)
```

Parameter description for `initialize`:
- **eh_hostname**: Fully Qualified Namespace aka EH Endpoint URL (*.servicebus.windows.net). Default, read $EVENTHUB_NAMESPACE
- **client_id**: client_id of service principal. Default, read $UAI_CLIENT_ID
- **eh_conn_str**: connection string of eventhub namespace. Default, read $EVENTHUB_CONN_STRING
- **eh_structured**: structured eventhub name. Default, read $EVENTHUB_AUX_STRUCTURED
- **eh_unstructured**: unstructured eventhub name. Default, read $EVENTHUB_AUX_UNSTRUCTURED
- **role**: role, Default: `RemoteModel`
- **instance**: instance, Default: `${ENDPOINT_NAME}|${ENDPOINT_VERSION}|{hostname}` or `${ENDPOINT_NAME}|${ENDPOINT_VERSION}|{_probably_unique_id()}`
- **sys_metrics_enable**: Whether to enable auto metrics reporting periodically for system info like gpu, memory and gpu. Default: True
- **sys_metrics_interval**: Interval in seconds of auo metrics reporting. Default: 60

```python

def event(self, key: str, code: str, numeric: float, detail: str='', corr_id: str='', elem: int=-1)
def infof(self, format: str, *args: Any)
def infocf(self, corr_id: str, elem: int, format: str, *args: Any)
def warnf(self, format: str, *args: Any)
def warncf(self, corr_id: str, elem: int, format: str, *args: Any)
def errorf(self, format: str, *args: Any)
def errorcf(self, corr_id: str, elem: int, ex: Optional[Exception], format: str, *args: Any)
def fatalf(self, format: str, *args: Any)
def fatalcf(self, corr_id: str, elem: int, ex: Optional[Exception], format: str, *args: Any)

```

### examples

```python
# export EVENTHUB_AUX_UNSTRUCTURED='ehunstruct'
# export EVENTHUB_AUX_STRUCTURED='ehstruct'
# export UAI_CLIENT_ID='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
# export EVENTHUB_NAMESPACE='xxx.servicebus.windows.net'

from pyraisdk import rlog
rlog.initialize()

rlog.infof('this is a info message %s', 123)
rlog.event('LifetimeEvent', 'STOP_GRACEFUL_SIGNAL', 0, 'detail info')

```

```python
# export EVENTHUB_AUX_UNSTRUCTURED='ehunstruct'
# export EVENTHUB_AUX_STRUCTURED='ehstruct'
# export EVENTHUB_CONN_STRING='<connection string>'

from pyraisdk import rlog
rlog.initialize()

rlog.infocf('corrid', -1, 'this is a info message: %s', 123)
rlog.event('RequestDuration', '200', 0.01, 'this is duration in seconds')

```

```python
from pyraisdk import rlog
rlog.initialize(eh_structured='ehstruct', eh_unstructured='ehunstruct', eh_conn_str='<eventhub-conn-str>')

rlog.errorcf('corrid', -1, Exception('error msg'), 'error message: %s %s', 1,2)
rlog.event('CpuUsage', '', 0.314, detail='cpu usage', corr_id='corrid', elem=-1)

```
