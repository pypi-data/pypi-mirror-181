#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import multiprocessing
from typing import List, Optional
from concurrent.futures.thread import ThreadPoolExecutor
from urllib.parse import urljoin
import humps  # noqa: I900
import warnings

from dli.models.file_model import FileModel

from platform_services_lib.lib.context.urls import consumption_urls
from platform_services_lib.lib.aspects.decorators import analytics_decorator, logging_decorator, log_public_functions_calls_using
from platform_services_lib.lib.services.dlc_attributes_dict import AttributesDict

THREADS = multiprocessing.cpu_count()


class InstanceModel(AttributesDict):

    def __init__(self, **kwargs):
        # Ignore the datafile's files
        kwargs.pop('files', [])
        super().__init__(**kwargs)

    def files(self) -> List[FileModel]:
        """

        :example:

            Basic usage:

            .. code-block:: python

                dataset = client.datasets.get('some-dataset-short-code')
                dataset.instances.latest().files()

        :return: list of file models for files in the instance.
        """
        url = urljoin(
            self._client._environment.consumption,
            consumption_urls.consumption_manifest.format(
                id=self.datafile_id
            )
        )

        response = self._client.session.get(url)
        return [
            self._client._File(
                datafile_id=self.datafile_id,
                **d['attributes']
            )
            for d in response.json()['data']
        ]

    @classmethod
    def _from_v1_entity(cls, entity, page_size=None):
        properties = humps.decamelize(entity['properties'])
        return cls(**properties)

    def download(self, to: Optional[str]='./', flatten: Optional[bool]=False) -> List[str]:
        """
        .. deprecated:: 1.20.0
            This method is to be deprecated and will be removed after release 1.21.0.
            Please change your workflow to instead get the dataset and then call download on
            that dataset. The new method has these features:
            1. Improved download speed.
            2. Increased stability when downloading gigabyte sized files.
            3. Advanced filtering across all instances. Filters can be provided to target data
            within specific partitions
            that exist on S3 for that dataset. For example, you can filter using `as_of_date`
            to get data from a single instance of the dataset, or target a range of
            `as_of_dates`, or get data from all the dates. Within your target you can
            filter on `country` to download only data on that date for that country  e.g.

        .. code-block:: python

            import dli

            client = dli.connect()

            dataset = client.datasets.get(
               short_code='ExampleDatasetShortCode',
               organisation_short_code='IHSMarkit',
            )

            dataset.download(
                destination_path='/some/path/',
                partitions=['as_of_date>=2020-01-01','country=US'],
            )

        Download the files for the instance, then return a list of the file
        paths that were written.

        :param str to: The path on the system, where the files
            should be saved. must be a directory, if doesn't exist, will be
            created.

        :param bool flatten: The flatten parameter default behaviour
            (flatten=False) will allow the user to specify that they would
            like to keep the underlying folder structure when writing the
            downloaded files to disk.

            When `flatten` is set to True, the folder structure is removed and all the data is downloaded to the
            specified path with the files re-named with sequential numbers (to avoid the issue of file names being
            identical across multiple partitions). The only reason to set this parameter to True is when using a
            Windows machine that has the limitation that the path length cannot be greater than 260-character and
            you are downloading a dataset with a folder structure that will not fit within the 260-character limit.

            Example:
            [
              'storm/climate/storm_data/storm_fatalities/as_of_date=2019-09-10/type=full/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',
              'storm/climate/storm_data/storm_fatalities/as_of_date=2019-09-10/type=full/StormEvents_details-ftp_v1.0_d1951_c20160223.csv.gz'
            ]

            When flatten = True, we remove the s3 structure. Example:

            Example output for new behaviour:
            [
              '1.csv.gz',
              '2.csv.gz'
            ]

        :return: List of paths to the downloaded files.

        :example:

            Downloading without flatten:

            .. code-block:: python

                >>> dataset = client.datasets.get(short_code='ExampleDatasetShortCode', organisation_short_code='IHSMarkit')
                >>> dataset.instances.latest().download('./local/path/')
                [
                  'as_of_date=2019-09-10/type=full/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',
                  'as_of_date=2019-09-11/type=full/StormEvents_details-ftp_v1.0_d1951_c20160223.csv.gz'
                ]


        :example:

            When flatten = True, we remove the s3 structure. Example:

            Example output for new behaviour:

            .. code-block:: python

                >>> dataset.instances.latest().download('./local/path/', flatten=True)
                [
                  'StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',
                  'StormEvents_details-ftp_v1.0_d1951_c20160223.csv.gz'
                ]


        """

        warnings.warn(
            'This method is to be deprecated and will be after release 1.20.0. '
            '\nPlease change your workflow to instead get the dataset and then call download on '
            'that dataset. The new method has these features: '
            '\n1. Improved download speed.'
            '\n2. Increased stability when downloading gigabyte sized files.'
            '\n3. Advanced filtering across all instances. Filters can be provided to target data '
            'within specific partitions '
            'that exist on S3 for that dataset. For example, you can filter using `as_of_date` '
            'to get data from a single instance of the dataset, or target a range of '
            '`as_of_dates`, or get data from all the dates. Within your target you can '
            'filter on `country` to download only data on that date for that country e.g. '
            '\n\n  import dli'
            '\n\n  client = dli.connect()'
            "\n\n  dataset = client.datasets.get(dataset_short_code='ExampleDatasetShortCode', "
            "organisation_short_code='IHSMarkit')"
            "\n\n  dataset.download(partitions=['as_of_date>=2020-01-01','country=US'], destination_path='/some/path/')"
            '\n\nThis `dataset.download` call will download the contents from S3.',
            PendingDeprecationWarning
        )

        files = self.files()

        def _download(index_and_file: (int, FileModel)):
            index, file_ = index_and_file
            return file_.download(to=to, flatten=flatten, rename_file=str(index))

        threads = min(THREADS, max(1, len(files)))
        with ThreadPoolExecutor(max_workers=threads) as executor:
            return list(executor.map(_download, enumerate(files)))

    def __str__(self):
        return f"\nINSTANCE {self.datafile_id} (size: {self.total_size/1048576 :.2f} Mb)"


log_public_functions_calls_using(
    [analytics_decorator, logging_decorator],
    class_fields_to_log=['datafile_id']
)(InstanceModel)


