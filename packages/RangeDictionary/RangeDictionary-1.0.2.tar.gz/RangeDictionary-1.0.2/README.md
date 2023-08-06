# RangeDictionary

RangeDictionary package provides Range and RangeDict classes.

    from range_dictionary import Range, RangeDict

## Range

Range objects represent an interval. They can be open, semi-open or closed.

    r1 = Range(1, 2) # open
    r2 = Range[1, 2] # closed
    r3 = Range(1, 2, closed_left=True) # semi-open
    r4 = Range(1, 2, closed_right=True) # semi-open

    2 in r1 # False
    2 in r2 # True

## RangeDict

RangeDict objects are dictionaries whose keys are Range objects. They can be initialized using any iterable of 2 int/float values (the corresponding Ranges are open by default).

    rd = RangeDict({
        (1, 2) : "first",
        Range[2, 5] : "second",
        Range(5, 7, closed_right=True) : "third",
        Range(7, float("inf")) : "fourth"
    })

Accessing an int/float from a RangeDict returns its corresponding value.

    3.5 in rd # True
    rd[3.5] # "second"

RangeDicts behave similarly to standard dictionaries.

    rd[Range(7, 9)] = "fifth"
    rd.insert(Range[9, 11], "sixth")

    del rd[Range[2, 5]]
    rd.remove(Range(1, 2))

    rd.get(8) # "fifth"
    rd.get(100) # None

    rd2 = RangeDict()
    rd == rd2 # False
    rd.clear()
    rd == rd2 # True

    # return generators, order not guaranteed
    rd.keys()
    rd.values()
    rd.items()

    # return sorted lists
    rd.keys_sorted()
    rd.values_sorted()
    rd.items_sorted()

    # merge RangeDicts
    rd3 = rd | rd2
    rd.update(rd2)

## Acknowledgements

Inspired by [rangedict](https://github.com/WKPlus/rangedict) by WKPlus.
