import random
import time
from datetime import UTC, datetime

import datasponge.core as ds


class Source(ds.SourceTerm):
    def __init__(self, key: str, delays: list[float]):
        super().__init__(name=key)
        self.key = key
        self.delays = delays

    def run(self):
        while True:
            delay = random.choice(self.delays)  # noqa: S311
            time.sleep(delay)
            out = ds.DataItem({self.key: datetime.now(UTC).strftime("%H:%M:%S")})
            self.output(out)


circuit = (
    (Source("A", [1, 2, 3]) | Source("B", [1, 2, 3]) | Source("C", [1, 2, 3]))
    * ds.Linearizer(info=False)
    * ds.Print()
    * ds.Stop()
)

circuit.start()
