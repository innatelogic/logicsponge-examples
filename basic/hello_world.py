import time

import logicsponge.core as ls


class Hello(ls.SourceTerm):
    def run(self):
        incomplete_message = "Hello"
        out = ls.DataItem({"message": incomplete_message})
        self.output(out)
        time.sleep(1)


class World(ls.FunctionTerm):
    def f(self, item: ls.DataItem) -> ls.DataItem:
        incomplete_message = item["message"]
        complete_message = incomplete_message + " World!"
        out = {"message": complete_message}
        return ls.DataItem(out)


sponge = Hello() * World() * ls.Print()

sponge.start()
