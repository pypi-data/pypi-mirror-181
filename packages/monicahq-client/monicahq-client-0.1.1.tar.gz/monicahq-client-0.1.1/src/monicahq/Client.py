from monicahq import Session
import requests, json

class Client():
    def __init__(self, session):
        """Initialize based upon a session"""
        if type(session) != Session.Session:
            raise TypeError(f"session variable is not of type monicahq.Session.Session, but {type(session)}")

        self.session = session

    def search_contacts(self, count=100):
        """Get list of contacts as JSON"""

        url = f"{self.session.url}/contacts?limit={count}"
        r = requests.get(url, headers=self.session.headers)
        return json.loads(r.text)