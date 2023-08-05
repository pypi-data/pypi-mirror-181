
from routeviews.ansible.data.collector import CollectorConfig
from routeviews.ansible.inventory import Inventory
from routeviews.ansible.data.neighbor import NeighborConfig

load = Inventory.load

__all__ = ['Inventory', 'CollectorConfig', 'NeighborConfig', 'load']
