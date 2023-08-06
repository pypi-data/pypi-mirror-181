from copy import deepcopy
from operator import attrgetter
from random import Random
from typing import Callable

from sampo.generator import SimpleSynthetic
from sampo.generator.types import SyntheticGraphType
from sampo.scheduler.utils.obstruction import Obstruction
from sampo.schemas.graph import WorkGraph, GraphNode
from sampo.utilities.collections import build_index


class BlockNode:
    """
    `BlockNode` represents the node of `BlockGraph` and contains corresponding
    `WorkGraph` and related dependencies between blocks in `BlockGraph`.
    """
    def __init__(self, wg: WorkGraph, obstruction: Obstruction | None = None):
        self.wg = wg
        self.obstruction = obstruction
        self.blocks_from: list[BlockNode] = []
        self.blocks_to: list[BlockNode] = []

    @property
    def id(self):
        return self.wg.start.id


class BlockGraph:
    """
    Represents the block graph, where blocks are instances of `WorkGraph` and
    edges are simple *FS* dependencies.
    """
    def __init__(self, nodes: list[WorkGraph], obstruction_getter: Callable[[int], Obstruction | None] = lambda _: None):
        self.nodes = [BlockNode(node, obstruction_getter(i)) for i, node in enumerate(nodes)]
        self.node_dict = build_index(self.nodes, attrgetter('id'))

    def __getitem__(self, item) -> BlockNode:
        return self.node_dict[item]

    def to_work_graph(self) -> WorkGraph:
        """
        Creates `WorkGraph` that are equal to this `BlockGraph`.
        """
        copied_nodes = deepcopy(self.nodes)
        global_start: GraphNode = [node for node in copied_nodes if len(node.blocks_from) == 0][0].wg.start
        global_end:   GraphNode = [node for node in copied_nodes if len(node.blocks_to) == 0][0].wg.finish

        for end in copied_nodes:
            end.wg.start.add_parents([start.wg.finish for start in end.blocks_from])

        return WorkGraph(global_start, global_end)

    @staticmethod
    def add_edge(start: BlockNode, end: BlockNode):
        start.blocks_to.append(end)
        end.blocks_from.append(start)
