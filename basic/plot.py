import time

import logicsponge.core as ls
import matplotlib.pyplot as plt
from logicsponge.core import plot


class Source(ls.SourceTerm):
    def run(self):
        self.state = {
            "time": 0,
            "cells": 10,
        }
        while True:
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


class Compute(ls.FunctionTerm):
    def f(self, item: ls.DataItem) -> ls.DataItem:
        print("Compute: received", item)
        time.sleep(0.1)
        out = ls.DataItem({"time": item["time"], "2xcells": 2 * item["cells"]})
        print("Compute: send", out)
        return out


circuit = (
    Source()
    * plot.Plot(x="time", y="cells")
    * Compute()
    * plot.Plot(x="time", y="2xcells")
    * plot.Plot(y="2xcells")
    * plot.Plot()
)

circuit.start()
plt.show()
