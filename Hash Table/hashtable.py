from collections import deque
from typing import NamedTuple, Any


class Pair(NamedTuple): #("Pair", [key, value])
   key: Any
   value: Any


class Hashtable:
   
   def __init__(self, capacity = 8, load_factor_threshold = 0.6): 
      if capacity < 1:
         raise ValueError("capacity must be a positive number")
      if not (0 < load_factor_threshold <= 1):
         raise ValueError("Load factor must be a number between (0,1]")        
      
      self._keys = [] 
      self._buckets = [deque() for _ in range(capacity)]  #deque() is a linked list with built in ways of addinng and removing elements
      self._load_factor_threshold = load_factor_threshold 
      self._original_capacity = capacity

   @property
   def keys(self):
      return self._keys.copy()
   
   @property
   def values(self):
      return [self[key] for key in self.keys]
   
   @property
   def pairs(self):
      return [(key, self[key]) for key in self.keys]
      
   @property
   def capacity(self):
      return len(self._buckets)

   @property
   def load_factor(self):
      return len(self) / self.capacity
   
   def __len__(self):
         return len(self.pairs)
   
   def __eq__(self, other):
      if self is other:
         return True
      if type(self) is not type(other):
         return False
      return set(self.pairs) == set(other.pairs)

   def _index(self, key):
      return hash(key) % self.capacity
   
   def __getitem__(self,key):
      bucket = self._buckets[self._index(key)]
      for pair in bucket:
         if pair.key == key:
            return pair.value
      raise KeyError(key)
   
   def __delitem__(self, key):
         bucket = self._buckets[self._index(key)]
         for index, pair in enumerate(bucket):
            if pair.key == key:
               del bucket[index]
               self._keys.remove(key)
               break
         else:
            raise KeyError(key)
   
   def __setitem__(self, key, value): 
      if self.load_factor >= self._load_factor_threshold:
         self._resize_and_rehash()
      
      bucket = self._buckets[self._index(key)] 
      for index,pair in enumerate(bucket):      
         if pair.key == key:
            bucket[index] = Pair(key, value)
            break
      else:
         bucket.append(Pair(key, value))
         self._keys.append(key)

   def _resize_and_rehash(self):
      copy =  Hashtable(capacity = self.capacity * 2)
      for key , value in self.pairs:
         copy[key] = value
      self._buckets =  copy._buckets

   def __contains__(self,key):
      try:
         self[key]
      except KeyError:
         return False
      else:
         return True

   def __iter__(self):
      yield from self.keys

   def __str__(self):
      pairs = []
      for key, value in self.pairs:
         pairs.append(f"{key!r}: {value!r}")
      return "{" + ", ".join(pairs) + "}" 
   
   def __repr__(self):
      cls = self.__class__.__name__
      return f"{cls}.dict_to_hashtable({str(self)})" 

   def get(self, key, default = None):
      try:
         return self[key]
      except KeyError:
         return default
      
   @classmethod
   def dict_to_hashtable(cls, dictionary, capacity = None):  
      hash_table = cls(capacity or len(dictionary)) # cls --> reference to class 
      for key, value in dictionary.items():
         hash_table[key] = value
      return hash_table

   def copy(self):
      return Hashtable.dict_to_hashtable(dict(self.pairs), self.capacity)

   #####
   
   def clear(self):
      self._buckets = [deque() for _ in range(self._original_capacity)]
      self._keys = []
      return self
   
   def update(self, other):
      for key, value in other.pairs:
            self[key] = value
