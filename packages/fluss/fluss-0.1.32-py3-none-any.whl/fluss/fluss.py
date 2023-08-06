
from koil.composition import Composition
from pydantic import Field

from fluss.rath import FlussRath


class Fluss(Composition):
    rath: FlussRath = Field(default_factory=FlussRath)
