import sqlite3
from scipy import stats
import numpy as np


db_path = 'zbiory.db'

class RepositoryException(Exception):
    def __init__(self, message, *errors):
        Exception.__init__(self, message)
        self.errors = errors

class przedmiot():
    def __init__(self, id, nazwa, zestaw=[] ):
        self.id = id
        self.nazwa = nazwa
        self.zestaw = zestaw
        self.ilosc = sum([item.amount for item in self.zestaw])

    def __repr__(self):
        return "<pr(id='%s', nazwa='%s', amount='%s', zestaw='%s')>" % (
                    self.id, self.nazwa, str(self.ilosc), str(self.zestaw))


class kartka():
    def __init__(self, lista, amount):
        self.lista = lista
        self.amount = amount

    def __repr__(self):
        return "<kartka(lista='%s', amount='%s')>" % (
                    self.lista, str(self.amount)
                )

class Repository():
    def __init__(self):
        try:
            self.conn = self.get_connection()
        except Exception as e:
            raise RepositoryException('GET CONNECTION:', *e.args)
        self._complete = False

    # wejście do with ... as ...
    def __enter__(self):
        return self

    # wyjście z with ... as ...
    def __exit__(self, type_, value, traceback):
        self.close()

    def complete(self):
        self._complete = True

    def get_connection(self):
        return sqlite3.connect(db_path)

    def close(self):
        if self.conn:
            try:
                if self._complete:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            except Exception as e:
                raise RepositoryException(*e.args)
            finally:
                try:
                    self.conn.close()
                except Exception as e:
                    raise RepositoryException(*e.args)

class przedmiotRepository(Repository):

    def add(self, przedmiot):


        try:
            c = self.conn.cursor()

            ilosc = sum([item.amount for item in przedmiot.zestaw])
            c.execute('INSERT INTO zbior (id, przedmiot, ilosc) VALUES(?, ?, ?)',
                        (przedmiot.id, str(przedmiot.nazwa), przedmiot.ilosc)
                    )

            if przedmiot.zestaw:
                for karta in przedmiot.zestaw:
                    try:
                        c.execute('INSERT INTO zadania (lista, amount, przedmiot_id) VALUES(?,?,?)',
                                        (karta.lista, karta.amount, przedmiot.id)
                                )
                    except Exception as e:
                        #print "item add error:", e
                        raise RepositoryException('error adding przedmiot item: %s, to przedmiot: %s' %
                                                    (str(karta), str(przedmiot.id))
                                                )
        except Exception as e:
            #print " add error:", e
            raise RepositoryException('error adding przedmiot %s' % str(przedmiot))

    def delete(self, przedmiot):

        try:
            c = self.conn.cursor()
            # usuń pozycje
            c.execute('DELETE FROM zadania WHERE przedmiot_id=?', (przedmiot.id,))
            # usuń nagłowek
            c.execute('DELETE FROM zbior WHERE id=?', (przedmiot.id,))

        except Exception as e:
            #print "invoice delete error:", e
            raise RepositoryException('error deleting przedmiot %s' % str(przedmiot))

    def getById(self, id):
        """Get invoice by id
        """
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM zbior WHERE id=?", (id,))
            przedmiot_row = c.fetchone()
            p = przedmiot(id=id, nazwa=przedmiot_row[1])
            if przedmiot_row == None:
                p=None
            else:
                p.nazwa = przedmiot_row[1]
                p.ilosc = przedmiot_row[2]
                c.execute("SELECT * FROM zadania WHERE przedmiot_id=? order by lista", (id,))
                przedmiot_items_rows = c.fetchall()
                items_list = []
                for item_row in przedmiot_items_rows:
                    item = kartka(lista=item_row[0], amount=item_row[1],)
                    items_list.append(item)
                p.zestaw=items_list
        except Exception as e:
            #print "invoice getById error:", e
            raise RepositoryException('error getting by id przedmiot_id: %s' % str(id))
        return p


    def update(self, przedmiot):

        try:
            # pobierz z bazy fakturę
            oryg = self.getById(przedmiot.id)
            if oryg != None:
                # faktura jest w bazie: usuń ją
                self.delete(przedmiot)
            self.add(przedmiot)

        except Exception as e:
            #print "invoice update error:", e
            raise RepositoryException('error updating invoice %s' % str(invoice))




if __name__ == '__main__':
    try:
        with przedmiotRepository() as przedmiot_repository:
            przedmiot_repository.add(
                przedmiot(id = 1, nazwa = "Teoria Reprezentacji",
                        zestaw = [
                            kartka(lista = "Teoria grup", amount = 15),
                            kartka(lista = "Macierze", amount = 10),
                            kartka(lista = "Reprezentacje", amount = 15),
                            kartka(lista = "Charaktery 1", amount = 4),
                            kartka(lista = "Charaktery 2", amount = 15),
                            kartka(lista = "Charaktery 3", amount = 13),
                            kartka(lista = "Algebry", amount = 9),
                            kartka(lista = "Reprezentacje indukowane", amount = 12),
                        ]
                    )
                )
            przedmiot_repository.complete()
    except RepositoryException as e:
        print(e)



    try:
        with przedmiotRepository() as przedmiot_repository:
            przedmiot_repository.add(
                przedmiot(id = 2, nazwa = "Teoria optymalizacji",
                        zestaw = [
                            kartka(lista = "Zagadnienia PL i PM", amount = 8),
                            kartka(lista = "Funkcja użyteczności", amount = 8),
                            kartka(lista = "Ortogonalizacja Gramma-Schmidta", amount = 12),
                            kartka(lista = "Metoda Symplex 1", amount = 6),
                            kartka(lista = "Metoda Symplex 2", amount = 7),
                            kartka(lista = "Zadania dualne", amount = 5),
                        ]
                    )
                )
            przedmiot_repository.complete()
    except RepositoryException as e:
        print(e)


    try:
        with przedmiotRepository() as przedmiot_repository:
            przedmiot_repository.add(
                przedmiot(id = 3, nazwa = "Metody numeryczne w finansach",
                        zestaw = [
                            kartka(lista = "Metoda Eulera", amount = 8),
                            kartka(lista = "Ruch Browna", amount = 9),
                            kartka(lista = "Całka Ito i lemat Ito", amount = 7),

                        ]
                    )
                )
            przedmiot_repository.complete()
    except RepositoryException as e:
        print(e)

    print(przedmiotRepository().getById(1))
    print(przedmiotRepository().getById(2))
    print(przedmiotRepository().getById(3))



    try:
        with przedmiotRepository() as przedmiot_repository:
            przedmiot_repository.update(
                przedmiot(id = 3,nazwa = "Teoria miary i całki",
                        zestaw = [
                            kartka(lista = "Miara zewnętrzna", amount = 8),
                            kartka(lista = "Zbiór Cantora", amount = 5),
                            kartka(lista = "Całka Lebesquea", amount = 10),
                        ]
                    )
                )
            przedmiot_repository.complete()
    except RepositoryException as e:
        print(e)



    print(przedmiotRepository().getById(1))
    print(przedmiotRepository().getById(2))
    print(przedmiotRepository().getById(3))


    n, (smin, smax), sm, sv, ss, sk = stats.describe([93,46,42])
    sstr = 'mean = %6.4f, variance = %6.4f, skew = %6.4f, kurtosis = %6.4f'
    print ('statystyka zbioru zadań na przedmiot:')
    print (sstr %(sm, sv, ss, sk))