"""Stems for organizing files based on their DSPS repeat number."""
from __future__ import annotations

import logging
from abc import ABC
from collections import defaultdict
from functools import cached_property
from typing import Type

from astropy.time import Time
from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.models.tags import StemName

from dkist_processing_vbi.models.constants import VbiBudName
from dkist_processing_vbi.parsers.vbi_l0_fits_access import VbiL0FitsAccess


class SingleMosaicTile:
    """
    An object that uniquely defines a (mosaic_step, exp_num, time_obs) tuple from any number of dsps repeats.

    This is just a fancy tuple.

    Basically, it just hashes the (mosaic_step, exp_num, time_obs) tuple so these objects can easily be compared.
    Also uses the time_obs property so that multiple DSPS repeats of the same (mosaic_step, modstate) can be sorted.

    This is just a fancy tuple.
    """

    def __init__(self, fits_obj: VbiL0FitsAccess):
        """Read mosaic step, exp_num, and obs time information from a FitsAccess object."""
        self.mosaic_step = fits_obj.current_spatial_step
        self.exposure_num = fits_obj.current_dsp_exp
        self.date_obs = Time(fits_obj.time_obs)

    def __repr__(self):
        return f"SingleMosaicTile with {self.mosaic_step = }, {self.exposure_num = }, and {self.date_obs = }"

    def __eq__(self, other: SingleMosaicTile) -> bool:
        """Two frames are equal if they have the same (mosaic_step, exp_num, date_obs) tuple."""
        if not isinstance(other, SingleMosaicTile):
            raise TypeError(f"Cannot compare SingleMosaicTile with type {type(other)}")

        for attr in ["mosaic_step", "exposure_num", "date_obs"]:
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True

    def __lt__(self, other: SingleMosaicTile) -> bool:
        """Only sort on date_obs."""
        return self.date_obs < other.date_obs

    def __hash__(self) -> int:
        # Not strictly necessary, but does allow for using set() on these objects
        return hash((self.mosaic_step, self.exposure_num, self.date_obs))


class VbiTotalDspsRepeatsBud(Stem, ABC):
    """Compute the total number of *complete* DSPS repeats.

    We can't use DKIST008 directly because it's possible that the last repeat has an aborted mosaic. Instead, we return
    the number of completed mosaics found.
    """

    # This only here so type-hinting of this complex dictionary will work.
    key_to_petal_dict: dict[str, SingleMosaicTile]

    def __init__(self):
        super().__init__(stem_name=BudName.num_dsps_repeats.value)

    @cached_property
    def mosaic_tile_dict(self) -> dict[int, dict[int, list[SingleMosaicTile]]]:
        """Nested dictionary that contains a SingleMosaicTile for each ingested frame.

        Dictionary structure is [mosaic_step (int), Dict[exp_num (int), List[SingleMosaicTile]]
        """
        scan_step_dict = defaultdict(lambda: defaultdict(list))
        for scan_step_obj in self.key_to_petal_dict.values():
            scan_step_dict[scan_step_obj.mosaic_step][scan_step_obj.exposure_num].append(
                scan_step_obj
            )

        return scan_step_dict

    def setter(self, fits_obj: VbiL0FitsAccess) -> SingleMosaicTile | Type[SpilledDirt]:
        """Ingest observe frames as SingleMosaicTile objects."""
        if fits_obj.ip_task_type != "observe":
            return SpilledDirt
        return SingleMosaicTile(fits_obj=fits_obj)

    def getter(self, key: str) -> int:
        """Compute the total number of DSPS repeats.

        The number of DSPS repeats for every mosaic step are calculated and if a mosaic is incomplete,
        it will not be included.
        Assumes the incomplete mosaic is always the last one due to summit abort or cancellation.
        """
        # HOW THIS WORKS
        ################
        # self.mosaic_tile_dict conceptually looks like this:
        # {mosaic_1:
        #    {exp_1: [file1, file2],
        #     exp_2: [file3, file4]},
        #  mosaic_2:
        #    {exp_1: [file5, file6],
        #     exp_2: [file7, file7]}}
        #
        # We assume that each file for a (mosaic_step, exp_num) tuple is a different DSPS repeat
        # (there are 2 repeats in the above example). So all we really need to do is find the lengths of all
        # of the lists at the "exp_N" level.

        # The k[0] assumes that a mosaic step has the same number of exposures for all DSPS repeats
        repeats_per_mosaic_tile = [
            k[0]
            # The following list is the number of files found for each mosaic location for each exp_num
            for k in [
                # exp_dict is a dict of {exp_num: list(SingleMosaicTile)}
                # so len(m) is the number of SingleMosaicTiles detected for each exp_num
                [len(m) for m in exp_dict.values()]
                for exp_dict in self.mosaic_tile_dict.values()
            ]
        ]
        logging.debug(f"{repeats_per_mosaic_tile = }")
        if min(repeats_per_mosaic_tile) + 1 < max(repeats_per_mosaic_tile):
            raise ValueError("More than one incomplete mosaic exists in the data.")
        return min(repeats_per_mosaic_tile)


class VbiDspsBase(Stem):
    """Base class for computing total number of DSPS repeats and individual DSPSNUMs."""

    def __init__(self, stem_name: str):
        super().__init__(stem_name=stem_name)
        self.metadata_key = "current_dsps_repeat"

        # Just to help pycharm get the type linting
        self.key_to_petal_dict: dict[str, int] = dict()

    @property
    def value_set(self) -> set[int]:
        """Return the unique set of discovered DSPSNUMS."""
        return set(self.key_to_petal_dict.values())

    def setter(self, fits_obj: VbiL0FitsAccess):
        """
        Set the current DSPS Repeat number.

        Parameters
        ----------
        fits_obj
            The input fits object
        Returns
        -------
        The current DSPS repeat number
        """
        if fits_obj.ip_task_type != "observe":
            return SpilledDirt

        return getattr(fits_obj, self.metadata_key)


class VbiDspsRepeatPedestalBud(VbiDspsBase):
    """The minimum DSPS repeat header value.

    This is needed because, while the pedestal is removed in `VbiDspsRepeatNumberFlower`, we still need to keep track
    of what it is so we can use it to correctly populate L1 headers. The DSPS-related header values are wrong, but they
    are wrong by a constant. This Bud is that constant.
    """

    def __init__(self):
        super().__init__(stem_name=VbiBudName.dsps_repeat_pedestal.value)

    def getter(self, key: str) -> int:
        """Find the minimum DSPS repeat number across all observe frames.

        We don't do any check for completeness here. That's done in `VbiDspsRepeatNumberFlower`.
        """
        return min(self.value_set) - 1


class VbiDspsRepeatNumberFlower(VbiDspsBase):
    """The current DSPS repeat.

    This is different than common's `DspsRepeatNumberFlower` because it turns out the DSPSREPS header key applies to
    *all* instrument programs executed during an OP. Fortunately, VBI seems to still have the individual DSPSNUM keys
    populated in sequence. The issue, though, is that VBI might not be the first instrument executed and there could
    thus be an offset between 1 and the start of the sequence of VBI DSPSNUMs. This Flower computes that offset so that
    the DSPSNUMs start at 1 as expected.
    """

    def __init__(self):
        super().__init__(stem_name=StemName.dsps_repeat.value)

    def getter(self, key: str) -> int:
        """
        Get the total current DSPSNUM and remove a potential offset.

        A check is also made that *all* DSPSNUMs form a set that makes sense.
        """
        value_set = self.value_set

        # The number of dsps repeats is the number of unique current_dsps values
        num_dsps_repeats = len(value_set)

        # The minimum value will be used to normalize all DSPSNUMs so the sequence starts at 1.
        min_dsps_num = min(value_set) - 1

        # Make sure all dsps nums are represented. I.e., a dsps num isn't missing. This would cause later failure in
        # science loops.
        sorted_dsps_nums = sorted(list(value_set))
        normalized_dsps_nums = [i - min_dsps_num for i in sorted_dsps_nums]

        if normalized_dsps_nums != list(range(1, num_dsps_repeats + 1)):
            raise ValueError(
                "Set of DSPS nums is not equal to the range of values expected from the number of DSPS nums found. "
                f"Expected range(1, {num_dsps_repeats + 1}), found {sorted_dsps_nums}."
            )

        return self.key_to_petal_dict[key] - min_dsps_num
