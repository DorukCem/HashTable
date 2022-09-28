import pytest
from hashtable import Hashtable
from pytest_unordered import unordered
from unittest.mock import patch
from collections import deque

def test_should_create_hashtable():
    assert Hashtable(capacity=100) is not None

def test_should_report_capacity(hash_table):
    assert hash_table.capacity == 100

def test_should_create_empty_pair_slots():
    assert Hashtable(capacity = 3)._buckets == [deque([]),deque([]),deque([])]

def test_should_insert_key_value_slots():
    hash_table = Hashtable(capacity=100)

    hash_table["hola"] = "hello"
    hash_table[98.6] = 31
    hash_table[False] = True

    assert ("hola", "hello") in hash_table.pairs
    assert (98.6, 31) in hash_table.pairs
    assert (False, True) in hash_table.pairs

    assert len(hash_table) == 3

def test_should_not_contain_none_value_when_created():
    assert None not in Hashtable(capacity=100).values

def test_should_be_able_to_insert_None_value():
    hash_table = Hashtable(capacity = 100)
    hash_table["key"] = None
    assert ("key", None) in hash_table.pairs

@pytest.fixture
def hash_table():
    sample_data = Hashtable(capacity=100)
    sample_data["hola"] = "hello"
    sample_data[98.6] = 31
    sample_data[False] = True
    return sample_data

def test_should_find_value_by_key(hash_table):
    assert hash_table["hola"] == "hello"
    assert hash_table[98.6] == 31
    assert hash_table[False] is True

def test_should_raise_erron_on_missing_key():
    hash_table = Hashtable(capacity = 100)
    with pytest.raises(KeyError) as exception_info:
        hash_table["missing key"]
    assert exception_info.value.args[0]

def test_should_find_key(hash_table):
    assert "hola" in hash_table

def test_should_not_find_key(hash_table):
    assert "missing key" not in hash_table

def test_should_get_value(hash_table):
    assert hash_table.get("hola") == "hello"

def test_should_get_none_when_missing_key(hash_table):
    assert hash_table.get("missing_key") is None

def test_should_get_none_when_missing_key(hash_table):
    assert hash_table.get("missing_key", "default") == "default"

def test_should_get_value_with_default(hash_table):
    assert hash_table.get("hola", "default") == "hello"

def test_should_delete_key_value_pair(hash_table):
    assert "hola" in hash_table
    assert ("hola","hello") in hash_table.pairs
    assert len(hash_table) == 3

    del hash_table["hola"]

    assert "hola" not in hash_table
    assert ("hola","hello") not in hash_table.pairs
    assert len(hash_table) == 2

def test_should_raise_key_error_when_deleteing(hash_table):
    with pytest.raises(KeyError) as exception_info:
        del hash_table["missing_key"]
    assert exception_info.value.args[0] == "missing_key"

def test_should_update_value(hash_table):
    assert hash_table["hola"] == "hello"
    hash_table["hola"] = "hallo"
    assert hash_table["hola"] == "hallo"
    assert hash_table[98.6] == 31
    assert hash_table[False] is True
    assert len(hash_table) == 3

def test_should_return_slots(hash_table):
    assert hash_table.pairs == [
        ("hola", "hello"),
        (98.6, 31),
        (False, True)
    ]

def test_should_get_slots_of_empty_hash_table():
    assert Hashtable(capacity=100).pairs == []


def test_should_not_include_blank_slots(hash_table):
    assert None not in hash_table.pairs

def test_should_return_duplicate_values():
    hash_table = Hashtable(capacity=100)
    hash_table["Alice"] = 24
    hash_table["Bob"] = 42
    hash_table["Joe"] = 42
    assert [24, 42, 42] == sorted(hash_table.values)

def test_should_get_values(hash_table):
    assert unordered(hash_table.values) == ["hello", 31, True]

def test_should_get_values_of_empty_hash_table():
    assert Hashtable(capacity = 100).values == []

def test_should_return_copy_of_values(hash_table):
    assert hash_table.values is not hash_table.values

def tests_should_get_keys(hash_table):
    assert hash_table.keys == ["hola", 98.6, False]

def tests_should_get_keys_of_empty_hash_table():
    assert Hashtable(capacity = 100).keys == []

def test_should_return_copy_of_keys(hash_table):
    assert hash_table.keys is not hash_table.keys

def test_should_convert_to_dict(hash_table):
    dictionary = dict(hash_table.pairs)
    assert list(dictionary.keys()) == hash_table.keys
    assert list(dictionary.items()) == hash_table.pairs
    assert (list(dictionary.values())) == unordered(hash_table.values)

def test_should_not_create_hashtable_with_zero_capacity():
    with pytest.raises(ValueError):
        Hashtable(capacity = 0)
    
def test_should_not_create_hashtable_with_negative_capacity():
    with pytest.raises(ValueError):
        Hashtable(capacity=-100)

def test_should_report_length(hash_table):
    assert len(hash_table) == 3

def test_should_report_capacity_of_empty_hashtable():
    assert Hashtable(capacity=100).capacity == 100

def test_should_itirate_over_keys(hash_table):
    for key in hash_table.keys:
        assert key in ("hola", 98.6, False)

def test_should_itirate_over_values(hash_table):
    for value in hash_table.values:
        assert value in ("hello",31, True)

def test_should_itirate_over_pairs(hash_table):
    for key, value in hash_table.pairs:
        assert key in hash_table.keys
        assert value in hash_table.values

def test_should_itirate_over_instance(hash_table):
    for key in hash_table:
        assert key in ("hola", 98.6, False)

def test_should_use_dict_literal_for_str(hash_table):
    assert str(hash_table) in {
        "{'hola': 'hello', 98.6: 31, False: True}",
        "{'hola': 'hello', False: True, 98.6: 31}",
        "{98.6: 31, 'hola': 'hello', False: True}",
        "{98.6: 31, False: True, 'hola': 'hello'}",
        "{False: True, 'hola': 'hello', 98.6: 31}",
        "{False: True, 98.6: 31, 'hola': 'hello'}",
    }

def test_should_create_hashtable_dict_to_hashtable():
    dictionary = {"hola": "hello", 98.6: 31, False: True}

    hash_table = Hashtable.dict_to_hashtable(dictionary)

    assert hash_table.keys == list(dictionary.keys())
    assert hash_table.pairs == list(dictionary.items())
    assert unordered(hash_table.values) == list(dictionary.values())   

def test_should_create_hashtable_dict_to_hashtable_with_custom_capacity():
    dictionary = {"hola": "hello", 98.6: 31, False: True}

    hash_table = Hashtable.dict_to_hashtable(dictionary, capacity = 100)

    assert hash_table.capacity == 100
    assert hash_table.keys == list(dictionary.keys())
    assert hash_table.pairs == list(dictionary.items())
    assert unordered(hash_table.values) == list(dictionary.values())

def test_should_have_canonical_string_representation(hash_table):
    assert repr(hash_table) in {
        "Hashtable.dict_to_hashtable({'hola': 'hello', 98.6: 31, False: True})",
        "Hashtable.dict_to_hashtable({'hola': 'hello', False: True, 98.6: 31})",
        "Hashtable.dict_to_hashtable({98.6: 31, 'hola': 'hello', False: True})",
        "Hashtable.dict_to_hashtable({98.6: 31, False: True, 'hola': 'hello'})",
        "Hashtable.dict_to_hashtable({False: True, 'hola': 'hello', 98.6: 31})",
        "Hashtable.dict_to_hashtable({False: True, 98.6: 31, 'hola': 'hello'})",
    }

def test_should_compare_equal_to_itself(hash_table):
    assert hash_table == hash_table

def test_should_compare_equal_to_copy(hash_table):
    assert hash_table is not hash_table.copy()
    assert hash_table == hash_table.copy()

def test_should_compare_equal_different_key_value_order(hash_table):
    h1 = Hashtable.dict_to_hashtable({"a": 1, "b": 2, "c": 3})
    h2 = Hashtable.dict_to_hashtable({"b": 2, "a": 1, "c": 3})
    assert h1 == h2

def test_should_compare_unequal_different_key_value_order(hash_table):
    other = Hashtable.dict_to_hashtable({"diffrent": "value"})
    assert hash_table != other

def test_should_compare_unequal_another_data_type(hash_table):
    assert hash_table != 42

def test_should_copy_keys_values_pairs_capacity(hash_table):
    copy = hash_table.copy()
    assert copy is not hash_table
    assert set(hash_table.keys) == set(copy.keys)
    assert unordered(hash_table.values) == copy.values
    assert set(hash_table.pairs) == set(copy.pairs)
    assert hash_table.capacity == copy.capacity

def test_should_compare_equal_different_capacity():
    data = {"a": 1, "b": 2, "c": 3}
    h1 = Hashtable.dict_to_hashtable(data, capacity=50)
    h2 = Hashtable.dict_to_hashtable(data, capacity=100)
    assert h1 == h2

@patch("builtins.hash", return_value = 42)
def test_should_detect_hash_collisions(hash_mock):
    assert hash("foobar") == 42

##########

def test_should_clear_all_pairs_in_hashtable(hash_table):
    hash_table.clear()
    assert hash_table.pairs == []
    assert hash_table.keys == []
    assert hash_table.values == []

def test_should_retain_original_capacity():
    hash_table = Hashtable(capacity = 60)
    hash_table.clear()
    assert hash_table.capacity == 60
    
def test_should_retain_original_capacity_after_resize():
    hash_table = Hashtable(capacity= 3)
    hash_table["a"] = 1
    hash_table["b"] = 2
    hash_table["c"] = 3
    hash_table["d"] = 4

    hash_table.clear()
    assert hash_table.capacity == 3

def test_clear_should_return_itself(hash_table):
    assert hash_table.clear().pairs == []
    
def test_should_update_hash_table(hash_table):
    other = Hashtable()
    other["hola"] = "merhaba"
    other["new key"] = "new value"
    hash_table.update(other)
    assert hash_table.pairs == unordered([("hola", "merhaba"), ("new key", "new value"), (98.6, 31), (False, True)])


#python -m pytest