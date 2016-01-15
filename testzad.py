import repozad
import sqlite3
import unittest

db_path = 'zbiory.db'

class RepositoryTest(unittest.TestCase):

    def setUp(self):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('DELETE FROM zadania')
        c.execute('DELETE FROM zbior')
        c.execute('''INSERT INTO zbior (id, przedmiot, ilosc) VALUES(1, 'Teoria reprezentacji', 19)''')
        c.execute('''INSERT INTO zadania (lista, amount, przedmiot_id) VALUES('Lista_1',14,1)''')
        c.execute('''INSERT INTO zadania (lista, amount, przedmiot_id) VALUES('Lista_2',5,1)''')
        conn.commit()
        conn.close()


    def tearDown(self):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('DELETE FROM zadania')
        c.execute('DELETE FROM zbior')
        conn.commit()
        conn.close()

    def testGetByIdInstance(self):
        przedmiot = repozad.przedmiotRepository().getById(1)
        self.assertIsInstance(przedmiot, repozad.przedmiot, "Objekt nie jest klasy przedmiot")


    def testGetByIdNotFound(self):
        self.assertEqual(repozad.przedmiotRepository().getById(22),
                None, "Powinno wyjść None")

    def testGetByIdInvitemsLen(self):
        self.assertEqual(len(repozad.przedmiotRepository().getById(1).zestaw),
                2, "Powinno wyjść 2")

    def testDeleteNotFound(self):
        self.assertRaises(repozad.RepositoryException,
                repozad.przedmiotRepository().delete, 22)



if __name__ == "__main__":
      unittest.main()