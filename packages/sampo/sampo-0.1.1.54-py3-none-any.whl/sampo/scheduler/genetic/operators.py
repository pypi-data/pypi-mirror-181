import random
from typing import List, Dict, Iterable

import numpy as np
from deap import creator, base, tools

from sampo.scheduler.genetic.converter import convert_chromosome_to_schedule
from sampo.scheduler.genetic.converter import convert_schedule_to_chromosome, ChromosomeType
from sampo.scheduler.topological.base import RandomizedTopologicalScheduler
from sampo.schemas.contractor import Contractor, WorkerContractorPool
from sampo.schemas.graph import GraphNode, WorkGraph
from sampo.schemas.resources import Worker
from sampo.schemas.schedule import ScheduledWork
from sampo.schemas.schedule_spec import ScheduleSpec
from sampo.schemas.time import Time
from sampo.schemas.time_estimator import WorkTimeEstimator

# create class FitnessMin, the weights = -1 means that fitness - is function for minimum

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
Individual = creator.Individual


def init_toolbox(wg: WorkGraph, contractors: List[Contractor], worker_pool: WorkerContractorPool,
                 index2node: Dict[int, GraphNode],
                 work_id2index: Dict[str, int], worker_name2index: Dict[str, int],
                 index2contractor: Dict[int, str],
                 index2contractor_obj: Dict[int, Contractor],
                 init_chromosomes: Dict[str, ChromosomeType],
                 mutate_order: float, mutate_resources: float, selection_size: int,
                 rand: random.Random,
                 spec: ScheduleSpec,
                 worker_pool_indices: dict[int, dict[int, Worker]],
                 contractor2index: dict[str, int],
                 node_indices: list[int],
                 index2node_list: list[tuple[int, GraphNode]],
                 work_estimator: WorkTimeEstimator = None) -> base.Toolbox:
    toolbox = base.Toolbox()
    # generate initial population
    toolbox.register("generate_chromosome", generate_chromosome, wg=wg, contractors=contractors,
                     index2node_list=index2node_list, work_id2index=work_id2index, worker_name2index=worker_name2index,
                     contractor2index=contractor2index,
                     init_chromosomes=init_chromosomes, rand=rand, work_estimator=work_estimator)

    # create from generate_chromosome function one individual
    toolbox.register("individual", tools.initRepeat, Individual, toolbox.generate_chromosome, n=1)
    # create population from individuals
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    # evaluation function
    toolbox.register("evaluate", chromosome_evaluation, index2node=index2node,
                     index2contractor=index2contractor_obj, worker_pool=worker_pool, node_indices=node_indices,
                     worker_pool_indices=worker_pool_indices, spec=spec, work_estimator=work_estimator)
    # crossover for order
    toolbox.register("mate", mate_scheduling_order, rand=rand)
    # mutation for order. Coefficient luke one or two mutation in individual
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=mutate_order)
    # selection. Some random individuals and arranges a battle between them as a result in a continuing genus,
    # this is the best among these it
    toolbox.register("select", tools.selTournament, tournsize=selection_size)

    # mutation for resources
    toolbox.register("mutate_resources", mut_uniform_int, probability_mutate_resources=mutate_resources,
                     contractor_count=len(index2contractor), rand=rand)
    # crossover for resources
    toolbox.register("mate_resources", mate_for_resources, rand=rand)

    toolbox.register("validate", is_chromosome_correct, index2node=index2node, worker_pool_indices=worker_pool_indices,
                     node_indices=node_indices)
    toolbox.register("schedule_to_chromosome", convert_schedule_to_chromosome, index2node=index2node_list,
                     work_id2index=work_id2index, worker_name2index=worker_name2index,
                     contractor2index=contractor2index)
    toolbox.register("chromosome_to_schedule", convert_chromosome_to_schedule, worker_pool=worker_pool,
                     index2node=index2node, index2contractor=index2contractor_obj,
                     worker_pool_indices=worker_pool_indices, spec=spec, work_estimator=work_estimator)
    return toolbox


def generate_chromosome(wg: WorkGraph, contractors: List[Contractor], index2node_list: list[tuple[int, GraphNode]],
                        work_id2index: Dict[str, int], worker_name2index: Dict[str, int],
                        contractor2index: Dict[str, int],
                        init_chromosomes: Dict[str, ChromosomeType], rand: random.Random,
                        work_estimator: WorkTimeEstimator = None) -> ChromosomeType:
    """
    It is necessary to generate valid scheduling, which are satisfied to current dependencies
    That's why will be used the approved order of works (HEFT order and Topological sorting)
    Topological sorts are generating always different
    HEFT is always the same(now not)
    HEFT we will choose in 30% of attempts
    Topological in others
    :param contractor2index:
    :param work_estimator:
    :param contractors:
    :param wg:
    :param work_id2index:
    :param index2node_list:
    :param worker_name2index:
    :param rand:
    :param init_chromosomes:
    :return: chromosome
    """

    # do random choice to choose type of generation current chromosome (HEFT or Topological type)
    chance = rand.random()
    if chance < 0.2:
        chromosome = init_chromosomes["heft_end"]
    elif chance < 0.4:
        chromosome = init_chromosomes["heft_between"]
    else:
        schedule = RandomizedTopologicalScheduler(work_estimator,
                                                  int(rand.random() * 1000000)) \
            .schedule(wg, contractors)
        chromosome = convert_schedule_to_chromosome(index2node_list, work_id2index, worker_name2index,
                                                    contractor2index, schedule)
    return chromosome


def chromosome_evaluation(individuals: List[ChromosomeType], index2node: Dict[int, GraphNode],
                          index2contractor: Dict[int, Contractor],
                          worker_pool_indices: dict[int, dict[int, Worker]], node_indices: list[int],
                          worker_pool: WorkerContractorPool, spec: ScheduleSpec,
                          work_estimator: WorkTimeEstimator = None) -> Time:
    chromosome = individuals[0]
    if is_chromosome_correct(chromosome, index2node, worker_pool_indices, node_indices):
        scheduled_works, _, _ = convert_chromosome_to_schedule(chromosome, worker_pool, index2node,
                                                               index2contractor, worker_pool_indices,
                                                               spec, work_estimator)
        return max(scheduled_works.values(), key=ScheduledWork.finish_time_getter()).finish_time
    else:
        return Time.inf()


def is_chromosome_correct(chromosome: ChromosomeType, index2node: Dict[int, GraphNode],
                          worker_pool_indices: dict[int, dict[int, Worker]], node_indices: list[int]) -> bool:
    return is_chromosome_order_correct(chromosome, index2node) and \
           is_chromosome_contractors_correct(chromosome, worker_pool_indices, node_indices)


def is_chromosome_order_correct(chromosome: ChromosomeType, index2node: Dict[int, GraphNode]) -> bool:
    work_order = chromosome[0]
    used = set()
    for work_index in work_order:
        node = index2node[work_index]
        for parent in node.parents:
            if parent.id not in used:
                return False
        used.add(node.id)
    return True


def is_chromosome_contractors_correct(chromosome: ChromosomeType,
                                      worker_pool_indices: dict[int, dict[int, Worker]],
                                      work_indices: Iterable[int]) -> bool:
    """
    Checks that assigned contractors can supply assigned workers
    :param chromosome:
    :param worker_pool_indices:
    :param work_indices:
    :return:
    """
    for work_ind in work_indices:
        resources_count = chromosome[1][:-1, work_ind]
        contractor_ind = chromosome[1][-1, work_ind]
        for ind, count in enumerate(resources_count):
            if worker_pool_indices[ind][contractor_ind].count < count:
                return False
    return True


def get_order_tail(head_set: List[int], other: List[int]) -> List[int]:
    head_set = set(head_set)
    return [node for node in other if node not in head_set]


def mate_scheduling_order(ind1: List[int], ind2: List[int], rand: random.Random) -> (List[int], List[int]):
    """
    Crossover for order
    Basis crossover is cxOnePoint
    But we checked not repeated works in individual order
    :param ind1:
    :param ind2:
    :param rand:
    :return: two cross individuals
    """
    # randomly select the point where the crossover will take place
    crossover_point = rand.randint(1, len(ind1))

    ind1_new_tail = get_order_tail(ind1[:crossover_point], ind2)
    ind2_new_tail = get_order_tail(ind2[:crossover_point], ind1)

    ind1[crossover_point:] = ind1_new_tail
    ind2[crossover_point:] = ind2_new_tail

    return ind1, ind2


def mut_uniform_int(chromosome: ChromosomeType, low: np.ndarray, up: np.ndarray, type_of_worker: int,
                    probability_mutate_resources: float, contractor_count: int, rand: random.Random) -> ChromosomeType:
    """
    Mutation function for resources
    It changes selected numbers of workers in random work in certain interval for this work
    :param contractor_count:
    :param chromosome:
    :param low:
    :param up:
    :param type_of_worker:
    :param probability_mutate_resources:
    :param rand:
    :return: mutate individual
    """
    # select random number from interval from min to max from uniform distribution
    size = len(chromosome[1][type_of_worker])

    if type_of_worker == len(chromosome[1]) - 1:
        # print('Contractor mutation!')
        for i in range(size):
            if rand.random() < probability_mutate_resources:
                chromosome[1][type_of_worker][i] = rand.randint(0, contractor_count - 1)
        return chromosome

    # change in this interval in random number from interval
    for i, xl, xu in zip(range(size), low, up):
        if rand.random() < probability_mutate_resources:
            chromosome[1][type_of_worker][i] = rand.randint(xl, xu)

    return chromosome


def mate_for_resources(ind1: np.ndarray, ind2: np.ndarray, rand: random.Random) -> (
        np.ndarray, np.ndarray):
    """
    CxOnePoint for resources
    :param ind1:
    :param ind2:
    :param rand:
    :return:
    """
    cxpoint = rand.randint(1, len(ind1))
    ind1[cxpoint:], ind2[cxpoint:] = ind2[cxpoint:], ind1[cxpoint:]
    return ind1, ind2
