"""State module for managing Cloud Key Management Service crypto keys."""
from copy import deepcopy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    crypto_key_version_id: str = None,
    project_id: str = None,
    location_id: str = None,
    key_ring_id: str = None,
    crypto_key_id: str = None,
    key_state: str = None,
    protection_level: str = None,
    algorithm: str = None,
    attestation: make_dataclass(
        "KeyOperationAttestation",
        [
            ("format", str, field(default=None)),
            ("content", str, field(default=None)),
            (
                "cert_chains",
                make_dataclass(
                    "CertificateChains",
                    [
                        ("cavium_certs", List[str], field(default=None)),
                        ("google_card_certs", List[str], field(default=None)),
                        ("google_partition_certs", List[str], field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    create_time: str = None,
    generate_time: str = None,
    destroy_time: str = None,
    destroy_event_time: str = None,
    import_job: str = None,
    import_time: str = None,
    import_failure_reason: str = None,
    external_protection_level_options: make_dataclass(
        "ExternalProtectionLevelOptions",
        [
            ("external_key_uri", str, field(default=None)),
            ("ekm_connection_key_path", str, field(default=None)),
        ],
    ) = None,
    reimport_eligible: bool = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Create a new `CryptoKey`_ within a `KeyRing`_.

    `CryptoKey.purpose`_ and `CryptoKey.version_template.algorithm`_ are required.

    Args:
        name(str):
            Idem name

        crypto_key_version_id(str, Optional):
            Output only. Set by the service.

        project_id(str, Optional):
            Project Id of the new crypto key version.

        location_id(str, Optional):
            Location Id of the new crypto key version .

        key_ring_id(str, Optional):
            Keyring Id of the new crypto key version.

        crypto_key_id(str, Optional):
            Cryptokey Id of the new crypto key version.

        resource_id(str, Optional): Idem resource id. Formatted as

            `projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}/cryptoKeyVersions/{crypto_key_version_id}`

    .. _CryptoKey: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKey
    .. _KeyRing: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings#KeyRing
    .. _CryptoKey.purpose: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKey.FIELDS.purpose
    .. _CryptoKey.version_template.algorithm: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKeyVersionTemplate.FIELDS.algorithm
    .. _Labeling Keys: https://cloud.google.com/kms/docs/labeling-keys
    .. _CryptoKeyVersions: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion
    .. _ProtectionLevel: https://cloud.google.com/kms/docs/reference/rest/v1/ProtectionLevel
    .. _ProtectionLevels: https://cloud.google.com/kms/docs/reference/rest/v1/ProtectionLevel

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

        crypto_key_test:
          gcp.cloudkms.crypto_key.present:
            - project_id: tango-gcp
            - location_id: us-east1
            - key_ring_id: idem-gcp-1
            - crypto_key_id: key-2

        crypto_key_version_test:
          gcp.cloudkms.crypto_key_version.present:
            - key_state: ENABLED
            - project_id: tango-gcp
            - location_id: us-east1
            - key_ring_id: idem-gcp-1
            - crypto_key_id: "${gcp.cloudkms.crypto_key:crypto_key_test:crypto_key_id}"

          # Update crypto key primary version with the one managed above
          gcp.cloudkms.crypto_key.present:
            - primary:
                name: "${gcp.cloudkms.crypto_key_version:crypto_key_version_test:resource_id}"
            - project_id: tango-gcp
            - location_id: us-east1
            - key_ring_id:  idem-gcp-1
            - crypto_key_id: "${gcp.cloudkms.crypto_key:crypto_key_test:crypto_key_id}"
    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    create_if_missing = False
    if not resource_id:
        if project_id and location_id and key_ring_id and crypto_key_id:
            if crypto_key_version_id:
                resource_id = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}/cryptoKeyVersions/{crypto_key_version_id}"
            else:
                create_if_missing = True
        else:
            result["result"] = False
            result["comment"].append(
                "When creating new resource crypto_key_version_id, project_id, location_id, key_ring_id and crypto_key_id parameters are required!"
            )
            return result
    else:
        els = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
            "cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions",
            resource_id,
        )
        if (
            project_id
            and location_id
            and key_ring_id
            and crypto_key_id
            and crypto_key_version_id
        ):
            if (
                els.get("project") != project_id
                or els.get("location") != location_id
                or els.get("keyring") != key_ring_id
                or els.get("cryptokey") != crypto_key_id
                or els.get("cryptokeyversions") != str(crypto_key_version_id)
            ):
                result["result"] = False
                result["comment"].append(
                    hub.tool.gcp.comment_utils.non_updatable_properties_comment(
                        "gcp.cloudkms.crypto_key",
                        resource_id,
                        {
                            "project_id",
                            "location_id",
                            "key_ring_id",
                            "crypto_key_id",
                            "crypto_key_version_id",
                        },
                    )
                )
                return result
        else:
            project_id = els.get("project")
            location_id = els.get("location")
            key_ring_id = els.get("keyring")
            crypto_key_id = els.get("cryptokey")
            crypto_key_version_id = els.get("cryptokeyversions")

    is_create = False
    if resource_id:
        old_get_ret = await hub.exec.gcp.cloudkms.crypto_key_version.get(
            ctx, resource_id=resource_id
        )
        if not old_get_ret["result"] or not old_get_ret["ret"]:
            if not create_if_missing:
                result["result"] = False
                result["comment"] += old_get_ret["comment"]
                return result
            is_create = True
        else:
            result["old_state"] = {
                "name": name,
                "project_id": project_id,
                "location_id": location_id,
                "key_ring_id": key_ring_id,
                "crypto_key_id": crypto_key_id,
                "crypto_key_version_id": crypto_key_version_id,
                **hub.tool.gcp.cloudkms.crypto_key_version_utils.to_state(
                    old_get_ret["ret"]
                ),
            }
    else:
        is_create = create_if_missing

    resource_body = {
        "state": key_state,
        "external_protection_level_options": external_protection_level_options,
    }
    resource_body = {k: v for (k, v) in resource_body.items() if v is not None}

    if ctx["test"]:
        if is_create:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    "gcp.cloudkms.crypto_key_version", resource_id
                )
            )
            result["new_state"] = {
                "resource_id": resource_id,
                "name": name,
                "project_id": project_id,
                "location_id": location_id,
                "key_ring_id": key_ring_id,
                "crypto_key_id": crypto_key_id,
                "crypto_key_version_id": crypto_key_version_id,
                **resource_body,
            }
        else:
            result["new_state"] = {
                **deepcopy(result["old_state"]),
                **{
                    "key_state" if k == "state" else k: v
                    for k, v in resource_body.items()
                },
            }
            update_mask = hub.tool.gcp.cloudkms.patch.calc_update_mask(
                resource_body,
                {
                    "state" if k == "key_state" else k: v
                    for k, v in result["old_state"].items()
                },
            )
            if update_mask:
                result["comment"].append(
                    hub.tool.gcp.comment_utils.would_update_comment(
                        "gcp.cloudkms.crypto_key_version", resource_id
                    )
                )
            else:
                result["comment"].append(
                    hub.tool.gcp.comment_utils.already_exists_comment(
                        "gcp.cloudkms.crypto_key_version", resource_id
                    )
                )
        return result

    if is_create:
        create_ret = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions.create(
            ctx,
            parent=f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}",
            body=resource_body,
        )
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] += create_ret["comment"]
            return result
        result["new_state"] = {
            "name": name,
            "project_id": project_id,
            "location_id": location_id,
            "key_ring_id": key_ring_id,
            "crypto_key_id": crypto_key_id,
            "crypto_key_version_id": crypto_key_version_id,
            **hub.tool.gcp.cloudkms.crypto_key_version_utils.to_state(
                create_ret["ret"]
            ),
        }
        result["comment"].append(
            hub.tool.gcp.comment_utils.create_comment(
                "gcp.cloudkms.crypto_key_version", result["new_state"]["resource_id"]
            )
        )
    else:
        update_mask = hub.tool.gcp.cloudkms.patch.calc_update_mask(
            resource_body,
            {
                "state" if k == "key_state" else k: v
                for k, v in result["old_state"].items()
            },
        )
        if (
            update_mask
            and result["old_state"].get("key_state") == "DESTROY_SCHEDULED"
            and key_state == "ENABLED"
        ):
            restore_ret = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions.restore(
                ctx, name_=resource_id
            )
            if not restore_ret["result"]:
                result["result"] = False
                result["comment"] += restore_ret["comment"]
                return result
        if update_mask:
            update_ret = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions.patch(
                ctx, name_=resource_id, updateMask=update_mask, body=resource_body
            )
            if not update_ret["result"]:
                result["result"] = False
                result["comment"] += update_ret["comment"]
                return result

            result["comment"].append(
                hub.tool.gcp.comment_utils.update_comment(
                    "gcp.cloudkms.crypto_key_version", resource_id
                )
            )
            result["new_state"] = {
                "name": name,
                "project_id": project_id,
                "location_id": location_id,
                "key_ring_id": key_ring_id,
                "crypto_key_id": crypto_key_id,
                "crypto_key_version_id": crypto_key_version_id,
                **hub.tool.gcp.cloudkms.crypto_key_version_utils.to_state(
                    update_ret["ret"]
                ),
            }
        else:
            result["comment"].append(
                hub.tool.gcp.comment_utils.already_exists_comment(
                    "gcp.cloudkms.crypto_key_version", resource_id
                )
            )
            result["new_state"] = deepcopy(result["old_state"])

    return result


async def absent(
    hub,
    ctx,
    name: str,
    crypto_key_version_id: str = None,
    project_id: str = None,
    location_id: str = None,
    key_ring_id: str = None,
    crypto_key_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Destroy crypto key version.

    After this operation the key material will no longer be stored. This version may only become `ENABLED` again if this
    version is `reimportEligible`_ and the original key material is reimported with a call to
    `KeyManagementService.ImportCryptoKeyVersion`_. Should provide either resource_id or all other *_id parameters.

    .. _KeyManagementService.ImportCryptoKeyVersion: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions/import#google.cloud.kms.v1.KeyManagementService.ImportCryptoKeyVersion
    .. _reimportEligible: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion.FIELDS.reimport_eligible

    Args:
        name(str):
            Idem name.

        crypto_key_version_id(str, Optional):
            Crypto key version name used to generate resource_id if it is not provided.

        project_id(str, Optional):
            Project Id of the new crypto key version.

        location_id(str, Optional):
            Location Id of the new crypto key version .

        key_ring_id(str, Optional):
            Keyring Id of the new crypto key version.

        crypto_key_id(str, Optional):
            Cryptokey Id of the new crypto key version.

        resource_id(str, Optional): Idem resource id. Formatted as

            `projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}/cryptoKeyVersions/{crypto_key_version_id}`
    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            {% set project_id = 'tango-gcp' %}
            {% set location_id = 'us-east1' %}
            {% set key_ring = 'key-ring' %}
            {% set crypto_key = 'crypto-key' %}
            {% set crypto_key_version = 'crypto-key-version' %}
            resource_is_absent:
              gcp.cloudkms.crypto_key_version.absent:
                - resource_id: projects/{{project_id}}/locations/{{location_id}}/keyRings/{{key_ring}}/cryptoKeys/{{crypto_key}}/cryptoKeyVersions/{{crypto_key_version}}
    """
    result = {
        "comment": [],
        "old_state": ctx.get("old_state"),
        "new_state": None,
        "name": name,
        "result": True,
    }

    if not resource_id:
        resource_id = (ctx.old_state or {}).get("resource_id")
        if (
            not resource_id
            and project_id
            and location_id
            and key_ring_id
            and crypto_key_id
            and crypto_key_version_id
        ):
            resource_id = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}/cryptoKeyVersions/{crypto_key_version_id}"
        else:
            result["result"] = False
            result["comment"] += ["Can not determine resource_id."]
            return result

    if ctx.test:
        result["comment"].append(
            hub.tool.gcp.comment_utils.would_delete_comment(
                "gcp.cloudkms.crypto_key_version", resource_id
            )
        )
        return result

    get_ret = await hub.exec.gcp.cloudkms.crypto_key_version.get(
        ctx, resource_id=resource_id
    )
    if not get_ret["result"]:
        result["comment"] += get_ret["comment"]
        return result
    elif not get_ret["ret"] or get_ret["ret"]["state"] in [
        "DESTROYED",
        "DESTROY_SCHEDULED",
    ]:
        result["comment"].append(
            hub.tool.gcp.comment_utils.already_absent_comment(
                "gcp.cloudkms.crypto_key_version", resource_id
            )
        )
        return result

    destroy_ret = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions.destroy(
        ctx, name_=resource_id
    )

    if destroy_ret["result"]:
        result["comment"].append(
            hub.tool.gcp.comment_utils.delete_comment(
                "gcp.cloudkms.crypto_key_version", resource_id
            )
        )
    else:
        result["comment"] += destroy_ret["comment"]
        result["result"] = False

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieve the list of available crypto key versions.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.cloudkms.crypto_key_version
    """
    result = {}

    locations = await hub.exec.gcp.cloudkms.location.list(
        ctx, project=ctx.acct.project_id
    )
    if not locations["result"]:
        hub.log.warning(
            f"Could not list gcp.cloudkms.location in {ctx.acct.project_id} {locations['comment']}"
        )
        return {}

    for location in locations["ret"]:
        key_rings = await hub.exec.gcp.cloudkms.key_ring.list(
            ctx, location=location["resource_id"]
        )
        if not key_rings["result"]:
            hub.log.warning(
                f"Could not list gcp.cloudkms.key_ring in {location['location_id']} {key_rings['comment']}"
            )
        else:
            for key_ring in key_rings["ret"]:
                crypto_keys = await hub.exec.gcp.cloudkms.crypto_key.list(
                    ctx, key_ring=key_ring["resource_id"]
                )
                if not crypto_keys["result"]:
                    hub.log.warning(
                        f"Could not describe gcp.cloudkms.crypto_key in {key_ring['resource_id']} {key_rings['comment']}"
                    )
                else:
                    for crypto_key in crypto_keys["ret"]:
                        crypto_key_versions = (
                            await hub.exec.gcp.cloudkms.crypto_key_version.list(
                                ctx, crypto_key=crypto_key["resource_id"]
                            )
                        )
                        if not crypto_keys["result"]:
                            hub.log.warning(
                                f"Could not describe gcp.cloudkms.crypto_key in {key_ring['resource_id']} {key_rings['comment']}"
                            )
                        else:
                            for crypto_key_version in crypto_key_versions["ret"]:
                                resource_id = crypto_key_version["resource_id"]
                                result[resource_id] = {
                                    "gcp.cloudkms.crypto_key_version.present": [
                                        {parameter_key: parameter_value}
                                        if parameter_key != "state"
                                        else {"key_state": parameter_value}
                                        for parameter_key, parameter_value in crypto_key_version.items()
                                    ]
                                }
                                els = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
                                    "cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions",
                                    resource_id,
                                )
                                p = result[resource_id][
                                    "gcp.cloudkms.crypto_key_version.present"
                                ]
                                p.append({"project_id": els["project"]})
                                p.append({"location_id": els["location"]})
                                p.append({"key_ring_id": els["keyring"]})
                                p.append({"crypto_key_id": els["cryptokey"]})
                                p.append(
                                    {"crypto_key_version_id": els["cryptokeyversions"]}
                                )

    return result
