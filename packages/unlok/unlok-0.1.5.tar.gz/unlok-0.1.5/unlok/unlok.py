from pydantic import Field
from koil import koilable
from koil.composition import Composition
from unlok.rath import UnlokRath


@koilable(add_connectors=True)
class Unlok(Composition):
    rath: UnlokRath = Field(default_factory=UnlokRath)
