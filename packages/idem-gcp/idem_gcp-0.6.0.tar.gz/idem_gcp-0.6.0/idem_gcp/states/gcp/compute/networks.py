"""State module for managing Networks."""
import copy
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
    resource_id: str = None,
    request_id: str = None,
    project: str = None,
    auto_create_subnetworks: bool = None,
    description: str = None,
    enable_ula_internal_ipv6: bool = None,
    internal_ipv6_range: str = None,
    i_pv4_range: str = None,
    mtu: int = None,
    network_firewall_policy_enforcement_order: str = None,
    routing_config: make_dataclass(
        "NetworkRoutingConfig",
        [
            ("routing_mode", str, field(default=None)),
        ],
    ) = None,
    peerings: List[
        make_dataclass(
            "NetworkPeering",
            [
                ("export_custom_routes", bool, field(default=None)),
                ("auto_create_routes", bool, field(default=None)),
                ("network", str, field(default=None)),
                ("name", str, field(default=None)),
                ("state", str, field(default=None)),
                ("peer_mtu", int, field(default=None)),
                ("import_subnet_routes_with_public_ip", bool, field(default=None)),
                ("import_custom_routes", bool, field(default=None)),
                ("state_details", str, field(default=None)),
                ("export_subnet_routes_with_public_ip", bool, field(default=None)),
                ("exchange_subnet_routes", bool, field(default=None)),
                ("stack_type", str, field(default=None)),
            ],
        )
    ] = None,
) -> Dict[str, Any]:
    r"""Creates a network in the specified project using the data included in the request.

    Args:
        name(str):
            An Idem name of the resource.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

        project(str):
            Project ID for this request.

        routing_config(NetworkRoutingConfig, Optional):
            The network-level routing configuration for this network. Used by Cloud Router to determine what type of network-wide routing behavior to enforce. Defaults to None.

        description(str, Optional):
            An optional description of this resource. Provide this field when you create the resource. Defaults to None.

        auto_create_subnetworks(bool, Optional):
            Must be set to create a VPC network. If not set, a legacy network is created. When set to true, the VPC network is created in auto mode. When set to false, the VPC network is created in custom mode. An auto mode VPC network starts with one subnet per region. Each subnet has a predetermined range as described in Auto mode VPC network IP ranges. For custom mode VPC networks, you can add subnets using the subnetworks insert method. Defaults to None.

        internal_ipv6_range(str, Optional):
            When enabling ula internal ipv6, caller optionally can specify the /48 range they want from the google defined ULA prefix fd20::/20. The input must be a valid /48 ULA IPv6 address and must be within the fd20::/20. Operation will fail if the speficied /48 is already in used by another resource. If the field is not speficied, then a /48 range will be randomly allocated from fd20::/20 and returned via this field. . Defaults to None.

        network_firewall_policy_enforcement_order(str, Optional):
            The network firewall policy enforcement order. Can be either AFTER_CLASSIC_FIREWALL or BEFORE_CLASSIC_FIREWALL. Defaults to AFTER_CLASSIC_FIREWALL if the field is not specified. Defaults to None.

        enable_ula_internal_ipv6(bool, Optional):
            Enable ULA internal ipv6 on this network. Enabling this feature will assign a /48 from google defined ULA prefix fd20::/20. . Defaults to None.

        i_pv4_range(str, Optional):
            Deprecated in favor of subnet mode networks. The range of internal addresses that are legal on this network. This range is a CIDR specification, for example: 192.168.0.0/16. Provided by the client when the network is created. Defaults to None.

        mtu(int, Optional):
            Maximum Transmission Unit in bytes. The minimum value for this field is 1300 and the maximum value is 8896. The suggested value is 1500, which is the default MTU used on the Internet, or 8896 if you want to use Jumbo frames. If unspecified, the value defaults to 1460. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        peerings(List[Dict[str, Any]], Optional): [Output Only] A list of network peerings for the resource. Defaults to None.
            * export_custom_routes(bool, Optional):
                Whether to export the custom routes to peer network. The default value is false.
            * auto_create_routes(bool, Optional):
                This field will be deprecated soon. Use the exchange_subnet_routes field instead. Indicates whether full mesh connectivity is created and managed automatically between peered networks. Currently this field should always be true since Google Compute Engine will automatically create and manage subnetwork routes between two networks when peering state is ACTIVE.
            * network(str, Optional):
                The URL of the peer network. It can be either full URL or partial URL. The peer network may belong to a different project. If the partial URL does not contain project, it is assumed that the peer network is in the same project as the current network.
            * name(str, Optional):
                Name of this peering. Provided by the client when the peering is created. The name must comply with RFC1035. Specifically, the name must be 1-63 characters long and match regular expression `[a-z]([-a-z0-9]*[a-z0-9])?`. The first character must be a lowercase letter, and all the following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
            * state(str, Optional):
                [Output Only] State for the peering, either `ACTIVE` or `INACTIVE`. The peering is `ACTIVE` when there's a matching configuration in the peer network.
                Enum type. Allowed values:
                "ACTIVE" - Matching configuration exists on the peer.
                "INACTIVE" - There is no matching configuration on the peer, including the case when peer does not exist.
            * peer_mtu(int, Optional):
                Maximum Transmission Unit in bytes.
            * import_subnet_routes_with_public_ip(bool, Optional):
                Whether subnet routes with public IP range are imported. The default value is false. IPv4 special-use ranges are always imported from peers and are not controlled by this field.
            * import_custom_routes(bool, Optional):
                Whether to import the custom routes from peer network. The default value is false.
            * state_details(str, Optional):
                [Output Only] Details about the current state of the peering.
            * export_subnet_routes_with_public_ip(bool, Optional):
                Whether subnet routes with public IP range are exported. The default value is true, all subnet routes are exported. IPv4 special-use ranges are always exported to peers and are not controlled by this field.
            * exchange_subnet_routes(bool, Optional):
                Indicates whether full mesh connectivity is created and managed automatically between peered networks. Currently this field should always be true since Google Compute Engine will automatically create and manage subnetwork routes between two networks when peering state is ACTIVE.
            * stack_type(str, Optional):
                Which IP version(s) of traffic and routes are allowed to be imported or exported between peer networks. The default value is IPV4_ONLY.
                Enum type. Allowed values:
                "IPV4_IPV6" - This Peering will allow IPv4 traffic and routes to be exchanged. Additionally if the matching peering is IPV4_IPV6, IPv6 traffic and routes will be exchanged as well.
                "IPV4_ONLY" - This Peering will only allow IPv4 traffic and routes to be exchanged, even if the matching peering is IPV4_IPV6.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            example_resource_name:
              gcp.compute.networks.present:
                - project: project-name
                - auto_create_subnetworks: false
    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    # Get the resource_id from ESM
    if not resource_id:
        resource_id = (ctx.get("old_state") or {}).get(
            "resource_id"
        ) or hub.tool.gcp.resource_prop_utils.construct_resource_id(
            "compute.networks", {**locals(), "network": name}
        )

    old = None

    if ctx.get("rerun_data"):
        handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
            ctx, ctx.get("rerun_data"), "compute.networks"
        )

        if not handle_operation_ret["result"]:
            result["result"] = False
            result["comment"] += handle_operation_ret["comment"]
            result["rerun_data"] = handle_operation_ret["rerun_data"]
            return result

        resource_id = handle_operation_ret["resource_id"]

    if resource_id:
        old_get_ret = await hub.exec.gcp_api.client.compute.networks.get(
            ctx, name=name, resource_id=resource_id
        )

        if not old_get_ret["result"]:
            # error other than non-existing resource
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        if old_get_ret["ret"]:
            # resource already exists

            # copy.copy(old_get_ret['ret']) is needed to convert any objects of type NamespaceDict to dict
            # in old_get_ret['ret']. This is done so that comparisons with the plan_state which has
            # objects of type dict works properly
            old = copy.deepcopy(copy.copy(old_get_ret["ret"]))
            result["old_state"] = old

        # do not return here even after fetching network post operation return,
        # as there are further update operations below which might need to run

    request_body = {
        "name": name,
        "description": description,
        "auto_create_subnetworks": auto_create_subnetworks,
        "enable_ula_internal_ipv6": enable_ula_internal_ipv6,
        "internal_ipv6_range": internal_ipv6_range,
        "i_pv4_range": i_pv4_range,
        "mtu": mtu,
        "network_firewall_policy_enforcement_order": network_firewall_policy_enforcement_order,
        "routing_config": routing_config,
        "peerings": peerings,
    }

    # TODO: How to handle query params which are not returned in the response body of get
    plan_state = {
        # "project": project,
        # "predefined_acl": predefined_acl,
        # "predefined_default_object_acl": predefined_default_object_acl,
        "resource_id": resource_id,
        **request_body,
    }

    plan_state = {k: v for (k, v) in plan_state.items() if v is not None}
    operation = None
    if old:
        changes = hub.tool.gcp.utils.compare_states(old, plan_state, "compute.networks")

        if not changes:
            result["result"] = True
            result["comment"].append(
                hub.tool.gcp.comment_utils.already_exists_comment(
                    "gcp.compute.networks", name
                )
            )
            result["new_state"] = result["old_state"]

            return result

    else:
        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    "gcp.compute.network", name
                )
            )
            result["new_state"] = plan_state
            return result

        # Create
        create_ret = await hub.exec.gcp_api.client.compute.networks.insert(
            ctx, name=name, project=project, body=request_body
        )
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] += create_ret["comment"]
            return result

        result["old_state"] = {}
        resource_id = create_ret["ret"].get("resource_id")
        if "compute#operation" in create_ret["ret"].get("kind"):
            operation = create_ret["ret"]

    if operation:
        operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
            operation.get("selfLink"), "compute.global_operations"
        )
        handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
            ctx, operation_id, "compute.networks"
        )

        if not handle_operation_ret["result"]:
            result["result"] = False
            result["comment"] += handle_operation_ret["comment"]
            result["rerun_data"] = handle_operation_ret["rerun_data"]
            return result

        resource_id = handle_operation_ret["resource_id"]

    # Try getting the resource again
    # TODO: Reconciliation or waiter loop?
    # TODO: Check if this can be removed because insert and update may also return the necessary data on success
    get_ret = await hub.exec.gcp_api.client.compute.networks.get(
        ctx, name=name, resource_id=resource_id
    )

    if not get_ret["result"] and not get_ret["ret"]:
        result["result"] = False
        result["comment"] += get_ret["comment"]
        return result

    result["new_state"] = get_ret["ret"]

    # Deal with network peerings
    old_peerings = result["new_state"].get("peerings", [])
    new_peerings = peerings if peerings is not None else old_peerings

    peerings_map = {peering.get("name"): peering for peering in old_peerings}
    peerings_to_add = []
    peerings_to_update = []

    for peering in new_peerings:
        if peering.get("name") not in peerings_map:
            peerings_to_add.append(peering)
        else:
            element = peerings_map.pop(peering.get("name"))
            needs_update: bool = (
                element.get("exchange_subnet_routes")
                != peering.get("exchange_subnet_routes")
                or element.get("export_custom_routes")
                != peering.get("export_custom_routes")
                or element.get("export_subnet_routes_with_public_ip")
                != peering.get("export_subnet_routes_with_public_ip")
                or element.get("import_custom_routes")
                != peering.get("import_custom_routes")
                or element.get("import_subnet_routes_with_public_ip")
                != peering.get("import_subnet_routes_with_public_ip")
                or element.get("name") != peering.get("name")
                or element.get("network") != peering.get("network")
                or element.get("peer_mtu") != peering.get("peer_mtu")
                or element.get("stack_type") != peering.get("stack_type")
            )

            if needs_update:
                peerings_to_update.append(peering)

    for peering in peerings_map.values():
        remove_peering_request_body = {"name": peering.get("name")}

        remove_ret = await hub.exec.gcp_api.client.compute.networks.removePeering(
            ctx, resource_id=resource_id, body=remove_peering_request_body
        )

        if not remove_ret["result"] and not remove_ret["ret"]:
            result["result"] = False
            result["comment"] += remove_ret["comment"]
            return result

        if "compute#operation" in remove_ret["ret"].get("kind"):
            operation = remove_ret["ret"]

            operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                operation.get("selfLink"), "compute.global_operations"
            )
            handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
                ctx, operation_id, "compute.networks", True
            )

            if not handle_operation_ret["result"]:
                result["result"] = False
                result["comment"] += handle_operation_ret["comment"]
                result["rerun_data"] = handle_operation_ret["rerun_data"]
                return result

            resource_id = handle_operation_ret["resource_id"]

    for peering in peerings_to_update:
        update_peering_request_body = {
            "network_peering": {
                "exchange_subnet_routes": peering.get("exchange_subnet_routes"),
                "export_custom_routes": peering.get("export_custom_routes"),
                "export_subnet_routes_with_public_ip": peering.get(
                    "export_subnet_routes_with_public_ip"
                ),
                "import_custom_routes": peering.get("import_custom_routes"),
                "import_subnet_routes_with_public_ip": peering.get(
                    "import_subnet_routes_with_public_ip"
                ),
                "name": peering.get("name"),
                "network": peering.get("network"),
                "peer_mtu": peering.get("peer_mtu"),
                "stack_type": peering.get("stack_type"),
            }
        }

        update_ret = await hub.exec.gcp_api.client.compute.networks.updatePeering(
            ctx, resource_id=resource_id, body=update_peering_request_body
        )

        if not update_ret["result"] and not update_ret["ret"]:
            result["result"] = False
            result["comment"] += update_ret["comment"]
            return result

        if "compute#operation" in update_ret["ret"].get("kind"):
            operation = update_ret["ret"]

            operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                operation.get("selfLink"), "compute.global_operations"
            )
            handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
                ctx, operation_id, "compute.networks", True
            )

            if not handle_operation_ret["result"]:
                result["result"] = False
                result["comment"] += handle_operation_ret["comment"]
                result["rerun_data"] = handle_operation_ret["rerun_data"]
                return result

            resource_id = handle_operation_ret["resource_id"]

    for peering in peerings_to_add:
        add_peering_request_body = {
            "network_peering": {
                "exchange_subnet_routes": peering.get("exchange_subnet_routes"),
                "export_custom_routes": peering.get("export_custom_routes"),
                "export_subnet_routes_with_public_ip": peering.get(
                    "export_subnet_routes_with_public_ip"
                ),
                "import_custom_routes": peering.get("import_custom_routes"),
                "import_subnet_routes_with_public_ip": peering.get(
                    "import_subnet_routes_with_public_ip"
                ),
                "name": peering.get("name"),
                "network": peering.get("network"),
                "peer_mtu": peering.get("peer_mtu"),
                "stack_type": peering.get("stack_type"),
            }
        }

        add_ret = await hub.exec.gcp_api.client.compute.networks.addPeering(
            ctx, resource_id=resource_id, body=add_peering_request_body
        )

        if not add_ret["result"] and not add_ret["ret"]:
            result["result"] = False
            result["comment"] += add_ret["comment"]
            return result

        if "compute#operation" in add_ret["ret"].get("kind"):
            operation = add_ret["ret"]

            operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                operation.get("selfLink"), "compute.global_operations"
            )
            handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
                ctx, operation_id, "compute.networks", True
            )

            if not handle_operation_ret["result"]:
                result["result"] = False
                result["comment"] += handle_operation_ret["comment"]
                result["rerun_data"] = handle_operation_ret["rerun_data"]
                return result

            resource_id = handle_operation_ret["resource_id"]

    peerings_changed = (
        len(peerings_to_add) > 0 or len(peerings_to_update) > 0 or len(peerings_map) > 0
    )

    if peerings_changed:
        get_ret = await hub.exec.gcp_api.client.compute.networks.get(
            ctx, name=name, resource_id=resource_id
        )

        if not get_ret["result"] and not get_ret["ret"]:
            result["result"] = False
            result["comment"] += get_ret["comment"]
            return result

        result["new_state"] = get_ret["ret"]

    return result


async def absent(
    hub,
    ctx,
    name: str = None,
    resource_id: str = None,
    request_id: str = None,
) -> Dict[str, Any]:
    r"""Deletes the specified network.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            my-network:
              gcp.compute.networks.absent:
                - resource_id: projects/project-name/global/networks/my-network

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

    if ctx.test:
        result["comment"].append(
            hub.tool.gcp.comment_utils.would_delete_comment(
                "gcp.compute.networks", name
            )
        )
        return result

    if not ctx.get("rerun_data"):
        # First iteration; invoke instance's delete()
        delete_ret = await hub.exec.gcp_api.client.compute.networks.delete(
            ctx, resource_id=resource_id
        )
        if delete_ret["ret"]:
            if "compute#operation" in delete_ret["ret"].get("kind"):
                result["result"] = False
                result["comment"] += delete_ret["comment"]
                result[
                    "rerun_data"
                ] = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                    delete_ret["ret"].get("selfLink"), "compute.global_operations"
                )
                return result

    else:
        # delete() has been called on some previous iteration
        handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
            ctx, ctx.get("rerun_data"), "compute.networks"
        )
        if not handle_operation_ret["result"]:
            result["result"] = False
            result["comment"] += handle_operation_ret["comment"]
            result["rerun_data"] = handle_operation_ret["rerun_data"]
            return result

        resource_id = handle_operation_ret["resource_id"]

    if not resource_id:
        result["comment"].append(
            hub.tool.gcp.comment_utils.already_absent_comment(
                "gcp.compute.networks", name
            )
        )

    result["comment"].append(
        hub.tool.gcp.comment_utils.delete_comment("gcp.compute.networks", name)
    )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves the list of networks available to the specified project.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.compute.networks

    """
    result = {}

    # TODO: Pagination
    describe_ret = await hub.exec.gcp_api.client.compute.networks.list(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(
            f"Could not describe gcp.compute.networks {describe_ret['comment']}"
        )
        return {}

    for resource in describe_ret["ret"]["items"]:
        resource_id = resource.get("resource_id")

        result[resource_id] = {
            "gcp.compute.networks.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result
