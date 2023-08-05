""" free qa task """
from wenxin_api.api import Task
from wenxin_api.error import IllegalRequestArgumentError
from wenxin_api import log
logger = log.get_logger()

class FreeQA(Task):
    """ free qa task """
    @staticmethod
    def _resolve_result(resp):
        rst = {}
        rst["result"] = resp["result"]
        return rst

    @classmethod
    def create(cls, text=None, model=None, **params):
        """ create """
        if text is None:
            raise IllegalRequestArgumentError("text shouldn't be none")
        model_id = 1 if model is None else model.id
        params["api_type"] = params.get("api_type", 5)
        logger.info("model {}: starts writing".format(model_id))
        resp = cls.default_request(text=text, **params)
        return cls._resolve_result(resp)