from abc import ABC, abstractmethod
from uuid import uuid4

from trainerbase.memory import ARCH, Address, pm, make_address
from pycca import asm


asm.instruction.ARCH = ARCH


Code = bytes | str | asm.instruction.Instruction | list[asm.instruction.Instruction]


class AbstractCodeInjection(ABC):
    DPG_TAG_PREFIX = "injection__"

    @abstractmethod
    def __init__(
        self,
        address: Address | int,
        code_to_inject: Code,
    ):
        self.address = make_address(address)
        self.code_to_inject = compile_asm(code_to_inject)
        self.dpg_tag = f"{self.DPG_TAG_PREFIX}{uuid4()}"

    @abstractmethod
    def inject(self):
        pass

    @abstractmethod
    def eject(self):
        pass


class CodeInjection(AbstractCodeInjection):
    def __init__(
        self,
        address: Address | int,
        code_to_inject: Code,
    ):
        super().__init__(address, code_to_inject)
        self.original_code: bytes = b""

    def inject(self):
        self.original_code = pm.read_bytes(self.address.resolve(), len(self.code_to_inject))
        pm.write_bytes(self.address.resolve(), self.code_to_inject, len(self.code_to_inject))

    def eject(self):
        pm.write_bytes(self.address.resolve(), self.original_code, len(self.original_code))


class AllocatingCodeInjection(AbstractCodeInjection):
    def __init__(
        self,
        address: Address | int,
        code_to_inject: Code,
        original_code_length: int = 0,
        new_memory_size: int = 1024,
    ):
        super().__init__(address, code_to_inject)
        self.original_code_length = original_code_length
        self.new_memory_size = new_memory_size
        self.original_code: bytes = b""
        self.new_memory_address: int = 0

    def __del__(self):
        if self.new_memory_address:
            self.eject()

    def inject(self):
        self.original_code = pm.read_bytes(self.address.resolve(), self.original_code_length)
        self.new_memory_address = pm.allocate(self.new_memory_size)

        jump_back = compile_asm(goto(self.address.resolve() + self.original_code_length))
        code_to_inject = self.code_to_inject + jump_back

        jump_to_new_mem = compile_asm(goto(self.new_memory_address))
        if len(jump_to_new_mem) < self.original_code_length:
            jump_to_new_mem += b"\x90" * (self.original_code_length - len(jump_to_new_mem))

        pm.write_bytes(self.new_memory_address, code_to_inject, len(code_to_inject))
        pm.write_bytes(self.address.resolve(), jump_to_new_mem, len(jump_to_new_mem))

    def eject(self):
        pm.write_bytes(self.address.resolve(), self.original_code, self.original_code_length)
        pm.free(self.new_memory_address)
        self.new_memory_address = 0


def compile_asm(code: Code) -> bytes:
    if isinstance(code, str):
        code = asm.parser.parse_asm(code)

    if isinstance(code, asm.instruction.Instruction):
        code = [code]

    if isinstance(code, list):
        code = b"".join(instruction.code for instruction in code)

    if not isinstance(code, bytes):
        raise TypeError("code must be bytes | str | list[Instruction]")

    return code


def goto(address: int) -> bytes:
    return compile_asm([
        asm.push(address),
        asm.ret(),
    ])
