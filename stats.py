import random
import time

import datasponge as ds
from datasponge import dashboard, stats


class Source(ds.SourceTerm):
    def __init__(self, key: str, mu=0.5, sigma=1.0):
        super().__init__(name=key, key=key)
        self.key = key
        self.mu = mu
        self.sigma = sigma

    def run(self):
        while True:
            time.sleep(0.05)
            out = DataItem(
                {self.key: random.normalvariate(mu=self.mu, sigma=self.sigma)}
            )
            self.output(out)


circuit1 = (
    Source("A")
    * dashboard.Plot("Source (1)")
    * stats.OneSampleTTest("t-Test", dim=0, mean=0.0)
    * ds.DataItemFilter(lambda d: d["p-value"] is not None)
    * ds.AddIndex(key="index")
    # * ds.Print()
    * dashboard.Plot("p-value (OneSampleTTest)", x="index", y=["p-value"])
)

circuit2 = (
    (Source("A", mu=0.0) | Source("B", mu=0.0) | Source("C", mu=1.0))
    * ds.ToSingleStream(flatten=True)
    * dashboard.Plot("Source (2)")
    * stats.KruskalWallis("t-Test")
    * ds.DataItemFilter(lambda d: d["p-value"] is not None)
    * ds.AddIndex(key="index")
    # * ds.Print()
    * dashboard.Plot("p-value (KruskalWallis)", x="index", y=["p-value"])
)

circuit = circuit1 * ds.Stop() | circuit2 * ds.Stop()
circuit.start()

# plt.show()
dashboard.show_stats(circuit)
dashboard.run()
