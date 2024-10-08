import logicsponge.core as ls
from logicsponge.core.file import CSVStreamer
from logicsponge.core.stats import Sum


class FloatConverter(ls.FunctionTerm):
    def f(self, data: ls.DataItem) -> ls.DataItem:
        return ls.DataItem({k: float(v) for k, v in data.items()})


circuit = (
    CSVStreamer(file_path="sum.csv")
    * ls.KeyFilter(key_filter=lambda k: k == "value")
    * FloatConverter()
    * ls.DataItemFilter(lambda data: data["value"] >= 0)
    * Sum(key="value")
    * ls.Print()
)

circuit.start()
