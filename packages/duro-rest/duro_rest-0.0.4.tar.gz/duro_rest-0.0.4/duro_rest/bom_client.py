# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Copyright 2022 Oxide Computer Company

from duro_rest.duro_client import Client

class FlattenedBOM(list):
  def __init__(self, data):
    list.__init__(self, data)
    self.__data = data

  def inner(self) -> list:
    self.__data

class NestedBOM(dict):
  def __init__(self, data):
    # Assign a default quantity of 1 to the top line item
    if not 'quantity' in data:
      data['quantity'] = 1

    dict.__init__(self, data)
    self.__data = data

  def flatten(self) -> FlattenedBOM:
    components = flatten_component(self.__data)

    unique_components = []

    for component in components:
      existing = next((c for c in unique_components if component['_id'] == c['_id']), None)

      if existing:

        # TODO: We have found two instances of a component in the nested BOM tree. We need to
        # combine their quantities, but what other fields need to be combined?
        existing['quantity'] = existing['quantity'] + component['quantity']
      else:
        unique_components.append(component)

    return FlattenedBOM(unique_components)

def flatten_component(component) -> list:
  flattened_children = flatten(map(flatten_component, component['children']))

  for child in flattened_children:
    child['quantity'] = component['quantity'] * child['quantity']

  component.pop('children', None)

  return [component] + flattened_children

class BOMClient(Client):
  def __init__(self, api_key, url="https://public-api.duro.app/v1/"):
    super().__init__(api_key, url)

  def product_bom(self, id) -> NestedBOM:
    return self.__nested_bom(self.product(id))

  def component_bom(self, id) -> NestedBOM:
    return self.__nested_bom(self.component(id))

  def __nested_bom(self, parent) -> NestedBOM:
    components = self.components()
    parent['children'] = list(map(lambda child: expand_child_components(child, components), parent['children']))

    return NestedBOM(parent)

def expand_child_components(parent, components):
  expanded_parent = {**parent, **next(component for component in components if component['_id'] == parent['component'])}
  expanded_parent['children'] = list(map(lambda child: expand_child_components(child, components), expanded_parent['children']))

  return expanded_parent

def flatten(l):
  return [item for sublist in l for item in sublist]