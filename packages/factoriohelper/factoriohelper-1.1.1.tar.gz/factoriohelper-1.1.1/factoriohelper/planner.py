#!/usr/bin/env python3

import math
import os
import re
import sys

import factoriohelper.graphs

class Item:
    def __init__(self, item, amount=None):
        if isinstance(item, Item):
            item = item.name
            if amount is None:
                amount = item.amount
        self.name = item.strip()
        self.amount = float(amount.strip()) if isinstance(amount, str) else amount

    def __eq__(self, other):
        if self.amount != None and other.amount != None and self.amount != other.amount:
            return False
        return self.name == other.name

    def __str__(self):
        if self.amount is None:
            return f"({self.name})"
        else:
            return f"({self.amount} {self.name})"

    def __repr__(self):
        return str(self)

    @staticmethod
    def parse(item_string):
        try:
            match = re.search("(\d+(?:.\d+)?)\s+(.*)", item_string)
            if match:
                amount, item_name = match.groups()
                return Item(item_name, amount)

            match = re.search("(.*)", item_string)
            if match:
                item_name = match.group(1)
                return Item(item_name)
        except:
            pass

        raise ValueError(f"Could not parse '{item_string}'")

class Recipe:
    def __init__(self, outputs, inputs, production_time):
        assert all([isinstance(o, Item) and o.amount != None for o in outputs])
        assert all([isinstance(i, Item) and i.amount != None for i in inputs])
        assert len(outputs) == len(set([o.name for o in outputs]))
        assert len(inputs) == len(set([i.name for i in inputs]))

        self.outputs = outputs
        self.inputs = inputs
        self.production_time = float(production_time)

    def __eq__(self, other):
        return self.products == other.products

    def __str__(self):
        outputs = " + ".join([str(o) for o in self.outputs])
        inputs = " + ".join([str(i) for i in self.inputs])
        production_time = self.production_time
        return f"{{ {outputs} = {inputs} ; {production_time} }}"

    def __repr__(self):
        return str(self)

    def parse_item(self, item):
        return Item(item_name, amount)

    @property
    def products(self):
        return [Item(output.name) for output in self.outputs]

    @property
    def ingredients(self):
        return [Item(input_.name) for input_ in self.inputs]

    def get_product(self, item):
        recipe_outputs = list(filter(lambda o: Item(o.name) == item, self.outputs))
        assert len(recipe_outputs) == 1
        return recipe_outputs[0]


class ProductionGraph(factoriohelper.graphs.NXGraph):
    def __init__(self, name):
        super().__init__(name)


class ProductionPlanner:
    def __init__(self):
        self.recipes = []

    def register_recipes(self, recipes):
        for recipe in recipes:
            self.register_recipe(recipe)

    def register_recipe(self, recipe):
        assert recipe not in self.recipes
        print(f"Register recipe: {recipe}")
        self.recipes.append(recipe)

    def get_recipe(self, item):
        recipe_matches = list(filter(lambda recipe: item in recipe.products, self.recipes))
        assert len(recipe_matches) <= 1
        if len(recipe_matches) > 0:
            return recipe_matches[0]

    def calculate_graph(self, item):
        assert isinstance(item, Item) and item.amount != None

        # initialize graph with item
        graph = ProductionGraph(str(item))

        # plan item production based on recipes
        items_to_produce = [item]
        items_planned = []
        while len(items_to_produce) > 0:
            item_to_produce = items_to_produce.pop(0)
            recipe = self.get_recipe(item_to_produce)
            if recipe is not None:
                recipe_output = recipe.get_product(item_to_produce)
                amount_multiplier = item_to_produce.amount / recipe_output.amount
                recipe_inputs = [Item(i, i.amount * amount_multiplier) for i in recipe.inputs]

                items_to_produce += recipe_inputs
            items_planned.append(item_to_produce)

        class ProductionItem(Item):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.num_machines = None

            def __str__(self):
                out = f"{super().__str__()}"
                if self.num_machines is not None:
                    out = f"{out} [{self.num_machines} machines]"
                return out

        # sum up production item volumes
        production_items = {i.name: ProductionItem(i.name, 0) for i in items_planned}
        for item in items_planned:
            production_items[item.name].amount += item.amount

        # calculate number of num_machines per production item
        for production_item_name, production_item in production_items.items():
            recipe = self.get_recipe(production_item)
            if recipe is not None:
                recipe_output = recipe.get_product(production_item)
                production_item.num_machines = production_item.amount / recipe_output.amount * recipe.production_time

        # create graph
        for production_item_name, production_item in production_items.items():
            recipe = self.get_recipe(production_item)
            if recipe is not None:
                recipe_output = recipe.get_product(production_item)
                for recipe_input in recipe.inputs:
                    input_item = production_items[recipe_input.name]
                    production_weight = production_item.amount * recipe_input.amount / recipe_output.amount

                    def get_item_label(item):
                        out = f"({item.amount:.2E} {item.name})"
                        if item.num_machines is not None:
                            num_machines = math.ceil(item.num_machines*100)/100
                            out += f"{os.linesep}[{item.num_machines:.2f} machines]"
                        return out

                    graph.add_edge(
                        get_item_label(input_item),
                        get_item_label(production_item),
                        weight=f"{production_weight:.2E}"
                    )
                    #graph.add_edge(input_item, production_item)

        return graph


class RecipesParser:
    @staticmethod
    def parse(recipe_list):
        recipes = []
        for recipe_line in recipe_list.splitlines():
            recipe_line = recipe_line.split("#")[0]
            if len(recipe_line.strip()) == 0:
                continue
            outputs, inputs, production_time = re.search("(.*)=(.*);(.*)", recipe_line).groups()
            outputs = [Item.parse(o) for o in outputs.split("+")]
            inputs = [Item.parse(i) for i in inputs.split("+")]
            production_time = float(production_time)
            recipes.append(Recipe(outputs, inputs, production_time))
        return recipes


if __name__ == "__main__":

    with open("recipes.txt") as file_:
        recipes = RecipesParser.parse(file_.read())

    planner = ProductionPlanner()
    planner.register_recipes(recipes)

    item_name = " ".join(sys.argv[1:])
    item = Item.parse(item_name)
    if item.amount is None:
        item.amount = 1
    planner.calculate_graph(item).show()
