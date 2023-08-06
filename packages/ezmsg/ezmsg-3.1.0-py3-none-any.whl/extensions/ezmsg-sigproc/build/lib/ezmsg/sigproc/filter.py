from dataclasses import replace

import ezmsg.core as ez
import scipy.signal
import numpy as np

from .timeseriesmessage import TimeSeriesMessage

from typing import (
    AsyncGenerator,
    Optional,
    Tuple
)


class FilterCoefficients(ez.Message):
    b: np.ndarray
    a: np.ndarray


class FilterSettings(ez.Settings):
    # If you'd like to statically design a filter, define it in settings
    filt: Optional[FilterCoefficients] = None


class FilterState(ez.State):
    zi: Optional[np.ndarray] = None
    filt: Optional[FilterCoefficients] = None
    samp_shape: Optional[Tuple[int, ...]] = None


class Filter(ez.Unit):
    SETTINGS: FilterSettings
    STATE: FilterState

    INPUT_FILTER = ez.InputStream(FilterCoefficients)
    INPUT_SIGNAL = ez.InputStream(TimeSeriesMessage)
    OUTPUT_SIGNAL = ez.OutputStream(TimeSeriesMessage)

    # Set up filter with static initialization if specified
    def initialize(self) -> None:
        if self.SETTINGS.filt is not None:
            self.STATE.filt = self.SETTINGS.filt

    # This is called to dynamically change filter during operation
    # Note, there will be discontinuities
    # TODO: Don't reset zi unless filter order changes
    @ez.subscriber(INPUT_FILTER)
    async def set_filter(self, message: FilterCoefficients) -> None:
        """ This is used for filter design and for adaptive filters """
        self.STATE.filt = message
        self.STATE.zi = None
        self.STATE.samp_shape = None

    @ez.subscriber(INPUT_SIGNAL)
    @ez.publisher(OUTPUT_SIGNAL)
    async def apply_filter(self, message: TimeSeriesMessage) -> AsyncGenerator:

        if self.STATE.filt is None:
            return

        # We will perform filter with time dimension as last axis
        arr_in: np.ndarray = np.moveaxis(message.data, message.time_dim, -1)
        samp_shape = arr_in[..., 0].shape

        # Re-calculate/reset zi if necessary
        if self.STATE.zi is None or samp_shape != self.STATE.samp_shape:
            zi: np.ndarray = scipy.signal.lfilter_zi(self.STATE.filt.b, self.STATE.filt.a)
            self.STATE.samp_shape = samp_shape
            self.STATE.zi = np.array([zi] * np.prod(self.STATE.samp_shape))
            self.STATE.zi = self.STATE.zi.reshape(
                tuple(list(self.STATE.samp_shape) + [zi.shape[0]])
            )

        arr_out, self.STATE.zi = scipy.signal.lfilter(
            self.STATE.filt.b,
            self.STATE.filt.a,
            arr_in,
            zi=self.STATE.zi
        )

        arr_out = np.moveaxis(arr_out, -1, message.time_dim)

        yield (self.OUTPUT_SIGNAL, replace(message, data=arr_out))
