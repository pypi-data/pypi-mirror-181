class UniException(Exception):
  def __init__(self, message, code, request_id=None):
    self.message = message
    self.code = code
    self.request_id = request_id

  def __str__(self):
    return "[{0}] {1}".format(self.code, self.message)
