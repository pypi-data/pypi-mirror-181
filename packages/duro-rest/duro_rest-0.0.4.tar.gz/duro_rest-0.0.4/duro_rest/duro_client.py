# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Copyright 2022 Oxide Computer Company

from datetime import datetime
import math
import requests

from duro_rest.error import AuthenticationError, BadRequestError, ForbiddenError, NotFoundError

class Client:
  def __init__(self, api_key, url = "https://public-api.duro.app/v1/"):
    self.__base_url = url
    self.__api_key = api_key

  def categories(
    self,
    name = None,
    type_ = None,
    prefix = None
  ):
    return self.__get_paginated(
      "categories",
      "categories",
      {
        "name": name,
        "type": type_,
        "prefix": prefix
      }
    )

  def change_order(self, id):
    return self.__get("changeorders/" + id).json()

  def change_orders(
    self,
    con = None,
    name = None,
    status = None,
    resolution = None
  ):
    return self.__get_paginated(
      "changeorders",
      "changeOrders",
      {
        "con": con,
        "name": name,
        "status": status,
        "resolution": resolution
      }
    )

  def component(self, id):
    return self.__get("components/" + id).json()

  def components(
    self,
    mass = None,
    modified = None,
    cpn = None,
    name = None,
    eid = None,
    revision = None,
    category = None,
    cat_group = None,
    status = None,
    document_name = None,
    document_mime_type = None,
    document_revision = None,
    document_status = None,
    document_type = None,
    procurement = None
  ):
    return self.__get_paginated(
      "components",
      "components",
      {
        "mass": mass,
        "modified": modified,
        "cpn": cpn,
        "name": name,
        "eid": eid,
        "revision": revision,
        "category": category,
        "catGroup": cat_group,
        "status": status,
        "documentName": document_name,
        "documentMimeType": document_mime_type,
        "documentRevision": document_revision,
        "documentStatus": document_status,
        "documentType": document_type,
        "procurement": procurement
      }
    )

  def component_revision(self, id):
    return self.__get("component/revision/" + id).json()

  def component_revisions(
    self,
    mass = None,
    modified = None,
    cpn = None,
    name = None,
    eid = None,
    revision = None,
    category = None,
    cat_group = None,
    status = None,
    document_name = None,
    document_mime_type = None,
    document_revision = None,
    document_status = None,
    document_type = None,
    procurement = None
  ):
    return self.__get_paginated(
      "component/revision",
      "componentRevisions",
      {
        "mass": mass,
        "modified": modified,
        "cpn": cpn,
        "name": name,
        "eid": eid,
        "revision": revision,
        "category": category,
        "catGroup": cat_group,
        "status": status,
        "documentName": document_name,
        "documentMimeType": document_mime_type,
        "documentRevision": document_revision,
        "documentStatus": document_status,
        "documentType": document_type,
        "procurement": procurement
      }
    )

  def document(self, id):
    return self.__get("documents/" + id).json()

  def product(self, id):
    return self.__get("products/" + id).json()

  def products(
    self,
    mass = None,
    modified = None,
    cpn = None,
    name = None,
    eid = None,
    revision = None,
    status = None,
    document_name = None,
    document_mime_type = None,
    document_revision = None,
    document_status = None,
    document_type = None,
    procurement = None
  ):
    return self.__get_paginated(
      "products",
      "products",
      {
        "mass": mass,
        "modified": modified,
        "cpn": cpn,
        "name": name,
        "eid": eid,
        "revision": revision,
        "status": status,
        "documentName": document_name,
        "documentMimeType": document_mime_type,
        "documentRevision": document_revision,
        "documentStatus": document_status,
        "documentType": document_type,
        "procurement": procurement
      }
    )

  def product_revision(self, id):
    return self.__get("product/revision/" + id).json()

  def product_revisions(
    self,
    mass = None,
    modified = None,
    cpn = None,
    name = None,
    eid = None,
    revision = None,
    status = None,
    document_name = None,
    document_mime_type = None,
    document_revision = None,
    document_status = None,
    document_type = None,
    procurement = None
  ):
    return self.__get_paginated(
      "product/revision",
      "productRevisions",
      {
        "mass": mass,
        "modified": modified,
        "cpn": cpn,
        "name": name,
        "eid": eid,
        "revision": revision,
        "status": status,
        "documentName": document_name,
        "documentMimeType": document_mime_type,
        "documentRevision": document_revision,
        "documentStatus": document_status,
        "documentType": document_type,
        "procurement": procurement
      }
    )

  def user(self, id):
    return self.__get("users/" + id).json()

  def users(
    self,
    email = None,
    role = None
  ):
    return self.__get_paginated(
      "users",
      "users",
      {
        "email": email,
        "role": role
      }
    )

  def __get_paginated(self, path, resultKey, params):
    resources = []

    page = self.__get(path, params = {"perPage": 100, **params}).json()

    total_results = page["resultCount"]
    pages = math.ceil(total_results / 100)

    resources = resources + page[resultKey]

    if pages > 1:
      for page_index in range(2, pages):
        page = self.__get(path, params = {"perPage": 100, "page": page_index}).json()
        resources = resources + page[resultKey]

    return resources

  def __get(self, path, headers = {}, params = {}, data = None):
    headers["x-api-key"] = self.__api_key

    resp = requests.get(self.__base_url + path, headers = headers, params = params, data = data)

    if resp.status_code == 400:
      raise BadRequestError(resp.json()["message"], resp.json()["errors"])
    if resp.status_code == 401:
      raise AuthenticationError(resp.json()["message"])
    if resp.status_code == 403:
      raise ForbiddenError(resp.json()["message"])
    if resp.status_code == 404:
      raise NotFoundError(resp.json()["message"])
    else:
      return resp