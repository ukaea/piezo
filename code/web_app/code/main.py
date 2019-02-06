import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import subprocess
import json

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)


class RunExample(tornado.web.RequestHandler):
    def get(self):
        # import submit_job_api as submit_job
        import submit_job_client as submit_job
        print("Running spark example")
        submit_job.run_job()
        self.write("Running spark example")

class GetLogs(tornado.web.RequestHandler):
    def get(self):
        import get_logs_client
        #import get_logs
        print("Running spark example")
        result = get_logs_client.go_get_logs()
        #os.system("kubectl logs spark-pi-driver")
        self.write(json.dumps(result))

class DeleteExample(tornado.web.RequestHandler):
    def get(self):
        import delete_job_api

        result = delete_job_api.delete()
        print(result)
        #os.system("kubectl logs spark-pi-driver")
        self.write(json.dumps(result))

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/runexample", RunExample),
        (r"/getlogs", GetLogs),
        (r"/deleteexample", DeleteExample),])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    print("Starting server")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()