#!/usr/bin/env python3
"""
DataStream endpoint definitions using new SDK (v2 API)
Replaces the old endpointdef.py with modern DataStream v2 API
"""

import os
import sys

# Add parent directory to path to import the SDK
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datastream_sdk import DataStreamClient

# Global client instance
_client = None


def get_client():
    """Get or create DataStream client instance"""
    global _client
    if _client is None:
        _client = DataStreamClient()
    return _client


# READ OPERATIONS


def listGroups(accountSwitchKey=None):
    """List the groups associated with the account"""
    client = get_client()
    return {"groups": client.list_groups(accountSwitchKey)}


def listConnectors(accountSwitchKey=None):
    """List connectors (compatibility layer - hardcoded values)"""
    return {
        "connectors": [
            {"connectorTypeId": 2, "connectorTypeName": "S3"},
            {"connectorTypeId": 7, "connectorTypeName": "Azure Storage"},
        ]
    }


def listProducts(accountSwitchKey=None):
    """List products (compatibility layer - hardcoded values)"""
    return {
        "products": [
            {
                "productId": "Adaptive_Media_Delivery",
                "productName": "Adaptive Media Delivery",
            },
            {"productId": "Ion_Standard", "productName": "Ion Standard"},
        ]
    }


def listStreamTypes(accountSwitchKey=None):
    """List stream types (compatibility layer)"""
    return {
        "streamTypes": [
            {
                "streamTypeId": 3,
                "streamTypeName": "2.0 BETA",
                "streamTypeIdentifier": "RAW_LOGS",
            }
        ]
    }


def listStreams(groupId, status=None, accountSwitchKey=None):
    """List streams in a group"""
    client = get_client()
    return {"streams": client.list_streams(groupId, status)}


def listProperties(groupId, productId, accountSwitchKey=None):
    """List properties for a group and product"""
    client = get_client()
    return {"properties": client.list_properties(groupId, productId)}


def listErrorStreams(groupId, accountSwitchKey=None):
    """List error streams (removed in v2)"""
    return {"errorStreams": []}


def getStream(streamId, accountSwitchKey=None):
    """Get details of a specific stream"""
    client = get_client()
    return client.get_stream(streamId)


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
