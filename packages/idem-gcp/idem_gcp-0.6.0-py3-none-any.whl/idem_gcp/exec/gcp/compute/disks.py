"""Exec module for managing Disks."""
__func_alias__ = {"list_": "list"}

from typing import Dict, List
from typing import Any

from deepdiff import DeepDiff


async def list_(
    hub,
    ctx,
    project: str,
    zone: str = None,
    filter: str = None,
    order_by: str = None,
):
    r"""Retrieves a list of persistent disks contained within the specified zone.

    Args:
        project(str):
            Project ID for this request.

        zone(str, Optional):
            The name of the zone for this request.

        filter(str, Optional):
            A filter expression that filters resources listed in the response. Most Compute resources support two types of filter expressions: expressions that support regular expressions and expressions that follow API improvement proposal AIP-160. If you want to use AIP-160, your expression must specify the field name, an operator, and the value that you want to use for filtering. The value must be a string, a number, or a boolean. The operator must be either `=`, `!=`, `>`, `<`, `<=`, `>=` or `:`. For example, if you are filtering Compute Engine instances, you can exclude instances named `example-instance` by specifying `name != example-instance`. The `:` operator can be used with string fields to match substrings. For non-string fields it is equivalent to the `=` operator. The `:*` comparison can be used to test whether a key has been defined. For example, to find all objects with `owner` label use: ``` labels.owner:* ``` You can also filter nested fields. For example, you could specify `scheduling.automaticRestart = false` to include instances only if they are not scheduled for automatic restarts. You can use filtering on nested fields to filter based on resource labels. To filter on multiple expressions, provide each separate expression within parentheses. For example: ``` (scheduling.automaticRestart = true) (cpuPlatform = \"Intel Skylake\") ``` By default, each expression is an `AND` expression. However, you can include `AND` and `OR` expressions explicitly. For example: ``` (cpuPlatform = \"Intel Skylake\") OR (cpuPlatform = \"Intel Broadwell\") AND (scheduling.automaticRestart = true) ``` If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Examples: `fieldname eq unquoted literal` `fieldname eq 'single quoted literal'` `fieldname eq \"double quoted literal\"` `(fieldname1 eq literal) (fieldname2 ne \"literal\")` The literal value is interpreted as a regular expression using Google RE2 library syntax. The literal value must match the entire field. For example, to filter for instances that do not end with name "instance", you would use `name ne .*instance`.

        order_by(str, Optional):
            Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the resource name. You can also sort results in descending order based on the creation timestamp using `orderBy=\"creationTimestamp desc\"`. This sorts results based on the `creationTimestamp` field in reverse chronological order (newest result first). Use this to sort resources like operations so that the newest operation is returned first. Currently, only sorting by `name` or `creationTimestamp desc` is supported.

    Examples:
        .. code-block: sls

            random-name:
              exec.run:
              - path: gcp.compute.disks.list
              - kwargs:
                  project: project-name
                  zone: zone-name
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    if zone:
        ret = await hub.exec.gcp_api.client.compute.disks.list(
            ctx,
            project=project,
            zone=zone,
            filter=filter,
            orderBy=order_by,
        )
    else:
        ret = await hub.exec.gcp_api.client.compute.disks.aggregatedList(
            ctx,
            project=project,
            filter=filter,
            orderBy=order_by,
        )

    if not ret["result"]:
        result["comment"] += ret["comment"]
        result["result"] = False
        return result

    result["ret"] = ret["ret"]["items"]
    return result


async def get(
    hub,
    ctx,
    project: str = None,
    zone: str = None,
    name: str = None,
    resource_id: str = None,
):
    r"""Returns a specified persistent disk.

    Use an un-managed disk as a data-source. Supply one of the inputs as the filter.
    Gets a list of available persistent disks by making a list() request.

    Args:
        project(str, Optional):
            Project ID for this request. Defaults to None.

        zone(str, Optional):
            The name of the zone for this request. Defaults to None.

        name(str, Optional):
            Name of the persistent disk to return. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Examples:
        .. code-block: sls

            random-name:
              exec.run:
              - path: gcp.compute.disks.get
              - kwargs:
                  disk: disk-name
                  project: project-name
                  zone: zone-name
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    if resource_id:
        ret = await hub.exec.gcp_api.client.compute.disks.get(
            ctx,
            resource_id=resource_id,
        )
    elif project and zone and name:
        ret = await hub.exec.gcp_api.client.compute.disks.get(
            ctx, project=project, zone=zone, disk=name
        )
    else:
        result["result"] = False
        result["comment"] = [
            f"gcp.compute.disks#get(): {name} either resource_id or project, zone and name"
            f" should be specified."
        ]
        return result

    result["comment"] += ret["comment"]
    if not ret["result"]:
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    return result


async def resize(
    hub,
    ctx,
    new_size_gb: str,
    current_size_gb: str = None,
    project: str = None,
    zone: str = None,
    name: str = None,
    resource_id: str = None,
    request_id: str = None,
) -> Dict[str, Any]:
    r"""Resizes the specified persistent disk. You can only increase the size of the disk.

    Args:
        new_size_gb(str):
            The new size of the persistent disk, which is specified in GB.

        current_size_gb(str, Optional):
            The current size of the persistent disk, which is specified in GB.

        project(str, Optional):
            Project ID for this request. Defaults to None.

        zone(str, Optional):
            The name of the zone for this request. Defaults to None.

        name(str, Optional):
            The name of the persistent disk. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).

    Examples:
        .. code-block: sls

            random-name:
              exec.run:
              - path: gcp.compute.disks.resize
                - kwargs:
                    resource_id: resource_id
                    new_size_gb: some_size_in_gb
    """
    result = dict(comment=[], result=True, ret=None)

    if (
        new_size_gb is None
        or new_size_gb == "None"
        or (current_size_gb is not None and current_size_gb == new_size_gb)
    ):
        return result

    if not resource_id and not (project and zone and name):
        result["result"] = False
        result["comment"] = [
            f"gcp.compute.disks#resize(): {name} either resource_id or project, zone and name"
            f" should be specified."
        ]
        return result

    if not resource_id:
        resource_id = f"projects/{project}/zones/{zone}/disks/{name}"

    if not ctx.get("test"):
        request_body = {"size_gb": new_size_gb}
        update_ret = await hub.exec.gcp_api.client.compute.disks.resize(
            ctx,
            resource_id=resource_id,
            body=request_body,
            request_id=request_id,
        )

        if not update_ret["result"]:
            result["result"] = False
            result["comment"] += update_ret["comment"]
            return result

        if "compute#operation" in update_ret["ret"].get("kind"):
            operation = update_ret["ret"]
            operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                operation.get("selfLink"), "compute.zone_operations"
            )
            op_ret = await hub.tool.gcp.operation_utils.handle_operation(
                ctx, operation_id, "compute.disks", True
            )
            if not op_ret["result"]:
                result["result"] = False
                result["comment"] += op_ret["comment"]
                result["rerun_data"] = op_ret["rerun_data"]
                return result

    result["ret"] = {"size_gb": new_size_gb}
    if ctx.get("test", False):
        result["comment"].append(
            hub.tool.gcp.comment_utils.would_update_property_comment(
                "gcp.compute.disk", resource_id, "size_gb", new_size_gb
            )
        )
    else:
        result["comment"].append(
            hub.tool.gcp.comment_utils.update_property_comment(
                "gcp.compute.disk", resource_id, "size_gb", new_size_gb
            )
        )

    return result


async def update_labels(
    hub,
    ctx,
    new_labels: Dict[str, str],
    label_fingerprint: str,
    current_labels: Dict[str, str] = None,
    project: str = None,
    zone: str = None,
    name: str = None,
    resource_id: str = None,
    request_id: str = None,
) -> Dict[str, Any]:
    r"""Sets the labels on a disk. To learn more about labels, read the Labeling Resources documentation.

    Args:
        new_labels(str):
            The labels to set for this resource.

        label_fingerprint(str):
            The fingerprint of the previous set of labels for this resource, used to detect conflicts. The fingerprint is initially generated by Compute Engine and changes after every request to modify or update labels. You must always provide an up-to-date fingerprint hash in order to update or change labels. Make a get() request to the resource to get the latest fingerprint.

        current_labels(str, Optional):
            The current labels for this resource.

        project(str, Optional):
            Project ID for this request. Defaults to None.

        zone(str, Optional):
            The name of the zone for this request. Defaults to None.

        name(str, Optional):
            The name of the persistent disk. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).

    Examples:
        .. code-block: sls

            random-name:
              exec.run:
                - path: gcp.compute.disks.update_labels
                - kwargs:
                    project: some-project
                    zone: some-zone
                    name: some-name
                    new_labels:
                      some-label-key: some-label-value
                    label_fingerprint: some-label-fingerprint
    """
    result = dict(comment=[], result=True, ret=None)

    # {} should be passed as new_labels if labels removal is wanted
    if (
        new_labels is None
        or new_labels == "None"
        or (current_labels is not None and current_labels == new_labels)
    ):
        return result

    if not resource_id and not (project and zone and name):
        result["result"] = False
        result["comment"] = [
            f"gcp.compute.disks#update_labels(): {name} either resource_id or project, zone and name"
            f" should be specified."
        ]
        return result

    if not resource_id:
        resource_id = f"projects/{project}/zones/{zone}/disks/{name}"

    if not ctx.get("test"):
        request_body = {"labels": new_labels, "label_fingerprint": label_fingerprint}
        update_ret = await hub.exec.gcp_api.client.compute.disks.setLabels(
            ctx,
            resource_id=resource_id,
            body=request_body,
            request_id=request_id,
        )

        if not update_ret["result"]:
            result["result"] = False
            result["comment"] += update_ret["comment"]
            return result

        if "compute#operation" in update_ret["ret"].get("kind"):
            operation = update_ret["ret"]
            operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                operation.get("selfLink"), "compute.zone_operations"
            )
            op_ret = await hub.tool.gcp.operation_utils.handle_operation(
                ctx, operation_id, "compute.disks", True
            )
            if not op_ret["result"]:
                result["result"] = False
                result["comment"] += op_ret["comment"]
                result["rerun_data"] = op_ret["rerun_data"]
                return result

    result["ret"] = {"labels": new_labels}
    if ctx.get("test", False):
        result["comment"].append(
            hub.tool.gcp.comment_utils.would_update_property_comment(
                "gcp.compute.disk", resource_id, "labels", new_labels
            )
        )

        return result

    result["comment"].append(
        hub.tool.gcp.comment_utils.update_property_comment(
            "gcp.compute.disk", resource_id, "labels", new_labels
        )
    )

    get_ret = await hub.exec.gcp.compute.disks.get(ctx, resource_id=resource_id)

    if not get_ret["result"] or not get_ret["ret"]:
        result["result"] = False
        result["comment"] += get_ret["comment"]
        return result

    # Setting the new label fingerprint after the labels have been updated
    result["ret"]["label_fingerprint"] = get_ret["ret"]["label_fingerprint"]

    return result


async def update_resource_policies(
    hub,
    ctx,
    new_resource_policies: List[str],
    current_resource_policies: List[str],
    project: str = None,
    zone: str = None,
    name: str = None,
    resource_id: str = None,
    request_id: str = None,
) -> Dict[str, Any]:
    r"""Adds existing resource policies to a disk. You can only add one policy which will be applied to this disk for scheduling snapshot creation. Removes resource policies from a disk.

    Args:
        new_resource_policies(List[str]):
            List of the new resource policies for the disk.

        current_resource_policies(List[str]):
            List of the current resource policies for the disk.

        project(str, Optional):
            Project ID for this request. Defaults to None.

        zone(str, Optional):
            The name of the zone for this request. Defaults to None.

        name(str, Optional):
            The name of the persistent disk. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).

    Examples:
        .. code-block: sls

            random-name:
              exec.run:
                - path: gcp.compute.disks.update_resource_policies
                - kwargs:
                    resource_id: resource_id
                    new_resource_policies:
                        - some-resource-policy
    """
    result = dict(comment=[], result=True, ret=None)

    if (
        new_resource_policies is None
        or new_resource_policies == "None"
        or (
            current_resource_policies is not None
            and not DeepDiff(
                current_resource_policies, new_resource_policies, ignore_order=True
            )
        )
    ):
        return result

    if not resource_id and not (project and zone and name):
        result["result"] = False
        result["comment"] = [
            f"gcp.compute.disks#update_resource_policies(): {name} either resource_id or project, zone and name"
            f" should be specified."
        ]
        return result

    if not resource_id:
        resource_id = f"projects/{project}/zones/{zone}/disks/{name}"

    new_resource_policies = list(set(new_resource_policies))

    # If (some) resource policies are links, parse them to resource policy resource ids
    new_resource_policies = [
        hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
            policy, "compute.resource_policies"
        )
        for policy in new_resource_policies
    ]
    current_resource_policies = [
        hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
            policy, "compute.resource_policies"
        )
        for policy in current_resource_policies
    ]

    resource_policies_to_remove = [
        policy
        for policy in current_resource_policies
        if policy not in new_resource_policies
    ]
    resource_policies_to_add = [
        policy
        for policy in new_resource_policies
        if policy not in current_resource_policies
    ]

    add_request_body = None
    if len(resource_policies_to_add) > 0:
        add_request_body = {"resource_policies": resource_policies_to_add}
    remove_request_body = None
    if len(resource_policies_to_remove) > 0:
        remove_request_body = {"resource_policies": resource_policies_to_remove}

    remove_ret = None
    if remove_request_body is not None:
        remove_ret = await hub.exec.gcp_api.client.compute.disks.removeResourcePolicies(
            ctx,
            resource_id=resource_id,
            body=remove_request_body,
            request_id=request_id,
        )

        if not remove_ret["result"]:
            result["result"] = False
            result["comment"] += remove_ret["comment"]
            return result

        if "compute#operation" in remove_ret["ret"].get("kind"):
            operation = remove_ret["ret"]
            operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                operation.get("selfLink"), "compute.zone_operations"
            )
            op_ret = await hub.tool.gcp.operation_utils.handle_operation(
                ctx, operation_id, "compute.disks", True
            )
            if not op_ret["result"]:
                result["result"] = False
                result["comment"] += op_ret["comment"]
                result["rerun_data"] = op_ret["rerun_data"]
                return result

    if (remove_ret is None or remove_ret["result"]) and add_request_body is not None:
        add_ret = await hub.exec.gcp_api.client.compute.disks.addResourcePolicies(
            ctx,
            resource_id=resource_id,
            body=add_request_body,
            request_id=request_id,
        )

        if not add_ret["result"]:
            result["result"] = False
            result["comment"] += add_ret["comment"]
            return result

        if "compute#operation" in add_ret["ret"].get("kind"):
            operation = add_ret["ret"]
            operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                operation.get("selfLink"), "compute.zone_operations"
            )
            op_ret = await hub.tool.gcp.operation_utils.handle_operation(
                ctx, operation_id, "compute.disks", True
            )
            if not op_ret["result"]:
                result["result"] = False
                result["comment"] += op_ret["comment"]
                result["rerun_data"] = op_ret["rerun_data"]
                return result

    result["ret"] = {"resource_policies": new_resource_policies}
    if ctx.get("test", False):
        result["comment"].append(
            hub.tool.gcp.comment_utils.would_update_property_comment(
                "gcp.compute.disk",
                resource_id,
                "resource_policies",
                new_resource_policies,
            )
        )
    else:
        result["comment"].append(
            hub.tool.gcp.comment_utils.update_property_comment(
                "gcp.compute.disk",
                resource_id,
                "resource_policies",
                new_resource_policies,
            )
        )

    return result
