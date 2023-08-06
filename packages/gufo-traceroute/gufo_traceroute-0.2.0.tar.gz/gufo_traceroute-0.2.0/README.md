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
* Built-in whois client for AS number resolution.
* Full Python typing support.
* Editor completion.
* Well-tested, battle-proven code.

## On Gufo Stack

This product is a part of [Gufo Stack][Gufo Stack] - the collaborative effort 
led by [Gufo Labs][Gufo Labs]. Our goal is to create a robust and flexible 
set of tools to create network management software and automate 
routine administration tasks.

To do this, we extract the key technologies that have proven themselves 
in the [NOC][NOC] and bring them as separate packages. Then we work on API,
performance tuning, documentation, and testing. The [NOC][NOC] uses the final result
as the external dependencies.

[Gufo Stack][Gufo Stack] makes the [NOC][NOC] better, and this is our primary task. But other products
can benefit from [Gufo Stack][Gufo Stack] too. So we believe that our effort will make 
the other network management products better.

[Gufo Labs]: https://gufolabs.com/
[Gufo Stack]: https://gufolabs.com/products/gufo-stack/
[NOC]: https://getnoc.com/