import json
from uni.exception import UniException

class UniResponse:
  REQUEST_ID_HEADER_KEY = 'x-uni-request-id'

  def __init__(self, res):
    raw_body = res.read()
    body = raw_body and json.loads(raw_body.decode("utf-8"))
    status = res.status
    status_text = res.reason
    request_id = res.getheader(self.REQUEST_ID_HEADER_KEY)

    if (body != None and body["code"] != None):
      code = body["code"]
      message = body["message"]

      if (code != "0"):
        raise UniException(message, code, request_id=request_id)
      else:
        self.code = code
        self.message = message
        self.data = body["data"]
    else:
      raise UniException(status_text, -1, request_id=request_id)

    self.raw = res
    self.request_id = request_id
