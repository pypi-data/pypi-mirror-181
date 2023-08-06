#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import contextlib
import shutil
from typing import Generator, Optional
from io import BufferedReader
from urllib.parse import urljoin
import warnings

from dli.models import _get_or_create_os_path

from platform_services_lib.lib.services.dlc_attributes_dict import AttributesDict
from platform_services_lib.lib.aspects.decorators import analytics_decorator, logging_decorator, log_public_functions_calls_using
from platform_services_lib.lib.context.urls import consumption_urls


class FileModel(AttributesDict):

    @contextlib.contextmanager
    def open(self) -> Generator[BufferedReader, None, None]:
        """
        Context manager that yields a file like object.

        :example:
            
            .. code-block::

                with file.open() as f:
                    print(f.read())
                    
        
        .. note::
            
            The return type is a BufferedReader. This is the
            raw HTTP stream. This means that unlike usual file
            objects you can no seek it, it can only be read
            in order. So save to a file or buffer if you wish
            to manipulate the file out of order.

        """
        response = self._client.session.get(
            urljoin(
                self._client._environment.consumption,
                consumption_urls.consumption_download.format(
                    id=self.datafile_id,
                    path=self.path
                )
            ),
            stream=True
        )
        # otherwise you get raw secure
        response.raw.decode_content = True
        yield response.raw
        response.close()

    def download(self, to='./', flatten=False, rename_file: Optional[str] = '0') -> str:
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

        This `dataset.download` call will download the contents from S3.

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

        :param str rename_file: Please ignore, this parameter exists to provide compatibility with the
            `instance_model.download` function (which is deprecated).
            When `rename_file` is not None then we want to rename the file (though not the
            extension), so the name `foo.parquet`will become `bar.parquet` and the name `foo` (no file extension) will
            become `bar` (no file extension). This is only used when the parameter flatten=True.

        :return: Directory to path of the downloaded files.

        :example:

            Downloading without flatten:

            .. code-block:: python

                >>> dataset.instances.lastest().files()[0].download('./local/path/')
                './local/path/as_of_date=2019-09-10/type=full/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',


        :example:

            When flatten = True, we remove the s3 structure. Example:

            Example output for new behaviour:

            .. code-block:: python

                >>> dataset.instances.lastest().files()[0].download('./local/path/', flatten=True)
                './local/path/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',

        """

        warnings.warn(
            'This method is to be deprecated and will be removed after release 1.20.0. '
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

        # A user can get to this function by either:
        # 1. calling file_model `download` directly.
        # 2. calling instance_model `download` which indirectly calls file_model `download`.

        to_path = _get_or_create_os_path(
            s3_path=self.path, to=to, flatten=flatten, rename_file=rename_file
        )

        print(f'Downloading {self.path} to: {to_path}...')

        with self.open() as download_stream:
            with open(to_path, 'wb') as target_download:
                # copyfileobj is just a simple buffered
                # file copy function with some sane
                # defaults and optimisations.
                shutil.copyfileobj(
                    download_stream, target_download
                )
                print(f'Completed download to: {to_path}.')

        return to_path


log_public_functions_calls_using(
    [analytics_decorator, logging_decorator],
    class_fields_to_log=['datafile_id', 'path']
)(FileModel)
