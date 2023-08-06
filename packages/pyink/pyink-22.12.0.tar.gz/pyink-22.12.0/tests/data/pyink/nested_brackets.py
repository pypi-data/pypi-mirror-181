WITH_SET = frozenset({
    1001,
    1002,
    1003,
    1004,
    1005,
})

WITH_LIST = frozenset([
    1001,
    1002,
    1003,
    1004,
    1005,
])

WITH_TUPLE = frozenset((
    1001,
    1002,
    1003,
    1004,
    1005,
))

MULTIPLE_LEVELS = array([[
    1001,
    1002,
    1003,
    1004,
    1005,
]])

TRAILING_COMMA = frozenset(
    {
        1001,
        1002,
        1003,
        1004,
        1005,
    },
)


# Make sure non-matching inner brackets are handled correctly.
PAIRS = [(1, 5), (1, 30), (1, 60), (2, 80)]


# When literal list/tuple/set/dict is used in functions and it fits on a single
# line, prefer breaking at outer brackets.
func_call_with_set = frozenset(
    {1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012}
)

func_call_with_list = frozenset(
    [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012]
)

func_call_with_tuple = frozenset(
    (1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012)
)

func_call_with_dict = frozenset(
    {1001: 1002, 1003: 1004, 1005: 1006, 1007: 1008, 1009: 1010, 1011: 1012}
)

func_call_multiple_levels = array(
    [[1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012]]
)
