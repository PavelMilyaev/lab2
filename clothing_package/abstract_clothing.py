from abc import ABC, abstractmethod


class Clothing(ABC):
    """Абстрактный базовый класс для одежды"""

    def __init__(self, name: str, size: int, fabric_price: float, accessories_price: float):
        self._name = name
        self._size = size
        self._fabric_price = fabric_price
        self._accessories_price = accessories_price
        self._fabric_consumption = 0.0

    @property
    def name(self):
        return self._name

    @property
    def size(self):
        return self._size

    @property
    def fabric_price(self):
        return self._fabric_price

    @property
    def accessories_price(self):
        return self._accessories_price

    @abstractmethod
    def calculate_fabric_consumption(self) -> float:
        """Расчёт расхода ткани"""
        pass

    @abstractmethod
    def calculate_sewing_cost(self) -> float:
        """Расчёт стоимости пошива"""
        pass

    def calculate_total_cost(self) -> float:
        """Общая стоимость изделия"""
        fabric_cost = self.calculate_fabric_consumption() * self._fabric_price
        return fabric_cost + self._accessories_price

    def __str__(self):
        return f"{self._name} (размер {self._size})"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._name}', {self._size}, {self._fabric_price}, {self._accessories_price})"