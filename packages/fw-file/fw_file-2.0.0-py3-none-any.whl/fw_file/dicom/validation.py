"""Functions to handle validation of DICOMs."""
import logging
import typing as t
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dicom_validator.spec_reader.edition_reader import EditionReader
from dicom_validator.validator.iod_validator import IODValidator
from pydicom.dataset import Dataset

from .config import get_config

if t.TYPE_CHECKING:  # pragma: no cover
    from . import DICOM

log = logging.getLogger(__name__)


@dataclass
class Standard:
    """DICOM Standard representation."""

    iod_info: dict
    mod_info: dict
    dict_info: dict


# Just cache the result, will be the same every time.
@lru_cache(maxsize=1)
def get_standard() -> Standard:
    """Get the dicom standard.

    Returns:
        dicom standard representation.
    """
    config = get_config()
    standard_path = config.standard
    standard_path.mkdir(parents=True, exist_ok=True)
    edition_reader = EditionReader(standard_path)
    destination = edition_reader.get_revision("current")
    json_path = Path(destination) / "json"
    dict_info = EditionReader.load_dict_info(json_path)
    iod_info = EditionReader.load_iod_info(json_path)
    mod_info = EditionReader.load_module_info(json_path)
    return Standard(iod_info, mod_info, dict_info)


def validate_dicom(
    standard: Standard, dcm: t.Union["DICOM", Dataset], log_level: int = logging.INFO
):
    """Validate a given dicom.

    Args:
        standard: Dicom standard representation
        dcm: DICOM or Dataset object
        log_level: Log level. Defaults to logging.INFO.

    Returns:
        Errors from dicom validation.
    """
    # Allow both DICOM and pydicom.Dataset to be passed in
    if hasattr(dcm, "dataset"):
        ds = dcm.dataset.raw
    else:
        ds = dcm
    validator = IODValidator(
        ds,
        standard.iod_info,
        standard.mod_info,
        standard.dict_info,
        log_level,
    )
    return validator.validate()


def get_tag_dict(
    standard: Standard, dcm: t.Union["DICOM", Dataset]
) -> t.Dict[int, bool]:
    """Get dictionary of tags and whether their value can be removed.

    Args:
        standard: Dicom standard
        dcm: Input dicom

    Returns:
        Output tag dict, keys are tag ints, value is True if
            tags value can be removed, False otherwise.
            If output is None, tag_dict could not be generated
    """
    # pylint: disable=protected-access,too-many-locals,too-many-branches
    tag_dict: t.Dict[int, bool] = {}
    validator = IODValidator(
        t.cast(Dataset, dcm),
        standard.iod_info,
        standard.mod_info,
        standard.dict_info,
        log_level=logging.WARNING,
    )
    sop_class_uid = validator._dataset.get("SOPClassUID")
    curr_iod_info = validator._iod_info.get(sop_class_uid)
    if not curr_iod_info:
        log.warning(f"Could not find IOD info for SOPClassUID: {sop_class_uid}")
        return tag_dict
    for name, module in curr_iod_info["modules"].items():
        # Modules can be mandatory or optional, or conditionally mandatory.
        # Here we don't care if they are mandatory or optional, we just want to
        # add its tags to the dictionary if it is present in the dataset.
        module_info = validator._get_module_info(module["ref"])
        usage = module["use"]
        condition = module.get("cond")
        if usage == "M":
            required = True
        elif usage == "U":
            required = False
        else:
            required, _ = validator._object_is_required_or_allowed(condition)
        present = validator._has_module(module_info)
        # Skip module if not required and not present
        if not required and not present:
            log.debug(f"Skipping module {name} as it was not found in dataset.")
            continue
        for tag_id_str, attribute in module_info.items():
            tag_id = validator._tag_id(tag_id_str)
            # Not adding any tags at PixelData or higher.
            if tag_id >= 0x7FE00010:
                continue
            attribute_type = attribute["type"]
            value_required = attribute_type in ("1", "1C")
            condition_dict = None
            if attribute_type in ("1", "2"):
                tag_required = True
            elif attribute_type in ("1C", "2C"):
                if "cond" in attribute:
                    condition_dict = attribute["cond"]
                    tag_required, _ = validator._object_is_required_or_allowed(
                        condition_dict
                    )
                else:  # pragma: no cover
                    tag_required = False
            else:
                tag_required = False
            # The tag dict only records whether or not a _value_ can be removed
            # since we never remove tags from the dataset in the fixers.  So we
            # want this to be True if the value is not required, but _only_ if
            # the tag itself is also required
            tag_dict[tag_id] = not (value_required and tag_required)
    return tag_dict
    # pylint: enable=protected-access,too-many-locals,too-many-branches


def get_required_tags(standard: Standard, dcm: t.Union["DICOM", Dataset]) -> t.Set[int]:
    """Get a list of required tags.

    Args:
        standard: Dicom standard
        dcm: Input dicom

    Returns:
        List of required tags or None.
    """
    tag_dict = get_tag_dict(standard, dcm)
    if not tag_dict:
        return set()
    return {tag for tag, res in tag_dict.items() if not res}
