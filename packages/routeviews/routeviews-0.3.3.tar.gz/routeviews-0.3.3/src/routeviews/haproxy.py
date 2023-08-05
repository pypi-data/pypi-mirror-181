import dataclasses
from typing import Dict, List

from routeviews import parse, typez


@dataclasses.dataclass(frozen=True)
class HAProxyTableStat:
    table: str
    type: str  # Assumed ip/ipv6
    key: typez.IPAddr
    size: int
    used: int
    conn_cnt: int
    conn_exp: int
    conn_cur: int
    conn_use: int
    bytes_in_rate: int
    bytes_out_rate: int

    @classmethod
    def from_data(cls, data: Dict):

        def parse_ipaddr(data: str):
            IPV6_IPV4_CONVERSION_PREFIX = '::ffff:'
            if data.startswith(IPV6_IPV4_CONVERSION_PREFIX):
                data = data[len(IPV6_IPV4_CONVERSION_PREFIX):]
            return parse.IPAddr(data)

        return cls(
            table=data['table'],
            type=data['type'],
            key=parse_ipaddr(data['key']),
            size=int(data['size']),
            used=int(data['used']),
            conn_cnt=int(data['conn_cnt']),
            conn_exp=int(data['conn_exp']),
            conn_cur=int(data['conn_cur']),
            conn_use=int(data['conn_use']),
            bytes_in_rate=int(data['bytes_in_rate']),
            bytes_out_rate=int(data['bytes_out_rate']),
        )


def parse_table_stats(data: List[Dict]):
    return [
        HAProxyTableStat.from_data(row)
        for row in data
    ]
