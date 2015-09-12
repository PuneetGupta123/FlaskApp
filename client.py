import requests

heading = 'this is the heading '
detail = 'this is the detail'
cid = '2'
content = 'you can contact me'
eid = '5'
uid = '2'

burl = 'http://192.168.208.1:5000/'
url = burl# + 'addreply?uid=' + str(uid) + '&content=' + str(content) + '&eid=' + str(cid)


r = requests.get(url)
print r.text
