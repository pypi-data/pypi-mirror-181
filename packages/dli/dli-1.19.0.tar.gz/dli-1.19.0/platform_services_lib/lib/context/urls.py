#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#

class dataset_urls:
    datafiles = '/__api/datasets/{id}/datafiles/'
    latest_datafile = '/__api/datasets/{id}/latest-datafile/'

    # This endpoint returns either RO or RW dependent on your permissions
    # and this depends on the role you have on the package of the dataset you are requesting it for
    # User is Data Steward + Technical Support for Package parent Dataset = RW (read/write from/to s3)
    # User is not = RO (read from s3)

    # As a user, you need this in the SDK if you are trying to access the files directly. Catalogue takes care of the
    # RO/RW permissioning, so if you can access the dataset, you can access the data. If you use S3-Proxy, you use
    # the S3-Proxy's permissions (via your JWT), whereas here, you get the keys and then can use them.
    access_keys = '/__api/request-access-keys/'

    # v2
    v2_index = '/__api_v2/datasets/'
    v2_by_id = '/__api_v2/datasets/{id}/'
    v2_by_short_code = '/__api_v2/by_short_code/dataset/{dataset_short_code}'
    v2_sample_data_schema = '/__api_v2/datasets/{id}/sample_data'
    v2_sample_data_file = '/__api_v2/datasets/{id}/sample_data/file'
    v2_schema_instance_version = '/__api_v2/datasets/{id}/dictionaries/{version}'
    v2_unstructured_document = '/__api_v2/datasets/{id}/documents'

    # TODO Deprecated - check for usages in services and remove, use below set instead! Think they are only used by SDK
    dictionary_fields = '/__api_v2/dictionaries/{id}/fields/'  # NO NEW ENDPOINT AS AT 2022-04-08
    # Implemented 2022-04-08 "Removal of versions from dictionaries"
    dataset_dictionary = "/__api_v2/datasets/{dataset_id}/dictionary/"

class autoreg_urls:
    autoreg_index = '/__api/auto-reg-metadata/'
    autoreg_instance = '/__api/auto-reg-metadata/{id}/'


class datafile_urls:
    datafiles_index = '/__api/datafiles/'
    datafiles_instance = '/__api/datafiles/{id}/'


class package_urls:
    package_index = '/__api/packages/'
    package_edit = '/__api/packages/{id}/'
    # package_datasets = '/__api/package/{id}/datasets/'

    # v2
    v2_package_datasets = '/__api_v2/packages/{id}/datasets'
    v2_package_by_id = '/__api_v2/packages/{id}'
    v2_package_index = '/__api_v2/packages'


class search_urls:
    search_root = '/__api/search/'
    search_packages = '/__api/search/packages/'
    search_datasets = '/__api/search/datasets/'


class consumption_urls:
    consumption_download = '/datafile/{id}/download/binary/{path}'
    consumption_manifest = '/datafile/{id}/manifest/'
    consumption_dataframe = '/dataset/{id}/dataframe/'
    consumption_analytics = '/analytics/'
    consumption_partitions = '/dataset/{id}/partitions/'


class sam_urls:
    sam_token = '/sso/oauth2/realms/root/realms/Customers/access_token'


class identity_urls:
    identity_token = '/api/identity/v2/auth/token'
    identity_postbox = '/api/identity/v1/postbox_login'
    identity_poll = '/api/identity/v2/auth/postbox'
    orgs_visible_to_user = '/api/identity/v2/organisations/visible'
    # `identity_pat_token` deprecated. The Catalogue endpoint is now able to handle PAT and application credential
    # flows, so switch to the more generic name `identity_token_exchange` below.
    identity_pat_token = '/api/identity/v2/auth/access_token'
    identity_token_exchange = '/api/identity/v2/auth/access_token'
