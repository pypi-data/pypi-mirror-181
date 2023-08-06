""" This module contains functions defining compositions of building blocks commonly used
for excitation in MRI """
__all__ = ["slice_selective_sinc_pulse", "slice_selective_se_pulses"]

import numpy as np
from pint import Quantity

import cmrseq


# pylint: disable=W1401, R0913, R0914
def slice_selective_sinc_pulse(system_specs: cmrseq.SystemSpec,
                               slice_thickness: Quantity,
                               flip_angle: Quantity,
                               pulse_duration: Quantity,
                               time_bandwidth_product: float = 4,
                               delay: Quantity = Quantity(0., "ms"),
                               slice_position_offset: Quantity = Quantity(0., "m"),
                               slice_normal: np.ndarray = np.array([0., 0., 1.]),
                               ) -> cmrseq.Sequence:
    """ Defines slice selective excitation using a Sinc-RF pulse and a slice selection gradient.

    .. code-block::

        .                     /\                           .
        .           ______/\ /  \ /\______                 .
        .                  \/   \/                         .
        .                                                  .
        .                __________                        .
        .           ____/          \       ___             .
        .                           \_____/                .
        .               |pulse-dur| |     |                .
        .                       shortest possible          .

    :param system_specs: SystemSpecifications
    :param slice_thickness: Quantity[Length] containing the required slice-thickness
    :param flip_angle: Quantity[Angle] containing the required flip_angle
    :param pulse_duration: Quantity[Time] Total pulse duration (corresponds to flat_duration of the
                            slice selection gradient)
    :param time_bandwidth_product: float - used to calculate the rf bandwidth from duration
    :param delay: Quantity[Time] added time-offset
    :param slice_position_offset: Quantity[Length] positional offset in slice normal direction
                                  defining the frequency offset of the RF pulse
    :param slice_normal: np.ndarray of shape (3, ) denoting the direction of the slice-normal.
    :return: cmrseq.Sequence
    """
    rf_bandwidth = time_bandwidth_product / pulse_duration.to("ms")
    amplitude = rf_bandwidth / slice_thickness / system_specs.gamma
    amplitude = amplitude.to("mT/m")

    frequency_offset = (system_specs.gamma.to("1/mT/ms") * slice_position_offset.to("m")
                        * amplitude.to("mT/m"))

    # Pulse is shifted by delay+rise-time after gradient definition
    rf_block = cmrseq.bausteine.SincRFPulse(system_specs=system_specs, flip_angle=flip_angle,
                                            duration=pulse_duration,
                                            time_bandwidth_product=time_bandwidth_product,
                                            frequency_offset=frequency_offset.to("Hz"),
                                            center=0.5, delay=Quantity(0, "ms"),
                                            apodization=0., name="rf_excitation")

    ssgrad = cmrseq.bausteine.TrapezoidalGradient.from_fdur_amp(system_specs=system_specs,
                                                                orientation=slice_normal,
                                                                amplitude=amplitude,
                                                                flat_duration=pulse_duration,
                                                                delay=delay,
                                                                name="slice_select")
    rf_block.shift_time(ssgrad.gradients[0][1])

    ssrefocus = cmrseq.bausteine.TrapezoidalGradient.from_area(
        system_specs=system_specs,
        orientation=-slice_normal,
        area=Quantity(np.abs(np.linalg.norm(ssgrad.area.m_as("mT/m*ms"), axis=-1) / 2), "mT/m*ms"),
        delay=ssgrad.gradients[0][-1],
        name="slice_select_rewind")
    seq = cmrseq.Sequence([rf_block, ssgrad, ssrefocus], system_specs=system_specs)
    return seq


def slice_selective_se_pulses(system_specs: 'cmrseq.SystemSpec',
                              echo_time: Quantity,
                              slice_thickness: Quantity,
                              pulse_duration: Quantity,
                              slice_orientation: np.ndarray,
                              time_bandwidth_product: float = 4.) -> cmrseq.Sequence:
    """ Define a pair of 90, 180 rf sinc pulses with slice selective gradients

    .. code-block::

                        |-----------echo_time/2---------|

       .                90°                            180°              .
       .                                                                 .
       .               /\                              /\                .
       .    _______/\ /  \ /\______________________/\ /  \ /\            .
       .            \/   \/                         \/   \/              .
       .                                                                 .
       .          ___________                      ___________           .
       .    ____ /           \       _____________/           \          .
       .                      \_____/                                    .
       .          |pulse-dur|                      |pulse-dur|           .


    :param system_specs: SystemSpecifications
    :param echo_time: Quantity[Time] containing the required echo-time
    :param slice_thickness: Quantity[Length] containing the required slice-thickness
    :param pulse_duration: Quantity[Time] Total pulse duration (corresponds to flat_duration of the
                            slice selection gradient)
    :param slice_orientation: np.ndarray of shape (3, ) denoting the direction of the slice-normal.
    :param time_bandwidth_product: float - used to calculate the rf bandwidth from duration
    :return:
    """
    excite = cmrseq.seqdefs.excitation.slice_selective_sinc_pulse(
        system_specs=system_specs,
        slice_thickness=slice_thickness,
        flip_angle=Quantity(np.pi / 2, "rad"),
        pulse_duration=pulse_duration,
        time_bandwidth_product=time_bandwidth_product,
        delay=Quantity(0., "ms"),
        slice_normal=slice_orientation)

    excitation_center_time = excite.rf_events[0][0]
    refocus_delay = excitation_center_time - pulse_duration / 2 + echo_time / 2
    refocus = cmrseq.bausteine.SincRFPulse(system_specs=system_specs,
                                           flip_angle=Quantity(np.pi, "rad"),
                                           duration=pulse_duration,
                                           time_bandwidth_product=time_bandwidth_product,
                                           center=0.5,
                                           delay=refocus_delay,
                                           name="rf_refocus")
    ss_grad = excite.get_block("slice_select_0")
    sliceselect_refocus = cmrseq.bausteine.TrapezoidalGradient(system_specs, slice_orientation,
                                                               ss_grad.amplitude, pulse_duration,
                                                               ss_grad.rise_time,
                                                               delay=refocus.tmin - ss_grad.rise_time,
                                                               name="slice_select_refocus")

    seq = excite + cmrseq.Sequence([refocus, sliceselect_refocus], system_specs=system_specs)
    return seq
