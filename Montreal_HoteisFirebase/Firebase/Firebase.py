import pyrebase, json


class FirebaseHoteis(object):

    def __init__(self):
        self.__firebaseConfig = {
                                    "apiKey": "AIzaSyCISPE_NAop9Y9qjnQTBdv1tVisNHN4D1Y",
                                    "authDomain": "montreal-hoteis.firebaseapp.com",
                                    "databaseURL": "https://montreal-hoteis.firebaseio.com",
                                    "projectId": "montreal-hoteis",
                                    "storageBucket": "montreal-hoteis.appspot.com",
                                    "messagingSenderId": "422296887431",
                                    "appId": "1:422296887431:web:55410d24e9044259fbd822",
                                    "measurementId": "G-XBYLSV3NSV"
                                }
        self.__firebase = pyrebase.initialize_app(self.__firebaseConfig)
        self.auth = self.__firebase.auth().sign_in_with_email_and_password('luiz.lemos@clubemontreal.com.br',
                                                                           'Luiz@10284355')
        self.database = self.__firebase.database()

    def set_data(self, child, data):
        return self.database.child(child).set(data, self.auth['idToken'])


