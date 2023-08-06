""" This module contains the implementation of the base class of all building blocks used in
Sequences"""
__all__ = ["SequenceBaseBlock"]

import itertools
from copy import deepcopy
from typing import Tuple
from warnings import warn
from types import SimpleNamespace

import numpy as np
from pint import Quantity

from cmrseq.core._system import SystemSpec


# pylint: disable=C0103
class SequenceBaseBlock(SimpleNamespace):
    """ Base class for all building blocks. All general operations performed on all sequence
    blocks must be compatible with this class. When implementing new building blocks, inherit
    from this class """
    #
    name: str
    #: Tuple containing defining points of gradient waveforms as np.array (wrapped as Quantity)
    #: with shape (time: (t, ), waveform: (3, t)). Between points, linear interpolation is assumed
    gradients: Tuple[Quantity, Quantity] = None

    #: Tuple containing defining points of RF-waveforms as np.array (wrapped as Quantity)
    #: with shape (time: (t, ), waveform: (3, t)). Between points, linear interpolation is assumed
    _rf: Tuple[Quantity, Quantity] = None
    #: Tuple containing rf events (time, flip_angle)
    rf_events: Tuple[Quantity, Quantity] = None

    #: Quantity[ms] defining sampling event times
    adc_timing: Quantity = None
    #: Quantity[ms] Time defining the center of the adc-events
    adc_center: Quantity = None

    def __init__(self, system_specs: SystemSpec, name: str, snap_to_raster: bool = False):
        """ Must be called as last line of subclass.__init__"""
        super().__init__(name=name)
        self._clean_gradients()
        if snap_to_raster:
            self.snap_to_raster(system_specs)
        # self.validate(system_specs)

    def __deepcopy__(self, memodict={}) -> "SequenceBaseBlock":
        ret = SequenceBaseBlock(system_specs=None, name=self.name)
        ret.__class__ = self.__class__  # pylint: disable=W0201
        ret.__dict__.update(deepcopy(self.__dict__))
        return ret

    def scale_gradients(self, factor: float) -> None:
        """ Scales gradients by given factor if gradients are defined.

        :param factor: factor to globally scale the amplitude of gradient defintion.
        """
        if self.gradients is not None:
            t, grads = self.gradients
            self.gradients = (t, factor * grads)

    def rotate_gradients(self, rotation_matrix: np.ndarray) -> None:
        """ Rotates gradients to according to the gradient axes transformation:

        [[1 0 0][0 1 0][0 0 0]].T -> rotation matrix

        :raises: ValueError - if rotation_matrix contains non-orthogonal column-vectors

        :param rotation_matrix: (3, 3) rotation matrix containing the new column basis vectors
                                (meaning in [:, i], i indexes the new orientation of MPS).
                                Vectors are normalized along axis=0 to ensure same magnitude
        """
        colums_orthogonal = [np.dot(rotation_matrix[:, i], rotation_matrix[:, j]) == 0.
                             for i, j in itertools.product(range(3), range(3)) if i != j]
        if not all(colums_orthogonal):
            raise ValueError(f"Rotation matrix\n {rotation_matrix.T} \ncontains non-orthogonal "
                             f"column-vectors: \n combination:"
                             f"{[(i, j) for i, j in itertools.product(range(3), range(3)) if i != j]}"
                             f"\nis ortho: {colums_orthogonal}")

        if self.gradients is not None:
            t, wf = self.gradients
            vector_norms = np.linalg.norm(rotation_matrix, axis=0, keepdims=True)
            rotation_matrix = rotation_matrix / vector_norms
            wf_rot = np.einsum("it, ij -> jt", wf.m_as("mT/m"), rotation_matrix)
            self.gradients = (t, Quantity(wf_rot, "mT/m"))
        else:
            warn(f"Tried to rotate gradient in {self.name}, where no gradients are defined")

    def shift_time(self, time_shift: Quantity) -> None:
        """ Translates all rf/gradients/adc definitions in time.
        :param time_shift: Quantity[time] value to shift

        """
        time_shift = Quantity(time_shift.m_as("ms"), "ms")
        if self.gradients is not None:
            self.gradients = (self.gradients[0] + time_shift, self.gradients[1])
        if self._rf is not None:
            self._rf = (self._rf[0] + time_shift, self._rf[1])
        if self.rf_events is not None:
            self.rf_events = (self.rf_events[0] + time_shift, self.rf_events[1])
        if self.adc_timing is not None:
            self.adc_timing += time_shift
        if self.adc_center is not None:
            self.adc_center += time_shift

    def time_reverse(self, time_flip: Quantity) -> None:
        """Time reverses block by flipping about a given time point"""
        time_flip = Quantity(time_flip.m_as("ms"), "ms")
        if self.gradients is not None:
            self.gradients = (np.flip(time_flip - self.gradients[0], axis=0),
                              np.flip(self.gradients[1], axis=1))
        if self._rf is not None:
            self._rf = (np.flip(time_flip - self._rf[0], axis=0), np.flip(self._rf[1], axis=1))
        if self.rf_events is not None:
            self._rf = (np.flip(time_flip - self.rf_events[0], axis=0),
                        np.flip(self.rf_events[1], axis=0))
        if self.adc_timing is not None:
            self.adc_timing = np.flip(time_flip - self.adc_timing, axis=0)
        if self.adc_center is not None:
            self.adc_center = np.flip(time_flip - self.adc_center, axis=0)

    def _clean_gradients(self):
        """ If gradient definition contains duplicate consecutive points, the second one is
        removed"""
        if self.gradients is not None:
            deltat = np.diff(np.around(self.gradients[0].to("ms").m, decimals=6), axis=0)
            deltag = np.diff(np.around(self.gradients[1].to("mT/m").m, decimals=6), axis=1)
            duplicate_idx = np.where(np.logical_and(deltat == 0., np.all(deltag == 0., axis=0)))
            t, g = self.gradients
            cleaned_t = Quantity(np.delete(t.m_as("ms"), duplicate_idx), "ms")
            cleaned_g = Quantity(np.delete(g.m_as("mT/m"), duplicate_idx, axis=1), "mT/m")
            self.gradients = (cleaned_t, cleaned_g)

    def snap_to_raster(self, system_specs: SystemSpec):
        warn("When calling snap_to_raster the waveform points are simply rounded to their nearest"
             f"neighbour if the difference is below the relative tolerance. Therefore this in"
             f" not guaranteed to be precise anymore")
        if self.gradients is not None:
            time_ndt = np.around(self.gradients[0].m_as("ms") /
                                 system_specs.grad_raster_time.m_as("ms"), decimals=0)
            time_ndt = time_ndt * system_specs.grad_raster_time.to("ms")
            self.gradients = (time_ndt.to("ms"), self.gradients[1].to("mT/m"))
            self._clean_gradients()

        if self._rf is not None:
            t_rf = system_specs.time_to_raster(self._rf[0], "rf")
            self._rf = (t_rf.to("ms"), self.rf[1])

    def validate(self, system_specs: SystemSpec) -> None:
        """ Validates if any definition contained in this block, is in-compatible with given
        system specifications.

        :raises: ValueError if validation fails due to defined rules
        :param system_specs:
        """
        self._validate_gradients(system_specs)

    def _validate_gradients(self, system_specs: SystemSpec) -> None:
        """ Validates if the contained gradient_definition is valid for the given system-
        specifications.
        """
        if self.gradients is not None:
            max_grad_in_specs = np.all(np.abs(self.gradients[1].m_as("mT/m"))
                                       <= system_specs.max_grad.m_as("mT/m"))
            grad_slew = (np.diff(self.gradients[1].m_as("mT/m"), axis=1) /
                         np.diff(self.gradients[0].m_as("ms"), axis=0)[np.newaxis])
            grad_slew_in_specs = np.all(np.around(grad_slew, decimals=6)
                                        <= system_specs.max_slew.m_as("mT/m/ms"))
            tgridded = self.gradients[0].m_as("ms") / system_specs.grad_raster_time.m_as("ms")
            grad_on_grid = np.allclose(tgridded, np.around(tgridded), rtol=1e-6)
            if not all([max_grad_in_specs, grad_slew_in_specs, grad_on_grid]):
                raise ValueError(f"Gradient definition of {self.name} invalid:\n"
                                 f"\t- max grad: {max_grad_in_specs}\n"
                                 f"\t- max slew: {grad_slew_in_specs}\n"
                                 f"\t- definition on grid: {grad_on_grid}")

    def _validate_rf(self, system_specs: SystemSpec) -> None:
        """ Validates if the contained rf-definition is valid for the given system-
        specifications"""
        if self._rf is not None:
            float_steps = self._rf[0].m_as("ms") / system_specs.rf_raster_time.m_as("ms")
            n_steps = np.around(float_steps)
            ongrid = np.allclose(n_steps, float_steps, rtol=1e-6)
            if not all([ongrid]):
                raise ValueError(f"RF definition invalid:\n"
                                 f"\t - definition on grid: {ongrid}\n")

    def _validate_adc(self, system_specs: SystemSpec) -> None:
        return

    @property
    def duration(self) -> Quantity:
        return self.tmax - self.tmin

    @property
    def tmin(self) -> Quantity:
        """ Calculates the smallest time occuring in all contained definitions.

        :return: Quantity[time]
        """
        tmin = None
        for channel in (self.gradients, self._rf, self.adc_timing):
            if channel is not None:
                if isinstance(channel, tuple):
                    channel = channel[0]
                temp = np.min(channel.to("ms"))
                if tmin is None or tmin > temp:
                    tmin = temp
        return Quantity(tmin, "ms")

    @property
    def tmax(self) -> Quantity:
        """ Calculates the largest time occuring in all contained definitions.

        :return: Quantity[time]
        """
        tmax = None
        for channel in (self.gradients, self._rf, self.adc_timing):
            if channel is not None:
                if isinstance(channel, tuple):
                    channel = channel[0]
                temp = np.max(channel.to("ms"))
                if tmax is None or tmax < temp:
                    tmax = temp
        return Quantity(tmax, "ms")
