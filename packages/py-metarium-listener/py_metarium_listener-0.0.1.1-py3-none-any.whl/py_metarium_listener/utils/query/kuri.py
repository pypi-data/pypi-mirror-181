from collections import namedtuple

KuriQuery = namedtuple(
    "KuriQuery",
    "parameters",
    defaults=[{}]
)