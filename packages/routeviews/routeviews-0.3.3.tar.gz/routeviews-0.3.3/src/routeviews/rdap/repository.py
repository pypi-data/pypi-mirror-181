from rdap.client import RdapClient

import routeviews.rdap


class Repository:
    """UNTESTED: Work in progress.
    """
    def __init__(self):
        self._client = RdapClient()

    def get_network(self, asn: int) -> 'routeviews.rdap.Network':
        response = self._client.get_asn(asn).data
        return routeviews.rdap.Network.from_data(response)
