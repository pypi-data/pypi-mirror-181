#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import datetime
import http.client
import json
import logging
import textwrap
import uuid
import warnings
from collections import defaultdict
from functools import partial
from typing import List, Optional, Union, Dict, Set
from urllib.parse import urljoin
from warnings import warn

import pandas
import pyarrow
from urllib3.exceptions import ProtocolError  # noqa: I900
from pyarrow.lib import ArrowInvalid
from tabulate import tabulate

from dli.models.dictionary_model import DictionaryModel
from dli.models.dataset_model import DatasetModel
from dli.models.sample_data_model import SampleDataModel

from platform_services_lib.lib.services.exceptions import DataframeStreamingException
from platform_services_lib.lib.aspects.decorators import analytics_decorator, logging_decorator, log_public_functions_calls_using
from platform_services_lib.lib.context.urls import consumption_urls, dataset_urls
from platform_services_lib.lib.handlers.s3_dataset_handler import S3PathDetails
from platform_services_lib.lib.handlers.s3_partition_handler import match_partitions, get_partitions_in_filepath

trace_logger = logging.getLogger('trace_logger')


class StructuredDatasetModel(DatasetModel):

    def __init__(self, page_size=25, **kwargs):
        super().__init__(**kwargs,)

        #: access to the :class:`~dli.models.InstanceModelCollection` (see :ref:`Instances`) to get individal files in the dataset, not the dataset itself.
        self.instances = self._client._InstancesCollection(dataset=self, page_size=page_size)
        self.fields_metadata = None

    def __repr__(self):
        return f'<Structured Dataset short_code={self.short_code}>'

    def __str__(self):
        separator = "-" * 80
        splits = "\n".join(textwrap.wrap(self.description))

        return f"\nDATASET \"{self.short_code}\" [{self.data_format}]\n" \
               f">> Shortcode: {self.short_code}\n"\
               f">> Available Date Range: {self.first_datafile_at} to {self.last_datafile_at}\n" \
               f">> ID: {self.id}\n" \
               f">> Published: {self.publishing_frequency} by {self.organisation_name}\n" \
               f">> Accessible: {self.has_access}\n" \
               f"\n" \
               f"{splits}\n" \
               f"{separator}"

    def __custom_filter(
        self,
        partitions: List[str],
        paths: List[S3PathDetails],
    ) -> List[S3PathDetails]:
        """
        Filters that apply to Structured datasets
        """

        trace_logger.info(
            f"Number of paths on S3 for this dataset "
            f"after filtering for load type: '{len(paths)}'"
        )

        if partitions:
            # Only return paths that match the partition(s) provided.
            paths = [
                path for path in paths if match_partitions(path["Key"], partitions)
            ]

        return paths

    @property
    def sample_data(self) -> SampleDataModel:
        return SampleDataModel(self)

    def dask_dataframe(
        self,
        # Parameters for reading from .parquet and .csv format files:
        partitions: Optional[Union[str, List[str]]] = None,
        # Parameters for reading from .parquet and .csv formats:
        **kwargs
    ):
        """
        Read a dataset into a Dask DataFrame.

        WARNING: Specific versions of the dependency S3FS have a version constraint between aiobotocore and botocore
        that conflicts with other dependencies. This was fix in S3FS release `2021.11.1` (but conflicts may be
        re-introduced in future releases of S3FS).

        WARNING: The dependency Pandas 1.0.4 has an issue reading parquet due
        to a Pandas library mismatch. This was fixed in Pandas 1.0.5. We
        advise users to not use Pandas 1.0.4.

        Background on Dask:

        A Dask DataFrame can be used to compute a Pandas Dataframe. Dask has
        the advantage of being able to process data that would be too large
        to fit into memory in a single Pandas Dataframe. The use case is to
        read the files with Dask, apply operations such as filtering and
        sorting to the Dask Dataframe (which implements most of the Pandas
        API) and finally compute the result to a Pandas Dataframe. As you
        have already done the filtering in Dask, the resulting Pandas
        Dataframe will be smaller in memory than if you tried to do
        everything in a single Pandas Dataframe.

        * Memory:

            *   Like Spark, when low on RAM it can save intermediate results to a temp directory on disk. This means more data can be processed.
            *   Copies of data will be removed from RAM when they are written to disk. Dask has the advantage of being able to process data that would be too large to fit into memory in a single Pandas Dataframe. As you have done the filtering in Dask, the Pandas Dataframe will be smaller in memory than if you tried to do everything in a single Pandas Dataframe.
            *   Lazy evaluation - Data is processed only when it is needed (like Spark). This means that less data needs to be in memory at one time before processing begins, unlike Pandas.

        * Speed - Can use a local or a remote cluster to process data in parallel. A cluster of 3 nodes would in an ideal world be 3 times faster (but usually it will be less due to network transfer speed between nodes). A Jupyter Notebook plugin is available to visualise the cluster. It is possible to have the nodes on your:

            * Local laptop.
            * Remote laptops (so a group of laptops can share the load).
            * Kubernetes cluster.

        *	Schema mismatch - clear instructions are given to the user for solving schema type mismatch. However, this is not automatically resolved (unlike Spark) and requires the user to add a `dtype` parameter (explained in the example below). Unfortunatly out-of-the-box it uses the pyarrow engine (the same as Pandas) which does not automatically support additive schemas. For dealing with additive schemas, you can:

            1. Change your code to read one file at a time as a Dask DataFrame, then `concat` the DataFrames together. The `concat` behaviour is the same as Pandas and will merge the schemas.
            2. Or switch the `engine` parameter from `pyarrow` to `fastparquet` and install `pip install fastparquet python-snappy`. Note this is difficult to install on Windows 10.

        *	API stability - Supports the API for Pandas, however they promise more stability between versions so if Pandas change something in their API, the Dask API should not change.
        *	Community support - Enterprise support is available through Coiled.io which is run by the creators of Dask.

        You can use the SDK to get a dataset, and then use the `dask_dataframe` endpoint which will return a Dask task that is setup to read the data files directly from S3 without downloading the files to the local machine.

        Please install or upgrade the SDK using the command `pip install dli[dask]` so that all of the dask plugins are installed.

        This endpoint can read data files in the following file formats:

            * .parquet
            * .csv

        into a Dask.dataframe, one file per partition.  It selects the index among the sorted columns if any exist.

        :Example:

            .. code-block:: python

                dataset.dask_dataframe()

            The Dask dataframe will calculate the tasks that need to be run, but
            it does not evaluate until you call an action on it. To run a full
            evaluation across the whole dataset and return a Pandas dataframe, run:

            .. code-block:: python

                dataset.dask_dataframe().compute()

            To run the evaluation and only return the first ten results:

            .. code-block:: python

                dataset.dask_dataframe().head(10)

            An additional parameter needs to be added when you are reading from
            compressed .csv files, for example the .csv.gz format.

            .. code-block:: python

                dataset.dask_dataframe(compression='gzip')

            Some datasets have problems with the column types changing between
            different data files. Dask will stop with an error message that
            explains the types you should pass. For example, if the error message
            that looks like this:

            /*
            ValueError: Mismatched dtypes found in `pd.read_csv`/`pd.read_table`.

            +------------+---------+----------+
            | Column     | Found   | Expected |
            +------------+---------+----------+
            | STATE_FIPS | float64 | int64    |
            +------------+---------+----------+

            Usually this is due to dask's dtype inference failing, and
            *may* be fixed by specifying dtypes manually by adding:

            dtype={'STATE_FIPS': 'float64'}
            */

            then you should do as the message says and add the parameters, then
            re-run. In this case the fix would look like this:

            .. code-block:: python

                dataset.dask_dataframe(dtype = {'STATE_FIPS': 'float64'})

            The Dask code for inferring schemas for .csv format files takes a sample from the first
            file it reads. The default behaviour is to infer using the first 10 rows of the first file.
            In some cases this value is too low, so from Dask release `2021.07.0` onwards you can
            increase the .csv file sample size by using the parameter `sample_rows` like this:

            .. code-block:: python

                dataset.dask_dataframe(sample_rows=100)

            You are able to provide extra parameters to this endpoint that will
            be used by dask.

            The following parameters are used to reading from
            .parquet and .csv format files:

        Parameters
        ----------
        :param List[str] partitions: Optional. A list of filters (partitions)
            to apply to the file paths on S3.

            This allows the user to filter the files they want to read from
            before they  have to read any data. This will reduce the amount
            of redundant data that is transferred over the network and
            reduce the amount of memory required on the user's machine.

            For any dataset, the paths on S3 may contain
            partitions that are key-value pairs in the format
            `<key>=<value>`, for example in the path:

                s3://example/as_of_date=2020-01-01/country=US/file.extension

            there are the partitions:

            * `country=US`
            * `as_of_date=2020-01-01`.

            You can find the available list of partitions for a dataset by
            calling the dataset's `.partitions()` endpoint.

            You can specify a list of partitions you want to get data from by
            passing in a list in the format `<key><operator><value>`. Please
            note that you should not include any extra quotation marks around
            the value, so `as_of_date=2020-01-01` is valid but
            `as_of_date='2020-01-01'` is invalid.

            The supported operators are: `<=`, `<`, `=`, `>`, `>=`.

            For a partition where the key is named `as_of_date`, the value
            is treated as a Python datetime object, so comparisons are done
            between dates. This means that the `>=` and `<=` operators can
            be used to get data in a date range where more than one
            `as_of_date` exists. For example, to get data from only dates in
            January 2020:

            .. code-block:: python

                dataset.dask_dataframe(partitions=[
                    'as_of_date>=2020-01-01',
                    'as_of_date<=2020-01-31',
                ])

            Other key names will have their values treated as string, so the
            operators will perform Python string comparisons.

            .. code-block:: python

                dataset.dask_dataframe(partitions=[
                    'country=US'
                ])

            A list of partitions is applied as a logical AND. So specifying
            `as_of_date` and `country` will match only those paths that
            match both `as_of_date` AND `country`.

            .. code-block:: python

                dataset.dask_dataframe(partitions=[
                    'as_of_date>=2020-01-01',
                    'country=US',
                ])

            **kwargs
                Extra keyword arguments can be passed into Dask. This endpoint calls `dask.dataframe.read_parquet` and
                `dask.dataframe.read_csv` depending on what the underlying data format for the dataset. The parameters on
                each of these functions are updated by a third party and may change depending on which version of Dask and
                Pandas are installed on the user's virtual environment.

                For working with datasets that are in PARQUET format, see the documentation for
                `dask.dataframe.read_parquet` for a list of parameters that are on available for the latest version of Dask.

                https://docs.dask.org/en/latest/generated/dask.dataframe.read_parquet.html

                For working with datasets that are in CSV format, see the documentation for both `dask.dataframe.read_csv`
                and `pandas.read_csv()` for a list of parameters that are on available for the latest version of Dask.

                https://docs.dask.org/en/latest/generated/dask.dataframe.read_csv.html

                https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html#pandas.read_csv
        """

        dependency_message = \
            '\n\nFix:' \
            '\nBefore you can use Dask the correct dependencies must be installed into ' \
            'your virtual environment.' \
            '\nNote: If you are running your code in a Jupyter Notebook, ' \
            'then before installing you will need to quit the ' \
            '`jupyter notebook` process that is running on the command ' \
            'line and start it again so that your notebooks see the ' \
            'version of Dask you have now installed.' \
            '\nPlease install DLI with Dask and S3FS using one of the following commands:' \
            '\n1. Run `pip install dli[dask] && pip install s3fs` to install this SDK ' \
            'with a compatible version of dask.' \
            '\n2. Or run `pip install dask[dataframe] && pip install s3fs` to install the latest ' \
            'version of Dask (which may be untested with this version ' \
            'of the SDK).'

        try:
            import dask.dataframe as dd
            import s3fs
        except (ImportError, AttributeError) as e:
            raise RuntimeError(dependency_message) from e

        self._check_access()

        start = datetime.datetime.now()
        request_id = str(uuid.uuid4())

        paths = self.__list(
            request_id=request_id,
            partitions=partitions,
        )

        if len(paths) == 0:
            trace_logger.info(
                'dask_dataframe endpoint:'
                f"\nrequest_id: '{request_id}'"
                f"\nendpoint_url: '{self._DatasetModel__handler.endpoint_url()}'"
                f"\nno paths retrieved from specified partitions"
                '\nlisting paths elapsed time: '
                f"'{datetime.datetime.now() - start}'"
            )
            print('Sorry, no data in the specified partitions. You can list the '
                  'available partitions for the dataset using the partitions method:'
                  'dataset.partitions()')
            return dd.from_pandas(pandas.DataFrame([]), 1)

        # Reverse the list of S3 keys so that the most recent schema is first. This matches what we do for Consumption
        # dataframe additive schema where we assume the most recent as_of has a superset of the schema so that
        # additive schema code works.
        # Do not try to change this code to S3 LIST like Consumption which reads the most recent common prefix first.
        # For Consumption this is good as you start streaming back quickly without a timeout waiting for the complete
        # S3 LIST (that can take more than 60 seconds for highly partitioned datasets). For SDK we do not have a
        # problem with LIST timing out as we run client side and paginate. In cases where the dataset is highly
        # partitioned, the performance is faster S3 listing the whole dataset (with our optimised code) and then
        # reversing the list versus doing it the Consumption way that causes one S3 LIST request per as_of.
        # TODO scott: I commented out as we would need to figure out why QA tests then don't seem to do additive schema
        # tests correctly, maybe their tests are broken, but right now no-one is asking for this and I'm doing support
        # tickets.
        #paths.reverse()

        storage_options = {
            'client_kwargs': {
                'endpoint_url': self._DatasetModel__handler.endpoint_url(),
            },
            'key': self._client.session.auth_key,
            'secret': 'noop',
        }

        data_format = self.data_format.lower()

        trace_logger.info(
            'dask_dataframe endpoint:'
            f"\nrequest_id: '{request_id}'"
            f"\nendpoint_url: '{self._DatasetModel__handler.endpoint_url()}'"
            f"\ndata_format: '{data_format}'"
            '\nlisting paths elapsed time: '
            f"'{datetime.datetime.now() - start}'"
        )

        def unsupported_keyword_message(ex: TypeError):
            return 'You passed one or more parameters to `dask_dataframe` that are not supported by the versions ' \
                'of Dask and Pandas that are installed. If you see an error message that looks like ' \
                "`read_csv() got an unexpected keyword argument 'some_parameter_name'` " \
                'then please remove that parameter from your call to `dask_dataframe`. ' \
                f'\nThe error message from Dask or Pandas was:\n{str(ex)}'

        if data_format == 'parquet':
            try:
                return dd.read_parquet(
                    path=paths,
                    storage_options=storage_options,
                    **kwargs
                )
            except (ImportError, AttributeError) as e:
                raise AttributeError(dependency_message) from e
            except TypeError as e:
                raise TypeError(unsupported_keyword_message(e)) from e
        elif data_format == 'csv':
            try:
                return dd.read_csv(
                    urlpath=paths,
                    storage_options=storage_options,
                    **kwargs
                )
            except (ImportError, AttributeError) as e:
                raise AttributeError(dependency_message) from e
            except TypeError as e:
                raise TypeError(unsupported_keyword_message(e)) from e
        else:
            print(
                f"Sorry, the dataset is in the format '{data_format}'. This "
                'endpoint is only setup to handle parquet and csv.'
            )
            return None

    def partitions(self) -> Dict[str, List[str]]:
        """
        Retrieves the list of available partitions for a given dataset.

        The data onboarding team have structured the file paths on S3 with
        simple partitions e.g. `as_of_date` or `location`.

        Their aim was to separate the data to reduce the size of the
        individual files. For example, data that has a `location` column with
        the options `us`, `eu` and `asia` can be separated into S3 paths like
        so:

        .. code-block::

            package-name/dataset/as_of_date=2019-09-10/location=eu/filename.csv
            package-name/dataset/as_of_date=2019-09-10/location=us/filename.csv

        in this case the `partitions` will be returned as:

        .. code-block::

            {'as_of_date': ['2019-09-10'], 'location': ['eu', 'us]}

        :Example:

            Basic usage:

            .. code:: python

                dataset.partitions()

        """
        if hasattr(self, 'organisation_short_code'):
            # Code that goes via S3 proxy requires that the dataset attributes contain the
            # `organisation_short_code`. A bug in the Catalogue means that the
            # `organisation_short_code` is not yet returned if the user gets a dataset by this
            # code path:
            #
            #   client.packages.get(name='example')
            #   datasets = packageDetails.datasets()
            #
            #   for key, dataset in datasets.items():
            #       dataset.metadata()
            #
            # so we need this if-statement until the Catalogue team release a fix to production.

            partitions: Dict[str, Set] = defaultdict(set)
            all_splits = (
                get_partitions_in_filepath(path) for path in self.__list()
            )

            # Accumulate the values for each partition in a set, which will only
            # keep unique values.
            for splits in all_splits:
                for k, v in splits:
                    partitions[k].add(v)

            # We want to return the values as a sorted list.
            return {k: sorted(v) for k, v in partitions.items()}
        else:
            # Old code. This can only be removed when the Catalogue fixes their dataset responses
            # in production to return the organisation short code for all dataset calls.
            response = self._client.session.get(
                urljoin(
                    self._client._environment.consumption,
                    consumption_urls.consumption_partitions.format(id=self.id)
                )
            )

            return response.json()["data"]["attributes"]["partitions"]

    def list(
        self,
        request_id=None,
        partitions: Optional[Union[str, List[str]]] = None,
        filter_path: Optional[str] = None,
        absolute_path: bool = True,
        skip_hidden_files: bool = True,
    ) -> List[str]:
        """
        List all the paths to files in the dataset. Calls go via the
        Datalake's S3 proxy, so the returned paths will be returned in the
        style of the S3 proxy, so in the pattern
        `s3://organisation_short_code/dataset_short_code/<path>`.
        S3 proxy does not return direct paths to the real location on S3 as
        they may be sensitive.

        The list will filter out paths where:
        * The size is zero bytes.
        * The name of any partition within the path is prefixed with a `.` or
        a `_` as that means it is intended as a hidden file.
        * The name of any partition within the path is exactly the word
        `metadata`.
        * It is a directory rather than a file.
        * Files with the wrong extension for the dataset's type i.e for
        a .parquet dataset we will return only .parquet files, zero .csv
        files.

        This list will filter based on `load_type` of the dataset. When the
        dataset's `load_type` is `Incremental Load` then files will be listed
        from all of the `as_of_date` partitions on S3. When the
        dataset's `load_type` is `Full Load` then files will be listed only
        the most recent `as_of_date` partition on S3.
        Please see the support library documentation for more information
        about how the `load type` affects the data you can access in a dataset:
        https://catalogue.datalake.ihsmarkit.com/__api_v2/documentation/knowledge_base/key_concepts.html#load-types 

        Parameters
        ----------
        :param str request_id: Optional. Automatically generated value
            used by our logs to correlate a user journey across several
            requests and across multiple services.

        :param List[str] partitions: Optional. A list of filters (partitions)
            to apply to the file paths on S3.

            This allows the user to filter the files they want to read from
            before they  have to read any data. This will reduce the amount
            of redundant data that is transferred over the network and
            reduce the amount of memory required on the user's machine.

            For any dataset, the paths on S3 may contain
            partitions that are key-value pairs in the format
            `<key>=<value>`, for example in the path:

                s3://example/as_of_date=2020-01-01/country=US/file.extension

            there are the partitions:

            * `country=US`
            * `as_of_date=2020-01-01`.

            You can find the available list of partitions for a dataset by
            calling the dataset's `.partitions()` endpoint.

            You can specify a list partitions you want to get data from by
            passing in a list in the format `<key><operator><value>`. Please
            note that you should not include any extra quotation marks around
            the value, so `as_of_date=2020-01-01` is valid but
            `as_of_date='2020-01-01'` is invalid.

            The supported operators are: `<=`, `<`, `=`, `>`, `>=` and
            `!=`.

            For a partition where the key is named `as_of_date`, the value
            is treated as a Python datetime object, so comparisons are done
            between dates. This means that the `>=` and `<=` operators can
            be used to get data in a date range where more than one
            `as_of_date` exists. For example, to get data from only dates in
            January 2020:

            .. code-block:: python

                dataset.list(partitions=[
                    'as_of_date>=2020-01-01',
                    'as_of_date<=2020-01-31',
                ])

            Other key names will have their values treated as string, so the
            operators will perform Python string comparisons.

            .. code-block:: python

                dataset.list(partitions=[
                    'country=US'
                ])

            A list of partitions is applied as a logical AND. So specifying
            `as_of_date` and `country` will match only those paths that
            match both `as_of_date` AND `country`.

            .. code-block:: python

                dataset.list(partitions=[
                    'as_of_date>=2020-01-01',
                    'country=US',
                ])

        :param str filter_path: Optional. If provided only a sub-paths on cloud storage (s3) matching
            the filter_path will be retrieved. This is less flexible than using
            the `partitions` parameter, so we recommend you pass in
            `partitions` instead. The `partitions` can deal with the
            partitions in the path being in any order, but filter_path relies
            on a fixed order of partitions that the user needs to know ahead
            of time.

            Example usage to get all paths that start with the `as_of_date`
            2020. Note this is a string comparison, not a datetime comparison.

            .. code-block:: python

                dataset.list(filter_path='as_of_date=2020')

        :param bool absolute_path: True (default) for returning an
            absolute path to the path on the S3 proxy. False to return a
            relative path (this is useful if using a TransferManager).

        :param bool skip_hidden_files: True (default) skips files that have
            been uploaded to S3 by Spark jobs. These usually start with a
            `.` or `_`.

        Example
        ----------
        :example:

            List all the paths to files in the dataset:

            .. code-block:: python

                dataset.list()

        :example:

            List the paths according to the partitions:

            .. code-block:: python

                dataset.list(partitions=[
                    'as_of_date>=2020-01-01',
                    'country=US',
                ])

        :example:

             List the paths according to the partitions, returning relative paths:

            .. code-block:: python

                dataset.list(partitions=[
                    'as_of_date>=2020-01-01',
                    'country=US',
                ], absolute_path=False)

        :example:

            List the paths according to the partitions, including paths of hidden files:

            .. code-block:: python

                dataset.list(partitions=[
                    'as_of_date>=2020-01-01',
                    'country=US',
                ], skip_hidden_files=False)

        """

        return self.__list(
            request_id=request_id,
            partitions=partitions,
            filter_path=filter_path,
            absolute_path=absolute_path,
            skip_hidden_files=skip_hidden_files,
        )

    def __list(
            self,
            request_id=None,
            partitions: Optional[Union[str, List[str]]] = None,
            filter_path: Optional[str] = None,
            absolute_path: bool = True,
            skip_hidden_files: bool = True,
    ) -> List[str]:
        """
        List all the paths to files in the dataset.

        This private function can be called internally by other functions
        such as `partitions` and `dask_dataframe`. This is private so that
        when there is an exception and aspects lists the public methods that
        we do not spam the logs.

        :param request_id:
        :param partitions:
        :param filter_path:
        :param absolute_path:
        :param skip_hidden_files:
        :return: List all the paths to files in the dataset.
        """
        if filter_path and partitions:
            raise ValueError(
                'Both `partitions` and `filter_path` are set. Please only '
                'provide one of these parameters.'
            )

        if type(partitions) == str:
            partitions = [partitions]

        return self._DatasetModel__list(
            request_id=request_id,
            custom_filter_func=partial(self.__custom_filter, partitions=partitions),
            filter_path=filter_path,
            absolute_path=absolute_path,
            skip_hidden_files=skip_hidden_files,
        )

    def download(
        self,
        destination_path: str,
        flatten: Optional[bool] = False,
        filter_path: Optional[str] = None,
        partitions: Optional[Union[str, List[str]]] = None,
    ) -> List[str]:
        """
        Downloads the original dataset files from the data lake to local copy
        destination of your choice.

        The flatten parameter retains only the file name, and places the
        files in the directory specified, else the files will be downloaded
        matching the directory structure as housed on the data lake.

        The filter path and partitions parameters specify that only a subset
        of the S3 path should be downloaded.

        Parameters
        ----------
        :param destination_path: The path on the system, where the
            files should be saved. Must be a directory, if doesn't exist, will
            be created.

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

        :param str filter_path: Optional. If provided only a sub-paths on cloud storage (s3) matching
            the filter_path will be retrieved. This is less flexible than using
            the `partitions` parameter, so we recommend you pass in
            `partitions` instead. The `partitions` can deal with the
            partitions in the path being in any order, but filter_path relies
            on a fixed order of partitions that the user needs to know ahead
            of time.

            Example usage to get all paths that start with the `as_of_date`
            2020. Note this is a string comparison, not a datetime comparison.

            .. code-block:: python

                dataset = client.datasets.get(short_code='ExampleDatasetShortCode', organisation_short_code='IHSMarkit')
                dataset.download(filter_path='as_of_date=2020')

        :param List[str] partitions: Optional. A list of filters (partitions)
            to apply to the file paths on S3.

            This allows the user to filter the files they want to read from
            before they  have to read any data. This will reduce the amount
            of redundant data that is transferred over the network and
            reduce the amount of memory required on the user's machine.

            For any dataset, the paths on S3 may contain
            partitions that are key-value pairs in the format
            `<key>=<value>`, for example in the path:

                s3://example/as_of_date=2020-01-01/country=US/file.extension

            there are the partitions:

            * `country=US`
            * `as_of_date=2020-01-01`.

            You can find the available list of partitions for a dataset by
            calling the dataset's `.partitions()` endpoint.

            You can specify a list of partitions you want to get data from by
            passing in a list in the format `<key><operator><value>`. Please
            note that you should not include any extra quotation marks around
            the value, so `as_of_date=2020-01-01` is valid but
            `as_of_date='2020-01-01'` is invalid.

            The supported operators are: `<=`, `<`, `=`, `>`, `>=` and
            `!=`.

            For a partition where the key is named `as_of_date`, the value
            is treated as a Python datetime object, so comparisons are done
            between dates. This means that the `>=` and `<=` operators can
            be used to get data in a date range where more than one
            `as_of_date` exists. For example, to get data from only dates in
            January 2020:

            .. code-block:: python

                dataset.download(partitions=[
                    'as_of_date>=2020-01-01',
                    'as_of_date<=2020-01-31',
                ])

            Other key names will have their values treated as string, so the
            operators will perform Python string comparisons.

            .. code-block:: python

                dataset.download(partitions=[
                    'country=US'
                ])

            A list of partitions is applied as a logical AND. So specifying
            `as_of_date` and `country` will match only those paths that
            match both `as_of_date` AND `country`.

            .. code-block:: python

                dataset.download(partitions=[
                    'as_of_date>=2020-01-01',
                    'country=US',
                ])

        :return: the list of the files that were downloaded successfully. Any
            failures will be printed.


        :example:

            Downloading without flatten:

            .. code-block:: python

                dataset = client.datasets.get(short_code='ExampleDatasetShortCode', organisation_short_code='IHSMarkit')
                dataset.download('./local/path/')

                [
                  'as_of_date=2019-09-10/type=full/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',
                  'as_of_date=2019-09-11/type=full/StormEvents_details-ftp_v1.0_d1951_c20160223.csv.gz'
                ]

        :example:

            Downloading with ``filter_path``

            .. code-block:: python

                dataset = client.datasets.get(short_code='ExampleDatasetShortCode', organisation_short_code='IHSMarkit')
                dataset.download(
                    './local/path/', filter_path='as_of_date=2019-09-10/'
                )
                [
                  'as_of_date=2019-09-10/type=full/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',
                ]


        :example:

            When flatten = True, we remove the s3 structure. Example:

            Example output for new behaviour:

            .. code-block:: python

                dataset = client.datasets.get(short_code='ExampleDatasetShortCode', organisation_short_code='IHSMarkit')
                dataset.download('./local/path/', flatten=True)
                [
                  'StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',
                  'StormEvents_details-ftp_v1.0_d1951_c20160223.csv.gz'
                ]


        """

        if filter_path and partitions:
            raise ValueError(
                'Both `partitions` and `filter_path` are set. Please only '
                'provide one of these parameters.'
            )

        if type(partitions) == str:
            partitions = [partitions]

        return self._DatasetModel__download(
            destination_path=destination_path,
            flatten=flatten,
            filter_path=filter_path,
            custom_filter_func=partial(self.__custom_filter, partitions=partitions),
            skip_hidden_files=True
        )

    def dataframe(
        self,
        nrows: Optional[int] = None,
        partitions: Optional[Union[str, List[str]]] = None,
        raise_: bool = True,
        use_compression: bool = False
    ) -> pandas.DataFrame:
        """
        Return the data from the files of the dataset
        as a pandas DataFrame (as per `load_type` logic).

        WARNING: The dependency Pandas 1.0.4 has an issue reading parquet due
        to an pandas library mismatch. This was fixed in Pandas 1.0.5.

        We currently support .csv and .parquet as our data file formats. The
        data files in the latest instance could all be .csv format or all be
        .parquet format. If there is a mix of .csv and .parquet or some other
        file format then we will not be able to parse the data and will
        return an error message.

        :param int nrows: Optional. The max number of rows to return.
            We use the nrows parameter to limit the amount of rows that are
            returned, otherwise for very large dataset it will take a long time
            or you could run out of RAM on your machine!
            If you want all of the rows, then leave this parameter set to the
            default None.

        :param List[str] partitions: Optional. A list of filters (partitions)
            to apply to the file paths on S3.

            This allows the user to filter the files they want to read from
            before they  have to read any data. This will reduce the amount
            of redundant data that is transferred over the network and
            reduce the amount of memory required on the user's machine.

            For any dataset, the paths on S3 may contain
            partitions that are key-value pairs in the format
            `<key>=<value>`, for example in the path:

                s3://example/as_of_date=2020-01-01/country=US/file.extension

            there are the partitions:

            * `country=US`
            * `as_of_date=2020-01-01`.

            You can find the available list of partitions for a dataset by
            calling the dataset's `.partitions()` endpoint.

            You can specify a list of partitions you want to get data from by
            passing in a list in the format `<key><operator><value>`. Please
            note that you should not include any extra quotation marks around
            the value, so `as_of_date=2020-01-01` is valid but
            `as_of_date='2020-01-01'` is invalid.

            The supported operators are: `<=`, `<`, `=`, `>`, `>=`.

            For a partition where the key is named `as_of_date`, the value
            is treated as a Python datetime object, so comparisons are done
            between dates. This means that the `>=` and `<=` operators can
            be used to get data in a date range where more than one
            `as_of_date` exists. For example, to get data from only dates in
            January 2020:

            .. code-block:: python

                dataset.dataframe(partitions=[
                    'as_of_date>=2020-01-01',
                    'as_of_date<=2020-01-31',
                ])

            Other key names will have their values treated as string, so the
            operators will perform Python string comparisons.

            .. code-block:: python

                dataset.dataframe(partitions=[
                    'country=US'
                ])

            A list of partitions is applied as a logical AND. So specifying
            `as_of_date` and `country` will match only those paths that
            match both `as_of_date` AND `country`.

            .. code-block:: python

                dataset.dataframe(partitions=[
                    'as_of_date>=2020-01-01',
                    'country=US',
                ])

        :param bool raise\_: Optional. Raise exception if the dataframe stream
            stopped prematurely

        :param use_compression: Optional. Whether the response from the
            backend should use compression. Setting to false should result
            in a faster initial response before the streaming begins.

        :example:

            Basic usage:

            .. code-block:: python

                    dataset = client.datasets.get(short_code='ExampleDatasetShortCode', organisation_short_code='IHSMarkit')
                    dataframe = dataset.dataframe()

        :example:

            Dataframe filtered by partition with nrows (partitions can be
            fetched using the `dataset.partitions()` endpoint:

            .. code-block:: python

                    dataset = client.datasets.get(short_code='ExampleDatasetShortCode', organisation_short_code='IHSMarkit')
                    dataframe = dataset.dataframe(
                        nrows=1000,
                        partitions=["as_of_date=2017-03-07"]
                    )
        """

        self._check_access()

        params = {}

        if nrows is not None:
            params['filter[nrows]'] = nrows

        if partitions is not None:
            if type(partitions) == str:
                partitions = [partitions]

            params['filter[partitions]'] = partitions

        dataframe_url = urljoin(
            self._client._environment.consumption,
            consumption_urls.consumption_dataframe.format(id=self.id)
        )

        headers = {}
        if not use_compression:
            headers['Accept-Encoding'] = 'identity;q=0'

        response = self._client.session.get(
            dataframe_url, stream=True,
            params=params,
            headers=headers,
        )

        try:
            # native_file only reads until end of dataframe
            # the rest of the stream has to be read from response raw.
            native_file = pyarrow.PythonFile(response.raw, mode='rb')

            # Now native_file "contains the complete stream as an in-memory
            # byte buffer. An important point is that if the input source
            # supports zero-copy reads (e.g. like a memory map,
            # or pyarrow.BufferReader), then the returned batches are also
            # zero-copy and do not allocate any new memory on read."
            reader = pyarrow.ipc.open_stream(native_file)

            dataframe = reader.read_pandas()
        except (
                ArrowInvalid,
                http.client.IncompleteRead,
                ProtocolError
        ) as ex:

            message = 'Sorry, the dataframe you are trying to read is too ' \
                      'large to fit into memory. Please consider one of ' \
                      'these alternatives:' \
                      '\n\n1. Run the same code on a machine that has more ' \
                      'RAM, for example a Jupyter Notebook hosted on an ' \
                      'AWS environment.' \
                      '\n2. Use a big data tool such as Spark, Dask or ' \
                      'similar to read the data via our S3 proxy. Unlike ' \
                      'Pandas, these big data tools are able to apply some ' \
                      'operations such as filtering without having to hold ' \
                      'all of the data into memory. See ' \
                      'https://catalogue.datalake.ihsmarkit.com/' \
                      '__api_v2/documentation/s3_proxy_tools/intro_s3.html ' \
                      f'\n\nOriginal exception: {ex}'

            raise ArrowInvalid(message) from ex

        # The pyarrow buffered stream reader stops once it
        # reaches the end of the IPC message. Afterwards we
        # get the rest of the data which contains the summary
        # of what we've downloaded including an error message.
        last_packet = response.raw.read()
        summary = json.loads(last_packet)

        if summary['status'] >= 400:
            exception = DataframeStreamingException(
                summary, dataframe_url, response=response,
            )

            # Optionally ignore bad data
            if raise_:
                raise exception
            else:
                warnings.warn(
                    str(exception),
                    UserWarning
                )

        return dataframe

    def contents(self):
        """
        Print IDs for all the instances in this dataset.

        :example:

            Basic usage:

            .. code-block:: python

                    dataset = client.datasets.get(short_code='ExampleDatasetShortCode', organisation_short_code='IHSMarkit')
                    contents = dataset.contents()

        Example output:

            INSTANCE 1111aaa-11aa-11aa-11aa-111111aaaaaa
        """
        for p in self.instances.all():
            print(str(p))

    def _dictionary_with_metadata(self) -> DictionaryModel:
        """
        Returns the dictionary model for the dictionary representing the fields in the dataset.
        For access to the fields themselves (List[Dict]), the user may use `ds.dictionary_with_metadata().fields`.

        Example usage:

        .. code:: python

            dataset = client.datasets.get('example-dataset-short-code')
            print(dataset.dictionary())

        :return: DictionaryModel
        """

        try:
            response = self._client.session.get(
                dataset_urls.dataset_dictionary.format(dataset_id=self.id)
            ).json()
        except Exception as e:
            print("There is no current dictionary available.")
            return self._client._DictionaryV2(json={'attributes': {'fields':[], 'dataset_id': self.id}, 'id': None}, client=self._client)

        # DO NOT RETURN .fields SINCE THIS LOSES THE METADATA OF THE DICTIONARY - RETURN A MODEL
        # followed by the fields for the dictionary...
        return self._client._DictionaryV2(
            {'id': response["data"]["id"], 'attributes': response["data"]["attributes"]},
            client=self._client
        )

    def dictionary(self) -> List[Dict]:
        """
        Helper method surround dictionary_with_metadata() for backwards-compatibility purposes.

        List of dictionaries for each field in the dataset's dictionary as
        returned by the Catalogue.

        If there are multiple historical values for the dataset's `dictionary`
        in the Catalogue, then you will see more than one item in the list,
        otherwise there will only be a single item in the list containing a
        dictionary of the current fields.

        Field names may include:

        * name
        * type
        * nullable
        * description
        * added_on

        :example:

            Basic usage:

            .. code:: python

                dataset = client.datasets.get('example-dataset-short-code')
                print(dataset.dictionary())

            Example output:

            .. code:: python

                [
                  {
                    'name': 'some-name',
                    'type': 'String',
                    'nullable': True,
                    'description': 'some-description'
                  }
                ]

        :return: List of each field in the dataset.
        """
        return self._dictionary_with_metadata().fields

    def info(self):
        """
        Prints the dataset's dictionary, showing each column name, type and nullability, if a dictionary
        for the dataset is available.

        :Example:

            Basic usage and example output for new behaviour:

            .. code-block:: python

                dataset = client.datasets.get(short_code='ExampleDatasetShortCode', organisation_short_code='IHSMarkit')
                dataset.info()
                name    type
                a       String (Nullable)
                b       Integer
                c       String


        """

        dct: DictionaryModel = self._dictionary_with_metadata()
        df = pandas.DataFrame(dct.fields)
        if df.shape[1] > 0:
            df["type"] = df.apply(
                lambda row: row["type"] + (" (Nullable)" if row["nullable"] else ""),
                axis=1)
            df = df[["name", "type"]]

            print(tabulate(df, showindex=False, headers=df.columns))
        else:
            print("No columns/info available.")


log_public_functions_calls_using(
    [analytics_decorator, logging_decorator],
    class_fields_to_log=['dataset_id']
)(StructuredDatasetModel)
