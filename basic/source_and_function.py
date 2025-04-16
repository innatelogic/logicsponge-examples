import time
from typing import TypedDict

import logicsponge.core as ls


class SourceState(TypedDict):
    time: float  # pint.Quantity
    cells: float  # pint.Quantity


class Source(ls.SourceTerm):
<<<<<<< HEAD
=======
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.state = {
            "time": 0,  # * u.min,
            "cells": 10,  # / u.mL,
        }

>>>>>>> b70c4485f8515ce0139f6602270fb6e0ab08b557
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
