**loafer** is an asynchronous message dispatcher for concurrent tasks
processing, with the following features:

* Encourages decoupling from message providers and consumers
* Easy to extend and customize
* Easy error handling, including integration with sentry
* Easy to create one or multiple services
* Generic Handlers
* Amazon SQS integration

---
:information_source: Currently, only AWS SQS is supported
---

## How to use

A simple message forwader, from ``source-queue`` to ``destination-queue``:

```python
from loafer.ext.aws.handlers import SQSHandler
from loafer.ext.aws.routes import SQSRoute
from loafer.managers import LoaferManager

routes = [
    SQSRoute('source-queue', handler=SQSHandler('destination-queue')),
]

if __name__ == '__main__':
    manager = LoaferManager(routes)
    manager.run()
```

## How to contribute

Fork this repository, make changes and send us a pull request. We will review
your changes and apply them. Before sending us your pull request please check
if you wrote and ran tests:

```bash
make test
```
