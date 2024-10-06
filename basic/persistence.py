import time

import datasponge.core as ds
from datasponge.core.datasponge import Dump


class Source(ds.SourceTerm):
    def run(self):
        out = (
            ds.DataItem({"data": 1}) if len(self._output) == 0 else ds.DataItem({"data": self._output[-1]["data"] + 1})
        )
        print("Source: send", out)
        self.output(out)

        time.sleep(2)


class Sink(ds.FunctionTerm):
    def f(self, item: ds.DataItem) -> ds.DataItem:
        time.sleep(3)
        print("Sink: received", item)
        return item


circuit = Source() * (Dump(name="source_dump") | (Sink() * Dump(name="sink_dump")))
circuit.start(persistent=True)
