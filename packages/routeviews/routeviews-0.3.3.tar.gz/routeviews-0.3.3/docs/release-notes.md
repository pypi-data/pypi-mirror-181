This project follows [Semantic Versioning](https://semver.org/).

> Notice: Major version "Zero" (0.y.z) is for initial development. Today, anything MAY change with each minor release.

## 0.3.3

- Fix `routeviews-peer-requests` to use consistent vertical whitespace.


## 0.3.2

* Upgrade `routeviews-peer-requests` to print the, "effected Collector's(es) IP Addresses" after updating the Ansible inventory.
    * For Maintainers to copy or reference when completing peer requests.

## 0.3.1

* Fix `routeviews-peer-requests` to ignore 'non-operational' Routers/Collectors.
    * Some Route Views collectors are non operational today.

## 0.3.0

> **⚠ NOTE:** Renamed `routeviews-build-peer` CLI Tool to `routeviews-peer-request`.
> (Updated throughout this project's documentation)

* Upgrade `routeviews-peer-requests` with full feature set! 🎉
    - Add `--show-options` flag that can be used by ANYONE to check their potential peerings (at Internet Exchanges) with Route Views.
    - Add `--multihop-index` argument, to create BGP multihop peering config on Route Views' Multihop Collectors.
* `rvm-haproxy-stats` will fallback to `nc` if `socat` unavailable.


## 0.2.6

* Fix `rvm-haproxy-stats` CLI tool.
    * InfluxDB line protocol was broken.
    * Fixed a typo in the code that printed the InfluxDB line protocol.

## 0.2.5

* Add `rvm-haproxy-stats` CLI tool.
    * Get stats from HAProxy Stick Tables on a Route Views collector.

## 0.2.4

* Add `--zipped` flag to `rvm-latest-mrt`.
    * Only report files that have the ".bz2" file extension.
    * *Why?* Ubuntu seems to continually update the MRT update file.
    This had made the 'age_sec' metric in InfluxDB pretty much useless.

## 0.2.3

* Update `rvm-latest-mrt` InfluxDB line protocol to be simpler.
    * Updates and RIBs are separate concerns, so send up separate measurements instead of combining them into one line.
    

## 0.2.2

* Create a 'GitHub Release' after delivering package to PyPI.org

## 0.2.1

* Add many InfluxDB tags to `rvm-latest-mrt`, and remove 2 fields (that were turned to tags).
    * Using tags enables more useful and efficient querying in Grafana!

## 0.2.0

* Add a set of `rvm` (Route Views Monitor) CLI tools.
    > **ℹ Tip:** The `rvm` tools listed below can run on any FRR-based Route Views collector.
    * `rvm-latest-mrt`: Get metrics about the latest MRT Dump files on a Route Views collector.
    * `rvm-bgp-status`: Get info about BGP Peerings on a Route Views collector.
    * `rvm-bmp-status`: Get info about BMP sessions on a Route Views collector.
* Add `--sudo` flag to CLI tools where appropriate.
    * CLI tools that depend on `vtysh` will only use raise privileges when running `vtysh`.
* Extract 'InfluxDB Line Protocol' logic into `routeviews.influx` module.
    * Generate InfluxDB Line Protocol -- useful when using CLI tools as [Telegraf Exec Input Plugins](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/exec).
* Extract 'TextFSM Template Parsing' logic into the `routeviews.parse.template_parse` function.
    * See additional [discussion of TextFSM in our Design Docs](./design.md#textfsm-conventions)

## 0.1.3

* Fix Bug: `routeviews-peer-request` CLI tool rearranges the 'Route Views Peer Config' in the Ansible Inventory.
    * Now we track the 'order' of attributes whenever loading any `routeviews.ansible.NeighborConfig` class from a YAML file.
    That 'order' is then used when subsequently dumping the data, thus ensuring that nothing is rearranged unnecessarily!

## 0.1.2

* Bug: `routeviews-peer-request` CLI tool rearranges the 'Route Views Peer Config' in the Ansible Inventory.

* Fix PeeringDB Authentication!
    * See the [relevant GitHub Issue](https://github.com/peeringdb/peeringdb/issues/1206#issuecomment-1202550667) where we discovered the following details about PeeringDB API Basic Authentication:
    > 1. Do NOT base64 encode
    > 2. Username/Password Must be space-separated (e.g., must not be colon ":" separated)
    > 3. Username when using API tokens is "Api-Key"
    > 4. Ensure "www" is in all API requests!
* Enable using PeeringDB API Key instead of username/password.
    * Exposed via `--peeringdb-key` argument in `routeviews-peer-request` CLI tool (or as env var: `PEERINGDB_KEY`).
* Add the filepath to the exception message when `routeviews.yaml` encounters a `ParseError`.
    * This enables fixing syntax issues very quickly.
    * "Unable to parse `<filepath>`" is the added message, seen below:
    ```
    ... omitted traceback for brevity...
    routeviews.yaml.ParseError: while parsing a block mapping
        in "<unicode string>", line 1, column 1:
            short_name: decix
            ^ (line: 1)
    expected <block end>, but found '-'
        in "<unicode string>", line 109, column 1:
            - peer_as: 8888
            ^ (line: 109)
    Unable to parse <working-tree>/ansible/inventory/host_vars/route-views.decix.routeviews.org
    ```
* Ensure that PyVCR cassettes do not contain HTTP Basic Authentication secrets.
    * Rotated the (randomly generated) Base64 encoded password that was previously exposed via HTTP Basic Authentication Headers. 

## 0.1.1

* Fix Bug: Package failed to declare some critical dependencies. 

## 0.1.0

> Bug: Package failed to declare some critical dependencies. 
> Was missing `uologging` and `raumel.yaml` dependencies deceleration in "setup.py".

The first release of the routeviews package contains some core CLI tools, as well as some functions/classes that might be useful to routeviews maintainers.

### CLI Tools

Provide new CLI tools! 🎉

* [`routeviews-peer-request` CLI tool](./user-guide.md#routeviews-peer-request-cli-tool): automation of updating ["Route Views Ansible inventory"](https://github.com/routeviews/infra), toward 'adding BGP peers to XYZ collectors'.
* [`routeviews-email-peers` CLI tool](./user-guide.md#routeviews-email-peers-cli-tool): get list of email addresses actively peered with a Route Views Collector.

### Libraries

* There is the `routeviews.peeringdb` package that has some great methods for interfacing with the PeeringDB API.
* There is the `routeviews.yaml` module that can load and save YAML config files (without rearranging them).
    * Depends on the [`ruamel.yaml` package](https://pypi.org/project/ruamel.yaml/)
* There is the `routeviews.ansible` package, that can load, modify, and save the Route Views Ansible Inventory.
* There is the `routeviews.bgpsummery` module, that defines a `BGPSummary` class as well as functions for retrieving a `BGPSummary` from any collector.
* There is the (start of a) `routeviews.api` module/package, for interfacing with the Route Views API/DB (undocumented).



