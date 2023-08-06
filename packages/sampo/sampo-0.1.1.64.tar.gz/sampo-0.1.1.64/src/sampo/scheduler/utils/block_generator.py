from enum import Enum
from random import Random
from typing import Callable

from sampo.generator import SimpleSynthetic
from sampo.generator.types import SyntheticGraphType
from sampo.scheduler.utils.block_graph import BlockGraph
from sampo.scheduler.utils.obstruction import Obstruction


class SyntheticBlockGraphType(Enum):
    Sequential = 0,
    Parallel = 1,
    Random = 2,
    Queues = 3


def generate_blocks(graph_type: SyntheticBlockGraphType, n_blocks: int, type_prop: list[int],
                    count_supplier: Callable[[int], tuple[int, int]],
                    edge_prob: float, rand: Random | None = Random(),
                    obstruction_getter: Callable[[int], Obstruction | None] = lambda _: None) -> BlockGraph:
    """
    Generate synthetic block graph according to given parameters.

    :param graph_type: type of BlockGraph
    :param n_blocks: the count of blocks
    :param type_prop: proportions of the `WorkGraph` types: General, Parallel, Sequential
    :param count_supplier: function that computes the borders of block size from it's index
    :param edge_prob: edge existence probability
    :param rand: a random reference
    :param obstruction_getter:
    :return: generated block graph
    """
    ss = SimpleSynthetic(rand)

    modes = rand.sample(list(SyntheticGraphType), counts=[p * n_blocks for p in type_prop], k=n_blocks)
    nodes = [ss.work_graph(mode, *count_supplier(i)) for i, mode in enumerate(modes)]
    bg = BlockGraph(nodes, obstruction_getter)

    match graph_type:
        case SyntheticBlockGraphType.Sequential:
            for idx, start in enumerate(bg.nodes[:-2]):
                bg.add_edge(start, bg.nodes[idx + 1])
        case SyntheticBlockGraphType.Parallel:
            for idx, start in enumerate(bg.nodes[:-2]):
                bg.add_edge(start, bg.nodes[idx + 1])
        case SyntheticBlockGraphType.Random:
            rev_edge_prob = int(1 / edge_prob)
            for idx, start in enumerate(bg.nodes):
                for end in bg.nodes[idx:]:
                    if start == end or rand.randint(0, rev_edge_prob) != 0:
                        continue
                    bg.add_edge(start, end)

    return bg