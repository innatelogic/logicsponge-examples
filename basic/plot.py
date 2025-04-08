import time

import logicsponge.core as ls
import matplotlib.pyplot as plt
import pint
from logicsponge.core import plot

u = pint.UnitRegistry()


class Source(ls.SourceTerm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.state = {
            "time": 0,
            "cells": 10,
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
        self.state["time"] += 5
        self.state["cells"] *= 1.1

        # time to measure...
        time.sleep(0.5)


class Fit(ls.FunctionTerm):
    def f(self, item: ls.DataItem) -> ls.DataItem:
        print("Fit: received", item)
        time.sleep(0.1)
        out = ls.DataItem({"time": item["time"], "2xcells": 2 * item["cells"]})
        print("Fit: send", out)
        return out


circuit = (
    Source()
    * ls.Print()
    * plot.Plot(x="time", y="cells")
    * Fit()
    * plot.Plot(x="time", y="2xcells")
    * plot.Plot(y="2xcells")
    * plot.Plot()
)

circuit.start()
plt.show()
