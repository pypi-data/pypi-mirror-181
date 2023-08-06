import datetime
import hashlib
import hmac
import logging
import uuid
from io import BytesIO
from typing import Callable, Tuple

import requests
import socketio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ango.sdk import SDK

try:
    import asyncio
except ImportError:
    import trollius as asyncio


class Plugin(socketio.ClientNamespace):

    def __init__(self, id: str, secret: str, callback: Callable):
        super().__init__('/plugin')
        self.id = id
        self.secret = secret
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.heartbeat, 'interval', seconds=60)
        scheduler.start()
        self.logger = logging.getLogger()
        self.callback = callback

    def on_connect(self):
        self.logger.warning("Connected")
        self.heartbeat()

    def on_disconnect(self):
        self.logger.warning("Disconnected")

    def heartbeat(self):
        self.emit('heartbeat', {"id": self.id, "secret": self.secret})

    def on_plugin(self, data):
        response = self.callback(data)
        return response


class ExportPlugin(Plugin):

    def __init__(self, id: str, secret: str, api_key: str, callback: Callable[[str, dict], Tuple[str, BytesIO]], host="https://api.ango.ai"):
        super().__init__(id, secret, callback)
        self.sdk = SDK(api_key=api_key, host=host)

    def on_plugin(self, data):
        """
        :param data: {project_id: str, assignees: List[str] = None, completed_at: List[datetime.datetime] = None,
               updated_at: List[datetime.datetime = None, tags: List[str] = None}
        :return:
        """
        completed_at = None
        updated_at = None
        project_id = data.get('projectId')
        if data.get("completed_at", None):
            completed_at = [datetime.datetime.fromisoformat(data.completed_at[0]), datetime.datetime.fromisoformat(data.completed_at[1])]
        if data.get("updated_at", None):
            updated_at = [datetime.datetime.fromisoformat(data.updated_at[0]), datetime.datetime.fromisoformat(data.updated_at[1])]
        json_export = self.sdk.export(project_id, data.get('assignees', None), completed_at=completed_at,
                                      updated_at=updated_at, tags=data.get('tags', None))
        file_name, export_bytes = self.callback(project_id, json_export)
        upload_url = self.sdk._get_upload_url(file_name)
        upload_resp = requests.put(upload_url, data=export_bytes.getvalue())
        if upload_resp.status_code != 200:
            logging.getLogger().error("Unable to upload exports!")
        response = upload_url.split("?")[0]
        return response


class ModelPlugin(Plugin):
    def __init__(self, id: str, secret: str, callback: Callable):
        super().__init__(id, secret, callback)


def run(plugin, host="https://api.ango.ai"):
    sio = socketio.Client()
    sio.register_namespace(plugin)
    sio.connect(host, namespaces=["/plugin"], wait_timeout=100)
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        logging.getLogger().warning("Plugin Stopped")
