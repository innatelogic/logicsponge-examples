import datasponge.core as ds
from datasponge.core.file import CSVStreamer
from datasponge.core.stats import Sum


class FloatConverter(ds.FunctionTerm):
    def f(self, data: ds.DataItem) -> ds.DataItem:
        return ds.DataItem({k: float(v) for k, v in data.items()})


circuit = (
    CSVStreamer(file_path="sum.csv")
    * ds.KeyFilter(key_filter=lambda k: k == "value")
    * FloatConverter()
    * ds.DataItemFilter(lambda data: data["value"] >= 0)
    * Sum(key="value")
    * ds.Print()
)

circuit.start()
