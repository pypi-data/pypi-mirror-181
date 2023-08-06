from typing import List, Dict
from deprecated import deprecated

from dli.models.dictionary_model import DictionaryModel
from platform_services_lib.lib.aspects.base_component import BaseComponent
from platform_services_lib.lib.context.urls import dataset_urls

class Dictionary(BaseComponent):

    @deprecated(reason='client.register_dictionary(<dataset_id>, ...) is deprecated. '
                'Please use client.datasets.get(<dataset_shortcode>).dictionary_with_metadata().register(<fields>)', version="1.18.0")
    def register_dictionary(
        self,
        dataset_id,
        fields: List[Dict],
        **kwargs
    ):
        """
        Registers dictionary metadata for a dataset.

        :param str dataset_id: Id of the dataset for the dictionary.
        :param list[dict] fields: Non empty list of `Field` as described below.
        :param **kwargs: Unused, future extensions

        :returns: The registered dictionary

        Types
        =====

        Dictionary Field:

        .. code-block:: python

            {
                name	        string  - required
                type	        string  - required
                nullable        boolean - required
                description	    string  - optional
                added_on        string  - optional
            }


            my_dictionary = client.register_dictionary(
                "my-dataset-id",
                fields=my_dictionary_fields,
            )
        """
        response = self.session.post(
            dataset_urls.dataset_dictionary.format(dataset_id=dataset_id),
            json={'data': {'attributes': {'fields': fields}}}
        )

        return DictionaryModel(response.json()['data'], client=self)

    @deprecated(reason='client.get_dictionary(<dataset_id>) is deprecated. '
                'Please use client.datasets.get(<dataset_shortcode>).dictionary_with_metadata()', version="1.18.0")
    def get_dictionary(self, dataset_id):
        """
        Looks up dictionary for a dataset.

        :param str dataset_id: The id of the dataset under which the dictionary is registered.
        :returns: The dictionary.

        - **Sample**

        .. code-block:: python

                client = dli.connect()
                dictionary = client.get_dictionary('my_dataset_id')

        """
        try:
            schema = self.session.get(dataset_urls.dataset_dictionary.format(dataset_id=dataset_id))
            json = schema.json()['data']
            return self._DictionaryV2(json, client=self)
        except Exception as e:
            print("There is no current dictionary available.")
            return self._DictionaryV2(json={'attributes': {'fields':[], 'dataset_id': dataset_id}, 'id': None}, client=self)

    @deprecated(reason='client.delete_dictionary(<dataset_id>) is deprecated. '
                'Please use client.datasets.get(<dataset_shortcode>).dictionary_with_metadata().delete()', version="1.18.0")
    def delete_dictionary(self, dataset_id):
        """

        Marks a dictionary for a dataset as deleted.

        :param str dataset_id: The id of the dataset under which the dictionary is registered.
        :returns: None

        - **Sample**

        .. code-block:: python

                # Delete dictionary

                client = dli.connect()
                client.delete_dictionary(dataset_id='my_dataset_id')

        """

        self.session.delete(dataset_urls.dataset_dictionary.format(dataset_id=dataset_id))

    @deprecated(reason='client.edit_dictionary(<dataset_id>) is deprecated. '
                'Please use client.datasets.get(<dataset_shortcode>).dictionary_with_metadata().edit(<payload: List[Dict]>)', version="1.18.0")
    def edit_dictionary(
        self,
        dataset_id,
        fields: List[Dict],
        **kwargs
    ):
        """
        Updates dictionary metadata for a dataset.
        If a field is passed as ``None`` then the field will not be updated.

        :param str dataset_id: Id of the dataset for the dictionary_instance.
        :param list[dict] fields: Optional. If provided, a non empty list of `Field` as described below.

        .. code-block:: python

                # Field:
                {
                    "name": "field_a", 		               # name of the column.
                    "nullable": True,  			           # defaulted to True - A boolean indicating whether the field is nullable or not.
                    "description": "field description"	   # optional description of this field
                    'added_on': '2022-04-21'               # the string representation of the date when the field was added
                }

        :returns: The updated dictionary.
        :rtype: dli.models.dictionary_model.DictionaryModel

        - **Sample**

        .. code-block:: python

                # Updating dictionary
                client = dli.connect()
                my_updated_schema = client.edit_dictionary(
                    "my-dataset-id",
                    fields=my_dictionary_fields,
                )
        """

        response = self.session.post(
            dataset_urls.dataset_dictionary.format(dataset_id=dataset_id),
            json={'data': {'attributes': {'fields': fields}}}
        )

        return DictionaryModel(response.json()['data'], client=self)
