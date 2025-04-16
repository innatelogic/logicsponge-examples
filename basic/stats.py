"""Example for statistics in logicsponge."""

import random
import time

import logicsponge.core as ls
from logicsponge.core import dashboard, stats


class GaussSource(ls.SourceTerm):
    """Stream Gaussian random values."""

    def __init__(self, key: str, mu: float = 0.5, sigma: float = 1.0) -> None:
        """Create a GaussSource.

        Args:
            key (str): the key in the DataItem that contains the random value.
            mu (float): mu of the distribution.
            sigma (float): sigma of the distribution.

        """
        super().__init__(name=key, key=key)
        self.key = key
        self.mu = mu
        self.sigma = sigma

    def run(self):
        """Run the source and terminate afterwards."""
        for _ in range(42):
            time.sleep(0.05)
            out = ls.DataItem({self.key: random.normalvariate(mu=self.mu, sigma=self.sigma)})
            self.output(out)


circuit1 = (
    GaussSource("A")
    * dashboard.Plot("GaussSource (1)")
    * stats.OneSampleTTest("t-Test", dim=0, mean=0.0)
    * ls.DataItemFilter(lambda d: d["p-value"] is not None)
    * ls.AddIndex(key="index")
    # * ls.Print()
    * dashboard.Plot("p-value (OneSampleTTest)", x="index", y=["p-value"])
)

circuit2 = (
    (GaussSource("A", mu=0.0) | GaussSource("B", mu=0.0) | GaussSource("C", mu=1.0))
    * ls.MergeToSingleStream()
    * ls.Flatten()
    * dashboard.Plot("GaussSource (2)")
    * stats.KruskalWallis("t-Test")
    * ls.DataItemFilter(lambda d: d["p-value"] is not None)
    * ls.AddIndex(key="index")
    # * ls.Print()
    * dashboard.Plot("p-value (KruskalWallis)", x="index", y=["p-value"])
)

circuit = circuit1 * ls.Stop() | circuit2 * ls.Stop()
circuit.start()
circuit.join()

# dashboard.show_stats(circuit)
# dashboard.run()
