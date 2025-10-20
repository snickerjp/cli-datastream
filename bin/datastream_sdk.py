#!/usr/bin/env python3
"""
Akamai DataStream SDK wrapper using EdgeGrid Python
"""

import os
from urllib.parse import urljoin

import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc


class DataStreamClient:
    def __init__(self, edgerc_path=None, section=None):
        """Initialize DataStream client with EdgeGrid authentication"""
        # Priority: 1. Argument, 2. Environment variable, 3. Default
        if section is None:
            section = os.getenv("AKAMAI_EDGERC_SECTION", "default")

        if edgerc_path is None:
            edgerc_path = os.getenv("AKAMAI_EDGERC")

            if edgerc_path is None:
                # Search in safe locations
                for path in ["./.edgerc", "~/.edgerc"]:
                    expanded_path = os.path.expanduser(path)
                    if os.path.exists(expanded_path):
                        edgerc_path = expanded_path
                        break

                if edgerc_path is None:
                    raise FileNotFoundError("No .edgerc file found")

        self.edgerc = EdgeRc(edgerc_path)
        self.section = section

        # Normalize host scheme to avoid double-prefix
        host = self.edgerc.get(section, "host")
        self.baseurl = (
            host if host.startswith(("http://", "https://")) else f"https://{host}"
        )

        self.session = requests.Session()
        self.session.auth = EdgeGridAuth.from_edgerc(self.edgerc, section)
        self.session.headers.update({"User-Agent": "akamai-datastream-cli/2.0"})
        self.timeout = (5, 30)  # (connect_timeout, read_timeout) in seconds

    def list_groups(self, account_switch_key=None):
        """List all groups in the account"""
        path = "/datastream-config-api/v2/log/groups"
        params = {}
        if account_switch_key:
            params["accountSwitchKey"] = account_switch_key

        response = self.session.get(
            urljoin(self.baseurl, path), params=params, timeout=self.timeout
        )
        response.raise_for_status()
        result = response.json()
        return result.get("groups", [])

    def list_streams(self, group_id, stream_status=None, account_switch_key=None):
        """List all streams in a group"""
        path = f"/datastream-config-api/v2/log/groups/{group_id}/streams"
        params = {}
        if stream_status:
            params["streamStatus"] = stream_status
        if account_switch_key:
            params["accountSwitchKey"] = account_switch_key

        response = self.session.get(
            urljoin(self.baseurl, path), params=params, timeout=self.timeout
        )
        response.raise_for_status()
        result = response.json()
        return result.get("streams", [])

    def get_stream(self, stream_id, version="latest"):
        """Get details of a specific stream"""
        path = f"/datastream-config-api/v2/log/streams/{stream_id}"
        params = {}
        if version != "latest":
            params["version"] = version

        response = self.session.get(urljoin(self.baseurl, path), params=params)
        response.raise_for_status()
        return response.json()

    def list_connectors(self, account_switch_key=None):
        """List all available connectors"""
        path = "/datastream-config-api/v2/log/connectors"
        params = {}
        if account_switch_key:
            params["accountSwitchKey"] = account_switch_key

        response = self.session.get(
            urljoin(self.baseurl, path), params=params, timeout=self.timeout
        )
        response.raise_for_status()
        result = response.json()
        return result.get("connectors", [])

    def list_dataset_fields(self, product_id=None, template_name=None):
        """List available dataset fields"""
        path = "/datastream-config-api/v2/log/datasets-fields"
        params = {}
        if product_id:
            params["productId"] = product_id
        if template_name:
            params["templateName"] = template_name

        response = self.session.get(urljoin(self.baseurl, path), params=params)
        response.raise_for_status()
        result = response.json()
        return result.get("datasetFields", [])

    def list_products(self, account_switch_key=None):
        """List all available products"""
        path = "/datastream-config-api/v2/log/products"
        params = {}
        if account_switch_key:
            params["accountSwitchKey"] = account_switch_key

        response = self.session.get(
            urljoin(self.baseurl, path), params=params, timeout=self.timeout
        )
        response.raise_for_status()
        result = response.json()
        return result.get("products", [])

    def list_properties(self, group_id, product_id, account_switch_key=None):
        """List properties for a group and product"""
        path = (
            f"/datastream-config-api/v2/log/groups/{group_id}/"
            f"products/{product_id}/properties"
        )
        params = {}
        if account_switch_key:
            params["accountSwitchKey"] = account_switch_key

        response = self.session.get(
            urljoin(self.baseurl, path), params=params, timeout=self.timeout
        )
        response.raise_for_status()
        result = response.json()
        return result.get("properties", [])

    def get_activation_history(self, stream_id):
        """Get activation history for a stream"""
        path = f"/datastream-config-api/v2/log/streams/{stream_id}/activation-history"

        response = self.session.get(urljoin(self.baseurl, path), timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_stream_history(self, stream_id):
        """Get stream history"""
        path = f"/datastream-config-api/v2/log/streams/{stream_id}/history"

        response = self.session.get(urljoin(self.baseurl, path), timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def create_stream(self, stream_data):
        """Create a new stream"""
        path = "/datastream-config-api/v2/log/streams"

        response = self.session.post(
            urljoin(self.baseurl, path), timeout=self.timeout, json=stream_data
        )
        response.raise_for_status()
        return response.json()

    def update_stream(self, stream_id, stream_data):
        """Update an existing stream"""
        path = f"/datastream-config-api/v2/log/streams/{stream_id}"

        response = self.session.put(
            urljoin(self.baseurl, path), timeout=self.timeout, json=stream_data
        )
        response.raise_for_status()
        return response.json()

    def activate_stream(self, stream_id):
        """Activate a stream"""
        path = f"/datastream-config-api/v2/log/streams/{stream_id}/activate"

        response = self.session.post(
            urljoin(self.baseurl, path), timeout=self.timeout, json={}
        )
        response.raise_for_status()
        return response.json()

    def deactivate_stream(self, stream_id):
        """Deactivate a stream"""
        path = f"/datastream-config-api/v2/log/streams/{stream_id}/deactivate"

        response = self.session.post(
            urljoin(self.baseurl, path), timeout=self.timeout, json={}
        )
        response.raise_for_status()
        return response.json()

    def delete_stream(self, stream_id):
        """Delete a stream"""
        path = f"/datastream-config-api/v2/log/streams/{stream_id}"

        response = self.session.delete(
            urljoin(self.baseurl, path), timeout=self.timeout
        )
        response.raise_for_status()
        return {} if response.status_code == 204 else response.json()


if __name__ == "__main__":
    import os

    client = DataStreamClient()

    # List groups
    groups = client.list_groups()
    print("Available groups:")
    for i, group in enumerate(groups):
        print(f"  {i}: {group.get('groupId')} - {group.get('groupName')}")

    # Get group ID from environment or prompt
    test_group_id = os.getenv("DATASTREAM_GROUP_ID")
    if not test_group_id and groups:
        print(f"\nSet DATASTREAM_GROUP_ID environment variable to test streams")
        print(f"Example: export DATASTREAM_GROUP_ID={groups[-1]['groupId']}")
        test_group_id = groups[-1]["groupId"]  # Default to last

    if test_group_id:
        print(f"\n=== Streams in Group {test_group_id} ===")
        try:
            streams = client.list_streams(int(test_group_id))
            if streams:
                for stream in streams:
                    print(
                        f"Stream: {stream.get('streamId')} - {stream.get('streamName')}"
                    )
            else:
                print("No streams found")
        except Exception as e:
            print(f"Error: {e}")

    # Test list_streams with first group
    if groups:
        group_id = groups[0]["groupId"]
        print(f"\n=== Streams in Group {group_id} ===")
        try:
            streams = client.list_streams(group_id)
            for stream in streams:
                print(f"Stream: {stream.get('streamId')} - {stream.get('streamName')}")
        except Exception as e:
            print(f"Error: {e}")
