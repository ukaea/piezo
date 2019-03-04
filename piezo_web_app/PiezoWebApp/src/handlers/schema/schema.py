# Adapted from tornado-json.schema to accept validation ruleset on the ApiHandler

import json
from functools import wraps

import jsonschema
import tornado.gen
from tornado_json.exceptions import APIError
from tornado_json.schema import input_schema_clean
from tornado_json.utils import container

try:
    from tornado.concurrent import is_future
except ImportError:
    # For tornado 3.x.x
    from tornado.concurrent import Future

    def is_future(x):
        isinstance(x, Future)

from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_from_validation_ruleset


def validate(output_schema=None,
             input_example=None, output_example=None,
             validator_cls=None,
             format_checker=None, on_empty_404=False,
             use_defaults=False):
    @container
    def _validate(rh_method):
        @wraps(rh_method)
        @tornado.gen.coroutine
        def _wrapper(self, *args, **kwargs):
            validation_ruleset = getattr(self, "validation_ruleset")
            input_schema = create_object_schema_from_validation_ruleset(validation_ruleset)
            if input_schema is not None:
                try:
                    encoding = "UTF-8"
                    input_ = json.loads(self.request.body.decode(encoding))
                except ValueError:
                    raise jsonschema.ValidationError(
                        "Input is malformed; could not decode JSON object."
                    )

                if use_defaults:
                    input_ = input_schema_clean(input_, input_schema)

                jsonschema.validate(
                    input_,
                    input_schema,
                    cls=validator_cls,
                    format_checker=format_checker
                )
            else:
                input_ = None

            setattr(self, "body", input_)
            output = rh_method(self, *args, **kwargs)
            if is_future(output):
                output = yield output

            if not output and on_empty_404:
                raise APIError(404, "Resource not found.")

            if output_schema is not None:
                try:
                    jsonschema.validate(
                        {"result": output},
                        {
                            "type": "object",
                            "properties": {
                                "result": output_schema
                            },
                            "required": ["result"]
                        }
                    )
                except jsonschema.ValidationError as error:
                    raise TypeError(str(error))

            self.success(output)

        setattr(_wrapper, "output_schema", output_schema)
        setattr(_wrapper, "input_example", input_example)
        setattr(_wrapper, "output_example", output_example)

        return _wrapper
    return _validate
