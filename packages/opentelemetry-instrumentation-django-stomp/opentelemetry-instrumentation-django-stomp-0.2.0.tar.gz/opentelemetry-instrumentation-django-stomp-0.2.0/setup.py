# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opentelemetry_instrumentation_django_stomp',
 'opentelemetry_instrumentation_django_stomp.instrumentors',
 'opentelemetry_instrumentation_django_stomp.utils']

package_data = \
{'': ['*']}

install_requires = \
['Django',
 'django-stomp>=5.0.0,<6.0.0',
 'opentelemetry-api',
 'opentelemetry-instrumentation',
 'opentelemetry-sdk']

setup_kwargs = {
    'name': 'opentelemetry-instrumentation-django-stomp',
    'version': '0.2.0',
    'description': 'Opentelemetry instrumentor for django-stomp package',
    'long_description': '# Opentelemetry auto instrumentation for django-stomp\n\n[//]: # ([![Build Status]&#40;https://dev.azure.com/juntos-somos-mais-loyalty/python/_apis/build/status/juntossomosmais.opentelemetry-instrumentation-django-stomp?branchName=main&#41;]&#40;https://dev.azure.com/juntos-somos-mais-loyalty/python/_build/latest?definitionId=272&branchName=main&#41;)\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=juntossomosmais_opentelemetry-instrumentation-django-stomp&metric=sqale_rating&token=80cebbac184a793f8d0be7a3bbe9792f47a6ef23)](https://sonarcloud.io/summary/new_code?id=juntossomosmais_opentelemetry-instrumentation-django-stomp)\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=juntossomosmais_opentelemetry-instrumentation-django-stomp&metric=coverage&token=80cebbac184a793f8d0be7a3bbe9792f47a6ef23)](https://sonarcloud.io/summary/new_code?id=juntossomosmais_opentelemetry-instrumentation-django-stomp)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=juntossomosmais_opentelemetry-instrumentation-django-stomp&metric=alert_status&token=80cebbac184a793f8d0be7a3bbe9792f47a6ef23)](https://sonarcloud.io/summary/new_code?id=juntossomosmais_opentelemetry-instrumentation-django-stomp)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![PyPI version](https://badge.fury.io/py/opentelemetry-instrumentation-django-stomp.svg)](https://badge.fury.io/py/opentelemetry-instrumentation-django-stomp)\n[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/juntossomosmais/opentelemetry-instrumentation-django-stomp/blob/main/LICENSE)\n\nThis library will help you to use opentelemetry traces and metrics on [Django STOMP](https://github.com/juntossomosmais/django-stomp) usage library.\n\n![Django stomp instrumentation](docs/example.gif?raw=true)\n\n\n####  Installation\npip install `opentelemetry-instrumentation-django-stomp`\n\n#### How to use ?\n\nYou can use the `DjangoStompInstrumentor().instrument()` for example in `manage.py` file.\n\n\n```python\n#!/usr/bin/env python\n"""Django\'s command-line utility for administrative tasks."""\nimport os\nimport sys\nimport typing\n\nfrom opentelemetry_instrumentation_django_stomp import DjangoStompInstrumentor\n\nfrom opentelemetry import trace\nfrom opentelemetry.sdk.trace import TracerProvider\nfrom opentelemetry.sdk.trace.export import BatchSpanProcessor\nfrom opentelemetry.sdk.trace.export import ConsoleSpanExporter\nfrom opentelemetry.trace.span import Span\n\n\ndef publisher_hook(span: Span, body: typing.Dict, headers: typing.Dict):\n    # Custom code in your project here we can see span attributes and make custom logic with then.\n    pass\n\n\ndef consumer_hook(span: Span, body: typing.Dict, headers: typing.Dict):\n    # Custom code in your project here we can see span attributes and make custom logic with then.\n    pass\n\n\nprovider = TracerProvider()\ntrace.set_tracer_provider(provider)\ntrace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))\n\ndef main():\n    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.settings")\n    DjangoStompInstrumentor().instrument(\n        trace_provider=trace,\n        publisher_hook=publisher_hook,\n        consumer_hook=consumer_hook,\n    )\n    try:\n        from django.core.management import execute_from_command_line\n    except ImportError as exc:\n        raise ImportError(\n            "Couldn\'t import Django. Are you sure it\'s installed and "\n            "available on your PYTHONPATH environment variable? Did you "\n            "forget to activate a virtual environment?"\n        ) from exc\n    execute_from_command_line(sys.argv)\n\n\nif __name__ == "__main__":\n    main()\n```\n\nThe code above will create telemetry wrappers inside django-stomp code and creates automatic spans with broker data.\n\nThe `DjangoStompInstrumentor` can receive three optional parameters:\n- **trace_provider**: The tracer provider to use in open-telemetry spans.\n- **publisher_hook**: The callable function on publisher action to call before the original function call, use this to override, enrich the span or get span information in the main project.\n- **consumer_hook**: The callable function on consumer action to call before the original function call, use this to override, enrich the span or get span information in the main project.\n\n:warning: The hook function will not raise an exception when an error occurs inside hook function, only a warning log is generated\n\n#### PUBLISHER example\n\nWith the django-stomp, we can publish a message to a broker using `publisher.send` and the instrumentator\ncan include a span with telemetry data in this function utilization.\n\n```python\n    from uuid import uuid4\n    from django_stomp.builder import build_publisher\n    publisher = build_publisher(f"publisher-unique-name-{uuid4()}")\n    publisher.send(\n        queue=\'/queue/a-destination\',\n        body={"a": "random","body": "message"},\n    )\n```\n\nThe publisher span had "PUBLISHER" name.\n\n![publisher example](docs/publisher_example.png?raw=true)\n\n#### CONSUMER example\nWith the django-stomp, we create a simple consumer using pubsub command and the instrumentator\ncan include a span with telemetry data in this function utilization.\n\n```bash\n   python manage.py pubsub QUEUE_NAME callback_function_to_consume_message\n```\n\nConsumer spans can generate up to three types:\n\n- CONSUMER\n![consumer example](docs/consumer_example.png?raw=true)\n- ACK\n![ack example](docs/ack_example.png?raw=true)\n- NACK\n![nack example](docs/nack_example.png?raw=true)\n\n#### Supress django-stomp traces and metrics\nWhen the flag `OTEL_PYTHON_DJANGO_STOMP_INSTRUMENT` has `False` value traces and metrics will not be generated.\nUse this to supress the django-stomp instrumentation.\n\n#### HOW TO CONTRIBUTE ?\nLook the [contributing](./CONTRIBUTING.md) specs\n',
    'author': 'Juntos Somos Mais',
    'author_email': 'labs@juntossomosmais.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/juntossomosmais/opentelemetry-instrumentation-django-stomp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
