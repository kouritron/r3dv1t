import enum


# You can do > < >= <= == comparison on these, ie: lvl_1.value >= lvl_2.value
# A filter set to LGLVL.DEBUG means filter nothing.
class LGLVL(enum.Enum):
    DBUG = 10
    INFO = 20
    WARN = 30
    ERRR = 40
    CRIT = 50

    def __str__(self):
        return super().__str__()[6:]  # chopping i.e. "LGLVL.DBUG", to "DBUG"
