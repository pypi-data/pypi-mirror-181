""" This module contains parametric definitions of complete multi-TR GRE-based sequences"""
__all__ = ["flash"]

from warnings import warn
from typing import List

import numpy as np
from pint import Quantity

import cmrseq


# pylint: disable=R0913, R0914
def flash(system_specs: cmrseq.SystemSpec,
          matrix_size: np.ndarray,
          inplane_resolution: Quantity,
          slice_thickness: Quantity,
          adc_duration: Quantity,
          flip_angle: Quantity,
          pulse_duration: Quantity,
          repetition_time: Quantity,
          echo_time: Quantity,
          slice_position_offset: Quantity = Quantity(0., "m"),
          time_bandwidth_product: float = 4.,
          dummy_shots: int = 0,
          fuse_slice_rewind_and_prephaser: bool = True) -> List[cmrseq.Sequence]:
    """ Defines a 2D gradient echo sequence.

    :param system_specs: SystemSpecifications
    :param matrix_size: array of shape (2, ) containing the resulting matrix dimensions
    :param inplane_resolution: Quantity[Length] of shape (2, ) containing the in-plane
                                voxel dimensions
    :param slice_thickness: Quantity[Length] containing the required slice-thickness
    :param adc_duration: Quantity[time] Total duration of adc-sampling for a single TR
    :param repetition_time: Quantity[Time] containing the required repetition_time
    :param echo_time: Quantity[Time] containing the required echo-time. If too short for
                    given system specifications, it is increased to minimum and a warning is raised.
    :param flip_angle: Quantity[Angle] containing the required flip_angle
    :param pulse_duration: Quantity[Time] Total pulse duration (corresponds to flat_duration of the
                            slice selection gradient)
    :param slice_position_offset: Quantity[Length] positional offset in slice normal direction
                                  defining the frequency offset of the RF pulse
    :param time_bandwidth_product: float - used to calculate the rf bandwidth from duration
    :param dummy_shots: number of dummy shots (TRs) without adc-events, with k-space center
                        phase encoding
    :param fuse_slice_rewind_and_prephaser: If True, the slice selection rewinder is recalculated
                to match the duration of the prephaser, resulting in the fastest possible 3D k-space
                traverse.
    :return: List of sequence objects, that each represent a single TR
    """
    rf_seq = cmrseq.seqdefs.excitation.slice_selective_sinc_pulse(
        system_specs=system_specs,
        slice_thickness=slice_thickness,
        flip_angle=flip_angle,
        pulse_duration=pulse_duration,
        time_bandwidth_product=time_bandwidth_product,
        slice_position_offset=slice_position_offset,
        slice_normal=np.array([0., 0., 1.]))
    ss_refocus = rf_seq.get_block("slice_select_rewind_0")

    if fuse_slice_rewind_and_prephaser:
        # Recalculate ss-gradient combined with ro/pe prephasers
        k_max_inplane = 2 / inplane_resolution.m_as("m")
        kz_refocus = (ss_refocus.area * system_specs.gamma).m_as("1/m")
        total_kspace_traverse = Quantity(np.linalg.norm([*k_max_inplane, kz_refocus[-1]]), "1/m")
        combined_gradient_area = total_kspace_traverse / system_specs.gamma.to("1/mT/ms")
        prephaser_duration = cmrseq.bausteine.TrapezoidalGradient.from_area(
            system_specs, np.array([1., 0., 0]), combined_gradient_area).duration

        rf_seq.remove_block("slice_select_rewind_0")
        ss_refocus = cmrseq.bausteine.TrapezoidalGradient.from_dur_area(system_specs,
                                                                        np.array([0., 0., -1.]),
                                                                        prephaser_duration,
                                                                        ss_refocus.area[-1],
                                                                        delay=rf_seq.duration,
                                                                        name="slice_select_rewind")
        rf_seq.add_block(ss_refocus)
    else:
        prephaser_duration = None

    ro_blocks = cmrseq.seqdefs.readout.multi_line_cartesian(
        system_specs=system_specs,
        fnc=cmrseq.seqdefs.readout.gre_cartesian_line,
        matrix_size=matrix_size,
        inplane_resolution=inplane_resolution,
        adc_duration=adc_duration,
        prephaser_duration=prephaser_duration,
        dummy_shots=dummy_shots)

    if prephaser_duration is None:
        prephaser_duration = ro_blocks[0].get_block("ro_prephaser_0").duration

    readout_gradient_duration = ro_blocks[dummy_shots].get_block("trapezoidal_readout_0").duration
    max_ssref_prephaser = max(ss_refocus.duration, prephaser_duration)
    adc_center = system_specs.time_to_raster(ro_blocks[dummy_shots].get_block('adc_0').adc_center)

    minimal_tr = readout_gradient_duration + max_ssref_prephaser + rf_seq.duration - ss_refocus.duration
    minimal_te = (rf_seq.duration - rf_seq.get_block("rf_excitation_0").rf_events[
        0] - ss_refocus.duration +
                  max_ssref_prephaser + adc_center - prephaser_duration)

    repetition_time = system_specs.time_to_raster(repetition_time)
    if repetition_time < minimal_tr:
        warn(f"Repetition time too short to be feasible, set TR to {minimal_tr}")
        repetition_time = minimal_tr

    maximum_te = repetition_time - (readout_gradient_duration - adc_center + prephaser_duration) \
                 - rf_seq.get_block("rf_excitation_0").rf_events[0]

    echo_time = system_specs.time_to_raster(echo_time)
    if echo_time < minimal_te:
        warn(f"Echo time too short to be feasible, set TE to {minimal_te}")
        echo_time = minimal_te

    if echo_time > maximum_te:
        warn(f"Echo time too long for given TR, set TE to {maximum_te}")
        echo_time = maximum_te

    te_shift = echo_time - minimal_te
    tr_delay = repetition_time - minimal_tr - te_shift

    # Concatenate readout blocks
    seq_list = []
    for ro_b in ro_blocks:
        ro_b.shift_in_time(
            rf_seq.duration - min(ss_refocus.duration, prephaser_duration) + te_shift)
        seq = rf_seq + ro_b
        seq.append(cmrseq.bausteine.Delay(system_specs, tr_delay))
        seq_list.append(seq)
    return seq_list
