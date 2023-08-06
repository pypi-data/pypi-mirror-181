""" This module contains in the implementation of radio-frequency pulse building blocks"""
__all__ = ["RFPulse", "SincRFPulse", "ArbitraryRFPulse"]

from typing import Tuple

from pint import Quantity
import numpy as np

from cmrseq.core.bausteine._base import SequenceBaseBlock
from cmrseq.core._system import SystemSpec


class RFPulse(SequenceBaseBlock):
    """ RF-specific extension to the SequenceBaseBlock, serves as base class for all
    RF implementations"""

    #: RF pulse bandwidth in kilo Hertz. Used to calculate gradient strength
    bandwidth: Quantity
    #: RF phase offset in radians. This is used phase shift the complex rf amplitude in self.rf
    phase_offset: Quantity
    #: RF frequency offset in Hertz. This is used to modulate the complex rf amplitude in self.rf
    frequency_offset: Quantity

    def __init__(self, system_specs: SystemSpec, name: str, frequency_offset: Quantity,
                 phase_offset: Quantity, bandwidth: Quantity, snap_to_raster: bool):
        self.phase_offset = phase_offset.to("rad")
        self.frequency_offset = frequency_offset.to("Hz")
        self.bandwidth = bandwidth.to("kHz")
        super().__init__(system_specs, name, snap_to_raster)

    @property
    def tmin(self):
        return self._rf[0][0]

    @property
    def rf(self):
        """ Returns the complex RF-amplitude shifted/modulated by the phase/frequency offsets """
        t, amplitude = self._rf
        t_zero_ref = t - t[0]
        if amplitude.m_as("uT").dtype in [np.complex64, np.complex128]:
            complex_amplitude = amplitude
        else:
            complex_amplitude = (amplitude + 1j * np.zeros_like(amplitude))
        phase_per_time = (self.phase_offset.m_as("rad") +
                          2 * np.pi * self.frequency_offset.m_as("kHz") * t_zero_ref.m_as("ms"))
        complex_amplitude *= np.exp(1j * phase_per_time)
        return t, complex_amplitude

    @rf.setter
    def rf(self, value: Tuple[Quantity, Quantity]):
        self._rf = value

    @property
    def normalized_waveform(self) -> (np.ndarray, Quantity, np.ndarray, Quantity):
        """
        :return: - Normalized amplitude between [-1, 1] [dimensionless] (flipped such that the
                    maximum normalized value is positive. Scaling with peak amplitude inverts the
                    shape again)
                 - Peak amplitude in uT
                 - Phase per timestep in rad
                 - Time raster definition points
        """
        t, amplitude = self._rf
        t_zero_ref = t - t[0]
        if amplitude.m_as("uT").dtype in [np.complex64, np.complex128]:
            phase = np.angle(amplitude.m_as("uT"))
            phase = phase - self.phase_offset.m_as("rad")
            phase -= (t_zero_ref * 2 * np.pi * self.frequency_offset).m_as("rad")
            amplitude = amplitude.m_as("uT") * np.exp(-1j * phase)
        else:
            phase = np.zeros(amplitude.shape, dtype=np.float64)
            amplitude = amplitude.m_as("uT")

        peak_amp_plus, peak_amp_minus = np.max(amplitude), np.min(amplitude)
        absolute_max_idx = np.argmax([np.abs(peak_amp_plus), np.abs(peak_amp_minus)])
        peak_amp = (peak_amp_plus, peak_amp_minus)[absolute_max_idx]
        normed_amp = np.divide(amplitude, peak_amp, out=np.zeros_like(amplitude),
                               where=(peak_amp != 0))
        return np.real(normed_amp), Quantity(peak_amp, "uT"), phase, t_zero_ref


class SincRFPulse(RFPulse):
    """Defines a Sinc-RF pulse on a time grid with step length defined by system_specs. """
    # pylint: disable=R0913, R0914
    def __init__(self,
                 system_specs: SystemSpec,
                 flip_angle: Quantity = Quantity(np.pi, "rad"),
                 duration: Quantity = Quantity(1., "ms"),
                 time_bandwidth_product: float = 4,
                 center: float = 0.5,
                 delay: Quantity = Quantity(0., "ms"),
                 apodization: float = 0.,
                 frequency_offset: Quantity = Quantity(0., "Hz"),
                 phase_offset: Quantity = Quantity(0., "rad"),
                 name: str = "sinc_rf"):
        """ Defines a Sinc-RF pulse on a time grid with step length defined by system_specs.

        :param flip_angle: Quantity[Angle] Desired Flip angle of the Sinc Pulse. For negative
                            Values the flip-angle is stored as positive absolute plus a phase offset
                            of 180°
        :param duration: Quantity[Time] Total duration of the pulse
        :param time_bandwidth_product: float - Used to calculated the pulse-bandwidth. For a
                    Sinc-Pulse bw = time_bandwidth_product/duration corresponds to the
                    half central-lobe-width
        :param center: float [0, 1] factor to compute the pulse center relative to duration
        :param delay:
        :param apodization: float from interval [0, 1] used to calculate cosine-apodization window
        :param frequency_offset: Frequency offset in Hz in rotating frame ()
        :param phase_offset: Phase offset in rad.
        :param name:
        """

        if flip_angle < Quantity(0, "rad"):
            phase_offset += Quantity(np.pi, "rad")
            flip_angle = -flip_angle

        # For Sinc-Pulse this t*bw/duration corresponds to half central lobe width
        bandwidth = Quantity(time_bandwidth_product / duration.to("ms"), "1/ms")

        raster_time = system_specs.grad_raster_time.to("ms")
        n_steps = np.around(duration.m_as("ms") / raster_time.m_as("ms"))
        time_points = Quantity(np.arange(0., n_steps+1, 1) * raster_time.m_as("ms"), "ms")
        time_rel_center = time_points.to("ms") - center * duration.to("ms")

        window = 1 - apodization + apodization * np.cos(2 * np.pi *
                                                        time_rel_center / duration.to("ms"))
        unit_wf = window * np.sinc((bandwidth.to("1/ms") * time_rel_center).m_as("dimensionless"))
        unit_wf =  Quantity(unit_wf.m_as("dimensionless"), "mT")

        # relative_flip_angle = np.sum(amplitude) * raster_time.m_as("ms") * 2. * np.pi
        unit_flip_angle = np.sum((unit_wf[1:] + unit_wf[:-1]) / 2) * raster_time.to("ms")\
                          * system_specs.gamma_rad.to("rad/mT/ms")

        amplitude = unit_wf * flip_angle.to("rad") / unit_flip_angle

        self._rf = (time_points + delay, amplitude)
        self.rf_events = (center * duration + delay, flip_angle)

        super().__init__(system_specs=system_specs, name=name, frequency_offset=frequency_offset,
                         phase_offset=phase_offset, bandwidth=bandwidth, snap_to_raster=False)


class ArbitraryRFPulse(RFPulse):
    """ Wrapper for arbitrary rf shapes, to adhere to building block concept"""
    def __init__(self, system_specs: SystemSpec, name: str,
                 time_points: Quantity,
                 waveform: Quantity,
                 delay: Quantity = Quantity(0., "ms"),
                 bandwidth: Quantity = None,
                 frequency_offset: Quantity = Quantity(0., "Hz"),
                 phase_offset: Quantity = Quantity(0., "rad"),
                 snap_to_raster: bool = False):
        """ The gridding is assumed to be on raster time and **not** shifted by half
        a raster time. This shift (useful for simulations) can be incorporated when
        calling the gridding function of the sequence.

        waveform is assumed to start and end with values of 0 uT

        :param system_specs:
        :param name:
        :param time_points: Shape (#steps)
        :param waveform: Shape (#steps
        :param bandwidth:
        :param frequency_offset:
        :param phase_offset:
        :param snap_to_raster:
        """
        self._rf = (time_points.to("ms") + delay, waveform.to("mT"))
        if bandwidth is None:
            # TODO: estimate bandwidth of arbitrary rf pulses
            bandwidth = Quantity(0, "kHz")
        #TODO estimate phase offset and freqoffset from complex wf

        super().__init__(system_specs, name, frequency_offset=frequency_offset,
                         phase_offset=phase_offset, bandwidth=bandwidth,
                         snap_to_raster=snap_to_raster)


