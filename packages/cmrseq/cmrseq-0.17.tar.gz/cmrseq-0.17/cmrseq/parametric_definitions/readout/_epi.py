""" This modules contains compositions of building blocks commonly used for in defining actual
signal acqusition and spatial encoding
"""
__all__ = ["epi_cartesian"]

from copy import deepcopy

from pint import Quantity
import numpy as np

import cmrseq


def _docstring_parameter(*sub):
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj
    return dec


# pylint: disable=W1401, R0913, R0914
def _epi_from_kspace_def(system_specs: cmrseq.SystemSpec,
                         num_samples: int,
                         k_readout: Quantity,
                         k_phase_start: Quantity,
                         k_phase_step: Quantity,
                         k_phase_lines: int,
                         adc_duration: Quantity,
                         delay: Quantity = Quantity(0., "ms"),
                         prephaser_duration: Quantity = None) -> cmrseq.Sequence:
    """**Dispatch - kSpace**:

    Dispatch function for `epi_cartesian` that uses the k-space extend define the EPI trajectory.

    **NOTE:** If the number of samples `num_samples` is even, the k-space center is found at `num_samples/2+1`.

    :param system_specs: SystemSpecification
    :param num_samples: Number of samples acquired during frequency encoding
    :param k_readout: Quantity[1/Length] :math:`FOV_{kx}` corresponds to :math:`1/\Delta x`
    :param k_phase_start: Quantity[1/Length] :math:`k_y` position for the first k-space line
    :param k_phase_step: Quantity[1/Length] :math:`\Delta k_y` step per blip
    :param k_phase_lines: Number of lines
    :param adc_duration: Quantity[time] Duration of adc-sampling for a single RO-line
    :param delay:
    :param prephaser_duration: Optional - if not specified the shortest possible duration for the
                                RO/PE prephaser is calculates
    :return: Sequence object containing RO- & PE-gradients as well as ADC events
    """
    adc_duration = system_specs.time_to_raster(adc_duration, raster="grad")
    ro_amp = (k_readout / adc_duration / system_specs.gamma).to("mT/m")

    # Determine blip times
    a = system_specs.max_slew ** 2  # pylint: disable=C0103
    b = - ro_amp ** 2  # pylint: disable=C0103
    c = - (k_phase_step / system_specs.gamma) ** 2  # pylint: disable=C0103

    # only keep positive root
    blip_rise = (-b + np.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    blip_rise = np.sqrt(blip_rise)

    blip_rise = system_specs.time_to_raster(blip_rise, raster="grad")
    blip_amplitude = k_phase_step / system_specs.gamma / blip_rise

    if blip_amplitude > system_specs.max_grad:
        blip_amplitude = system_specs.max_grad
        blip_rise = np.sqrt(ro_amp ** 2 + blip_amplitude ** 2) / system_specs.max_slew
        blip_rise = system_specs.time_to_raster(blip_rise, raster="grad")

        blip_flat_time = k_phase_step / system_specs.max_grad / system_specs.gamma - blip_rise
        blip_flat_time = system_specs.time_to_raster(blip_flat_time, raster="grad")
        if blip_flat_time < 0:
            blip_flat_time = Quantity(0., "ms")

        blip_amplitude = k_phase_step / (blip_flat_time + blip_rise) / system_specs.gamma

    else:
        blip_flat_time = Quantity(0., "ms")

    # now we know the slew time for the traverse gradient
    readout_pulse = cmrseq.bausteine.TrapezoidalGradient(
        system_specs=system_specs,
        orientation=np.array([1., 0., 0.]),
        flat_duration=adc_duration,
        rise_time=blip_rise,
        amplitude=ro_amp, delay=Quantity(0., "ms"),
        name='readout_pulse')

    # And we can calculate the traverse gradient
    prephaser_ro_area = readout_pulse.area[0] / 2.
    prephaser_pe_area = np.abs(k_phase_start / system_specs.gamma)

    # if num_samples % 2:
    #     prephaser_pe_area = np.abs(k_phase_start / system_specs.gamma) #* ((num_samples + 1) / num_samples)
    # else:
    #     prephaser_pe_area = np.abs(k_phase_start / system_specs.gamma)

    # Total gradient traverse is a combination of ro and pe directions.
    # Need to solve as single gradient to ensure slew and strength restrictions are met
    combined_kspace_traverse = np.sqrt((prephaser_ro_area * system_specs.gamma) ** 2
                                       + k_phase_start ** 2)
    [fastest_prep_amp, fastest_prep_ramp, fastest_prep_flatdur] = \
        system_specs.get_shortest_gradient(combined_kspace_traverse / system_specs.gamma)

    # If prephaser duration was not specified use the fastest posible prephaser
    if prephaser_duration is None:
        prephaser_duration = fastest_prep_flatdur + 2 * fastest_prep_ramp
    else:
        # Check if duration is sufficient for _combined_ prephaser gradients
        if prephaser_duration < fastest_prep_flatdur + 2 * fastest_prep_ramp:
            raise ValueError("Prephaser duration is to short to for combined PE+RO "
                             "k-space traverse.")

    pe_direction = np.array([0., 1., 0.]) * np.sign(k_phase_start)
    pe_prep_pulse = cmrseq.bausteine.TrapezoidalGradient.from_dur_area(
        system_specs=system_specs,
        orientation=pe_direction,
        duration=prephaser_duration,
        area=prephaser_pe_area,
        delay=delay,
        name="pe_prephaser")

    ro_prep_pulse = cmrseq.bausteine.TrapezoidalGradient.from_dur_area(
        system_specs=system_specs,
        orientation=np.array([-1., 0., 0.]),
        duration=prephaser_duration,
        area=prephaser_ro_area,
        delay=delay,
        name="ro_prephaser")

    seq = cmrseq.Sequence([ro_prep_pulse, pe_prep_pulse],
                          system_specs=system_specs)

    blip_pulse = cmrseq.bausteine.TrapezoidalGradient(
        system_specs=system_specs,
        orientation=np.array([0., -1., 0.]),
        flat_duration=blip_flat_time,
        rise_time=blip_rise,
        amplitude=blip_amplitude,
        name="blip")

    ro_duration = readout_pulse.duration

    for line in range(k_phase_lines):
        ro_shift = prephaser_duration + delay + (ro_duration + blip_flat_time) * line

        blip_shift = prephaser_duration + delay + (adc_duration + blip_rise) \
                     + (ro_duration + blip_flat_time) * line
        if not(num_samples % 2) and line % 2:
            adc_shift = ro_shift + blip_rise + adc_duration / num_samples
        else:
            adc_shift = ro_shift + blip_rise

        # Copy readout pulse, adjust amplitude and time shift according to k-space line
        readout_pulse_new = deepcopy(readout_pulse)
        readout_pulse_new.scale_gradients((-1) ** line)
        readout_pulse_new.shift_time(ro_shift)

        # Copy blip, adjust time shift according to k-space line
        blip_pulse_new = deepcopy(blip_pulse)
        blip_pulse_new.shift_time(blip_shift)

        adc = cmrseq.bausteine.SymmetricADC(system_specs=system_specs, num_samples=num_samples,
                                            duration=adc_duration,
                                            delay=adc_shift)
        if not(line == k_phase_lines-1):
            seqline = cmrseq.Sequence([readout_pulse_new, blip_pulse_new, adc], system_specs=system_specs)
        else:
            seqline = cmrseq.Sequence([readout_pulse_new, adc], system_specs=system_specs)
        seq += seqline

    return seq


def _epi_from_fov_def(system_specs: cmrseq.SystemSpec,
                      field_of_view: Quantity,
                      matrix_size: np.ndarray,
                      adc_duration: Quantity,
                      blip_direction: str = "up",
                      partial_fourier_lines: int = 0) -> cmrseq.Sequence:
    """**Dispatch - FOV**:

    Dispatch function for `epi_cartesian` that uses the spatial extend of the fov to define the
    EPI trajectory.

    For even number of phase encoding lines, k-max is only reached by the last line, where as for
    odd numbers -k-max and k-max is reached. This is necessary to guarantee the k-space center to
    be acquired in all cases.

    :raises: - ValueError if partial_fourier_lines > matrix_size[1]//2-1 to avoid too high
                    partial fourier factors

    :param system_specs: cmrseq.SystemSpeecs
    :param field_of_view: Quantity[Length] - Defines the spatial extend in readout and
                            phase-encoding direction
    :param matrix_size: np.ndarray (2, ) - number of samples in readout/phase-encoding direction
                        if partial fourier is enabled the lines are subtracted from this parameter
    :param adc_duration: Quantity[Time] Duration per readout, corresponds to flat duration
    :param blip_direction: (str) from ['up', 'down'] specifies the direction of phase encoding steps
    :param partial_fourier_lines: (int) number of lines to be skipped before k-space center
    :return: Sequence object
    """
    n_pe_lines = matrix_size[1]
    n_pe_center_index = np.floor((matrix_size[1] - 1)/ 2)
    print(n_pe_center_index)
    if n_pe_center_index - 1 < partial_fourier_lines:
        raise ValueError("Partial fourier factor too high. k-space centre won't be sampled")

    effective_kpe_lines = n_pe_lines - partial_fourier_lines
    resolution = Quantity(field_of_view.m_as("m") / matrix_size, "m")
    kmax = 1 / (2 * resolution)

    # definition for blip up:
    n_steps_to_kmax = n_pe_lines - n_pe_center_index
    kpe_step = kmax[1] / n_steps_to_kmax
    start_phase = -kpe_step * (n_pe_center_index - partial_fourier_lines)

    # definition for blip down:
    if blip_direction.lower() == "down":
        start_phase *= -1
        kpe_step *= -1

    seq = _epi_from_kspace_def(system_specs=system_specs, num_samples=matrix_size[0],
                               k_readout=1/resolution[0], k_phase_start=start_phase,
                               k_phase_step=-kpe_step, k_phase_lines=effective_kpe_lines,
                               adc_duration=adc_duration)
    return seq


@_docstring_parameter(_epi_from_kspace_def.__doc__, _epi_from_fov_def.__doc__)
def epi_cartesian(system_specs: cmrseq.SystemSpec, *args, **kwargs) -> cmrseq.Sequence:
    """  Defines an EPI readout-train. Dispatches to implementation depending on the
    input arguments.

    :raises: ValueError if signature is not found. Signature matching is based on keyword arguments,
                so consider using keyword arguments only.

    .. code-block:: python

        .                                                                     .
        .           ADC:     |||  |||  |||  |||  |||  |||                     .
        .                         ___       ___       ___                     .
        .           RO:          /   \     /   \     /   \                    .
        .                   \___/     \___/     \___/     \___/               .
        .                                                                     .
        .           PE:          ____/\___/\___/\___/\___/\_______            .
        .                   \___/                                             .
        .                                  |  |                               .
        .                                adc_duration                         .


    {0}

    {1}

    """
    if any((k in kwargs.keys() for k in ['k_readout', 'k_phase_start',
                                         'k_phase_step', 'k_phase_lines'])):
        return _epi_from_kspace_def(system_specs, *args, **kwargs)
    elif (k in kwargs.keys() for k in ['field_of_view', 'matrix_size', 'blip_direction',
                                       'partial_fourier_lines']):
        return _epi_from_fov_def(system_specs, *args, **kwargs)
    else:
        raise ValueError("Dispatched function signature for `epi_cartesian` not recognized."
                         "If you specified only positional arguments consider specifying the "
                         "input as keyword arguments")
