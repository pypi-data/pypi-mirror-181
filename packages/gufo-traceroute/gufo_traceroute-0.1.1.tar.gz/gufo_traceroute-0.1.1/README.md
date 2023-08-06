# Gufo Traceroute

*Gufo Traceroute is the Python asyncio IPv4 traceroute implementation.*

[![PyPi version](https://img.shields.io/pypi/v/gufo_traceroute.svg)](https://pypi.python.org/pypi/gufo_traceroute/)
![Python Versions](https://img.shields.io/pypi/pyversions/gufo_traceroute)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![Build](https://img.shields.io/github/workflow/status/gufolabs/gufo_traceroute/Run%20Tests/master)
![Sponsors](https://img.shields.io/github/sponsors/gufolabs)

---

**Documentation**: [https://docs.gufolabs.com/gufo_traceroute/](https://docs.gufolabs.com/gufo_traceroute/)

**Source Code**: [https://github.com/gufolabs/gufo_traceroute/](https://github.com/gufolabs/gufo_traceroute/)

---

*Gufo Traceroute* is the Python asyncio library for IPv4 traceroute. It consist of a clean Python API
which hides all raw-socket manipulation details.

``` py
async with Traceroute() as tr:
    async for hop in tr.traceroute("8.8.8.8", tries=3):
        print(hop)
```

Unlike the others traceroute implementation, Gufo Traceroute works well in noisy environments,
i.e. on hosts generating and receiving large volumes of ICMP traffic.

## Virtues

* Clean async API.
* IPv4 support.
* High-performance.
* Full Python typing support.
* Editor completion.
* Well-tested, battle-proven code.
