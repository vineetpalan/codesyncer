import base64
import json
import requests


class GitHub(object):

    def __init__(self):
        self.headers = {'User-Agent': 'vineetpalan', 'Authorization': 'token 5afea47dd1ded252c0590c84e4159d5ee0c'}

    def get_data(self,file_name,message):
        data = {
            "message": message,
            "committer": {
                "name": "Vineet Palan",
                "email": "vineetpalan@gmail.com" },
            "content": self.get_base64_contents(file_name)
        }
        return data

    def get_base64_contents(self,file_name):
        with open(file_name, 'r') as myfile:
            file_content = myfile.read()
        encoded_file =  base64.b64encode(file_content.encode("utf-8"))
        return encoded_file

    def add_to_hackerrank_git(self,file_name,message):
        url = 'https://api.github.com/repos/vineetpalan/hackerrank/contents/'
        response = requests.put(url + message + '.java', data=json.dumps(self.get_data(file_name,message)), headers=self.headers)
        print response.content
