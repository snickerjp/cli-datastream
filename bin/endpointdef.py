"""
DataStream endpoint definitions using new SDK (v2 API)
Replaces the old endpointdef.py with modern DataStream v2 API
"""

from datastream_sdk import DataStreamClient

# Global client instance
_client = None


def get_client(edgerc_path=None, section=None):
    """Get or create DataStream client instance"""
    global _client
    if _client is None:
        if edgerc_path and section:
            _client = DataStreamClient(edgerc_path=edgerc_path, section=section)
        else:
            _client = DataStreamClient()
    return _client


# READ OPERATIONS


def listGroups(accountSwitchKey=None):
    """List the groups associated with the account"""
    client = get_client()
    return client.list_groups(accountSwitchKey)


def listConnectors(accountSwitchKey=None):
    """List all available connectors"""
    client = get_client()
    return client.list_connectors()


def listProducts(accountSwitchKey=None):
    """List all available products"""
    client = get_client()
    return {"products": client.list_products()}


def listStreamTypes(accountSwitchKey=None):
    """List stream types (compatibility layer)"""
    return {
        "streamTypes": [
            {
                "streamTypeId": 3,
                "streamTypeName": "2.0 BETA",
                "streamType": "RAW_LOGS",
                "streamTypeIdentifier": "RAW_LOGS",
                "isRaw": True,
            }
        ]
    }


def listStreams(groupId, status=None, accountSwitchKey=None):
    """List streams in a group"""
    client = get_client()
    return client.list_streams(groupId, status, account_switch_key=accountSwitchKey)


def listProperties(groupId, productId, accountSwitchKey=None):
    """List properties for a group and product"""
    client = get_client()
    return {
        "properties": client.list_properties(
            groupId, productId, account_switch_key=accountSwitchKey
        )
    }


def listErrorStreams(groupId, accountSwitchKey=None):
    """List error streams (removed in v2)"""
    return {"errorStreams": []}


def getStream(streamId, accountSwitchKey=None):
    """Get details of a specific stream"""
    from config import EdgeGridConfig

    config = EdgeGridConfig({"verbose": False}, "default")
    client = get_client()
    version = getattr(config, "version", "latest")
    return client.get_stream(streamId, version=version)


def getStreamActHistory(streamId, accountSwitchKey=None):
    """Get activation history for a stream"""
    client = get_client()
    return client.get_activation_history(streamId)


def getStreamHistory(streamId, accountSwitchKey=None):
    """Get stream history"""
    client = get_client()
    return client.get_stream_history(streamId)


def getDatasets(templatename, accountSwitchKey=None):
    """List available dataset fields"""
    client = get_client()
    return {"datasetFields": client.list_dataset_fields(template_name=templatename)}


# WRITE OPERATIONS


def createStream(data, accountSwitchKey=None):
    """Create a new stream"""
    client = get_client()
    return client.create_stream(data)


def updateStream(data, streamid, accountSwitchKey=None):
    """Update an existing stream"""
    client = get_client()
    return client.update_stream(streamid, data)


def activateStream(streamId, accountSwitchKey=None):
    """Activate a stream"""
    client = get_client()
    return client.activate_stream(streamId)


def deActivateStream(streamId, accountSwitchKey=None):
    """Deactivate a stream"""
    client = get_client()
    return client.deactivate_stream(streamId)


def deleteStream(streamId, accountSwitchKey=None):
    """Delete a stream"""
    client = get_client()
    return client.delete_stream(streamId)
