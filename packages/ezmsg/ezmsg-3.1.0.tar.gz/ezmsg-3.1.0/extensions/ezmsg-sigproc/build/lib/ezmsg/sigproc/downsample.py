from dataclasses import replace

import ezmsg.core as ez
import numpy as np

from .timeseriesmessage import TimeSeriesMessage

from typing import (
    AsyncGenerator,
    Optional,
)


class DownsampleSettings(ez.Settings):
    factor: int  # Downsample factor


class DownsampleState(ez.State):
    s_idx: int = 0


class Downsample(ez.Unit):

    SETTINGS: DownsampleSettings
    STATE: DownsampleState

    INPUT_SIGNAL = ez.InputStream(TimeSeriesMessage)
    OUTPUT_SIGNAL = ez.OutputStream(TimeSeriesMessage)

    @ez.subscriber(INPUT_SIGNAL)
    @ez.publisher(OUTPUT_SIGNAL)
    async def on_signal(self, msg: TimeSeriesMessage) -> AsyncGenerator:

        samples = np.arange(msg.n_time) + self.STATE.s_idx
        samples = samples % self.SETTINGS.factor
        self.STATE.s_idx = samples[-1] + 1

        pub_samples = np.where(samples == 0)[0]

        if len(pub_samples) != 0:

            time_view = np.moveaxis(msg.data, msg.time_dim, 0)
            data_down = time_view[pub_samples, ...]
            data_down = np.moveaxis(data_down, 0, -(msg.time_dim))

            yield (
                self.OUTPUT_SIGNAL,
                replace(
                    msg,
                    data=data_down,
                    fs=msg.fs / self.SETTINGS.factor
                )
            )
