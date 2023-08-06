from enum import Enum
from typing import Optional, Union

from hcube.api.exceptions import ConfigurationError
from hcube.api.models.dimensions import Dimension
from hcube.api.models.metrics import Metric


class AggregationOp(Enum):
    """
    Defines different aggregation operations which each cube backend should implement.
    """

    SUM = "sum"
    COUNT = "count"
    MAX = "max"
    MIN = "min"


class Aggregation:

    allow_metric_none = False

    def __init__(self, metric: Union[str, Metric], op: AggregationOp, name: Optional[str] = None):
        self.metric = metric
        self.op: AggregationOp = op
        self.name: str = name if name else op.value


class AggregationShorthand(Aggregation):
    """
    aggregation shorthands can be used to more easily express the aggregation
    """

    agg_op = None

    def __init__(self, metric: Union[str, Metric], name: Optional[str] = None):
        super().__init__(metric, self.agg_op, name)


class Sum(AggregationShorthand):
    agg_op = AggregationOp.SUM


class Count(AggregationShorthand):
    agg_op = AggregationOp.COUNT
    allow_metric_none = True

    def __init__(
        self,
        metric: Optional[Union[str, Metric]] = None,
        distinct: Optional[Union[str, Dimension]] = None,
        name: Optional[str] = None,
    ):
        """
        Count does not need a metric
        """
        super().__init__(metric, name)
        self.distinct = distinct
        if self.distinct and self.metric:
            raise ConfigurationError(
                "`distinct` [Dimension] and `metric` [Metric] are mutually exclusive"
            )


class Min(AggregationShorthand):
    agg_op = AggregationOp.MIN


class Max(AggregationShorthand):
    agg_op = AggregationOp.MAX
