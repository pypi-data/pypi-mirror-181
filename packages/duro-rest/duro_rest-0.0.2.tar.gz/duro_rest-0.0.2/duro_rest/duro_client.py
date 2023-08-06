# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Copyright 2022 Oxide Computer Company

from datetime import datetime
import math
import requests

from duro_rest.error import AuthenticationError, ForbiddenError, NotFoundError

class Client:
  def __init__(self, api_key, url = "https://public-api.duro.app/v1/"):
    self.__base_url = url
    self.__api_key = api_key

  def categories(self):
    return self.__get_paginated("categories", "categories")

  def change_order(self, id):
    return self.__get("changeorders/" + id).json()

  def change_orders(self):
    return self.__get_paginated("changeorders", "changeOrders")

  def component(self, id):
    return self.__get("components/" + id).json()

  def components(self):
    return self.__get_paginated("components", "components")

  def component_revision(self, id):
    return self.__get("component/revision/" + id).json()

  def component_revisions(self):
    return self.__get_paginated("component/revision", "componentRevisions")

  def document(self, id):
    return self.__get("documents/" + id).json()

  def product(self, id):
    return self.__get("products/" + id).json()

  def products(self):
    return self.__get_paginated("products", "products")

  def product_revision(self, id):
    return self.__get("product/revision/" + id).json()

  def product_revisions(self):
    return self.__get_paginated("product/revision", "productRevisions")

  def user(self, id):
    return self.__get("users/" + id).json()

  def users(self):
    return self.__get_paginated("users", "users")

  def __get_paginated(self, path, resultKey):
    resources = []

    page = self.__get(path, params = {"perPage": 100}).json()

    total_results = page["resultCount"]
    pages = math.ceil(total_results / 100)

    resources.append(page[resultKey])

    for page_index in range(2, pages):
      page = self.__get(path, params = {"perPage": 100, "page": page_index}).json()
      resources.append(page[resultKey])

    return resources

  def __get(self, path, headers = {}, params = {}, data = None):
    headers["x-api-key"] = self.__api_key

    resp = requests.get(self.__base_url + path, headers = headers, params = params, data = data)

    if resp.status_code == 401:
      raise AuthenticationError(resp.json()["message"])
    if resp.status_code == 403:
      raise ForbiddenError(resp.json()["message"])
    if resp.status_code == 404:
      raise NotFoundError(resp.json()["message"])
    else:
      return resp