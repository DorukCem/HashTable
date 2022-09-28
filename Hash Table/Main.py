
from hashtable import Hashtable

hash_table = Hashtable()

hash_table["key1"] = "value1"
hash_table["key2"] = "value2"

print(hash_table.keys)
print(hash_table.values)
print(hash_table.pairs)
print(hash_table)

print(len(hash_table))

other = {"dict key": "dict value"}
other = Hashtable.dict_to_hashtable(other)

print(other == hash_table)

hash_table.update(other)
print(hash_table.pairs)

hash_table.clear()
print(hash_table)

a = {"a":1, "b":2}