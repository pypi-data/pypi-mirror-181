__all__ = ["balanced_ssfp"]

from typing import Tuple, List
from copy import deepcopy

import numpy as np
from pint import Quantity

import cmrseq


def balanced_ssfp(system_specs: cmrseq.SystemSpec,
                  matrix_size: np.ndarray,
                  inplane_resolution: Quantity,
                  slice_thickness: Quantity,
                  adc_duration: Quantity,
                  flip_angle: Quantity,
                  pulse_duration: Quantity,
                  slice_position_offset: Quantity = Quantity(0., "m"),
                  repetition_time: Quantity=None,
                  time_bandwidth_product: float = 4.,
                  dummy_shots: int = None) -> List[cmrseq.Sequence]:
    """ Defines a balanced steady state free precession sequence with a/2-TR/2 preparation.

    Signle TR defintition:

    .. code-block::

        .                 |                  TR                  |                 .
        .                     |       TE         |                                 .
        .                                                                          .
        .            RF:     /\                                                    .
        .            ADC   \/  \/      |||||||||||||||||||||                       .
        .                  ______                                                  .
        .            SS:  /      \    _______________________                      .
        .                         \__/                       \__/                  .
        .                              _____________________                       .
        .            RO:  ________    /                     \                      .
        .                         \__/                       \__/                  .
        .            PE:  ________    ______________________                       .
        .                         \__/                      \__/                   .


    :param system_specs: SystemSpecification
    :param matrix_size: array of shape (2, )
    :param inplane_resolution: Quantity[Length] of shape (2, )
    :param repetition_time: Quantity[Time] containing the required repetition_time
    :param slice_thickness: Quantity[Length] containing the required slice-thickness
    :param adc_duration: Quantity[time] Total duration of adc-sampling for a single TR
    :param flip_angle: Quantity[Angle] containing the required flip_angle
    :param pulse_duration: Quantity[Time] Total pulse duration (corresponds to flat_duration of the
                            slice selection gradient)
    :param slice_position_offset: Quantity[Length] positional offset in slice normal direction
                              defining the frequency offset of the RF pulse
    :param time_bandwidth_product: float - used to calculate the rf bandwidth from duration
    :param dummy_shots: number of shots(TRs) without adc-events before starting the acquisition
    :return: List of length (n_dummy+matrix_size[1]) containting one Sequence object per TR
    """
    rf_seq = cmrseq.seqdefs.excitation.slice_selective_sinc_pulse(
                                    system_specs=system_specs,
                                    slice_thickness=slice_thickness,
                                    flip_angle=flip_angle/2,
                                    pulse_duration=pulse_duration,
                                    time_bandwidth_product=time_bandwidth_product,
                                    slice_position_offset=slice_position_offset,
                                    slice_normal=np.array([0., 0., 1.]))
    ss_refocus = rf_seq.get_block("slice_select_rewind_0")

    # Recalculate ss-gradient combined with ro/pe prephasers
    k_max_inplane = 2 / inplane_resolution.m_as("m")
    kz_refocus = (ss_refocus.area * system_specs.gamma).m_as("1/m")
    total_kspace_traverse = Quantity(np.linalg.norm([*k_max_inplane, kz_refocus[-1]]), "1/m")
    combined_gradient_area = total_kspace_traverse / system_specs.gamma.to("1/mT/ms")
    prephaser_duration = cmrseq.bausteine.TrapezoidalGradient.from_area(
                            system_specs, np.array([1., 0., 0]), combined_gradient_area).duration
    rf_seq.remove_block("slice_select_rewind_0")

    rf_seq.append(cmrseq.bausteine.TrapezoidalGradient.from_dur_area(system_specs,
                                                                     np.array([0., 0., -1.]),
                                                                     prephaser_duration,
                                                                     ss_refocus.area[-1] / 2,
                                                                     name="slice_select_rewind"))
    ss_refocus = rf_seq.get_block("slice_select_rewind_0")

    # Construct the readout and phase encoding gradients
    ro_blocks = cmrseq.seqdefs.readout.multi_line_cartesian(
                                    system_specs=system_specs,
                                    fnc=cmrseq.seqdefs.readout.balanced_gre_cartesian_line,
                                    matrix_size=matrix_size,
                                    inplane_resolution=inplane_resolution,
                                    adc_duration=adc_duration,
                                    prephaser_duration=prephaser_duration,
                                    dummy_shots=dummy_shots)
    minimal_tr = ro_blocks[0].duration + rf_seq.duration - prephaser_duration
    # Adjust alternating phase offset for adc-events
    for ro_idx, ro_b in enumerate(ro_blocks):
        phase_offset = Quantity(np.mod(ro_idx, 2) * np.pi, "rad")
        adc_block = ro_b.get_block("adc_0")
        if adc_block is not None:
            adc_block.phase_offset = phase_offset

    # Check if repetition time is feasible in case it was specified
    if repetition_time is None:
        repetition_time = minimal_tr
        repetition_time = system_specs.time_to_raster(repetition_time)
    else:
        if repetition_time < minimal_tr:
            raise ValueError("Repetition time too short to be feasible")
        repetition_time = system_specs.time_to_raster(repetition_time)
        # If TR is longer than necessary, shift read-blocks to match TE=TR/2
        n_dummy = dummy_shots if dummy_shots is not None else 0
        shift = system_specs.time_to_raster(
                        (repetition_time - rf_seq.get_block("slice_select_0").duration) / 2
                        - ro_blocks[n_dummy].get_block("adc_0").adc_center, "grad")
        for ro_b in ro_blocks[n_dummy:]:
            ro_b.shift_in_time(shift)

    # Add delay to match TR/2 after the first exication
    rf_seq.append(cmrseq.bausteine.Delay(system_specs, repetition_time/2 - rf_seq.duration))

    # Create the slice selection compensation
    ss_compensate = deepcopy(ss_refocus)
    ss_compensate.shift_time(-ss_compensate.tmin + repetition_time - ss_refocus.duration)
    ss_compensate.name = "ss_compensate"

    # Assemble blocks to list of sequences each representing one TR
    seq_list = [rf_seq]
    for tr_idx, ro_b in enumerate(ro_blocks):
        flip_angle_phase = (-1) ** tr_idx * flip_angle
        rf_seq = cmrseq.seqdefs.excitation.slice_selective_sinc_pulse(
                                                    system_specs=system_specs,
                                                    slice_thickness=slice_thickness,
                                                    flip_angle=flip_angle_phase,
                                                    pulse_duration=pulse_duration,
                                                    slice_position_offset=slice_position_offset,
                                                    time_bandwidth_product=time_bandwidth_product,
                                                    slice_normal=np.array([0., 0., 1.]))
        rf_seq.remove_block("slice_select_rewind_0")
        rf_seq.append(cmrseq.bausteine.TrapezoidalGradient.from_dur_area(system_specs,
                                                                         np.array([0., 0., -1.]),
                                                                         prephaser_duration,
                                                                         ss_refocus.area[-1],
                                                                         name="slice_select_rewind"))
        compensated_rf = rf_seq + cmrseq.Sequence([ss_compensate, ], system_specs)
        ro_b.shift_in_time(rf_seq.duration - prephaser_duration)
        seq = compensated_rf + ro_b
        seq_list.append(seq)
    return seq_list
