class MoxfieldSearchAPI:

    def search_single(self, query):
        pageNum = 1
        params = {"q": query, "page": pageNum}
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        r = self.session.get('https://api.moxfield.com/v2/cards/search', params=params, headers=headers)
        r.raise_for_status()
        resp = r.json()

        if 'code' in resp and resp['code'] == 'not_found':
            return None

        return resp['data'][0]

    def search_named_fuzzy(self, query):
        params = {"fuzzy": query}
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        r = self.session.get('https://api.moxfield.com/v2/cards/named', params=params, headers=headers)
        r.raise_for_status()
        resp = r.json()

        if 'code' in resp and resp['code'] == 'not_found':
            return None

        return resp


    def __init__(self, session):
        self.session = session
        pass
    