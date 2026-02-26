from typing import List
from .abstract_clothing import Clothing


class ClothingCalculator:
    """Калькулятор для расчётов одежды"""

    def __init__(self):
        self._items: List[Clothing] = []

    def add_item(self, item: Clothing):
        self._items.append(item)

    def remove_item(self, index: int):
        if 0 <= index < len(self._items):
            self._items.pop(index)

    def get_items(self) -> List[Clothing]:
        return self._items.copy()

    def calculate_total_fabric(self) -> float:
        """Общий расход ткани"""
        return sum(item.calculate_fabric_consumption() for item in self._items)

    def calculate_total_sewing_cost(self) -> float:
        """Общая стоимость пошива"""
        return sum(item.calculate_sewing_cost() for item in self._items)

    def calculate_total_material_cost(self) -> float:
        """Общая стоимость материалов"""
        return sum(item.calculate_total_cost() for item in self._items)

    def __len__(self):
        return len(self._items)

    def __call__(self, fabric_price_per_meter: float):
        """При вызове объекта пересчитывает все стоимости с новой ценой ткани"""
        total = 0
        for item in self._items:
            total += item.calculate_fabric_consumption() * fabric_price_per_meter + item._accessories_price
        return total