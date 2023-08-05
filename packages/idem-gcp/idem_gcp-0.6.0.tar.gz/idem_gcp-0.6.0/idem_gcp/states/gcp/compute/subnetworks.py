"""State module for managing subnetworks."""
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
    project: str,
    region: str,
    request_id: str = None,
    enable_flow_logs: bool = None,
    private_ip_google_access: bool = None,
    kind: str = None,
    description: str = None,
    network: str = None,
    stack_type: str = None,
    external_ipv6_prefix: str = None,
    self_link: str = None,
    log_config: make_dataclass(
        "SubnetworkLogConfig",
        [
            ("aggregation_interval", str, field(default=None)),
            ("filter_expr", str, field(default=None)),
            ("enable", bool, field(default=None)),
            ("flow_sampling", float, field(default=None)),
            ("metadata_fields", List[str], field(default=None)),
            ("metadata", str, field(default=None)),
        ],
    ) = None,
    role: str = None,
    ipv6_cidr_range: str = None,
    creation_timestamp: str = None,
    gateway_address: str = None,
    id_: str = None,
    state: str = None,
    ipv6_access_type: str = None,
    fingerprint: str = None,
    internal_ipv6_prefix: str = None,
    secondary_ip_ranges: List[
        make_dataclass(
            "SubnetworkSecondaryRange",
            [
                ("ip_cidr_range", str, field(default=None)),
                ("range_name", str, field(default=None)),
            ],
        )
    ] = None,
    purpose: str = None,
    private_ipv6_google_access: str = None,
    ip_cidr_range: str = None,
    drain_timeout_seconds: int = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Creates a subnetwork in the specified project using the data included in the request.

    Args:
        name(str): An Idem name of the resource.
        project(str): Project ID for this request.
        region(str): Name of the region scoping this request.
        request_id(str, optional): An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.
        enable_flow_logs(bool, optional): Whether to enable flow logging for this subnetwork. If this field is not explicitly set, it will not appear in get listings. If not set the default behavior is determined by the org policy, if there is no org policy specified, then it will default to disabled. This field isn't supported with the purpose field set to INTERNAL_HTTPS_LOAD_BALANCER. Defaults to None.
        private_ip_google_access(bool, optional): Whether the VMs in this subnet can access Google services without assigned external IP addresses. This field can be both set at resource creation time and updated using setPrivateIpGoogleAccess. Defaults to None.
        kind(str, optional): [Output Only] Type of the resource. Always compute#subnetwork for Subnetwork resources. Defaults to None.
        description(str, optional): An optional description of this resource. Provide this property when you create the resource. This field can be set only at resource creation time. Defaults to None.
        network(str, optional): The URL of the network to which this subnetwork belongs, provided by the client when initially creating the subnetwork. This field can be set only at resource creation time. Defaults to None.
        stack_type(str, optional): The stack type for the subnet. If set to IPV4_ONLY, new VMs in the subnet are assigned IPv4 addresses only. If set to IPV4_IPV6, new VMs in the subnet can be assigned both IPv4 and IPv6 addresses. If not specified, IPV4_ONLY is used. This field can be both set at resource creation time and updated using patch.
            Enum type. Allowed values:
            "IPV4_IPV6" - New VMs in this subnet can have both IPv4 and IPv6 addresses.
            "IPV4_ONLY" - New VMs in this subnet will only be assigned IPv4 addresses. Defaults to None.
        external_ipv6_prefix(str, optional): The external IPv6 address range that is owned by this subnetwork. Defaults to None.
        self_link(str, optional): [Output Only] Server-defined URL for the resource. Defaults to None.
        log_config(Dict[str, Any], optional): This field denotes the VPC flow logging options for this subnetwork. If logging is enabled, logs are exported to Cloud Logging.
            SubnetworkLogConfig: The available logging options for this subnetwork. Defaults to None.
            * aggregation_interval (str, optional): Can only be specified if VPC flow logging for this subnetwork is enabled. Toggles the aggregation interval for collecting flow logs. Increasing the interval time will reduce the amount of generated flow logs for long lasting connections. Default is an interval of 5 seconds per connection.
                Enum type. Allowed values:
                "INTERVAL_10_MIN"
                "INTERVAL_15_MIN"
                "INTERVAL_1_MIN"
                "INTERVAL_30_SEC"
                "INTERVAL_5_MIN"
                "INTERVAL_5_SEC"
            * filter_expr (str, optional): Can only be specified if VPC flow logs for this subnetwork is enabled. The filter expression is used to define which VPC flow logs should be exported to Cloud Logging.
            * enable (bool, optional): Whether to enable flow logging for this subnetwork. If this field is not explicitly set, it will not appear in get listings. If not set the default behavior is determined by the org policy, if there is no org policy specified, then it will default to disabled.
            * flow_sampling (float, optional): Can only be specified if VPC flow logging for this subnetwork is enabled. The value of the field must be in [0, 1]. Set the sampling rate of VPC flow logs within the subnetwork where 1.0 means all collected logs are reported and 0.0 means no logs are reported. Default is 0.5 unless otherwise specified by the org policy, which means half of all collected logs are reported.
            * metadata_fields (List[str], optional): Can only be specified if VPC flow logs for this subnetwork is enabled and "metadata" was set to CUSTOM_METADATA.
            * metadata (str, optional): Can only be specified if VPC flow logs for this subnetwork is enabled. Configures whether all, none or a subset of metadata fields should be added to the reported VPC flow logs. Default is EXCLUDE_ALL_METADATA.
                Enum type. Allowed values:
                "CUSTOM_METADATA"
                "EXCLUDE_ALL_METADATA"
                "INCLUDE_ALL_METADATA"
        role(str, optional): The role of subnetwork. Currently, this field is only used when purpose = INTERNAL_HTTPS_LOAD_BALANCER. The value can be set to ACTIVE or BACKUP. An ACTIVE subnetwork is one that is currently being used for Internal HTTP(S) Load Balancing. A BACKUP subnetwork is one that is ready to be promoted to ACTIVE or is currently draining. This field can be updated with a patch request.
            Enum type. Allowed values:
            "ACTIVE" - The ACTIVE subnet that is currently used.
            "BACKUP" - The BACKUP subnet that could be promoted to ACTIVE. Defaults to None.
        ipv6_cidr_range(str, optional): [Output Only] This field is for internal use. Defaults to None.
        creation_timestamp(str, optional): [Output Only] Creation timestamp in RFC3339 text format. Defaults to None.
        gateway_address(str, optional): [Output Only] The gateway address for default routes to reach destination addresses outside this subnetwork. Defaults to None.
        id_(str, optional): [Output Only] The unique identifier for the resource. This identifier is defined by the server. Defaults to None.
        state(str, optional): [Output Only] The state of the subnetwork, which can be one of the following values: READY: Subnetwork is created and ready to use DRAINING: only applicable to subnetworks that have the purpose set to INTERNAL_HTTPS_LOAD_BALANCER and indicates that connections to the load balancer are being drained. A subnetwork that is draining cannot be used or modified until it reaches a status of READY
            Enum type. Allowed values:
            "DRAINING" - Subnetwork is being drained.
            "READY" - Subnetwork is ready for use. Defaults to None.
        ipv6_access_type(str, optional): The access type of IPv6 address this subnet holds. It's immutable and can only be specified during creation or the first time the subnet is updated into IPV4_IPV6 dual stack.
            Enum type. Allowed values:
            "EXTERNAL" - VMs on this subnet will be assigned IPv6 addresses that are accessible via the Internet, as well as the VPC network.
            "INTERNAL" - VMs on this subnet will be assigned IPv6 addresses that are only accessible over the VPC network. Defaults to None.
        fingerprint(str, optional): Fingerprint of this resource. A hash of the contents stored in this object. This field is used in optimistic locking. This field will be ignored when inserting a Subnetwork. An up-to-date fingerprint must be provided in order to update the Subnetwork, otherwise the request will fail with error 412 conditionNotMet. To see the latest fingerprint, make a get() request to retrieve a Subnetwork. Defaults to None.
        internal_ipv6_prefix(str, optional): [Output Only] The internal IPv6 address range that is assigned to this subnetwork. Defaults to None.
        secondary_ip_ranges(List[Dict[str, Any]], optional): An array of configurations for secondary IP ranges for VM instances contained in this subnetwork. The primary IP of such VM must belong to the primary ipCidrRange of the subnetwork. The alias IPs may belong to either primary or secondary ranges. This field can be updated with a patch request. Defaults to None.
            * ip_cidr_range (str, optional): The range of IP addresses belonging to this subnetwork secondary range. Provide this property when you create the subnetwork. Ranges must be unique and non-overlapping with all primary and secondary IP ranges within a network. Only IPv4 is supported. The range can be any range listed in the Valid ranges list.
            * range_name (str, optional): The name associated with this subnetwork secondary range, used when adding an alias IP range to a VM instance. The name must be 1-63 characters long, and comply with RFC1035. The name must be unique within the subnetwork.
        purpose(str, optional): The purpose of the resource. This field can be either PRIVATE_RFC_1918 or INTERNAL_HTTPS_LOAD_BALANCER. A subnetwork with purpose set to INTERNAL_HTTPS_LOAD_BALANCER is a user-created subnetwork that is reserved for Internal HTTP(S) Load Balancing. If unspecified, the purpose defaults to PRIVATE_RFC_1918. The enableFlowLogs field isn't supported with the purpose field set to INTERNAL_HTTPS_LOAD_BALANCER.
            Enum type. Allowed values:
            "INTERNAL_HTTPS_LOAD_BALANCER" - Subnet reserved for Internal HTTP(S) Load Balancing.
            "PRIVATE" - Regular user created or automatically created subnet.
            "PRIVATE_RFC_1918" - Regular user created or automatically created subnet.
            "PRIVATE_SERVICE_CONNECT" - Subnetworks created for Private Service Connect in the producer network.
            "REGIONAL_MANAGED_PROXY" - Subnetwork used for Regional Internal/External HTTP(S) Load Balancing. Defaults to None.
        private_ipv6_google_access(str, optional): This field is for internal use. This field can be both set at resource creation time and updated using patch.
            Enum type. Allowed values:
            "DISABLE_GOOGLE_ACCESS" - Disable private IPv6 access to/from Google services.
            "ENABLE_BIDIRECTIONAL_ACCESS_TO_GOOGLE" - Bidirectional private IPv6 access to/from Google services.
            "ENABLE_OUTBOUND_VM_ACCESS_TO_GOOGLE" - Outbound private IPv6 access from VMs in this subnet to Google services. Defaults to None.
        ip_cidr_range(str, optional): The range of internal addresses that are owned by this subnetwork. Provide this property when you create the subnetwork. For example, 10.0.0.0/8 or 100.64.0.0/10. Ranges must be unique and non-overlapping within a network. Only IPv4 is supported. This field is set at resource creation time. The range can be any range listed in the Valid ranges list. The range can be expanded after creation using expandIpCidrRange. Defaults to None.
        drain_timeout_seconds(int, optional): The drain timeout specifies the upper bound in seconds on the amount of time allowed to drain connections from the current ACTIVE subnetwork to the current BACKUP subnetwork. The drain timeout is only applicable when the following conditions are true: - the subnetwork being patched has purpose = INTERNAL_HTTPS_LOAD_BALANCER - the subnetwork being patched has role = BACKUP - the patch request is setting the role to ACTIVE. Note that after this patch operation the roles of the ACTIVE and BACKUP subnetworks will be swapped. Defaults to None.
        resource_id(str, optional): An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            example_resource_name:
              gcp.compute.subnetworks.present:
                - name: value
                - region: value
                - project: value
    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    result["comment"].append(
        "No-op: There is no create/update function for gcp.compute.subnetworks"
    )

    return result


async def absent(
    hub,
    ctx,
    name: str,
    project: str,
    region: str,
    request_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Deletes the specified subnetwork.

    Args:
        name(str): An Idem name of the resource.
        project(str): Project ID for this request.
        region(str): Name of the region scoping this request.
        request_id(str, optional): An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.
        resource_id(str, optional): An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              gcp.compute.subnetworks.absent:
                - name: value
                - project: value
                - region: value
    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    result["comment"].append(
        "No-op: There is no absent function for gcp.compute.subnetworks"
    )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves a list of subnetworks available to the specified project.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.compute.subnetworks
    """
    result = {}

    list_result = await hub.exec.gcp.compute.subnetworks.list(
        ctx, project=ctx.acct.project_id
    )

    if not list_result["result"]:
        hub.log.debug(f"Could not describe subnetworks {list_result['comment']}")
        return {}

    for resource in list_result["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "gcp.compute.subnetworks.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result
