from dataclasses import dataclass, field


# TODO: make subclasses for every field type
@dataclass(frozen=True)
class Field:
    id: int
    lib_id: str
    type: str = field(compare=False)
    name: str = field(compare=False)
    order: int = field(compare=False)
    options: str = field(compare=False, default=None)
    role: str = field(compare=False, default=None)
