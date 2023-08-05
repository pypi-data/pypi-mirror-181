"""Utility functions for crypto key version resources."""
import copy
from typing import Any
from typing import Dict


def to_state(hub, state: Dict[str, Any]) -> Dict[str, Any]:
    """`state` is reserved in Idem and can be a parameter name in `present`.

    This method returns a copy of the original new/old state to get rid of NamespacedDict
    and replaces `state` with `key_state`. GCP `name` is translated to Idem `resource_id`.

    Args:
        state: new_state or old_state formatted variable

    Returns:
        Dict[str, Any]
    """
    result = copy.copy(state)
    if "state" in result:
        key_state = result["state"]
        del result["state"]
        result["key_state"] = key_state

    if "resource_id" in result:
        els = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
            "cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions",
            result["resource_id"],
        )
        result["crypto_key_version_id"] = els["cryptokeyversions"]
    return result
