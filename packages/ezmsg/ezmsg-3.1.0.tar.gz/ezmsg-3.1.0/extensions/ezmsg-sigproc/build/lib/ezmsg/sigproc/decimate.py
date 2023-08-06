import ezmsg.core as ez

import scipy.signal

from .downsample import Downsample, DownsampleSettings
from .filter import Filter, FilterCoefficients, FilterSettings
from .timeseriesmessage import TimeSeriesMessage


class Decimate(ez.Collection):

    SETTINGS: DownsampleSettings

    INPUT_SIGNAL = ez.InputStream(TimeSeriesMessage)
    OUTPUT_SIGNAL = ez.OutputStream(TimeSeriesMessage)

    FILTER = Filter()
    DOWNSAMPLE = Downsample()

    def configure(self) -> None:

        self.DOWNSAMPLE.apply_settings(self.SETTINGS)

        # See scipy.signal.decimate for IIR Filter Condition
        system = scipy.signal.dlti(
            *scipy.signal.cheby1(8, 0.05, 0.8 / self.SETTINGS.factor)
        )

        self.FILTER.apply_settings(
            FilterSettings(
                filt=FilterCoefficients(
                    b=system.num,
                    a=system.den
                )
            )
        )

    def network(self) -> ez.NetworkDefinition:
        return (
            (self.INPUT_SIGNAL, self.FILTER.INPUT_SIGNAL),
            (self.FILTER.OUTPUT_SIGNAL, self.DOWNSAMPLE.INPUT_SIGNAL),
            (self.DOWNSAMPLE.OUTPUT_SIGNAL, self.OUTPUT_SIGNAL),
        )
