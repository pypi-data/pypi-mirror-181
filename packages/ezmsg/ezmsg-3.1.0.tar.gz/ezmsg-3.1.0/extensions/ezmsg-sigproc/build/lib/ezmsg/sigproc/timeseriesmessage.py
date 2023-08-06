from dataclasses import field

import numpy as np

from typing import (
    Tuple
)

from ezmsg.util.stampedmessage import StampedMessage


class TimeSeriesMessage(StampedMessage):
    """
    TimeSeriesMessage -- Base message type for timeseries data flowing through ezbci

    General Principles to a TimeSeries Message
    1. Time dim is the 0'th dimension of the data arrays.
        (I'm working on relaxing this requirement, but it's slow goings. - Griff)
    """

    data: np.ndarray
    fs: float

    time_dim: int = field(default=0, init=False)

    @property
    def shape(self) -> Tuple[int, ...]:
        """ Shape of data """
        return self.data.shape

    @property
    def n_time(self) -> int:
        """ Number of time values in the mesage """
        return self.shape[self.time_dim]
