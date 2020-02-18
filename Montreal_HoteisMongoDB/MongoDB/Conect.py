from pymongo import MongoClient


class Conect(object):

    def __init__(self):
        self.user, self.__password = 'montreal-python', 'montreal-db-12rPYh'
        self.client = MongoClient(f'mongodb://{self.user}:{self.__password}@ds249583.mlab.com:49583/montreal-hoteis',
                                  retryWrites=False)


if __name__ == '__main__':
    conect = Conect()
    db = conect.client['montreal-hoteis']
    from Montreal_HoteisMongoDB.DAO.Hoteis.HoteisBancoMontrealDAO import HoteisBancoMontrealDTO

    a = HoteisBancoMontrealDTO().parceiros().head(n=3)
    print(list(a.to_dict(orient='index').values()))
    # db.hoteis.insert_many(a)

