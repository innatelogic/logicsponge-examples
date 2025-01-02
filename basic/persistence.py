import time

import logicsponge.core as ls
from logicsponge.core.logicsponge import Dump


class Source(ls.SourceTerm):
    def run(self):
        while True:
            out = (
                ls.DataItem({"data": 1})
                if len(self._output) == 0
                else ls.DataItem({"data": self._output[-1]["data"] + 1})
            )
            print("Source: send", out)
            self.output(out)

            time.sleep(2)


class Sink(ls.FunctionTerm):
    def f(self, item: ls.DataItem) -> ls.DataItem:
        time.sleep(3)
        print("Sink: received", item)
        return item


circuit = Source() * (Dump(name="source_dump") | (Sink() * Dump(name="sink_dump")))
circuit.start(persistent=True)
