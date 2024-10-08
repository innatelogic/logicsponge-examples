import time
from typing import ClassVar, TypedDict

import logicsponge.core as ls
import pint

u = pint.UnitRegistry()


class SourceState(TypedDict):
    time: float  # pint.Quantity
    cells: float  # pint.Quantity


class Source(ls.SourceTerm):
    state: ClassVar[SourceState] = {
        "time": 0,  # * u.min,
        "cells": 10,  # / u.mL,
    }

    def run(self):
        # send measurmemt
        out = ls.DataItem(
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
        time.sleep(3)


class Fit(ls.FunctionTerm):
    def f(self, di: ls.DataItem) -> ls.DataItem:
        print("Fit: received", di)
        time.sleep(0.5)
        out = ls.DataItem({"time": di["time"], "cells": di["cells"]})
        print("Fit: send", out)
        return out


circuit = Source() * Fit()
circuit.start()

time.sleep(2)
circuit.stop()
