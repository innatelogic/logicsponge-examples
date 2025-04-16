"""
This is a simple code to demonstrate the use of threads in logicsponge.
Run it an check your system's CPU usage.

You should see all of the terms being run in parallel and, depending on your Python version,
using different cores.
"""

import time

import logicsponge.core as ls


class Source(ls.SourceTerm):
    def run(self):
        self.state = {
            "time": 0,
            "cells": 10,
        }
        while True:
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
            self.state["time"] += 5
            self.state["cells"] *= 1.1


class Compute(ls.FunctionTerm):
    def f(self, item: ls.DataItem) -> ls.DataItem:
        # something slow and computationally costly...
        k = 0
        for i in range(10000000):
            k += i

        # output the result
        return ls.DataItem({"time": item["time"], "cells": k})


circuit = Source() * (
    Compute("a")
    | Compute("b")
    | Compute("c")
    | Compute("d")
    | Compute("e")
    | Compute("f")
    | Compute("g")
    | Compute("h")
)
circuit.start()
