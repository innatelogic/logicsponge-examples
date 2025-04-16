import time
from typing import ClassVar, TypedDict

import logicsponge.core as ls


class SourceState(TypedDict):
    time: float  # pint.Quantity
    cells: float  # pint.Quantity


class Source(ls.SourceTerm):
    def run(self):
        self.state = {
            "time": 0,
            "cells": 10,
        }
        for _ in range(10):
            # time to measure...
            time.sleep(0.1)

            # send measurmemt
            out = ls.DataItem(
                {
                    "time": self.state["time"],
                    "cells": self.state["cells"],
                }
            )
            self.output(out)

            # update state
            self.state["time"] += 5  # * u.min
            self.state["cells"] *= 1.1


class Compute(ls.FunctionTerm):
    def f(self, di: ls.DataItem) -> ls.DataItem:
        out = ls.DataItem({"time": di["time"], "cells": di["cells"]})
        return out


circuit = Source() * Compute() * ls.Print()
circuit.start()
