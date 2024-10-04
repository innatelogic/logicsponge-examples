import time
from typing import ClassVar, TypedDict

import matplotlib.pyplot as plt
import pint

import datasponge.core as ds
from datasponge.core import plot

u = pint.UnitRegistry()


class SourceState(TypedDict):
    time: float
    cells: float


class Source(ds.SourceTerm):
    state: ClassVar[SourceState] = {
        "time": 0,
        "cells": 10,
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
        self.state["time"] += 5
        self.state["cells"] *= 1.1

        # time to measure...
        time.sleep(0.5)


class Fit(ds.FunctionTerm):
    def f(self, item: ds.DataItem) -> ds.DataItem:
        print("Fit: received", item)
        time.sleep(0.1)
        out = ds.DataItem({"time": item["time"], "2xcells": 2 * item["cells"]})
        print("Fit: send", out)
        return out


circuit = (
    Source()
    * ds.Print()
    * plot.Plot(x="time", y="cells")
    * Fit()
    * plot.Plot(x="time", y="2xcells")
    * plot.Plot(y="2xcells")
    * plot.Plot()
)

circuit.start()
plt.show()
