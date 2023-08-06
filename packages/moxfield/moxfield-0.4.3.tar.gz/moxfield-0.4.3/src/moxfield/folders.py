# https://api.moxfield.com/v1/deck-folders/{folder-id}/decks/{deck-internal} POST (move) DELETE (remove)
# https://api.moxfield.com/v1/deck-folders/{folder-id}/ DELETE
# https://api.moxfield.com/v1/deck-folders?pageNumber=n&pageSize=n GET POST (no query params)
import urllib.parse

class MoxfieldDeckFoldersAPI:

    def create(self, name: str):
        payload = {"name": name}
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json'
        }
        r = self.session.post('https://api.moxfield.com/v1/deck-folders', json=payload, headers=headers)
        r.raise_for_status()
        resp = r.json()
        return MoxfieldSpecificDeckFolderAPI(resp['id'], self.session)

    def get(self):
        pageNum = 1
        params = {"pageNumber": pageNum, "pageSize": 100}
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        r = self.session.get('https://api.moxfield.com/v1/deck-folders', params=params, headers=headers)
        r.raise_for_status()
        resp = r.json()

        for pageNumber in range(2, resp['totalPages'] + 1):
            for obj in resp['data']:
                yield MoxfieldSpecificDeckFolderAPI(obj['id'], self.session)
            
            params['pageNumber'] = pageNumber
            r = self.session.get(f'https://api.moxfield.com/v2/decks/search', params=params, headers=headers)
            r.raise_for_status()
            resp = r.json()

    def __init__(self, session):
        self.session = session

class MoxfieldSpecificDeckFolderAPI:
    
    def remove_deck(self, specific_deck):
        deck = specific_deck.get()
        deck_id = deck['id']
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        r = self.session.delete(f'https://api.moxfield.com/v1/deck-folders/{self.folder_id}/decks/{deck_id}', headers=headers)
        r.raise_for_status()

    def add_deck(self, specific_deck):
        deck = specific_deck.get()
        deck_id = deck['id']
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        r = self.session.post(f'https://api.moxfield.com/v1/deck-folders/{self.folder_id}/decks/{deck_id}', headers=headers)
        r.raise_for_status()

    def delete(self):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        r = self.session.delete(f'https://api.moxfield.com/v1/deck-folders/{self.folder_id}', headers=headers)
        r.raise_for_status()

    def __init__(self, folder_id, session):
        self.folder_id = urllib.parse.quote(folder_id)
        self.session = session