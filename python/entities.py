#!/usr/bin/python
"""
classes defining shopping list objects
"""
from collections import namedtuple
from functools import reduce


class Amount:
    def __init__(self, number, unit):
        self.number = number
        self.unit = unit

    def __eq__(self, other):
        return self.number == other.number and self.unit == other.unit

    def __add__(self, other):
        if other.number == 0:
            return self
        if self.number == 0:
            return other
        if(self.unit == other.unit):
            return Amount(self.number + other.number, self.unit)
        else:
            raise ArithmeticError("unit can't be added ({} + {})".format(self.unit, other.unit))

    def __rmul__(self, other):
        '''scalar multiplication'''
        assert isinstance(other, int) or isinstance(other, float)
        return Amount(self.number*other, self.unit)

    def __hash__(self):
        return hash((self.number, self.unit))

Amount.zero = Amount(0, '')
Amount.__repr__ = lambda self: "{} {}".format(self.number, self.unit)

Ingredient = namedtuple("Ingredient", ["name", "amount"])
Ingredient.__repr__ = lambda self: self.name + ": " + repr(self.amount)


class IngredientList:
    def __init__(self, ingredients):
        self.ingredients = frozenset(ingredients)

    def __add__(self, other):
        if other == self.zero:
            return self
        if self == self.zero:
            return other
        set1 = dict((i.name, i) for i in self.ingredients)
        set2 = dict((i.name, i) for i in other.ingredients)
        all_dicts = [set1, set2]
        all_keys = tuple(reduce(lambda r, x: r.union(set(x)), map(dict.keys, all_dicts), set()))

        def summed(key):
            ingredients = filter(lambda x: x, (d.get(key, None) for d in all_dicts))
            amounts = list(i.amount for i in ingredients)
            return Ingredient(name=key, amount=sum(amounts, Amount.zero))

        return IngredientList(summed(key) for key in all_keys)

    def __repr__(self):
        return "[" + ", ".join(map(repr, self.ingredients)) + "]"

    def __eq__(self, other):
        return self.ingredients == other.ingredients

    def __iter__(self):
        return iter(self.ingredients)

IngredientList.zero = IngredientList([])

Recipe = namedtuple("Recipe", ["for_people", "ingredients"])
Serving = namedtuple("Serving", ["recipe_name", "for_people"])
