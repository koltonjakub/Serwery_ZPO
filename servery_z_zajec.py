#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, List, Dict
from abc import abstractmethod
from copy import deepcopy
from re import fullmatch


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty
    #  wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności --
    #  i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)

    def __init__(self, name: str, price: float):
        if isinstance(name, str) and (isinstance(price, float) or isinstance(price, int)):
            self.name = name
            self.price = float(price)
        else:
            print(type(name), type(price))
            raise WrongProductInitialData

    def __eq__(self, other):
        if isinstance(other, Product):
            if self.name == other.name and self.price == other.price:
                return True
            return False
        return False  # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


class WrongProductInitialData(Exception):
    # Wyjątek związany ze złymi danymi produktu
    pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class Server:  # Interfejs dla ListServer i MapServer
    '''Interfejs nie trzyma żadnych pól klasy
    '''
    # @abstractmethod
    # def get_list_of_products(self) -> List[Product]:


    @abstractmethod
    def get_entries(self, n_letters) -> List[Product]:
        pass


class ListServer(Server):
    def __init__(self, products: List[Product]):
        self.products = [Product(p.name, p.price) for p in deepcopy(products)]
        self.n_max = 7

    def get_entries(self, n_letters) -> List[Product]:
        self.pattern = '^[a-zA-Z]{n}[0-9]{2,3}$'.replace('n',str(n_letters))
        self.found_products = [p for p in self.products if fullmatch(self.pattern, p.name)]
        if len(self.found_products) > self.n_max:
            raise TooManyProductsFoundError
        else:
            return sorted(self.found_products, key=lambda x: x.price)

class MapServer(Server):
    def __init__(self, products: List[Product]):
        self.products = [p.name for p in deepcopy(products)]


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        raise NotImplementedError()

# test
