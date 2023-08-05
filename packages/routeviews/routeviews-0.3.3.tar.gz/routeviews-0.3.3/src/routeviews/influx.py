from typing import Dict, Optional, Union

SupportedDataTypes = Union[int,float,bool,str]


def encode_value(value: SupportedDataTypes) -> str:
    """Encode a field value for a InfluxDB Line Protocol measurement.

    > Learn more about [InfluxDB Line Protocol](https://docs.influxdata.com/influxdb/v1.8/write_protocols/line_protocol_tutorial/)

    Args:
        value (Union[int,float,bool,str]): The value to encode.

    Returns:
        str: The field value encoded into InfluxDB Line Protocol.

    Examples:
        >>> encode_value(123)
        '123i'
        >>> encode_value(1.3)
        '1.3'
        >>> encode_value(False)
        'F'
        >>> encode_value('testing a string')
        '"testing a string"'
    """
    as_datatype = {
        int: lambda: f'{value}i',
        str: lambda: f'"{value}"',
        bool: lambda: 'T' if value else 'F',
        float: lambda: str(value),
    }
    try:
        return as_datatype[type(value)]()
    except KeyError:
        raise TypeError(
            f'Unable to handle value: {value} (type: {type(value)})'
            f'\n\n    Use supported data types: {SupportedDataTypes}')

def measurement_line(name: str, 
                     fields: Dict[str,SupportedDataTypes], 
                     tags: Optional[Dict[str,str]] = None):
    """Generate a InfluxDB Line Protocol string.

    > Learn more about [InfluxDB Line Protocol](https://docs.influxdata.com/influxdb/v1.8/write_protocols/line_protocol_tutorial/)

    Args:
        name (str): The name of the measurement.
        tags (Dict): Tags for the measurement.
        fields (Dict): The fields of the measurement itself.

    Returns:
        str: Measurement(s) to be ingested into InfluxDB as Line Protocol.

    Example: 

        >>> measurement_line('test',
        ...     tags = {
        ...         'host': 'test-example.com',
        ...     }, 
        ...     fields = {
        ...         'speed': 123.45,
        ...         'engaged': True,
        ...         'rank': 15,
        ...         'comment': 'Did the thing!',
        ...     }
        ... )
        'test,host=test-example.com speed=123.45,engaged=T,rank=15i,comment="Did the thing!"'
    """
    fields_encoded = ','.join([
        f'{field}={encode_value(val)}'  # Be sure to encode the value!
        for field, val in fields.items()
    ])
    if tags:
        tags_encoded = ','.join([
            f'{tag}={val}' 
            for tag, val in tags.items()
        ])
        return f'{name},{tags_encoded} {fields_encoded}'
    else:
        return f'{name} {fields_encoded}'
