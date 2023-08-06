## Testing

```shell
pip install flake8
flake8 --max-line-length 119 ./opentelemetry_wrapper/

pip install sqlalchemy2-stubs
pip install mypy
mypy ./opentelemetry_wrapper/
```

also run the following files:

* experiment_otel_logging.py
* fastapi_main.py
* setup_otel_logging.py

## publishing (notes for myself)

* init
    * `pip install flit`
    * `flit init`
    * make sure `opentelemetry_wrapper/__init__.py` contains a docstring and version
* publish / update
    * increment `__version__` in `opentelemetry_wrapper/__init__.py`
    * `flit publish`

## references / best practices to consider

* [ ] [Implementing health checks](https://aws.amazon.com/builders-library/implementing-health-checks/)
* [ ] [Instrumenting distributed systems for operational visibility](https://aws.amazon.com/builders-library/instrumenting-distributed-systems-for-operational-visibility/)
* [ ] https://tersesystems.com/blog/2019/07/22/targeted-diagnostic-logging-in-production/
* [ ] https://www.honeycomb.io/blog/so-you-want-to-build-an-observability-tool/
* [x] [Instana ASGI Middleware](https://github.com/instana/python-sensor/blob/master/instana/middleware.py)
* [x] [IBM Best Practices](https://www.ibm.com/docs/en/obi/current?topic=tracing-best-practices)
* [x] [10 Things We Forgot to Monitor](https://word.bitly.com/post/74839060954/ten-things-to-monitor)
* [x] `/var/run/secrets/kubernetes.io/serviceaccount/namespace`
    * [x] or `/var/run/secrets/kubernetes.io/serviceaccount/token` which is a jwt containing the namespace
    * [x] also see `/etc/hostname`
* available instrumentation
    * [x] https://github.com/open-telemetry/opentelemetry-python
    * [x] [`pip install opentelemetry-instrumentation-fastapi`](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html)
    * [ ] [`pip install opentelemetry-instrumentation-sqlalchemy`](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/sqlalchemy/sqlalchemy.html)
    * [x] [`pip install opentelemetry-instrumentation-requests`](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/requests/requests.html)
    * [x] [`pip install opentelemetry-instrumentation-logging`](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/logging/logging.html)
* examples
    * jaeger
        * https://github.com/Blueswen/fastapi-jaeger
        * https://github.com/fike/fastapi-blog
        * https://guitton.co/posts/fastapi-monitoring

## todo

* `with ...` instrumentation for non-callable code (e.g. settings, semi-hardcoded config)
* type-checking decorator, with warning on unmatched types
    * https://github.com/prechelt/typecheck-decorator/blob/master/README.md
    * https://stackoverflow.com/questions/36879932/python-type-checking-decorator
    * https://towardsdatascience.com/the-power-of-decorators-fef4dc97020e
    * https://typeguard.readthedocs.io/en/latest/userguide.html
* correctly handle generators and context managers (and async versions of them)
* instrument pydantic?
* support metrics somehow
    * the asgi/fastapi already supports some metrics
    * https://github.com/instana/python-sensor/blob/master/instana/autoprofile/samplers
        * memory profiling
        * reading frames to make a statistical guess how much time is spent in each function
    * https://psutil.readthedocs.io/en/latest/
    * Request Error Duration metrics can be calculated from spans
* add [usage](./README.md#usage)
* builtin `tracemalloc` can be used locate the source file and line number of a function, if started early enough
* somehow mark function as do-not-instrument, for extremely spammy functions? or specify a sampling ratio?
