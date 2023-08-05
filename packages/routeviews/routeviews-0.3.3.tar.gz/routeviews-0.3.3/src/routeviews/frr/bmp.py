import textwrap
from dataclasses import dataclass
from typing import Dict

import humanize
import pytimeparse

from routeviews import parse, typez


@dataclass(frozen=True)
class BMPConnection:
    bmp_collector: typez.IPAddr
    uptime_seconds: float
    byte_queue: int
    byte_queue_kernel: int
    byte_sent_count: int
    mirror_lost: int
    mirror_sent: int
    monitor_sent: int

    @classmethod
    def from_textfsm(cls, raw_data: Dict[str, str]):
        def parse_uptime_seconds(uptime: str) -> float:
            uptime_seconds = pytimeparse.parse(uptime)
            if uptime_seconds:
                return uptime_seconds
            return 0

        return cls(
            bmp_collector=parse.IPAddr(raw_data['remote']),
            # Default to "0" uptime if unable to parse
            uptime_seconds=parse_uptime_seconds(raw_data['uptime']),
            byte_queue=int(raw_data['ByteQ']),
            byte_queue_kernel=int(raw_data['ByteQKernel']),
            byte_sent_count=int(raw_data['ByteSent']),
            mirror_lost=int(raw_data['MirrLost']),
            mirror_sent=int(raw_data['MirrSent']),
            monitor_sent=int(raw_data['MonSent']),
        )

    def pprint(self) -> str:
        return textwrap.dedent(f'''
            BMP Collector: {self.bmp_collector}
              Connection Uptime: {humanize.naturaldelta(self.uptime_seconds)}
              Data sent: {humanize.naturalsize(self.byte_sent_count)}
              Bytes queued: {humanize.naturalsize(self.byte_queue)}
              Bytes queued to Kernel: {humanize.naturalsize(self.byte_queue_kernel)}
            ''').strip()
