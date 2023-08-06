import urllib.parse
from typing import Dict
from uuid import uuid4

class MoxfieldDeckAPI:

    def create(self, name: str = None, deck: Dict[str, int] = None, format='none', visibility: str = 'public'):
        if name is None:
            name = str(uuid4())
        if deck is None:
            deck = {}
        payload = {
            'name': name,
            'format': format,
            'visibility': visibility,
            'importText': '\n'.join(f'{val} {key}' for key, val in deck.items()),
            'playStyle': 'paperDollars',
            'pricingProvider': 'tcgplayer'
        }
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json'
        }
        r = self.session.post(url="https://api.moxfield.com/v2/decks", json=payload, headers=headers)
        r.raise_for_status()
        resp = r.json()
        return MoxfieldSpecificDeckAPI(resp['publicId'], self.session)

    def __getitem__(self, public_id):
        return MoxfieldSpecificDeckAPI(public_id, self.session)

    def __init__(self, session):
        self.session = session


class MoxfieldSpecificDeckAPI:

    def bulk_edit(self, mainboard, sideboard, maybeboard):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        json = {
            "mainboard":'\n'.join(f'{value} {key}' for key, value in mainboard.items()),
            "sideboard":'\n'.join(f'{value} {key}' for key, value in sideboard.items()),
            "maybeboard":'\n'.join(f'{value} {key}' for key, value in maybeboard.items()),
            "playStyle":"paperDollars",
            "pricingProvider":"tcgplayer"
        }
        url = f'https://api.moxfield.com/v2/decks/{self.public_id}/bulk-edit'
        r = self.session.put(url, json=json, headers=headers)
        return r.json()

    def get(self):
        public_id = urllib.parse.quote(self.public_id, safe='')
        r = self.session.get(
            f'https://api.moxfield.com/v2/decks/all/{public_id}')
        
        r.raise_for_status()

        return r.json()

    def delete(self):
        deck = self.get()
        deck_internal_id = deck['id']
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        url = f'https://api.moxfield.com/v1/decks/{deck_internal_id}'
        r = self.session.delete(url, headers=headers)
        r.raise_for_status()

    def __init__(self, public_id, session):
        self.public_id = urllib.parse.quote(public_id, safe='')
        self.commanders = MoxfieldSpecificDeckCommandersAPI(self, session)
        self.mainboard = MoxfieldSpecificDeckCardsAPI(self, session, 'mainboard')
        self.sideboard = MoxfieldSpecificDeckCardsAPI(self, session, 'sideboard')
        self.maybeboard = MoxfieldSpecificDeckCardsAPI(self, session, 'maybeboard')
        self.comments = MoxfieldSpecificDeckCommentsAPI(self, session)
        self.session = session
        pass

class MoxfieldSpecificDeckCommandersAPI:

    def set(self, commander_ids):
        json = {
            "clearCommanders": True
        }

        commander_id, partner_id = commander_ids

        if commander_id is not None:
            json['commanderCardId'] = str(commander_id)
            if partner_id is not None:
                json['partnerCardId'] = str(partner_id)

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
        }

        deck = self.deck.get()
        deck_id = deck['id']

        url = f'https://api.moxfield.com/v2/decks/{deck_id}/commanders'
        r = self.session.put(url, json=json, headers=headers)
        r.raise_for_status()
        return r

    def __init__(self, deck, session):
        self.deck = deck
        self.session = session
        pass

class MoxfieldSpecificDeckCommentsAPI:

    def create(self, text: str):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        json = {
            "text": text
        }
        url = f'https://api.moxfield.com/v1/decks/all/{self.deck.public_id}/comments'
        r = self.session.post(url, json=json, headers=headers)
        return r.json()

    def __init__(self, deck, session):
        self.deck = deck
        self.session = session

class MoxfieldSpecificDeckCardsAPI:

    def set(self, card_id, card_amount):
        deck = self.deck.get()
        deck_id = deck['id']
        deck_board = deck[self.board]

        value = 0
        for obj in deck_board.values():
            if obj['card']['id'] == card_id:
                value = obj['quantity']

        # No change in card value
        if value == card_amount:
            return

        json = {
            'cardId': card_id, 
            'quantity': card_amount
        }

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
        }

        url_card_id = urllib.parse.quote(card_id, safe='')

        r = None
        if value == 0:
            url = f'https://api.moxfield.com/v2/decks/{deck_id}/cards/{self.board}'
            r = self.session.post(url, json=json, headers=headers)
        elif card_amount == 0:
            url = f'https://api.moxfield.com/v2/decks/{deck_id}/cards/{self.board}/{url_card_id}'
            r = self.session.delete(url, headers=headers)
        else:
            url = f'https://api.moxfield.com/v2/decks/{deck_id}/cards/{self.board}/{url_card_id}'
            r = self.session.put(url, json=json, headers=headers)
        
        r.raise_for_status()
        return r

    def __init__(self, deck, session, board):
        self.deck = deck
        self.session = session
        self.board = board