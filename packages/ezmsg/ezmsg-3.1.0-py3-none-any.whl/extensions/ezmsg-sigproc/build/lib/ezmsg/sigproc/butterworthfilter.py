import ezmsg.core as ez
import scipy.signal
import numpy as np

from .filter import FilterCoefficients, Filter
from .timeseriesmessage import TimeSeriesMessage

from typing import (
    AsyncGenerator,
    Optional,
    Tuple
)


class ButterworthFilterSettings(ez.Settings):
    order: int
    cuton: Optional[float] = None  # Hz
    cutoff: Optional[float] = None  # Hz


class ButterworthFilterDesignState(ez.State):
    fs: Optional[float] = None  # Hz


class ButterworthFilterDesign(ez.Unit):

    SETTINGS: ButterworthFilterSettings
    STATE: ButterworthFilterDesignState

    INPUT_SIGNAL = ez.InputStream(TimeSeriesMessage)
    OUTPUT_FILTER = ez.OutputStream(FilterCoefficients)

    def design_filter(self, fs: Optional[float] = None) -> Tuple[np.ndarray, ...]:
        assert (self.SETTINGS.cuton is not None) or (self.SETTINGS.cutoff is not None)
        if self.SETTINGS.cuton is None and self.SETTINGS.cutoff is not None:
            btype, cut = 'lowpass', self.SETTINGS.cutoff
        elif self.SETTINGS.cuton is not None and self.SETTINGS.cutoff is None:
            btype, cut = 'highpass', self.SETTINGS.cuton
        elif self.SETTINGS.cuton is not None and self.SETTINGS.cutoff is not None:
            if self.SETTINGS.cuton <= self.SETTINGS.cutoff:
                btype, cut = 'bandpass', (
                    self.SETTINGS.cuton,
                    self.SETTINGS.cutoff
                )
            else:
                btype, cut = 'bandstop', (
                    self.SETTINGS.cutoff,
                    self.SETTINGS.cuton
                )

        return scipy.signal.butter(
            self.SETTINGS.order,
            Wn=cut,
            btype=btype,
            fs=fs,
            output='ba'
        )

    @ez.subscriber(INPUT_SIGNAL)
    @ez.publisher(OUTPUT_FILTER)
    async def redesign(self, message: TimeSeriesMessage) -> AsyncGenerator:
        if self.STATE.fs != message.fs:
            self.STATE.fs = message.fs
            b, a = self.design_filter(message.fs)
            yield (self.OUTPUT_FILTER,
                   FilterCoefficients(b=b, a=a)
                   )


class ButterworthFilter(ez.Collection):

    SETTINGS: ButterworthFilterSettings

    INPUT_SIGNAL = ez.InputStream(TimeSeriesMessage)
    OUTPUT_SIGNAL = ez.OutputStream(TimeSeriesMessage)

    DESIGN = ButterworthFilterDesign()
    FILTER = Filter()

    def configure(self) -> None:
        self.DESIGN.apply_settings(self.SETTINGS)

    def network(self) -> ez.NetworkDefinition:
        return (

            (self.INPUT_SIGNAL, self.DESIGN.INPUT_SIGNAL),
            (self.DESIGN.OUTPUT_FILTER, self.FILTER.INPUT_FILTER),

            (self.INPUT_SIGNAL, self.FILTER.INPUT_SIGNAL),
            (self.FILTER.OUTPUT_SIGNAL, self.OUTPUT_SIGNAL)

        )
