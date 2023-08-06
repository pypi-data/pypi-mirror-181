from monicahq import Session
import requests, json

class Client():
    def __init__(self, session):
        """Initialize based upon a session"""
        if type(session) != Session.Session:
            raise TypeError(f"session variable is not of type monicahq.Session.Session, but {type(session)}")

        self.session = session

    def search_contacts(self, limit=100,page=1):
        """Get list of contacts as JSON"""

        url = f"{self.session.url}/contacts?limit={limit}&page={page}"
        r = requests.get(url, headers=self.session.headers)
        return json.loads(r.text)

    def get_contat(self, id):
        """Get contact by id as JSON"""

        url = f"{self.session.url}/contacts/{id}"
        r = requests.get(url, headers=self.session.headers)
        return json.loads(r.text)

    def search_reminders(self, limit=100,page=1):
        """Get list of reminders as JSON"""

        url = f"{self.session.url}/reminders?limit={limit}&page={page}"
        r = requests.get(url, headers=self.session.headers)
        return json.loads(r.text)

    def get_reminder(self, id):
        """Get reminders by id as JSON"""

        url = f"{self.session.url}/reminders/{id}"
        r = requests.get(url, headers=self.session.headers)
        return json.loads(r.text)