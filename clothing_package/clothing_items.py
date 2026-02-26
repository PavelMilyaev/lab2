from .abstract_clothing import Clothing


class Jacket(Clothing):
    """Класс для пиджака"""

    def __init__(self, name: str, size: int, fabric_price: float, accessories_price: float,
                 has_lining: bool = True, pockets_count: int = 4):
        super().__init__(name, size, fabric_price, accessories_price)
        self._has_lining = has_lining
        self._pockets_count = pockets_count
        self._fabric_consumption = self.calculate_fabric_consumption()

    @property
    def has_lining(self):
        return self._has_lining

    @has_lining.setter
    def has_lining(self, value: bool):
        self._has_lining = value
        self._fabric_consumption = self.calculate_fabric_consumption()

    @property
    def pockets_count(self):
        return self._pockets_count

    @pockets_count.setter
    def pockets_count(self, value: int):
        if value < 0:
            raise ValueError("Количество карманов не может быть отрицательным")
        self._pockets_count = value
        self._fabric_consumption = self.calculate_fabric_consumption()

    def calculate_fabric_consumption(self) -> float:
        """Расход ткани для пиджака (2.5м + 0.2м на каждый размер больше 48)"""
        base_consumption = 2.5
        if self._size > 48:
            base_consumption += (self._size - 48) * 0.2

        # Добавляем на подкладку и карманы
        if self._has_lining:
            base_consumption *= 1.3
        base_consumption += self._pockets_count * 0.1

        return round(base_consumption, 2)

    def calculate_sewing_cost(self) -> float:
        """Стоимость пошива пиджака"""
        base_cost = 5000
        base_cost += max(0, self._size - 48) * 200
        base_cost += self._pockets_count * 150
        return base_cost

    def __add__(self, other):
        if isinstance(other, Trousers):
            return ThreePieceSuit("Костюм (пиджак+брюки)", self, other, None)
        return NotImplemented

    def __len__(self):
        """Возвращает расход ткани в сантиметрах"""
        return int(self._fabric_consumption * 100)


class Trousers(Clothing):
    """Класс для брюк"""

    def __init__(self, name: str, size: int, fabric_price: float, accessories_price: float,
                 has_belt: bool = False, is_classic: bool = True):
        super().__init__(name, size, fabric_price, accessories_price)
        self._has_belt = has_belt
        self._is_classic = is_classic
        self._fabric_consumption = self.calculate_fabric_consumption()

    @property
    def has_belt(self):
        return self._has_belt

    @has_belt.setter
    def has_belt(self, value: bool):
        self._has_belt = value
        self._fabric_consumption = self.calculate_fabric_consumption()

    @property
    def is_classic(self):
        return self._is_classic

    def calculate_fabric_consumption(self) -> float:
        """Расход ткани для брюк (1.5м + 0.15м на каждый размер больше 50)"""
        base_consumption = 1.5
        if self._size > 50:
            base_consumption += (self._size - 50) * 0.15

        # Классические брюки требуют больше ткани
        if self._is_classic:
            base_consumption *= 1.2

        if self._has_belt:
            base_consumption += 0.2

        return round(base_consumption, 2)

    def calculate_sewing_cost(self) -> float:
        """Стоимость пошива брюк"""
        base_cost = 3000
        base_cost += max(0, self._size - 50) * 150
        if self._is_classic:
            base_cost += 500
        return base_cost

    def __add__(self, other):
        if isinstance(other, Jacket):
            return ThreePieceSuit("Костюм (пиджак+брюки)", other, self, None)
        return NotImplemented


class ThreePieceSuit(Clothing):
    """Класс для костюма-тройки"""

    def __init__(self, name: str, jacket: Jacket, trousers: Trousers, vest=None):
        self._jacket = jacket
        self._trousers = trousers
        self._vest = vest
        self._name = name
        self._size = jacket.size
        self._fabric_price = jacket.fabric_price
        self._fabric_consumption = self.calculate_fabric_consumption()

    @property
    def jacket(self):
        return self._jacket

    @property
    def trousers(self):
        return self._trousers

    @property
    def vest(self):
        return self._vest

    def calculate_fabric_consumption(self) -> float:
        """Общий расход ткани для костюма"""
        total = self._jacket.calculate_fabric_consumption() + self._trousers.calculate_fabric_consumption()
        if self._vest:
            # Расход ткани на жилет
            vest_consumption = 1.0 + max(0, self._size - 48) * 0.1
            total += vest_consumption
        return round(total, 2)

    def calculate_sewing_cost(self) -> float:
        """Общая стоимость пошива костюма со скидкой 10%"""
        total = self._jacket.calculate_sewing_cost() + self._trousers.calculate_sewing_cost()
        if self._vest:
            total += 2000
        # Скидка за комплект
        return int(total * 0.9)

    def calculate_total_cost(self) -> float:
        """Общая стоимость материалов для костюма"""
        total = self._jacket.calculate_total_cost() + self._trousers.calculate_total_cost()
        if self._vest:
            vest_cost = self._vest.calculate_total_cost()
            total += vest_cost
        return round(total, 2)

    def __str__(self):
        return f"Костюм-тройка '{self._name}', размер {self._size}"

    def __getitem__(self, index):
        items = [self._jacket, self._trousers]
        if self._vest:
            items.append(self._vest)
        return items[index]