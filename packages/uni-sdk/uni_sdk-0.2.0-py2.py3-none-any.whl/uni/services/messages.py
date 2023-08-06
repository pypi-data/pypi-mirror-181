class MessageService(object):

  def __init__(self, client):
    self.client = client

  def send(self, params):
    return self.client.request("sms.message.send", params)
