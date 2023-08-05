import time
from typing import Any
from typing import Dict


async def handle_operation(
    hub, ctx, operation_id: str, resource_type: str, wait_until_done: bool = False
) -> Dict[str, Any]:
    result = {
        "comment": [],
        "result": True,
        "rerun_data": None,
        "resource_id": None,
    }

    operation_type = hub.tool.gcp.operation_utils.get_operation_type(operation_id)

    if operation_type is None:
        result["result"] = False
        result["comment"].append(
            f"Cannot determine operation scope (zonal/regional/global) {operation_id}"
        )
        return result

    if operation_type == "compute.zone_operations":
        get_ret = await hub.exec.gcp_api.client.compute.zone_operations.get(
            ctx, resource_id=operation_id
        )
    elif operation_type == "compute.region_operations":
        get_ret = await hub.exec.gcp_api.client.compute.region_operations.get(
            ctx, resource_id=operation_id
        )
    elif operation_type == "compute.global_operations":
        get_ret = await hub.exec.gcp_api.client.compute.global_operations.get(
            ctx, resource_id=operation_id
        )

    if not get_ret["result"] or not get_ret["ret"]:
        result["result"] = False
        result["comment"] = get_ret["comment"]
        return result

    operation = get_ret["ret"]
    if operation["status"] != "DONE":
        if wait_until_done:
            operation = await hub.tool.gcp.operation_utils.wait_for_operation(
                ctx, operation, operation_type
            )
        else:
            result["result"] = False
            result[
                "rerun_data"
            ] = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                operation.get("selfLink"), operation_type
            )
            result["comment"] += get_ret["comment"]
            return result

    if operation.get("error"):
        result["result"] = False
        result["comment"] += str(operation.get("error", {}))
        return result

    result["resource_id"] = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
        operation.get("targetLink"), resource_type
    )

    return result


async def wait_for_operation(hub, ctx, operation, operation_type: str) -> Dict:
    while True:
        if operation_type == "compute.zone_operations":
            op_ret = await hub.exec.gcp_api.client.compute.zone_operations.wait(
                ctx, resource_id=operation["selfLink"]
            )
        elif operation_type == "compute.region_operations":
            op_ret = await hub.exec.gcp_api.client.compute.region_operations.wait(
                ctx, resource_id=operation["selfLink"]
            )
        elif operation_type == "compute.global_operations":
            op_ret = await hub.exec.gcp_api.client.compute.global_operations.wait(
                ctx, resource_id=operation["selfLink"]
            )

        operation = op_ret["ret"]
        if operation["status"] == "DONE" or "error" in operation:
            break

        time.sleep(1)

    return operation


def get_operation_type(hub, operation_id) -> str:
    if "/zones/" in operation_id:
        return "compute.zone_operations"
    elif "/regions/" in operation_id:
        return "compute.region_operations"
    elif "/global/" in operation_id:
        return "compute.global_operations"
    else:
        return None
