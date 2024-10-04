import time
from typing import ClassVar, TypedDict

# import innatelogic.v2.circuits.platereader as pr
import pint

import datasponge.core as ds

u = pint.UnitRegistry()


class SourceState(TypedDict):
    time: float  # pint.Quantity
    cells: float  # pint.Quantity


class Source(ds.SourceTerm):
    state: ClassVar[SourceState] = {
        "time": 0,  # * u.min,
        "cells": 10,  # / u.mL,
    }

    def run(self):
        # send measurmemt
        out = ds.DataItem(
            {
                "time": self.state["time"],
                "cells": self.state["cells"],
            }
        )
        print("Source: send", out)
        self.output(out)

        # update state
        self.state["time"] += 5  # * u.min
        self.state["cells"] *= 1.1

        # time to measure...
        time.sleep(1.5)


class Fit(ds.FunctionTerm):
    def f(self, item: ds.DataItem) -> ds.DataItem:
        print("Fit: received", item)
        k = 0
        for i in range(10000000):
            k += i
        out = ds.DataItem({"time": item["time"], "cells": k})
        print("Fit: send", out)
        return out


circuit = Source() * (
    Fit("a")
    | Fit("b")
    | Fit("c")
    | Fit("d")
    | Fit("e")
    | Fit("f")
    | Fit("g")
    | Fit("h")
)
circuit.start()
