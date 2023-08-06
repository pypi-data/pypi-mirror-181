#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
from typing import Dict, List

from platform_services_lib.lib.context.urls import dataset_urls
from platform_services_lib.lib.aspects.decorators import analytics_decorator, logging_decorator, log_public_functions_calls_using
from platform_services_lib.lib.adapters.pagination_adapters import Paginator
from platform_services_lib.lib.services.dlc_attributes_dict import AttributesDict


@log_public_functions_calls_using(
    [analytics_decorator, logging_decorator], class_fields_to_log=['dictionary_id']
)
class DictionaryModel(AttributesDict):

    @property
    def id(self):
        return self.dictionary_id

    def __init__(self, json, client=None):
        self._client = client

        super().__init__(
            json['attributes'],
            dictionary_id=json['id'],
        )

    def _register(self, fields: List[Dict], **kwargs):
        """
          Registers dictionary metadata for a dataset. Synonymous with .edit() as both are on a POST route.

          :param str dataset_id: Id of the dataset for the dictionary.
          :param list[dict] fields: Non empty list of `Field` as described below.
          :param **kwargs: Unused, future extensions

          :returns: The registered dictionary

          Types
          =====

          Dictionary Field:

          .. code-block:: python

              {
                  name	          string  - required
                  type	          string  - required
                  nullable        boolean - required
                  description	  string  - optional
                  added_on        string  - optional
              }


              my_dictionary = client.register_dictionary(
                  "my-dataset-id",
                  fields=my_dictionary_fields,
              )
          """
        return self.edit(fields, **kwargs)

    def _edit(self, fields: List[Dict], **kwargs):
        """
           Updates dictionary metadata for a dataset.
           If a field is passed as ``None`` then the field will not be updated.

           :param str dataset_id: Id of the dataset for the dictionary_instance.
           :param list[dict] fields: Optional. If provided, a non empty list of `Field` as described below.

           .. code-block:: python

                   # Field:
                   {
                       "name": "field_a", 	    # name of the column.
                       "nullable": True,  		# defaulted to True - A boolean indicating whether the field is nullable or not.
                       "metadata": None			# optional dictionary with metadata for this column.
                   }

           :returns: The updated dictionary.
           :rtype: dli.models.dictionary_model.DictionaryModel

           - **Sample**

           .. code-block:: python

                   # Updating description and valid_as_of date for my dictionary
                   client = dli.connect()
                   my_updated_schema = client.edit_dictionary(
                       "my-dataset-id",
                       fields=my_dictionary_fields,
                   )
       """
        response = self._client.session.post(
            dataset_urls.dataset_dictionary.format(dataset_id=self.dataset_id),
            json={'data': {'attributes': {'fields': fields}}}
        )

        return DictionaryModel(response.json()['data'], client=self)

    def _delete(self):
        self._client.session.delete(dataset_urls.dataset_dictionary.format(dataset_id=self.dataset_id))
