import requests
import config
import time

LOGIN_URL = config.LOGIN_URL
JSON_URL = config.JSON_URL
REFRESH_URL = config.REFRESH_URL

username = config.DIRECTUS_USERNAME
password = config.DIRECTUS_PASSWORD

loggedIn = False
needsRefresh = True

refreshToken = ""
accessToken = ""
refreshTimer = time.time()

def loginAction():
    print("login")
    print(JSON_URL + " login")
    request = requests.post(LOGIN_URL,
                            headers={"Accept": "application/json", "Content-Type": "application/json; charset=utf-8"},
                            json={"email": username, "password": password})
    if request.status_code == 200:
        responseJSON = request.json()
        accessToken = responseJSON["data"]["access_token"]
        print(accessToken)
        refreshToken = responseJSON["data"]["refresh_token"]
        loggedIn = True
        dataAction(loggedIn,accessToken)
        return refreshToken

    else:
        print(request.text)


def refreshLogin(refreshToken):
    print('refreshLogin()')
    refresh = refreshToken
    if needsRefresh:
        loggedIn = False
        print(REFRESH_URL + " login")

        request = requests.post(REFRESH_URL,
                                headers={"Accept": "application/json",
                                         "Content-Type": "application/json; charset=utf-8"},
                                json={"refresh_token": refresh})
        if request.status_code == 200:
            responseJSON = request.json()
            accessToken = responseJSON["data"]["access_token"]
            refresh = responseJSON["data"]["refresh_token"]
            loggedIn = True
            dataAction(loggedIn,accessToken)
            return refresh
        else:
            print(request.text)

def dataAction(loggedIn,accessToken):
    if loggedIn:
        print("dataAction()")
        request = requests.get(JSON_URL,
                               headers={"Authorization": f"Bearer {accessToken}", "Accept": "application/json"})
        if request.status_code == 200:
            print(request.json())
        else:
            print(request.text)
        return loggedIn,accessToken



def main():

    refreshToken = loginAction()

    if time.time() - refreshTimer > 3:
        needsRefresh = True
        refreshLogin(refreshToken)

if __name__ == "__main__":
    main()