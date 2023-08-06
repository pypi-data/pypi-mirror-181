from time import time
from jiange.log import LogAgent
from jiange.file import dump_json
from jiange.time import get_time_string


class AgentBase(object):

    def __init__(self, *args, **kwargs):
        self.skill_name = None
        self.log = LogAgent()

    def dispatch(self, *args, **kwargs):
        raise NotImplementedError

    def response(self, *args, **kwargs):
        """

        e.g.
        response = {
            'code': 200,
            'message': 'success',
            'data': {
                'output': output,
                'skill_name': self.skill_name
            }
        }
        """
        raise NotImplementedError

    def log_request_response(self, request, response, **kwargs):
        body = {
            'timestamp': int(time() * 1000),
            'date': get_time_string(),
            'request': request,
            'response': response,
            **kwargs
        }
        body = dump_json(body, indent=False)
        self.log.info(body)
