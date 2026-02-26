import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clothing_package import Jacket, Trousers, ThreePieceSuit, ClothingCalculator


class TestJacket:
    """Тесты для класса Jacket"""

    def test_jacket_creation(self):
        jacket = Jacket("Test Jacket", 50, 1000, 500, True, 4)
        assert jacket.name == "Test Jacket"
        assert jacket.size == 50
        assert jacket.fabric_price == 1000
        assert jacket.accessories_price == 500
        assert jacket.has_lining == True
        assert jacket.pockets_count == 4

    def test_fabric_consumption_base(self):
        jacket = Jacket("Test", 48, 1000, 500, False, 2)
        # Расчёт: 2.5 + 2*0.1 = 2.7
        assert jacket.calculate_fabric_consumption() == 2.7

    def test_fabric_consumption_with_lining(self):
        jacket = Jacket("Test", 48, 1000, 500, True, 2)
        # Расчёт: (2.5 * 1.3) + 0.2 = 3.45
        assert jacket.calculate_fabric_consumption() == 3.45

    def test_sewing_cost(self):
        jacket = Jacket("Test", 52, 1000, 500, True, 4)
        expected = 5000 + (52 - 48) * 200 + 4 * 150  # 5000 + 800 + 600 = 6400
        assert jacket.calculate_sewing_cost() == expected

    def test_total_cost(self):
        jacket = Jacket("Test", 50, 1000, 500, False, 2)
        fabric_consumption = jacket.calculate_fabric_consumption()
        # Для размера 50: 2.5 + (50-48)*0.2 + 2*0.1 = 2.5 + 0.4 + 0.2 = 3.1
        expected_cost = 3.1 * 1000 + 500  # 3100 + 500 = 3600
        assert jacket.calculate_total_cost() == expected_cost

    def test_pockets_setter(self):
        jacket = Jacket("Test", 50, 1000, 500, False, 2)
        jacket.pockets_count = 3
        assert jacket.pockets_count == 3

        with pytest.raises(ValueError):
            jacket.pockets_count = -1

    def test_len_method(self):
        jacket = Jacket("Test", 50, 1000, 500, False, 2)
        # Расход ткани 3.1 м * 100 = 310 см
        assert len(jacket) == 310


class TestTrousers:
    """Тесты для класса Trousers"""

    def test_trousers_creation(self):
        trousers = Trousers("Test Trousers", 52, 800, 300, True, True)
        assert trousers.name == "Test Trousers"
        assert trousers.size == 52
        assert trousers.has_belt == True
        assert trousers.is_classic == True

    def test_fabric_consumption_classic(self):
        trousers = Trousers("Test", 50, 800, 300, False, True)
        # Классические брюки размера 50: 1.5 * 1.2 = 1.8
        # После округления round(1.8, 2) = 1.8
        assert trousers.calculate_fabric_consumption() == 1.8

    def test_fabric_consumption_with_belt(self):
        trousers = Trousers("Test", 50, 800, 300, True, False)
        # Обычные брюки с поясом: 1.5 + 0.2 = 1.7
        assert trousers.calculate_fabric_consumption() == 1.7

    def test_fabric_consumption_large_size(self):
        trousers = Trousers("Test", 54, 800, 300, False, True)
        # Классические брюки размера 54: (1.5 + (54-50)*0.15) * 1.2 = (1.5 + 0.6) * 1.2 = 2.1 * 1.2 = 2.52
        assert trousers.calculate_fabric_consumption() == 2.52

    def test_sewing_cost_classic(self):
        trousers = Trousers("Test", 52, 800, 300, False, True)
        expected = 3000 + (52 - 50) * 150 + 500  # 3000 + 300 + 500 = 3800
        assert trousers.calculate_sewing_cost() == expected

    def test_sewing_cost_regular(self):
        trousers = Trousers("Test", 52, 800, 300, False, False)
        expected = 3000 + (52 - 50) * 150  # 3000 + 300 = 3300
        assert trousers.calculate_sewing_cost() == expected


class TestThreePieceSuit:
    """Тесты для класса ThreePieceSuit"""

    def test_suit_creation(self):
        jacket = Jacket("Jacket", 50, 1000, 500, True, 4)
        trousers = Trousers("Trousers", 50, 800, 300, True, True)
        suit = ThreePieceSuit("Test Suit", jacket, trousers, None)

        assert suit.name == "Test Suit"
        assert suit.size == 50
        assert suit.jacket == jacket
        assert suit.trousers == trousers

    def test_suit_fabric_consumption(self):
        jacket = Jacket("Jacket", 50, 1000, 500, False, 2)
        trousers = Trousers("Trousers", 50, 800, 300, False, False)
        suit = ThreePieceSuit("Test Suit", jacket, trousers, None)

        jacket_consumption = jacket.calculate_fabric_consumption()  # 3.1
        trousers_consumption = trousers.calculate_fabric_consumption()  # 1.5
        expected = round(jacket_consumption + trousers_consumption, 2)  # 4.6
        assert suit.calculate_fabric_consumption() == expected

    def test_suit_sewing_cost_with_discount(self):
        jacket = Jacket("Jacket", 50, 1000, 500, False, 2)
        trousers = Trousers("Trousers", 50, 800, 300, False, False)
        suit = ThreePieceSuit("Test Suit", jacket, trousers, None)

        jacket_sewing = jacket.calculate_sewing_cost()  # 5000
        trousers_sewing = trousers.calculate_sewing_cost()  # 3000
        expected = int((jacket_sewing + trousers_sewing) * 0.9)  # 8000 * 0.9 = 7200
        assert suit.calculate_sewing_cost() == expected

    def test_suit_total_cost(self):
        jacket = Jacket("Jacket", 50, 1000, 500, False, 2)
        trousers = Trousers("Trousers", 50, 800, 300, False, False)
        suit = ThreePieceSuit("Test Suit", jacket, trousers, None)

        jacket_total = jacket.calculate_total_cost()  # 3600
        trousers_total = trousers.calculate_total_cost()  # 1500
        expected = jacket_total + trousers_total  # 5100
        assert suit.calculate_total_cost() == expected

    def test_add_operator(self):
        jacket = Jacket("Jacket", 50, 1000, 500, False, 2)
        trousers = Trousers("Trousers", 50, 800, 300, False, False)

        suit1 = jacket + trousers
        suit2 = trousers + jacket

        assert isinstance(suit1, ThreePieceSuit)
        assert isinstance(suit2, ThreePieceSuit)
        assert suit1.name == "Костюм (пиджак+брюки)"
        assert suit2.name == "Костюм (пиджак+брюки)"
        assert suit1.jacket == jacket
        assert suit1.trousers == trousers

    def test_getitem(self):
        jacket = Jacket("Jacket", 50, 1000, 500, False, 2)
        trousers = Trousers("Trousers", 50, 800, 300, False, False)
        suit = ThreePieceSuit("Test Suit", jacket, trousers, None)

        assert suit[0] == jacket
        assert suit[1] == trousers


class TestClothingCalculator:
    """Тесты для класса ClothingCalculator"""

    def test_add_item(self):
        calc = ClothingCalculator()
        jacket = Jacket("Test", 50, 1000, 500, False, 2)
        calc.add_item(jacket)

        assert len(calc) == 1
        assert calc.get_items()[0] == jacket

    def test_remove_item(self):
        calc = ClothingCalculator()
        jacket = Jacket("Test", 50, 1000, 500, False, 2)
        trousers = Trousers("Test2", 50, 800, 300, False, False)

        calc.add_item(jacket)
        calc.add_item(trousers)
        calc.remove_item(0)

        assert len(calc) == 1
        assert calc.get_items()[0] == trousers

    def test_total_fabric(self):
        calc = ClothingCalculator()
        # Пиджак размера 50: 2.5 + (50-48)*0.2 + 2*0.1 = 2.5 + 0.4 + 0.2 = 3.1
        jacket = Jacket("Test", 50, 1000, 500, False, 2)
        # Брюки размера 50: 1.5
        trousers = Trousers("Test2", 50, 800, 300, False, False)

        calc.add_item(jacket)
        calc.add_item(trousers)

        expected = 3.1 + 1.5  # 4.6
        assert calc.calculate_total_fabric() == expected

    def test_total_sewing_cost(self):
        calc = ClothingCalculator()
        # Пиджак размера 48 с 2 карманами: 5000 + 2*150 = 5300
        jacket = Jacket("Test", 48, 1000, 500, False, 2)
        # Брюки размера 50 без особенностей: 3000
        trousers = Trousers("Test2", 50, 800, 300, False, False)

        calc.add_item(jacket)
        calc.add_item(trousers)

        expected = 5300 + 3000  # 8300
        assert calc.calculate_total_sewing_cost() == expected

    def test_total_sewing_cost_with_different_sizes(self):
        """Тест с разными размерами для проверки надбавок"""
        calc = ClothingCalculator()
        # Пиджак размера 52 с 4 карманами: 5000 + (52-48)*200 + 4*150 = 5000 + 800 + 600 = 6400
        jacket = Jacket("Test", 52, 1000, 500, True, 4)
        # Брюки размера 54 классические: 3000 + (54-50)*150 + 500 = 3000 + 600 + 500 = 4100
        trousers = Trousers("Test2", 54, 800, 300, False, True)

        calc.add_item(jacket)
        calc.add_item(trousers)

        expected = 6400 + 4100  # 10500
        assert calc.calculate_total_sewing_cost() == expected

    def test_call_method(self):
        calc = ClothingCalculator()
        # Пиджак с расходом ткани 3.1 м
        jacket = Jacket("Test", 50, 1000, 500, False, 2)
        calc.add_item(jacket)

        # При цене 1200 за метр: 3.1 * 1200 + 500 = 3720 + 500 = 4220
        result = calc(1200)
        assert result == 4220

    def test_empty_calculator(self):
        """Тест пустого калькулятора"""
        calc = ClothingCalculator()
        assert len(calc) == 0
        assert calc.calculate_total_fabric() == 0
        assert calc.calculate_total_sewing_cost() == 0
        assert calc.calculate_total_material_cost() == 0
        assert calc(1000) == 0

@pytest.fixture
def sample_jacket():
    """Фикстура для создания тестового пиджака"""
    return Jacket("Test Jacket", 50, 1000, 500, False, 2)


@pytest.fixture
def sample_trousers():
    """Фикстура для создания тестовых брюк"""
    return Trousers("Test Trousers", 50, 800, 300, False, False)


@pytest.mark.parametrize("size,expected_fabric", [
    (48, 2.7),  # 2.5 + 2*0.1
    (50, 3.1),  # 2.5 + 0.4 + 0.2
    (52, 3.5),  # 2.5 + 0.8 + 0.2
])
def test_jacket_fabric_parametrized(size, expected_fabric):
    """Параметризованный тест расхода ткани пиджака"""
    jacket = Jacket("Test", size, 1000, 500, False, 2)
    assert jacket.calculate_fabric_consumption() == expected_fabric


@pytest.mark.parametrize("size,is_classic,has_belt,expected", [
    (50, True, False, 1.8),  # классические, без пояса
    (50, False, True, 1.7),  # не классические, с поясом
    (54, True, False, 2.52),  # большой размер, классические
])
def test_trousers_fabric_parametrized(size, is_classic, has_belt, expected):
    """Параметризованный тест расхода ткани брюк"""
    trousers = Trousers("Test", size, 800, 300, has_belt, is_classic)
    assert trousers.calculate_fabric_consumption() == expected


if __name__ == "__main__":
    pytest.main(["-v", __file__])