import requests
cookie_jar = requests.cookies.RequestsCookieJar()
cookie_jar.set("session", "eyJ0ZWFtX3Rva2VuIjoiYmNjMWI2ZDgtYjI4Mi00MmRkLWFjNmUtMmJlMTJhNDhkZTlkIn0.asn8mQ.gVj7rTF92DEzB4aWr4imi3yNEqY", domain="localhost")
r = requests.get("http://localhost:8080/api/check_stage6_access", cookies=cookie_jar)
print("Status:", r.status_code)
