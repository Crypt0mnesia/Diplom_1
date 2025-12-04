import pytest
from unittest.mock import Mock, patch
from praktikum.burger import Burger


class TestBurger:
    """Юнит-тесты для класса Burger"""

    # 1. Тест инициализации
    def test_burger_init(self):
        burger = Burger()
        assert burger.bun is None
        assert burger.ingredients == []

    # 2. Тест установки булочки
    def test_set_buns(self):
        burger = Burger()
        mock_bun = Mock()
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    # 3. Тест добавления ингредиента
    def test_add_ingredient(self):
        burger = Burger()
        mock_ingredient = Mock()
        burger.add_ingredient(mock_ingredient)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient

    # 4. Тест удаления ингредиента
    def test_remove_ingredient(self):
        burger = Burger()
        mock_ingredient = Mock()
        burger.add_ingredient(mock_ingredient)
        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 0

    # 5. Тест удаления с ошибкой
    def test_remove_ingredient_invalid_index(self):
        burger = Burger()
        with pytest.raises(IndexError):
            burger.remove_ingredient(999)

    # 6. Тест перемещения ингредиента
    def test_move_ingredient(self):
        burger = Burger()
        mock1, mock2 = Mock(), Mock()
        burger.add_ingredient(mock1)
        burger.add_ingredient(mock2)
        burger.move_ingredient(0, 1)
        assert burger.ingredients == [mock2, mock1]

    # 7. Тест перемещения с ошибкой
    def test_move_ingredient_invalid_index(self):
        burger = Burger()
        mock = Mock()
        burger.add_ingredient(mock)
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
    def test_get_receipt(self):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = "Булочка"
        burger.set_buns(mock_bun)

        mock_ingredient = Mock()
        mock_ingredient.get_type.return_value = "SAUCE"
        mock_ingredient.get_name.return_value = "Соус"
        burger.add_ingredient(mock_ingredient)

        with patch.object(burger, 'get_price', return_value=1000):
            receipt = burger.get_receipt()
            assert "Булочка" in receipt
            assert "sauce Соус" in receipt
            assert "Price: 1000" in receipt

    # 11. Тест чека без булочки
    def test_get_receipt_without_bun(self):
        burger = Burger()
        with pytest.raises(AttributeError):
            burger.get_receipt()

    # 12. Тест чека вызывает get_price
    def test_get_receipt_calls_get_price(self):
        burger = Burger()
        mock_bun = Mock()
        burger.set_buns(mock_bun)

        with patch.object(burger, 'get_price', return_value=1000) as mock_get_price:
            burger.get_receipt()
            mock_get_price.assert_called_once()