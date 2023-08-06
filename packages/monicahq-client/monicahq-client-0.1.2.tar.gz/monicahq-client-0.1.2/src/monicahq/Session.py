"""Set up a session with the monicahq server"""

import requests, json

class Session():
    def __init__(self, host, token):
        """Initialize using hostname and token"""
        self.token = f'Bearer {token}'
        self.headers = {'Authorization': self.token}
        self.host = host
        self.url = f"https://{self.host}/api"

    def create(self):
        """Create the session"""
        r=requests.get(self.url,headers=self.headers)
        data = json.loads(r.text)
        try:
            data['success']
            return True
        except:
            return False
        