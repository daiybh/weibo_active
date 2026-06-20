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
    #print(response.text)

    token = response.json()["data"]["token"]


    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {token}"}
    url = f"{baseURL}/envs?t={(int(datetime.datetime.now().timestamp() * 1000))}"
    data = {"id": "1","name": "WEIBO_COOKIE", "value": WEIBO_COOKIE, "remarks": datetime.datetime.now().ctime()}
    response = requests.put(url, headers=headers, json=data)
    print(f"正在更新 {clientID} 的环境变量 WEIBO_COOKIE...")
    print(response.json())

    url = f"{baseURL}/crons?t={(int(datetime.datetime.now().timestamp() * 1000))}"
    data = {"id": "1","name": "WEIBO_COOKIE", "value": WEIBO_COOKIE, "remarks": datetime.datetime.now().ctime()}
    response = requests.get(url, headers=headers)
    print(f"正在获取 {clientID} 的 cron 信息...")
    print(response.json())
    cron_data = response.json()["data"]["data"]
    print(f"当前 {clientID} 的 cron 数量为 {len(cron_data)}")
    cronTask=['qlpublic','weibo 超话签到']
    for cron in cron_data:
        if cron["name"] in cronTask:
            url = f"{baseURL}/crons/stop?t={(int(datetime.datetime.now().timestamp() * 1000))}"
            response = requests.put(url, headers=headers,json=[cron["id"]])
            import time
            time.sleep(1)
            url = f"{baseURL}/crons/run?t={(int(datetime.datetime.now().timestamp() * 1000))}"
            print(f"正在run {clientID} 的 cron {cron['name']}  id {cron['id']}...")
            response = requests.put(url, headers=headers,json=[cron["id"]])
            print(response.status_code)
            print(response.text)
            time.sleep(1)

    



if __name__ == "__main__":
    update_env()


