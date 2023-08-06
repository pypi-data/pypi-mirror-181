import tempfile

from geoformat.conf.path import (
    path_to_file_path,
    verify_input_path_is_file,
    verify_input_path_is_http,
    path_is_file,
    path_is_http,
    open_http_path,
)
from geoformat.conf.format_data import value_to_iterable_value

def _get_recast_field_type_mapping(fields_metadata, geoformat_type_to_output_driver_type):
    """
    From geolayer field's metadata to output driver recast dict

    :param fields_metadata: geolayer field's metadata
    :param geoformat_type_to_output_driver_type: dict that make translation between geoformat type and output driver
    type

    :return: dict that allow to recast field
    """
    recast_field_mapping = {}
    if fields_metadata:
        for field_name, field_metadata in fields_metadata.items():
            recast_to_python_type = geoformat_type_to_output_driver_type.get(field_metadata['type'], None)
            if recast_to_python_type is not None:
                recast_field_mapping[field_name] = {
                    "recast_value_to_python_type": recast_to_python_type,
                    "resize_value_width": None,
                    "resize_value_precision": None
                }

    return recast_field_mapping


def load_data(path, encoding='utf8', headers=None, extension=None):
    """
    From path return data

    :param path: file path or http path
    :param encoding: specify file char encoding (default value utf8)
    :param headers: optionally you can add headers of http parameters
    :param extension: extension or list of extension to delete from filename
    :return:
    """
    extension = value_to_iterable_value(extension, output_iterable_type=list)

    # create temporary file
    fp = tempfile.NamedTemporaryFile(mode="w")

    if path_is_file(path=path):
        p = verify_input_path_is_file(path=path)
        # open file
        with open(file=p, mode='r', encoding=encoding) as file:
            fp.write(file.read())
            file_name = p.stem

    elif path_is_http(path=path, headers=headers):
        p = verify_input_path_is_http(path=path, headers=headers)
        http_req = open_http_path(path=p, headers=headers)
        # file_object = http_req
        http_req_str = http_req.read().decode(encoding)
        fp.write(http_req_str)
        file_name = http_req.info().get_filename()
        # delete extension from name
        if extension and file_name:
            for ext in extension:
                file_name.replace(ext, "")

    fp.seek(0)

    return fp, file_name