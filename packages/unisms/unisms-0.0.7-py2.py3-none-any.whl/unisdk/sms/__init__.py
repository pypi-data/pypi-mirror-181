from uni.client import UniClient

class UniSMS:
  def __init__(self, *args, **kwargs):
    self.client = UniClient(*args, **kwargs)
    self.client.endpoint = 'https://uni.apistd.com'

  def send(self, params):
    return self.client.messages.send(params)
