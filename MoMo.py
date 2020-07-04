import json
import urllib.request
import uuid
import hmac
import hashlib
import webbrowser

# parameters send to MoMo get get payUrl
endpoint = "https://test-payment.momo.vn/gw_payment/transactionProcessor"
partnerCode = "MOMO"
accessKey = "F8BBA842ECF85"
serectkey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
orderInfo = "pay with MoMo"
returnUrl = "https://momo.vn/return"
notifyurl = "https://dummy.url/notify"
amount = "50000"
orderId = str(uuid.uuid4())
requestId = str(uuid.uuid4())
requestType = "captureMoMoWallet"
# pass empty value if your merchant does not have stores else merchantName=[storeName]; merchantId=[storeId] to identify a transaction map with a physical store
extraData = "merchantName=;merchantId="

# before sign HMAC SHA256 with format
# partnerCode=$partnerCode&accessKey=$accessKey&requestId=$requestId&amount=$amount&orderId=$oderId&orderInfo=$orderInfo&returnUrl=$returnUrl&notifyUrl=$notifyUrl&extraData=$extraData
rawSignature = "partnerCode=" + partnerCode + "&accessKey=" + accessKey + "&requestId=" + requestId + "&amount=" \
               + amount + \
               "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&returnUrl=" + \
               returnUrl + "&notifyUrl=" + notifyurl + "&extraData=" + extraData

# puts raw signature
print("--------------------RAW SIGNATURE----------------")
print(rawSignature)
# signature
# h=hmac.new(b'serectkey', data.encode('utf-8'), hashlib.sha256).hexdigest()
# h = hmac.new(b'serectkey', rawSignature.encode('utf-8'), hashlib.sha256)
h = hmac.new(serectkey.encode('utf-8'), rawSignature.encode('utf-8'), hashlib.sha256)

signature = h.hexdigest()
print("--------------------SIGNATURE----------------")
print(signature)

# json object send to MoMo endpoint

data = {
    'partnerCode': partnerCode,
    'accessKey': accessKey,
    'requestId': requestId,
    'amount': amount,
    'orderId': orderId,
    'orderInfo': orderInfo,
    'returnUrl': returnUrl,
    'notifyUrl': notifyurl,
    'extraData': extraData,
    'requestType': requestType,
    'signature': signature
}
print("--------------------JSON REQUEST----------------\n")

# from obj in python to string by json.dumps then convert to binary
data = str.encode(json.dumps(data))

print(data)

clen = len(data)

print(data)
req = urllib.request.Request(endpoint, data, {'Content-Type': 'application/json', 'Content-Length': clen})

f = urllib.request.urlopen(req)

print(f)
response = f.read()
f.close()
print("--------------------JSON response----------------\n")
print(response)

print("payUrl\n")
url = json.loads(response)['payUrl']

urllib.request.urlopen(url)

# open url return by MoMo
webbrowser.open(url)
