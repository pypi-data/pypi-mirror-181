import os
import http.client
import urllib.parse
import time
import hmac
import json
from unisdk.response import UniResponse
from unisdk.exception import UniException
from unisdk.__version__ import __version__

class Uni:
  name = "uni-python-sdk"
  version = __version__

  def __init__(self, access_key_id, access_key_secret, endpoint="uni.apistd.com", signing_algorithm="hmac-sha256"):
    self.access_key_id = access_key_id
    self.access_key_secret = access_key_secret
    self.endpoint = endpoint
    self.signing_algorithm = signing_algorithm
    self.hmac_algorithm = signing_algorithm.split("-")[1]

  def __sign(self, query):
    if (self.access_key_secret != None):
      query["algorithm"] = self.signing_algorithm
      query["timestamp"] = int(time.time())
      query["nonce"] = os.urandom(8).hex()

      sorted_query = sorted(query.items(), key=lambda x:x[0])
      str_to_sign = urllib.parse.urlencode(sorted_query)
      h = hmac.new(bytes(self.access_key_secret, "utf8"), bytes(str_to_sign, "utf8"), digestmod=self.hmac_algorithm)
      query["signature"] = h.hexdigest()

    return query;

  def request(self, action, data):
    conn = http.client.HTTPSConnection(self.endpoint)
    headers = {
      "User-Agent": self.name + "/" + self.version,
      "Content-Type": "application/json;charset=utf-8",
      "Accept": "application/json",
    }
    query = {
      "action": action,
      "accessKeyId": self.access_key_id
    }
    query = self.__sign(query)
    query_str = urllib.parse.urlencode(query)
    conn.request("POST", "/?" + query_str, json.dumps(data), headers)
    res = conn.getresponse()
    return UniResponse(res)
