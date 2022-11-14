#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, List, Dict
from abc import abstractmethod
from copy import deepcopy
from re import fullmatch


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu
    #  (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.price == other.price and self.name == other.name
        raise IncorrectTypeOfParamError
          # FIXME: zwróć odpowiednią wartość
    
    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError(BaseException):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass

class IncorrectTypeOfParamError(BaseException):
    # Reprezentuje wyjątek związany z porównywaniem niewłaściwych typów z produktem
    pass

# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z
#   typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną
#   dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class Server:
    @abstractmethod
    def get_entries(self, n_letters: int) -> List[Product]:
        pass

class ListServer(Server):
    def __init__(self, products: List[Product]):
        self.products = [Product(p.name, p.price) for p in deepcopy(products)]
        self.n_max_returned_entries = 7

    def get_entries(self, n_letters: int) -> List[Product]:
        pattern = '^[a-zA-Z]{n}[0-9]{2,3}$'.replace('n',str(n_letters))
        found_products = [p for p in self.products if fullmatch(pattern, p.name)]
        if len(found_products) > self.n_max_returned_entries:
            raise TooManyProductsFoundError
        return sorted(found_products, key=lambda x: x.price)

class MapServer(Server):
    # typ dict, kluczem jest nazwa produktu, wartością – obiekt reprezentujący produkt
    def __init__(self, products: List[Product]):
        self.products = {p.name: Product(p.name, p.price) for p in deepcopy(products)}
        self.n_max_returned_entries = 7

    def get_entries(self, n_letters: int) -> List[Product]:
        pattern = '^[a-zA-Z]{n}[0-9]{2,3}$'.replace('n',str(n_letters))
        found_products = [p for name, p in self.products.items() if fullmatch(pattern, p.name)]
        if len(found_products) > self.n_max_returned_entries:
            raise TooManyProductsFoundError
        return sorted(found_products, key=lambda x: x.price)

class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server: Server):
        self.server = server


    def get_total_price(self, n_letters: Optional[int] = 1) -> Optional[float]:
        try:
            found_products = self.server.get_entries(n_letters)
        except TooManyProductsFoundError:
            return None
        else:
            if len(found_products) == 0:
                return None
            else:
                return sum([p.price for p in found_products])
    

