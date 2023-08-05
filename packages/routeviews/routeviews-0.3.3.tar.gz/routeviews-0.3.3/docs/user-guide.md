Route Views requires many tools to support its functionality.
This package is a place for those tools to live.

> Today, this package also acts as the primary 'python programming library' for Route Views.

# CLI Tools

As of today, there are two types of tools provided by this package: monitoring, and automation.

> ℹ The  CLI tools have certain prefix based on tool type:
>
> * `rvm-` is for Monitoring tools that are used only to learn about the running state of Route Views.
> * `routeviews-` is for Automation tools that enable some automated workflow.


## `rvm-latest-mrt` CLI tool

Monitoring tool that shows information about the latest Route Views MRT files (RIB, UPDATE) on a collector.

> Use the `--help` flag to learn more about this tool's abilities.

    $ rvm-latest-mrt
    Latest RIB:    /mnt/storage/bgpdata/2022.08/RIBS/rib.20220802.0800.bz2
    Latest UPDATE: /mnt/storage/bgpdata/2022.08/UPDATES/update.20220802.0800.bz2

## `rvm-bmp-status` CLI tool

Monitoring tool that shows information about BMP connections on a collector.

> Use the `--help` flag to learn more about this tool's abilities.

    $ sudo rvm-bmp-status
    BMP Collector: bmp.routeviews.org
      Connection Uptime: 8 hours
      Data sent: 1.5 GB
      Bytes queued: 2 Bytes
      Bytes queued to Kernel: 3 Bytes

## `rvm-bgp-status` CLI tool

Monitoring tool that shows relevant information about BGP connections on a collector.

> Use the `--help` flag to learn more about this tool's abilities.

    $ sudo  rvm-bgp-status
      ASN  Peer Address        State          Prefixes    Uptime     InQ    Uptime
    -----  ------------------  -----------  ----------  --------  ------  --------
    65129  128.223.51.78       ESTABLISHED           0         0  149732         1
     3582  128.223.253.9       ESTABLISHED      899115         0  149732         1
     3582  128.223.253.10      ESTABLISHED      899147         0  149732         1
     3582  2001:468:d01:fd::9  ESTABLISHED      162442         0  149732         1
     3582  2001:468:d01:fd::a  ESTABLISHED      162443         0  149732         1

## `rvm-haproxy-stats` CLI tool

Get stats from HAProxy Stick Tables on a Route Views collector. 

> ℹ HAProxy runs on our collectors to enable telnet access.

    $ rvm-haproxy-stats --min-conn-cnt 10 --sudo
    Key                         Current Conn.    Total Conn.  Data In Rate    Date Out Rate
    ------------------------  ---------------  -------------  --------------  ---------------
    175.30.79.245                           0             10  0 Bytes         901 Bytes
    141.255.166.2                           0             12  69 Bytes        1.3 kB
    179.43.187.243                          0             13  0 Bytes         1.5 kB
    180.103.51.200                          0             14  0 Bytes         1.0 kB
    31.220.3.140                            0             27  0 Bytes         907 Bytes
    2001:468:d01:33::80df:78                0             27  457 Bytes       9.0 kB

## `routeviews-peer-request` CLI tool

This tool is for (consistently) updating the [Route Views ansible inventory (private repo)](https://github.com/routeviews/infra) when folks submit new peer requests. 

> This tool uses information provided by PeeringDB for the peering information.

### Prerequisites

1. *Route Views Ansible Inventory*: You must have a local copy of the Route Views ansible inventory available, for this tool to update.
    * If you will be running this command with any regularity, is useful to export the `ROUTEVIEWS_INVENTORY` environment variable to point to your local copy of the [Route Views ansible inventory repository (private)](https://github.com/routeviews/infra).
    ```
    # (Optional) Place in your ~/.bashrc
    $ export ROUTEVIEWS_INVENTORY='<WORKING_TREE>/ansible/inventory'
    ```
    * `<WORKING_TREE>` refers to wherever you've cloned the repository on your filesystem.

### Example: Show Options between Route Views and Autonomous System (AS)

If an AS would like to know what peering sessions are possible according to this tool, we do have a `--show-options` flag that will enable this!
Provide only the `asn` argument along with the `show-options` flag to try this out!

> ℹ Anyone can run this solution!
> This solution only depends on the public PeeringDB API.

    $ routeviews-peer-request --asn 15169 --show-options

    Potential BGP Peerings for networks:

    - RouteViews (ASN: 6447), and 
    - Google LLC (ASN: 15169).

    Exchange                                        RV Collector              Router
    ----------------------------------------------  ------------------------  ------------------------
    Equinix Chicago                                 208.115.136.187           208.115.136.21
    Equinix Chicago                                 2001:504:0:4::6447:1      2001:504:0:4:0:1:5169:1
    Equinix Palo Alto                               198.32.176.5              198.32.176.31
    Equinix Palo Alto                               2001:504:d::5             2001:504:d::1f
    LINX LON1: Main                                 195.66.225.222            195.66.224.125
    LINX LON1: Main                                 2001:7f8:4::192f:1        2001:7f8:4::3b41:1
    Digital Realty Atlanta                          198.32.132.3              198.32.132.41
    Digital Realty Atlanta                          2001:478:132::3           2001:478:132::41
    DE-CIX Frankfurt: DE-CIX Frankfurt Peering LAN  80.81.193.49              80.81.192.108
    DE-CIX Frankfurt: DE-CIX Frankfurt Peering LAN  2001:7f8::192f:0:1        2001:7f8::3b41:0:1
    DE-CIX Frankfurt: DE-CIX Frankfurt Peering LAN  80.81.193.49              80.81.193.108
    DE-CIX Frankfurt: DE-CIX Frankfurt Peering LAN  2001:7f8::192f:0:1        2001:7f8::3b41:0:2
    DIX-IE                                          202.249.2.166             202.249.2.189
    ... trimmed for brevity...

### Example: Peer with an Autonomous System (AS) at ***ALL*** IXes

If an AS is wanting to connect wherever possible, provide only the `asn` argument and the tool will determine all the possible `ip` arguments from PeeringDB.

    $ routeviews-peer-request \
        --inventory <WORKING_TREE>/ansible/inventory \
        --asn 15169
    
    ### Changes

    +++ <WORKING_TREE>/ansible/inventory/host_vars/route-views.perth.routeviews.org
    + peer_as: 15169
    + peer_address: 218.100.52.3
    + description: 'IX Australia (Sydney NSW): NSW-IX'
    + afi_safis:
    +   - ipv4_unicast
    + peer_as: 15169
    + peer_address: 2001:7fa:11:4:0:3b41:0:1
    + description: 'IX Australia (Sydney NSW): NSW-IX'
    + afi_safis:
    +   - ipv6_unicast
    + peer_as: 15169
    + peer_address: 218.100.53.29
    + description: 'IX Australia (Sydney NSW): NSW-IX'
    + afi_safis:
    +   - ipv4_unicast
    + peer_as: 15169
    + peer_address: 2001:7fa:11:4:0:3b41:0:2
    + description: 'IX Australia (Sydney NSW): NSW-IX'
    + afi_safis:
    +   - ipv6_unicast
    + peer_as: 15169
    + peer_address: 218.100.78.154
    + description: 'IX Australia (Melbourne VIC): VIC-IX'
    + afi_safis:
    +   - ipv4_unicast
    + peer_as: 15169
    + peer_address: 2001:7fa:11:1:0:3b41:0:2
    + description: 'IX Australia (Melbourne VIC): VIC-IX'
    + afi_safis:
    +   - ipv6_unicast
    + peer_as: 15169
    + peer_address: 218.100.78.153
    + description: 'IX Australia (Melbourne VIC): VIC-IX'
    + afi_safis:
    +   - ipv4_unicast
    + peer_as: 15169
    + peer_address: 2001:7fa:11:1:0:3b41:0:1
    + description: 'IX Australia (Melbourne VIC): VIC-IX'
    + afi_safis:
    +   - ipv6_unicast

    +++ <WORKING_TREE>/ansible/inventory/host_vars/route-views.amsix.routeviews.org
    + peer_as: 15169
    + peer_address: 80.249.208.247
    + description: AMS-IX
    + afi_safis:
    +   - ipv4_unicast
    + peer_as: 15169
    + peer_address: 2001:7f8:1::a501:5169:1
    + description: AMS-IX
    + afi_safis:
    ... trimmed for brevity...

### Example: Peer with an Autonomous System (AS) using IP Addresses

This tool supports arguments for `asn`, as well as `ip`.
The `ip` argument can be used multiple times to peer with multiple IP Addresses at once.

> ⚠ Only supports peering with one AS at a time.

> ℹ Use the `--help` flag to learn more about how to use these arguments.

As discussed in the [prerequisites](#prerequisites-1), there is also the `inventory` argument required that points to the "inventory/" directory.

> ℹ Tip: Provide an `asn` and omit the `ip` argument entirely -- the tool will attempt to peer with ALL compatible IP Addresses for the provided `asn`!

    $ routeviews-peer-request \
        --inventory <WORKING_TREE>/ansible/inventory \
        --asn 15169 \
        --ip 202.249.2.189 \
        --ip 2001:200:0:fe00::3b41:0 \
        --ip 80.249.208.247 \
        --ip 2001:7f8:1::a501:5169:1

    ### Changes

    +++ <WORKING_TREE>/ansible/inventory/host_vars/route-views.amsix.routeviews.org
    + peer_as: 15169
    + peer_address: 80.249.208.247
    + description: AMS-IX
    + afi_safis:
    +   - ipv4_unicast
    + peer_as: 15169
    + peer_address: 2001:7f8:1::a501:5169:1
    + description: AMS-IX
    + afi_safis:
    +   - ipv6_unicast

    +++ <WORKING_TREE>/ansible/inventory/host_vars/route-views.wide.routeviews.org
    + peer_as: 15169
    + peer_address: 202.249.2.189
    + description: DIX-IE
    + afi_safis:
    +   - ipv4_unicast
    + peer_as: 15169
    + peer_address: 2001:200:0:fe00::3b41:0
    + description: DIX-IE
    + afi_safis:
    +   - ipv6_unicast


### Example: Multihop Peering - Peer with a Remote Autonomous System (AS)

If an AS is wanting to connect but we are not at the same exchange, we can provide a Multihop BGP session.
The `--multihop-index` option is used to select which collector to use.

    $ routeviews-peer-request \
        --inventory <WORKING_TREE>/ansible/inventory \
        --ip 1.2.3.4 \
        --ip 1.2.3.5 \
        --asn 15169 \
        --multihop-index 5  # I.e. route-views5.routeviews.org

    ### Changes

    +++ <WORKING_TREE>/ansible/inventory/host_vars/route-views5.routeviews.org
    + peer_address: 1.2.3.5
    + peer_as: 15169
    + description: Google LLC
    + afi_safis:
    +   - ipv4_unicast
    + options:
    +   - ebgp-multihop 255

## `routeviews-email-peers` CLI tool

This tool will get a list of email addresses for any networks that are actively peered with a particular Route Views Collector.
This tool is for gathering email address information about Route Views Collector's peers around the world, leveraging [PeeringDB]() and [RDAP](TODO).

> Future Plan: Use SMTP server to automate actually sending *many* types of 'standard Route Views Operations emails' (use Jinja2 Templates for the email templates).

### Prerequisites

1. *SSH Access*: This script uses NetMiko, and assumes that the current user can SSH into the collector using SSH keys (recommend using an `ssh-agent`).

### Example

Run the `routeviews-email-peers` command against a specific Route Views collector, e.g. "route-views4.routeviews.org".

Today, this command will to produce a semicolon-separated list of email addresses for each (established) peering session on that collector.

    $ routeviews-email-peers --collector route-views4.routeviews.org
    WARNING:routeviews.scripts.get_peers_email:PeeringDB is missing ASN: 56665
    2022-12-09 18:18:29 WARNING   PeeringDB is missing ASN: 61138 [.../routeviews/scripts/get_peers_email.py:92]
    ... trimmed for brevity...
    WARNING:routeviews.scripts.get_peers_email:PeeringDB is missing ASN: 61138
    2022-12-09 18:18:29 WARNING   PeeringDB is missing ASN: 204028 [.../routeviews/scripts/get_peers_email.py:92]
    WARNING:routeviews.scripts.get_peers_email:PeeringDB is missing ASN: 204028
    support@arelion.com; noc@level3carrier.com; inoc@vtc.vn; peering@uvm.edu;

## YAML Python API

We have a custom YAML module for handling (Ansible) YAML config files.
In particular, this module will handle whitespace matching the standard way used throughout the Route Views Infrastructure repo.
Further, this module ensures that the order data dumped is the same as ingested.

> Today, this functionality comes thanks to the [ruamel.yaml package (PyPI)](https://pypi.org/project/ruamel.yaml/)!

### Example

This example loads a file by filename, then saves that file back.

> In this case, this will essentially create a copy the "vars.yml" file.
>
> ℹ Tip: The "vars2.yml" copy, or any file dumped using `routeviews.yaml`, will follow the Route Views YAML styling convention.

    import routeviews.yaml

    my_variables = routeviews.yaml.load('vars.yml')

    # ... make updates to `my_variables`...

    routeviews.yaml.dump(my_variables, 'vars2.yml')

## Additional APIs

Besides the CLI tools discussed above, this package contains many internal packages/modules that might be useful.

> ⚠ NOTICE: Major version zero (0.y.z) is for initial development. Anything MAY change at any time. This public API SHOULD NOT be considered stable.

* There is the `routeviews.peeringdb` package that has some great methods for interfacing with the PeeringDB API.
* There is the `routeviews.yaml` module that can load and save YAML config files (without rearranging them).
    * Depends on the [`ruamel.yaml` package](https://pypi.org/project/ruamel.yaml/)
* There is the `routeviews.ansible` package, that can load, modify, and save the Route Views Ansible Inventory.
* There is the `routeviews.bgpsummery` module, that defines a `BGPSummary` class as well as functions for retrieving a `BGPSummary` from any collector.
* There is the (start of a) `routeviews.api` module/package, for interfacing with the Route Views API/DB (undocumented).






