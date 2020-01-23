import requests

#
# register_url = "http://127.0.0.1:8000/user/register"
# res = requests.post(register_url, data={'username': '13777893888', 'password': 'Lly19980726.'})
# print(res.text)
#
login_url = "http://127.0.0.1:8000/user/login"
res = requests.post(login_url, data={'username': '13777893886', 'password': 'Lly19980726.'})
print(res.text)

# recharge_url = "http://127.0.0.1:8000/user/recharge"
# res = requests.post(recharge_url, data={'username': '13777893886', 'card_number': '10000', 'password':
#     'El2O4ip3XPaFFFj'})
# print(res.text)