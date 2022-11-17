import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):
    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))


class ExceptionTest(unittest.TestCase):
    def test_too_many_products(self):
        products = [Product('PP234', 2), Product('PP235', 2), Product('PP236', 2), Product('PP237', 2), Product('PP238', 2), Product('PP239', 2), Product('PP240', 2), Product('PP241', 2)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(client.get_total_price(2), None)


class EmptyEntryListTest(unittest.TestCase):
    def test_too_many_products(self):
        products = [Product('1P234', 2), Product('PP23', 2), Product('&P234', 2), Product('P*234', 2),
                    Product('P123*', 2), Product('P12P', 2), Product('PPP', 2), Product('1233', 2)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(client.get_total_price(1), None)

#TODO testy dla różnych długości n = [1, 2, 3, ...]
#TODO dane wejściowe dobre, część może być zła np ilość liter nie zawierająca się w n

class DiffrentN_letterTest(unittest.TestCase):
    def test_too_many_products(self):
        products = [Product('P12', 1), Product('P13', 1), Product('P14', 1), Product('P1P', 1), Product('P2P', 1),
                    Product('PP12', 2), Product('PP13', 2), Product('PP14', 2), Product('PP1P', 2), Product('PP2P', 2),
                    Product('PPP12', 3), Product('PPP13', 3), Product('PPP14', 3), Product('PPP1P', 3), Product('PPP2P', 3),
                    Product('PPPP12', 4), Product('PPPP13', 4), Product('PPPP14', 4), Product('PPPP1P', 4), Product('PPPP2P', 4)]
        n_entries = [1, 2, 3, 4]
        proper_results = [3, 6, 9, 12]
        for server_type in server_types:
            for n, expected in zip(n_entries, proper_results):
                server = server_type(products)
                client = Client(server)
                self.assertEqual(client.get_total_price(n), expected)

if __name__ == '__main__':
    unittest.main()