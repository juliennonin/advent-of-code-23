# %%
import re

from helpers.load_puzzle import puzzle


# %%
def parse_category_map(category_map_str):
    # category_label, *ranges_str = category_map_str.split("\n")
    category_label, ranges_str = category_map_str.split(" map:\n")
    # ranges = [tuple(map(int, re.findall(r"\d+", range_str))) for range_str in ranges_str]
    ranges = eval("[[" + ranges_str.replace(" ", ",").replace("\n", "],[") + "]]")
    return category_label, ranges


class MapSourceToDestination:
    def __init__(self, ranges):
        self.ranges = []
        for range_ in ranges:
            destination_range_start, source_range_start, range_length = range_
            source_range = range(source_range_start, source_range_start + range_length)
            mapping_constant = destination_range_start - source_range_start
            self.ranges.append((source_range, mapping_constant))

    def apply_map(self, source):
        for source_range, mapping_constant in self.ranges:
            if source in source_range:
                return source + mapping_constant
        return source

    def __repr__(self) -> str:
        s = "["
        for source_range, mapping_constant in self.ranges:
            s += f"({source_range.start}, {source_range.stop}) → {mapping_constant}), "
        s = s[:-2] + "]"
        return s


# %%
if __name__ == "__main__":
    with open(puzzle(5), "r") as f:
        data = f.read().strip().split("\n\n")

    seeds_str, *category_maps_str = data
    seeds = list(map(int, seeds_str.removeprefix("seeds: ").split(" ")))
    # categories = dict(map(parse_category_map, category_maps_str))
    categories_ranges = [
        parse_category_map(ranges_str)[1] for ranges_str in category_maps_str
    ]
    categories_maps = [MapSourceToDestination(ranges) for ranges in categories_ranges]

    locations = seeds.copy()
    for category_map in categories_maps:
        locations = map(category_map.apply_map, locations)

    print("Part 1 —", min(locations))

# %%
