import time

import logicsponge.core as ls
from logicsponge.core.logicsponge import Dump


class Source(ls.SourceTerm):
    def run(self):
        for _ in range(5):
            out = (
                ls.DataItem({"data": 1})
                if len(self._output) == 0
                else ls.DataItem({"data": self._output[-1]["data"] + 1})
            )
            print("\nSource: send", out)
            self.output(out)

            time.sleep(1)


class Sink(ls.FunctionTerm):
    def f(self, item: ls.DataItem) -> ls.DataItem:
        time.sleep(2)
        print("Sink: received", item)
        return item


class Counter(ls.FunctionTerm):
    counter: int
    only_even: bool

    def __init__(self, *args, only_even: bool, **kwargs) -> None:
        super().__init__(*args, only_even, **kwargs)
        self.counter = 0
        self.only_even = only_even

    def f(self, item: ls.DataItem) -> ls.DataItem:
        if item["data"] % 2 == 0 or not self.only_even:
            self.counter += 1
        print("Counter: ", self.counter)
        new_item = {"num": self.counter, **item}
        print("Counter Flow: ", new_item)
        return ls.DataItem(new_item)


circuit = Source() * (Dump(name="source_dump") | (Sink() * Dump(name="sink_dump")) | Counter(only_even=True))
circuit.start(persistent=True)
