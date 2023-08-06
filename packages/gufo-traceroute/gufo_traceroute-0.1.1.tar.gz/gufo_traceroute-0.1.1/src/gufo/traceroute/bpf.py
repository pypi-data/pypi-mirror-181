# ---------------------------------------------------------------------
# Gufo Traceroute: BPF primitives
# ---------------------------------------------------------------------
# Copyright (C) 2022, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
from typing import Union, Optional, Iterable, List
from dataclasses import dataclass
import struct

# Constants from FreeBSD's net/bpf.h
# Classes
BPF_LD = 0x00
BPF_LDX = 0x01
BPF_ST = 0x02
BPF_STX = 0x03
BPF_ALU = 0x04
BPF_JMP = 0x05
BPF_RET = 0x06
BPF_MISC = 0x07
BPF_CLASS_MASK = 0x7

# Size
BPF_W = 0x00
BPF_H = 0x08
BPF_B = 0x10
BPF_SIZE_MASK = 0x18

# Mode
BPF_IMM = 0x00
BPF_ABS = 0x20
BPF_IND = 0x40
BPF_MEM = 0x60
BPF_LEN = 0x80
BPF_MSH = 0xA0
BPF_MODE_MASK = 0xE0

# ALU/JMP fields
BPF_ADD = 0x00
BPF_SUB = 0x10
BPF_MUL = 0x20
BPF_DIV = 0x30
BPF_OR = 0x40
BPF_AND = 0x50
BPF_LSH = 0x60
BPF_RSH = 0x70
BPF_NEG = 0x80
BPF_MOD = 0x90
BPF_XOR = 0xA0

# JMP fields
BPF_JA = 0x00
BPF_JEQ = 0x10
BPF_JGT = 0x20
BPF_JGE = 0x30
BPF_JSET = 0x40
BPF_OP_MASK = 0xF0

# Source
BPF_K = 0x00
BPF_X = 0x08

# Structs
S_OP = struct.Struct("HBBI")

# Types
REF = Union[int, str]


@dataclass
class Op(object):
    """
    BPF opcode.

    Args:
        code: Operarion code
        jt: Jump if true
        jf: Jump if false
        k: k-register
        label: Optional label.
    """

    code: int
    jt: REF
    jf: REF
    k: REF
    label: Optional[str] = None

    def compile(self) -> bytes:
        """
        Compile opcode to the binary form.

        Returns: 8-byte binary representation
        """
        if isinstance(self.jt, str):
            raise ValueError("Cannot compile symbolic jt reference")
        if isinstance(self.jf, str):
            raise ValueError("Cannot compile symbolic jf reference")
        if isinstance(self.k, str):
            raise ValueError("Cannot compile symbolic k reference")
        return S_OP.pack(self.code, self.jt, self.jf, self.k)


def ldb(k: int, *, label: Optional[str] = None) -> Op:
    return Op(BPF_LD | BPF_B | BPF_ABS, 0, 0, k, label=label)


def ldh(k: int, *, label: Optional[str] = None) -> Op:
    return Op(BPF_LD | BPF_H | BPF_ABS, 0, 0, k, label=label)


def ld(k: int, *, label: Optional[str] = None) -> Op:
    return Op(BPF_LD | BPF_W | BPF_ABS, 0, 0, k, label=label)


def ret(k: int, *, label: Optional[str] = None) -> Op:
    return Op(BPF_RET | BPF_K, 0, 0, k, label=label)


def ja(t: REF, *, label: Optional[str] = None) -> Op:
    return Op(BPF_JMP | BPF_JA | BPF_K, 0, 0, t, label=label)


def jeq(k: int, jt: REF, jf: REF = 0, *, label: Optional[str] = None) -> Op:
    return Op(BPF_JMP | BPF_JEQ | BPF_K, jt, jf, k, label=label)


def jne(k: int, jt: REF, jf: REF = 0, *, label: Optional[str] = None) -> Op:
    return Op(BPF_JMP | BPF_JEQ | BPF_K, jf, jt, k, label=label)


def preprocess_bpf(prog: Iterable[Op]) -> List[Op]:
    """
    Expand symbolic references
    """

    def resolve(current: int, label: REF) -> int:
        if isinstance(label, int):
            return label
        target = labels[label]
        if target <= current:
            raise ValueError(f"Error in line {current}: Backward reference")
        return target - current - 1

    ops = list(prog)
    # Get label positions, name -> line
    labels = {op.label: n for n, op in enumerate(ops) if op.label is not None}
    res_prog: List[Op] = []
    # Resolve label references
    for n, op in enumerate(ops):
        if (
            isinstance(op.jt, int)
            and isinstance(op.jf, int)
            and isinstance(op.k, int)
        ):
            res_prog.append(op)  # Unchanged
        else:
            # Resolve references
            res_prog.append(
                Op(
                    code=op.code,
                    jt=resolve(n, op.jt),
                    jf=resolve(n, op.jf),
                    k=resolve(n, op.k),
                    label=op.label,
                )
            )
    return res_prog


def compile_bpf(prog: Iterable[Op]) -> bytes:
    return b"".join(op.compile() for op in preprocess_bpf(prog))
