import ipykernel
import json
import tornado
import zmq

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from jupyter_client.jsonutil import date_default

from packaging import version


USAGE_IS_SUPPORTED = version.parse("6.9.0") <= version.parse(ipykernel.__version__)

MAX_RETRIES = 3


class RouteHandler(APIHandler):

    @tornado.web.authenticated
    async def get(self, matched_part=None, *args, **kwargs):

        if not USAGE_IS_SUPPORTED:
            self.write(json.dumps({}))
            return

        kernel_id = matched_part
        km = self.kernel_manager
        lkm = km.pinned_superclass.get_kernel(km, kernel_id)
        session = lkm.session
        client = lkm.client()

        control_channel = client.control_channel
        usage_request = session.msg("usage_request", {})

        control_channel.send(usage_request)
        poller = zmq.Poller()
        control_socket = control_channel.socket
        poller.register(control_socket, zmq.POLLIN)
        for i in range(1, MAX_RETRIES + 1):
            timeout_ms = 1000 * i
            events = dict(poller.poll(timeout_ms))
            if not events:
                self.write(json.dumps({}))
                break
            if control_socket not in events:
                continue
            res = await client.control_channel.get_msg(timeout=0)
            self.write(json.dumps(res, default=date_default))
            break


def setup_handlers(web_app):
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "jupyterlab_kernel_usage", r"get_usage/(.+)$")
    handlers = [
        (route_pattern, RouteHandler)
    ]
    web_app.add_handlers(host_pattern, handlers)
