# %%
import bisect

from helpers.load_puzzle import puzzle


# %%
def parse_category_map(category_map_str):
    category_label, ranges_str = category_map_str.split(" map:\n")
    ranges = eval("[[" + ranges_str.replace(" ", ",").replace("\n", "],[") + "]]")
    return category_label, ranges


def to_pairs(L):
    return list(zip(L, L[1:]))


def group_by_two(L):
    return list(zip(L[0::2], L[1::2]))


# %%
class MapSourceToDestination:
    def __init__(self, ranges):
        if not ranges:
            self.bins, self.deltas = [], [0]
            return

        ranges.sort(key=lambda x: x[1])
        self.bins = [ranges[0][1]]
        self.deltas = [0]

        for range_ in ranges:
            destination_range_start, source_range_start, range_length = range_
            source_range_end = source_range_start + range_length
            mapping_constant = destination_range_start - source_range_start

            if source_range_start != self.bins[-1]:
                self.bins.append(source_range_start)
                self.deltas.append(0)

            self.bins.append(source_range_end)
            self.deltas.append(mapping_constant)
        self.deltas.append(0)

        assert len(self.bins) + 1 == len(
            self.deltas
        ), f"bins {len(self.bins)}, deltas {len(self.deltas)}"

    def apply_map(self, source):
        index = bisect.bisect(self.bins, source)
        return source + self.deltas[index]

    def apply_map_to_range(self, source_range):
        start, end = source_range
        i = bisect.bisect(self.bins, start)
        j = bisect.bisect(self.bins, end)
        range_bins = [start] + self.bins[i:j] + [end]
        bins = to_pairs(range_bins)
        deltas = self.deltas[i : j + 1]

        destination_ranges = [(b[0] + d, b[1] + d) for b, d in zip(bins, deltas)]
        return destination_ranges

    def apply_map_to_ranges(self, source_ranges):
        destination_ranges = []
        for source_range in source_ranges:
            destination_ranges.extend(self.apply_map_to_range(source_range))
        return destination_ranges

    def __repr__(self) -> str:
        return f" (bins: {self.bins})" + f" (values: {self.deltas})"


# %%
def part1(seeds, categories_maps):
    locations = seeds.copy()
    for category_map in categories_maps:
        locations = map(category_map.apply_map, locations)
    return min(locations)


def part2(seeds, categories_maps):
    locations_pairs = group_by_two(seeds)
    locations_ranges = [(start, start + delta) for start, delta in locations_pairs]
    for category_map in categories_maps:
        locations_ranges = category_map.apply_map_to_ranges(locations_ranges)
    return min(locations_ranges, key=lambda x: x[0])[0]


# %%
if __name__ == "__main__":
    with open(puzzle(5), "r") as f:
        data = f.read().strip().split("\n\n")

    seeds_str, *category_maps_str = data
    seeds = list(map(int, seeds_str.removeprefix("seeds: ").split(" ")))
    categories_ranges = [
        parse_category_map(ranges_str)[1] for ranges_str in category_maps_str
    ]
    categories_maps = [MapSourceToDestination(ranges) for ranges in categories_ranges]

    print("Part 1 —", part1(seeds, categories_maps))
    print("Part 2 –", part2(seeds, categories_maps))

# %%
