import random
import time

import logicsponge.core as ls
from logicsponge.core import dashboard, stats


class Source(ls.SourceTerm):
    def __init__(self, key: str, mu=0.5, sigma=1.0):
        super().__init__(name=key, key=key)
        self.key = key
        self.mu = mu
        self.sigma = sigma

    def run(self):
        for _ in range(42):
            time.sleep(0.05)
            out = ls.DataItem({self.key: random.normalvariate(mu=self.mu, sigma=self.sigma)})
            self.output(out)


circuit1 = (
    Source("A")
    * dashboard.Plot("Source (1)")
    * stats.OneSampleTTest("t-Test", dim=0, mean=0.0)
    * ls.DataItemFilter(lambda d: d["p-value"] is not None)
    * ls.AddIndex(key="index")
    # * ls.Print()
    * dashboard.Plot("p-value (OneSampleTTest)", x="index", y=["p-value"])
)

circuit2 = (
    (Source("A", mu=0.0) | Source("B", mu=0.0) | Source("C", mu=1.0))
    * ls.ToSingleStream()
    * ls.Flatten()
    * dashboard.Plot("Source (2)")
    * stats.KruskalWallis("t-Test")
    * ls.DataItemFilter(lambda d: d["p-value"] is not None)
    * ls.AddIndex(key="index")
    # * ls.Print()
    * dashboard.Plot("p-value (KruskalWallis)", x="index", y=["p-value"])
)

circuit = circuit1 * ls.Stop() | circuit2 * ls.Stop()
circuit.start()

# plt.show()
dashboard.show_stats(circuit)
dashboard.run()
