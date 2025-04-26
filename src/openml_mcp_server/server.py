import os
import httpx
import json
import logging
from typing import List, Dict, Union, Any

from mcp.server.fastmcp import FastMCP


class OpenMLApiError(Exception):
    pass


class OpenMLRequestError(Exception):
    pass


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

OPENML_API_BASE = "https://www.openml.org/api/v1/json"
OPENML_API_KEY = os.environ.get("OPENML_API_KEY")
USER_AGENT = "mcp-python-sdk-openml-example/1.0"

mcp = FastMCP("OpenML Explorer")


async def _fetch_openml_data(
    endpoint: str, params: Dict[str, Any] = None
) -> Union[Dict, List, str]:
    """Helper function to fetch data from the OpenML API."""
    if params is None:
        params = {}
    if OPENML_API_KEY:
        params["api_key"] = OPENML_API_KEY

    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    url = f"{OPENML_API_BASE}{endpoint}"

    transport = httpx.AsyncHTTPTransport(retries=3)
    async with httpx.AsyncClient(transport=transport) as client:
        try:
            logging.debug(f"MCP_DEBUG: Requesting URL: {url} with params: {params}")
            response = await client.get(
                url, params=params, headers=headers, timeout=30.0
            )
            response.raise_for_status()
            if response.status_code == 204 or not response.content:
                return f"Success with status {response.status_code}, but no content returned."
            try:
                return response.json()
            except json.JSONDecodeError:
                return f"Received non-JSON response (status {response.status_code}): {response.text[:500]}"
        except httpx.HTTPStatusError as e:
            error_message = f"OpenML API Error {e.response.status_code}"
            try:
                error_data = e.response.json()
                message = error_data.get("error", {}).get(
                    "message", "No specific error message provided."
                )
                code = error_data.get("error", {}).get("code", "N/A")
                error_message += f" (Code: {code}): {message}"
            except json.JSONDecodeError:
                error_message += f": {e.response.text[:200]}"
            logging.error(f"MCP_ERROR: {error_message}")
            raise OpenMLApiError(error_message)
        except httpx.RequestError as e:
            error_message = f"HTTP Request Error connecting to OpenML: {e}"
            logging.error(f"MCP_ERROR: {error_message}")
            raise OpenMLRequestError(error_message)
        except Exception as e:
            error_message = f"An unexpected error occurred: {type(e).__name__} - {e}"
            logging.error(f"MCP_ERROR: {error_message}")
            raise OpenMLRequestError(error_message)


@mcp.tool()
async def get_task_description(task_id: int) -> Union[Dict, str]:
    """
    Get the description for a specific OpenML task by its ID.
    Describes ML tasks like classification or regression, including inputs and evaluation criteria.

    Args:
        task_id: The integer ID of the task.
    """
    return await _fetch_openml_data(f"/task/{task_id}")


@mcp.tool()
async def list_tasks(filters: str) -> Union[Dict, str]:
    """
    List OpenML tasks, applying filters specified as part of the path.
    Example filters: 'limit/10/offset/0', 'type/1/tag/study_1' (type 1 is Supervised Classification).
    See OpenML API docs for detailed filter syntax.

    Args:
        filters: The filter string (e.g., 'limit/10/offset/0', 'type/1').
    """
    if not filters:
        return "Please provide filters. Example: 'limit/10/offset/0/type/1'"
    filters = filters.strip("/")
    return await _fetch_openml_data(f"/task/list/{filters}")


@mcp.tool()
async def get_flow_description(flow_id: int) -> Union[Dict, str]:
    """
    Get the description for a specific OpenML flow (model/pipeline) by its ID.
    Includes parameters, dependencies, etc.

    Args:
        flow_id: The integer ID of the flow.
    """
    return await _fetch_openml_data(f"/flow/{flow_id}")


@mcp.tool()
async def list_flows(filters: str) -> Union[Dict, str]:
    """
    List OpenML flows, applying filters specified as part of the path.
    Example filters: 'limit/10/offset/0', 'tag/weka'.
    See OpenML API docs for detailed filter syntax.

    Args:
        filters: The filter string (e.g., 'limit/10/offset/0', 'uploader/1').
    """
    if not filters:
        return "Please provide filters. Example: 'limit/10/offset/0'"
    filters = filters.strip("/")
    return await _fetch_openml_data(f"/flow/list/{filters}")


@mcp.tool()
async def check_flow_exists(name: str, version: str) -> Union[Dict, str]:
    """
    Check if a flow with a specific name and external version exists on OpenML.

    Args:
        name: The name of the flow (e.g., 'weka.J48').
        version: The external version string (e.g., 'Weka_3.7.5_9117').
    """
    return await _fetch_openml_data(f"/flow/exists/{name}/{version}")


@mcp.tool()
async def get_run_description(run_id: int) -> Union[Dict, str]:
    """
    Get the description for a specific OpenML run (experiment result) by its ID.
    Includes task, flow, setup, evaluations, and output files.

    Args:
        run_id: The integer ID of the run.
    """
    return await _fetch_openml_data(f"/run/{run_id}")


@mcp.tool()
async def list_runs(filters: str) -> Union[Dict, str]:
    """
    List OpenML runs, applying filters specified as part of the path.
    Requires filters like task, flow, setup, or uploader ID. Max 10,000 results.
    Example filters: 'limit/10/offset/0/task/1', 'flow/67/uploader/1'.
    See OpenML API docs for detailed filter syntax.

    Args:
        filters: The filter string (e.g., 'limit/10/task/28', 'flow/67'). Must include task, flow, setup, uploader, or run filter.
    """
    if not filters:
        return "Please provide filters. Must include task, flow, setup, uploader, or run filter. Example: 'limit/10/task/28'"
    filters = filters.strip("/")
    return await _fetch_openml_data(f"/run/list/{filters}")


@mcp.tool()
async def get_run_trace(run_id: int) -> Union[Dict, str]:
    """
    Get the optimization trace for a specific OpenML run (if available).
    Shows hyperparameter settings tried during tuning and their evaluations.

    Args:
        run_id: The integer ID of the run.
    """
    return await _fetch_openml_data(f"/run/trace/{run_id}")


@mcp.tool()
async def list_evaluations(filters: str) -> Union[Dict, str]:
    """
    List OpenML run evaluations, applying filters specified as part of the path.
    Requires filters like function, task, flow, setup, uploader, or run ID. Max 10,000 results.
    Example filters: 'limit/10/offset/0/task/1/function/predictive_accuracy'.
    See OpenML API docs for detailed filter syntax.

    Args:
        filters: The filter string (e.g., 'limit/10/task/68/function/f_measure'). Must include filters.
    """
    if not filters:
        return "Please provide filters. Must include function, task, flow, setup, uploader, or run filter. Example: 'limit/10/task/68/function/f_measure'"
    filters = filters.strip("/")
    return await _fetch_openml_data(f"/evaluation/list/{filters}")


@mcp.tool()
async def get_setup_description(setup_id: int) -> Union[Dict, str]:
    """
    Get the description for a specific OpenML setup (hyperparameter configuration) by its ID.

    Args:
        setup_id: The integer ID of the setup.
    """
    return await _fetch_openml_data(f"/setup/{setup_id}")


@mcp.tool()
async def list_setups(filters: str) -> Union[Dict, str]:
    """
    List OpenML setups, applying filters specified as part of the path. Max 1,000 results.
    Example filters: 'limit/10/offset/0/flow/65'.
    See OpenML API docs for detailed filter syntax.

    Args:
        filters: The filter string (e.g., 'limit/10/flow/65', 'setup/10,12').
    """
    if not filters:
        return "Please provide filters. Example: 'limit/10/flow/65'"
    filters = filters.strip("/")
    return await _fetch_openml_data(f"/setup/list/{filters}")


@mcp.tool()
async def get_study_description(study_id_or_alias: str) -> Union[Dict, str]:
    """
    Get the description for a specific OpenML study (collection of tasks/runs) by its ID or alias.

    Args:
        study_id_or_alias: The integer ID or string alias of the study.
    """
    return await _fetch_openml_data(f"/study/{study_id_or_alias}")


@mcp.tool()
async def list_studies(filters: str) -> Union[Dict, str]:
    """
    List OpenML studies, applying filters specified as part of the path.
    Example filters: 'limit/10/offset/0', 'main_entity_type/task'.
    See OpenML API docs for detailed filter syntax.

    Args:
        filters: The filter string (e.g., 'limit/10/offset/0', 'main_entity_type/task'). Can be empty for all studies.
    """
    filters = filters.strip("/")
    # Handle case where no filters are provided - list all
    if not filters:
        return await _fetch_openml_data(
            "/study/list/"
        )  # Need trailing slash for empty filters
    return await _fetch_openml_data(f"/study/list/{filters}")


@mcp.tool()
async def list_task_types() -> Union[Dict, str]:
    """
    List all task types supported by OpenML (e.g., Supervised Classification, Regression).
    """
    return await _fetch_openml_data("/tasktype/list")


@mcp.tool()
async def get_task_type_description(task_type_id: int) -> Union[Dict, str]:
    """
    Get the description for a specific OpenML task type by its ID.

    Args:
        task_type_id: The integer ID of the task type (e.g., 1 for Supervised Classification).
    """
    return await _fetch_openml_data(f"/tasktype/{task_type_id}")


@mcp.tool()
async def list_evaluation_measures() -> Union[Dict, str]:
    """
    List all evaluation measures supported by OpenML (e.g., predictive_accuracy, area_under_roc_curve).
    """
    return await _fetch_openml_data("/evaluationmeasure/list")


@mcp.tool()
async def list_estimation_procedures() -> Union[Dict, str]:
    """
    List all estimation procedures supported by OpenML (e.g., 10-fold Crossvalidation).
    """
    return await _fetch_openml_data("/estimationprocedure/list")
