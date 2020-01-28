from mock import mock

from animalz.fetcher import is_animal_table, parse_animal_from_row


def test_is_animal_table_when_not_animal_table():
    mock_animal_table = mock.Mock()
    mock_animal_table.find.return_value = None
    assert not is_animal_table(mock_animal_table)


def test_is_animal_table_when_is_animal_table():
    mock_animal_table = mock.Mock()
    mock_row = mock_animal_table.find.return_value
    mock_column = mock_row.find.return_value
    mock_column.get_text.return_value = 'Animal'
    assert is_animal_table(mock_animal_table)


def test_parse_animal_from_row():
    row = mock.Mock()
    mock_name_column = mock.Mock()
    mock_name_attrs = {'href': mock.Mock()}
    mock_name_column.find.return_value.attrs = mock_name_attrs
    mock_collateral_adjectives_column = mock.Mock()

    collateral_adjectives = ['a', 'b']
    mock_collateral_adjectives_column.contents = collateral_adjectives + [mock.Mock()]
    row.find_all.return_value = [mock_name_column, None, None, None, None, mock_collateral_adjectives_column, None]

    animal = parse_animal_from_row(row)
    assert animal.collateral_adjectives == collateral_adjectives
    assert animal.name == mock_name_column.get_text.return_value
    assert animal.link == mock_name_attrs['href']
