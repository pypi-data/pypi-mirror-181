import requests
import json

def create(url, uploadType, shot, resourceId, filePath, volumeName):
    url_path = f"{url}/qcc/job"

    headers = {
        #"Content-Type": "application/x-www-form-urlencoded"
        "Content-Type": "application/json"
    }

    data = json.dumps({
        "uploadType": uploadType,
        "shot": shot,
        "resourceId": resourceId,
        "filePath": filePath,
        "volumeName": volumeName
    })

    # params = {
    #     "namespace": f"{nameSpace}"
    # }

    response = requests.post(f"{url_path}", headers=headers, data=data) 

    print("[Job CREATE] ",response.text, flush=True)

    return response.text

def getList(url):
    url_path = f"{url}/qcc/jobs"

    # params = {
    #     "volumeName": volumeName,
    #     "hostPath": hostPath
    # }

    response = requests.get(f"{url_path}") # , params=params)

    print("[Job LIST] ", response.text, flush=True)

    return response.text
