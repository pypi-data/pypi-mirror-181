"""Exec module for managing Cloud Key Management Service crypto key versions."""
from typing import Any
from typing import Dict


__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    resource_id: str,
):
    """Returns a crypto key version by its Idem resource ID.

    Args:
        resource_id(str):
            Idem resource ID. ``projects/{project id}/locations/{location id}/keyRings/{keyRing}/cryptoKeys/{cryptoKey}/cryptoKeyVersions/{cryptoKeyVersion}``

    Returns:
        CryptoKeyVersion resource

    Examples:
        .. code-block:: sls

            {% set project_id = 'project-name' %}
            {% set location_id = 'us-east1' %}
            {% set key_ring = 'key-ring' %}
            {% set crypto_key = 'crypto-key' %}
            {% set crypto_key_version = 'crypto-key-version' %}
            get-key-ring:
                exec.run:
                    - path: gcp.cloudkms.crypto_key_version.get
                    - kwargs:
                        resource_id: projects/{{project_id}}/locations/{{location_id}}/keyRings/{{key_ring}}/cryptoKeys/{{crypto_key}}/cryptoKeyVersions/{{crypto_key_version}}
    """
    result = {
        "comment": [],
        "ret": [],
        "result": True,
    }

    crypto_key = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions.get(
        ctx, _name=resource_id
    )

    if not crypto_key["result"]:
        result["comment"] += crypto_key["comment"]
        result["result"] = False
        return result

    result["ret"] = crypto_key["ret"]

    if not result["ret"]:
        result["comment"] += (
            hub.tool.gcp.comment_utils.get_empty_comment(
                "gcp.cloudkms.crypto_key_version", resource_id
            ),
        )

    return result


async def list_(
    hub, ctx, crypto_key: str, filter: str = None, order_by: str = None
) -> Dict[str, Any]:
    r"""Retrieves the crypto key versions in a crypto key.

    Args:
        crypto_key(str):
            key ring resource_id.

        filter(str, Optional):
            Only include resources that match the filter in the response. For more information, see
            `Sorting and filtering list results`_.

        order_by(str, Optional):
            Specify how the results should be sorted. If not specified, the results will be sorted in the default order.
            For more information, see `Sorting and filtering list results`_.

    .. _Sorting and filtering list results: https://cloud.google.com/kms/docs/sorting-and-filtering

    Examples:
        .. code-block:: sls

            list-crypto-keys-filtered:
                exec.run:
                   - path: gcp.cloudkms.crypto_key_version.list
                   - kwargs:
                         crypto_key: projects/project-name/locations/global/keyRings/kr-global-test
                         filter: algorithm = GOOGLE_SYMMETRIC_ENCRYPTION
    """
    result = {
        "comment": [],
        "ret": [],
        "result": True,
    }

    crypto_key_versions = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions.list(
        ctx, parent=crypto_key, filter=filter, orderBy=order_by
    )
    if not crypto_key_versions["result"]:
        result["comment"] += crypto_key_versions["comment"]
        result["result"] = False
        return result

    if crypto_key_versions["ret"].get("items"):
        result["ret"].extend(crypto_key_versions["ret"]["items"])

    if not result["ret"]:
        result["comment"] += (
            hub.tool.gcp.comment_utils.list_empty_comment(
                "gcp.cloudkms.crypto_key_version", crypto_key
            ),
        )

    return result
