from kuay.rath import KuayRath
from koil.composition import Composition
from pydantic import Field

from lok.rath import ManRath


class Man(Composition):
    rath: ManRath = Field(default_factory=ManRath)
