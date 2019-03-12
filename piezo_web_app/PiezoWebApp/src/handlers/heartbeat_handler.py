from tornado_json import schema
from tornado_json.requesthandlers import APIHandler


class HeartbeatHandler(APIHandler):
    @schema.validate(
        output_schema={
            "type": "object",
            "properties": {
                "running": {"type": "string"},
            },
        }
    )
    def get(self, *args, **kwargs):
        self.clear_header("Server")
        status = {'running': 'true'}
        return status

