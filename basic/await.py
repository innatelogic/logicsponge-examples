import random
import time
from datetime import UTC, datetime

import logicsponge.core as ls


class Source(ls.SourceTerm):
    def __init__(self, key: str, delays: list[float]):
        super().__init__(name=key)
        self.key = key
        self.delays = delays

    def run(self):
        while True:
            delay = random.choice(self.delays)  # noqa: S311
            time.sleep(delay)
            out = ls.DataItem({self.key: datetime.now(UTC).strftime("%H:%M:%S")})
            self.output(out)


circuit = (
    (Source("A", [1, 2, 3]) | Source("B", [1, 2, 3]) | Source("C", [1, 2, 3]))
    * ls.Linearizer(info=False)
    * ls.Print()
    * ls.Stop()
)

circuit.start()
