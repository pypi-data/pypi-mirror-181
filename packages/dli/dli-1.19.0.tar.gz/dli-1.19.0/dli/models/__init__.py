#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import ntpath
import os
from collections import UserDict
from typing import Mapping, Optional
from urllib.parse import urlparse


class AttributesDict(UserDict):

    def __init__(self, *args, **kwargs):
        # recursively provide the rather silly attribute access
        data = {}

        for arg in args:
            data.update(arg)

        data.update(**kwargs)

        for key, value in data.items():
            if isinstance(value, Mapping):
                self.__dict__[key] = AttributesDict(value)
            else:
                self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        attributes = ' '.join([
            '{}={}'.format(k, v) for k,v in self.__dict__.items()
            if not k.startswith('_')
        ])

        return "{}({})".format(self.__class__.__name__, attributes)


def print_model_metadata(model: AttributesDict):
    for (k, v) in vars(model).items():
        if k == "documentation" and type(v) is str:
            val = v[0:100].replace('\n', ' ').replace('\r', '') + "..." \
                if len(v) > 100 else v
        else:
            val = v

        if not (hasattr(v, '__dict__') or k.startswith("_")):
            print(f"{k}: " + f"{val}")


def _flatten_s3_file_path(s3_path: str, rename_file: Optional[str] = None) -> str:
    """
    This is an internal helper function that is called from other functions. Users do not need to call it directly.

    Extract only the file name from an S3 path and return a flattened path. This is needed to handle limitations in the
    Windows operating system.

    :param str s3_path: The S3 path + file name we want to flatten. The file name may include the file extension.

    :param str rename_file: When `rename_file` is not None then we want to rename the file (though not the
        extension), so the name `foo.parquet`will become `bar.parquet` and the name `foo` (no file extension) will
        become `bar` (no file extension). This is only used when the parameter flatten=True.

    :return: Path flattened.
    """
    path = urlparse(s3_path)[2]  # [scheme, netloc, path, ...]
    head, tail = ntpath.split(path)
    file = tail or ntpath.basename(head)
    if rename_file:
        head, *tail = file.rsplit('.', 2)
        if tail:
            # Re-add the file extension.
            return f"{rename_file}.{'.'.join(tail)}"
        else:
            return rename_file
    else:
        return file


def _get_or_create_os_path(s3_path: str, to: str, flatten: bool, rename_file: Optional[str] = None) -> str:
    """
    This is an internal helper function that is called from other functions. Users do not need to call it directly.

    :param str s3_path: The S3 path + file name we want to flatten. The file name may include the file extension.

    :param str to: Relative or absolute path for where the user wants to save the files on the local file system.

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

    :param str rename_file: When `rename_file` is not None then we want to rename the file (though not the extension),
        so the name `foo.parquet`will become `bar.parquet` and the name `foo` (no file extension) will become `bar`
        (no file extension). This is only used when the parameter flatten=True.

    :return: Path for local filesystem.
    """
    if flatten:
        destination_key = _flatten_s3_file_path(s3_path, rename_file)
    else:
        destination_key = urlparse(s3_path).path.lstrip('/')

    to_path = os.path.join(
        to, os.path.normpath(destination_key)
    )

    to_path = os.path.abspath(to_path)

    if len(to_path) > 259 and os.name == 'nt':
        raise Exception(f"Apologies {s3_path} can't be downloaded "
                        f"as the file name would be too long. You "
                        f"may want to try calling again with "
                        f"`.download(flatten=True)`, which "
                        f"will put the file in a directory of your choice")

    else:
        directory, _ = os.path.split(to_path)
        os.makedirs(directory, exist_ok=True)

    return to_path
