import traceback

class Helper:
    def get_traceback(self, e: Exception) -> list:
        new = []
        af = traceback.format_exc().split("\n")
        for x in af:
            new.append(f"|   {x}")
        return new