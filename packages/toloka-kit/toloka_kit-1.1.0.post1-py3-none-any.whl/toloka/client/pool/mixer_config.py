__all__ = ['MixerConfig']

from ..primitives.base import BaseTolokaObject
from ..task_distribution_function import TaskDistributionFunction
from ...util._codegen import attribute


class MixerConfig(BaseTolokaObject):
    """Parameters for automatically creating a task suite ("smart mixing").

    For more information about creating task see Toloka Requester's guide.

    Attributes:
        real_tasks_count: The number of main tasks to put in a task suite.
            The maximum number of tasks in a task suite if training_task_distribution_function or
            golden_task_distribution_function are used.
        golden_tasks_count: The number of control ("golden set") tasks to put in a task suite.
        training_tasks_count: The number of training tasks to put in a task suite.
        min_real_tasks_count: Minimum number of main tasks in a task suite (if the number of assignments left is less
            than the one specified in real_tasks_count). Minimum — 0. By default, the value is the same as in
            real_tasks_count.
        min_golden_tasks_count: Minimum number of control tasks in a task suite (if the number of assignments left is
            less than the one specified in golden_tasks_count). Minimum — 0. By default, the value is the same as
            in golden_tasks_count.
        min_training_tasks_count: Minimum number of training tasks in a task suite (if the number of assignments left is
            less than the one specified in golden_tasks_count). Minimum — 0. By default, the value is the same
            as in training_tasks_count.
        force_last_assignment: Setup for the last set of tasks in the pool, if less than the minimum remaining number of
            tasks are not completed (mixer_config.min_real_tasks_count). Values:
            * true - issue an incomplete task set.
            * false - don't issue tasks. This option can be used if you are adding tasks after the pool is started.
            This parameter only applies to main tasks. The number of control and training tasks in the last set must be
            complete (golden_tasks_count, training_tasks_count).
        force_last_assignment_delay_seconds: Waiting time (in seconds) since the addition of the task, or increase in
            the overlap, prior to the issuance of the last set of tasks in the pool. The minimum is 0, the maximum is
            86,400 seconds (one day).
            This parameter can be used if the pool has force_last_assignment: True.
        mix_tasks_in_creation_order: The order for including tasks in suites:
            * True — Add tasks to suites in the order in which they were uploaded. For example, in a pool with an
                overlap of 5, the first uploaded task will be included in the first 5 task suites. They will be
                assigned to 5 Tolokers.
            * False — Add tasks to suites in random order.
        shuffle_tasks_in_task_suite: The order of tasks within a suite:
            * True — Random.
            * False — The order in which tasks were uploaded.
        golden_task_distribution_function: Issue of control tasks with uneven frequency. The option allows you to change
            the frequency of checking as the Toloker completes more tasks.
        training_task_distribution_function: Issue of training tasks with uneven frequency. The option allows you to
            change the frequency of training tasks as the Toloker completes more tasks.
    """

    real_tasks_count: int = attribute(default=0, required=True)
    golden_tasks_count: int = attribute(default=0, required=True)
    training_tasks_count: int = attribute(default=0, required=True)
    min_real_tasks_count: int
    min_golden_tasks_count: int
    min_training_tasks_count: int
    force_last_assignment: bool
    force_last_assignment_delay_seconds: int
    mix_tasks_in_creation_order: bool
    shuffle_tasks_in_task_suite: bool
    golden_task_distribution_function: TaskDistributionFunction
    training_task_distribution_function: TaskDistributionFunction
