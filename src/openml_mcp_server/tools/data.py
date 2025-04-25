from ..server import mcp, _fetch_openml_data
from typing import Dict, Union

@mcp.tool()
async def get_dataset_description(dataset_id: int) -> Union[Dict, str]:
    """
    Get the description for a specific OpenML dataset by its ID.
    Contains all the meta-data about the dataset.

    Args:
        dataset_id: The integer ID of the dataset.
    """
    return await _fetch_openml_data(f"/data/{dataset_id}")

@mcp.tool()
async def list_datasets(filters: str) -> Union[Dict, str]:
    """
    List OpenML datasets, applying filters specified as part of the path.
    Example filters: 'limit/10/offset/0', 'status/active/tag/uci', 'number_instances/0..1000'.
    See OpenML API docs for detailed filter syntax.

    Args:
        filters: The filter string (e.g., 'limit/10/offset/0', 'status/active').
    """
    if not filters:
        return "Please provide filters. Example: 'limit/10/offset/0'"
    filters = filters.strip('/')
    return await _fetch_openml_data(f"/data/list/{filters}")

@mcp.tool()
async def get_dataset_features(dataset_id: int) -> Union[Dict, str]:
    """
    Get the features (attributes/columns) description for a specific OpenML dataset.

    Args:
        dataset_id: The integer ID of the dataset.
    """
    return await _fetch_openml_data(f"/data/features/{dataset_id}")

@mcp.tool()
async def get_dataset_qualities(dataset_id: int) -> Union[Dict, str]:
    """
    Get the calculated qualities (meta-features) for a specific OpenML dataset.

    Args:
        dataset_id: The integer ID of the dataset.
    """
    return await _fetch_openml_data(f"/data/qualities/{dataset_id}")

@mcp.tool()
async def list_data_qualities() -> Union[Dict, str]:
    """
    List all available data quality measures supported by OpenML.
    """
    return await _fetch_openml_data("/data/qualities/list")
