from typing import List, Optional, Dict, Iterable

from sampo.scheduler.base import Scheduler, SchedulerType
from sampo.scheduler.heft.prioritization import prioritization
from sampo.scheduler.heft.time_computaion import calculate_working_time_cascade
from sampo.scheduler.resource.base import ResourceOptimizer
from sampo.scheduler.resource.coordinate_descent import CoordinateDescentResourceOptimizer
from sampo.scheduler.timeline.just_in_time_timeline import JustInTimeTimeline
from sampo.scheduler.utils.multi_contractor import get_best_contractor_and_worker_borders
from sampo.schemas.contractor import Contractor, get_worker_contractor_pool
from sampo.schemas.graph import WorkGraph, GraphNode
from sampo.schemas.schedule import Schedule
from sampo.schemas.schedule_spec import ScheduleSpec
from sampo.schemas.scheduled_work import ScheduledWork
from sampo.schemas.time_estimator import WorkTimeEstimator
from sampo.utilities.base_opt import dichotomy_int
from sampo.utilities.validation import validate_schedule


class HEFTScheduler(Scheduler):

    def __init__(self,
                 scheduler_type: SchedulerType = SchedulerType.HEFTAddEnd,
                 resource_optimizer: ResourceOptimizer = CoordinateDescentResourceOptimizer(dichotomy_int),
                 work_estimator: Optional[WorkTimeEstimator or None] = None):
        super().__init__(scheduler_type, resource_optimizer, work_estimator)

    def schedule(self, wg: WorkGraph,
                 contractors: List[Contractor],
                 spec: ScheduleSpec = ScheduleSpec(),
                 validate: bool = False) \
            -> Schedule:
        ordered_nodes = prioritization(wg, self.work_estimator)

        schedule = Schedule.from_scheduled_works(
            self.build_scheduler(ordered_nodes, contractors, spec, self.work_estimator),
            wg
        )

        if validate:
            validate_schedule(schedule, wg, contractors)

        return schedule

    def build_scheduler(self,
                        ordered_nodes: List[GraphNode],
                        contractors: List[Contractor],
                        spec: ScheduleSpec,
                        work_estimator: WorkTimeEstimator = None) \
            -> Iterable[ScheduledWork]:
        """
        Find optimal number of workers who ensure the nearest finish time.
        Finish time is combination of two dependencies: max finish time, max time of waiting of needed workers
        This is selected by iteration from minimum possible numbers of workers until then the finish time is decreasing
        :param contractors:
        :param work_estimator:
        :param spec: spec for current scheduling
        :param ordered_nodes:
        :return:
        """
        worker_pool = get_worker_contractor_pool(contractors)
        # dict for writing parameters of completed_jobs
        node2swork: Dict[GraphNode, ScheduledWork] = {}
        # list for support the queue of workers
        timeline = JustInTimeTimeline(worker_pool)

        for index, node in enumerate(reversed(ordered_nodes)):  # the tasks with the highest rank will be done first
            work_unit = node.work_unit
            work_spec = spec.get_work_spec(work_unit.id)
            if node in node2swork:  # here
                continue

            min_count_worker_team, max_count_worker_team, contractor, workers \
                = get_best_contractor_and_worker_borders(worker_pool, contractors, work_unit.worker_reqs)

            best_worker_team = [worker.copy() for worker in workers]

            def get_finish_time(worker_team):
                return timeline.find_min_start_time(node, worker_team, node2swork) \
                       + calculate_working_time_cascade(node, worker_team, work_estimator)

            # apply worker team spec
            self.optimize_resources_using_spec(work_unit, best_worker_team, work_spec,
                                               lambda optimize_array: self.resource_optimizer.optimize_resources(
                                                   worker_pool, best_worker_team,
                                                   optimize_array,
                                                   min_count_worker_team, max_count_worker_team,
                                                   get_finish_time))

            # apply work to scheduling
            c_ft = timeline.schedule(index, node, node2swork, best_worker_team, contractor,
                                     work_spec.assigned_time, work_estimator)

            # add using resources in queue for workers
            timeline.update_timeline(c_ft, best_worker_team)

        # parallelize_local_sequence(ordered_nodes, 0, len(ordered_nodes), work_id2schedule_unit)
        # recalc_schedule(reversed(ordered_nodes), work_id2schedule_unit, worker_pool, work_estimator)

        return node2swork.values()
