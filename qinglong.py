import requests
import datetime
import dotenv
dotenv.load_dotenv()
import os   
baseURL = f"{os.getenv('qinglong_baseURL')}/open"
clientID = os.getenv('qinglong_clientID')
clientSecret = os.getenv('qinglong_clientSecret')


def update_env(WEIBO_COOKIE=""):
#GET /open/auth/token
    if not WEIBO_COOKIE:
        WEIBO_COOKIE = os.getenv('WEIBO_COOKIE')
    if not WEIBO_COOKIE:
        return
    print(f"正在获取 {clientID} 的 access_token...")
    url=f"{baseURL}/auth/token"
    print(url)
    response = requests.get(url, params={"client_id": clientID, "client_secret": clientSecret})
    print(response.text)

    token = response.json()["data"]["token"]


    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {token}"}
    url = f"{baseURL}/envs?t={(int(datetime.datetime.now().timestamp() * 1000))}"
    data = {"id": "1","name": "WEIBO_COOKIE", "value": WEIBO_COOKIE, "remarks": datetime.datetime.now().ctime()}
    response = requests.put(url, headers=headers, json=data)
    print(response.json())

    url = f"{baseURL}/crons?t={(int(datetime.datetime.now().timestamp() * 1000))}"
    data = {"id": "1","name": "WEIBO_COOKIE", "value": WEIBO_COOKIE, "remarks": datetime.datetime.now().ctime()}
    response = requests.get(url, headers=headers)
    print(response.json())

    print(f"正在run {clientID} 的 cron...")
    url = f"{baseURL}/crons/run?t={(int(datetime.datetime.now().timestamp() * 1000))}"
    data = [1,2]
    response = requests.put(url, headers=headers,json=data)
    print(response.json())



if __name__ == "__main__":
    update_env()


