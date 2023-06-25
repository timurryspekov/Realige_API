import requests


def api_request(file_name):

    
    url = 'http://192.168.1.32:9090'
    url = url+'/uploader'
    files = {'file': open(file_name, 'rb')}

    r = requests.post(url, files=files)
    return r.text


file_name = input('File name:')

print(api_request(file_name))
