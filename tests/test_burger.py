import pytest
from unittest.mock import Mock
from praktikum.burger import Burger


class TestBurger:
    """Юнит-тесты для класса Burger"""

    # 1. Тест инициализации
    def test_burger_init(self, bun):
        burger = Burger()
        assert burger.bun is None
        assert burger.ingredients == []

    # 2. Тест установки булочки
    def test_set_buns(self, bun):
        burger = Burger()
        burger.set_buns(bun)
        assert burger.bun == bun

    # 3. Тест добавления ингредиента
    def test_add_ingredient(self, bun, ingredient):
        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == ingredient

    # 4. Тест удаления ингредиента
    def test_remove_ingredient(self, bun, ingredient):
        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient)
        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 0

    # 5. Тест удаления с ошибкой
    def test_remove_ingredient_invalid_index(self, bun, ingredient):
        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient)
        with pytest.raises(IndexError):
            burger.remove_ingredient(999)

    # 6. Тест перемещения ингредиента
    def test_move_ingredient(self, bun):
        burger = Burger()
        burger.set_buns(bun)
        mock1, mock2 = Mock(), Mock()
        burger.add_ingredient(mock1)
        burger.add_ingredient(mock2)
        burger.move_ingredient(0, 1)
        assert burger.ingredients == [mock2, mock1]

    # 7. Тест перемещения с ошибкой
    def test_move_ingredient_invalid_index(self, bun, ingredient):
        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient()  )
        with pytest.raises(IndexError):
            burger.move_ingredient(999, 0)

    # 8. Параметризованный тест цены
    @pytest.mark.parametrize("bun_price,ingredient_prices,expected", [
        (100, [50, 75], 325),
        (0, [10, 20, 30], 60),
        (250, [], 500),
        (150, [100], 400),
    ])
    def test_get_price(self, bun_price, ingredient_prices, expected):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)

        for price in ingredient_prices:
            mock = Mock()
            mock.get_price.return_value = price
            burger.add_ingredient(mock)

        assert burger.get_price() == expected

    # 9. Тест цены без булочки
    def test_get_price_without_bun(self):
        burger = Burger()
        with pytest.raises(AttributeError):
            burger.get_price()

    # 10. Тест чека
    def test_get_receipt(self, bun, ingredient):
        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient)

        receipt = burger.get_receipt()
        assert "Тестовая булочка" in receipt
        assert "sauce Тестовый соус" in receipt
        assert "Price: 250" in receipt

    # 11. Тест чека без булочки
    def test_get_receipt_without_bun(self):
        burger = Burger()
        with pytest.raises(AttributeError):
            burger.get_receipt()

    # 12. Тест чек  содержит цену из get_price
    def test_get_receipt_contains_price_from_get_price(self, bun, ingredient):
        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient)

        expected_price = burger.get_price()
        receipt = burger.get_receipt()
        assert f"Price: {expected_price}" in receipt