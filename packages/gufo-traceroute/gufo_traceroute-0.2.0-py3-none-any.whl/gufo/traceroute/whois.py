# ---------------------------------------------------------------------
# Gufo Traceroute: Whois client
# ---------------------------------------------------------------------
# Copyright (C) 2022, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
import asyncio


class WhoisError(Exception):
    pass


class WhoisConnectionError(Exception):
    pass


class WhoisClient(object):
    """
    Asynchorous whois client.

    Args:
        addr: Whois server address or FQDN.
        port: Whois server port.
        timeout: Request timeout.
    """

    def __init__(self, addr: str, port: int = 43, timeout: float = 5.0):
        self.addr = addr
        self.port = port
        self.timeout = timeout

    async def resolve_as(self, addr: str) -> int:
        """
        Resolve IP address and return the AS.

        Args:
            addr: IPv4/IPv6 address

        Returns:
            AS number.

        Raises:
            WhoisConnectionError: If failed to connect to whois server.
            WhoisError: On resolution error.
        """
        return await asyncio.wait_for(self._resolve_as(addr), self.timeout)

    async def _resolve_as(self, addr: str) -> int:
        """
        Interenal implementation for `resolve_as`.

        Args:
            addr: IPv4/IPv6 address

        Returns:
            AS number.

        Raises:
            WhoisConnectionError: If failed to connect to whois server.
            WhoisError: On resolution error.
        """

        try:
            reader, writer = await asyncio.open_connection(
                self.addr, self.port
            )
        except ConnectionRefusedError:
            raise WhoisConnectionError("Connection refused")
        # Send request
        if ":" in addr:
            plen = 128  # IPv6
        else:
            plen = 32  # IPv4
        req = f"!r{addr}/{plen},l\n"
        writer.write(req.encode())
        # Wait for reply
        data = await reader.read(4096)
        writer.close()
        await writer.wait_closed()
        # Parse data
        resp = data.decode()
        if resp[0] != "A":
            raise WhoisError(f"Whois error: {resp}")
        for line in resp.splitlines():
            if line.startswith("origin:"):
                return int(line[7:].strip()[2:])
        raise WhoisError("No origin found")
