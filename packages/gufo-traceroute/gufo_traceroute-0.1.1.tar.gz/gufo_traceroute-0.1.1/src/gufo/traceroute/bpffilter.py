# ---------------------------------------------------------------------
# Gufo Traceroute: BPF-filter implementation
# ---------------------------------------------------------------------
# Copyright (C) 2022, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
from typing import Iterable, List
import socket
import struct
from ctypes import create_string_buffer, addressof

# Gufo Labs modules
from .bpf import Op, compile_bpf, ret, ldb, jeq, ja, jne, ldh, ld

S_PROG = struct.Struct("HL")
SO_ATTACH_FILTER = 26


def _apply_filter(sock: socket.socket, prog: Iterable[Op]) -> None:
    ops = list(prog)
    bpf = compile_bpf(ops)
    buf = create_string_buffer(bpf)
    bpf_prog = S_PROG.pack(len(ops), addressof(buf))
    sock.setsockopt(socket.SOL_SOCKET, SO_ATTACH_FILTER, bpf_prog)


def apply_ipv4_filter(
    sock: socket.socket, dst_addr: str, src_port: int, dst_port: int
) -> None:
    def addr_to_int(a: str) -> int:
        parts = [int(x) for x in a.split(".")]
        return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]

    # Offsets
    ICMP_TYPE_OFFSET = 20
    ORIG_PKT_OFFSET = 28
    ORIG_PROTO_OFFSET = ORIG_PKT_OFFSET + 9
    ORIG_DST_ADDR_OFFSET = ORIG_PKT_OFFSET + 16
    ORIG_SRC_PORT_OFFSET = ORIG_PKT_OFFSET + 20
    ORIG_DST_PORT_OFFSET = ORIG_PKT_OFFSET + 22
    # Constants
    ICMP_UNREACH = 3
    ICMP_TTL_EXP = 11
    PROTO_UDP = 17
    # The program
    prog: List[Op] = [
        # icmp type in (3, 11)
        ldb(ICMP_TYPE_OFFSET),  # Load icmp type
        jeq(ICMP_UNREACH, "valid_type"),  # Type 3?
        jeq(ICMP_TTL_EXP, "valid_type"),  # Type 11?
        ja("drop"),  # Not 3 or 11, drop
        # check rejected packet
        # proto is UDP
        ldb(ORIG_PROTO_OFFSET, label="valid_type"),
        jne(PROTO_UDP, "drop"),
        # Check destination addreess
        ld(ORIG_DST_ADDR_OFFSET),
        jne(addr_to_int(dst_addr), "drop"),
        # Check source port
        ldh(ORIG_SRC_PORT_OFFSET),
        jne(src_port, "drop"),
        # Check destination port
        ldh(ORIG_DST_PORT_OFFSET),
        jne(dst_port, "drop"),
        # Pass
        ret(0xFFFFFFFF, label="ok"),
        # Drop
        ret(0, label="drop"),
    ]
    _apply_filter(sock, prog)
