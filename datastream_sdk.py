#!/usr/bin/env python3
"""
Akamai DataStream SDK wrapper using EdgeGrid Python
"""

import json
import os
import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from urllib.parse import urljoin


class DataStreamClient:
    def __init__(self, edgerc_path=None, section=None):
        """Initialize DataStream client with EdgeGrid authentication"""
        # Priority: 1. Argument, 2. Environment variable, 3. Default
        if section is None:
            section = os.getenv('AKAMAI_EDGERC_SECTION', 'default')
        
        if edgerc_path is None:
            edgerc_path = os.getenv('AKAMAI_EDGERC')
            
            if edgerc_path is None:
                # Search in safe locations
                for path in ['./.edgerc', '~/.edgerc']:
                    expanded_path = os.path.expanduser(path)
                    if os.path.exists(expanded_path):
                        edgerc_path = expanded_path
                        break
                
                if edgerc_path is None:
                    raise FileNotFoundError("No .edgerc file found")
        
        self.edgerc = EdgeRc(edgerc_path)
        self.section = section
        self.baseurl = f"https://{self.edgerc.get(section, 'host')}"
        
        self.session = requests.Session()
        self.session.auth = EdgeGridAuth.from_edgerc(self.edgerc, section)
    
    def list_groups(self, account_switch_key=None):
        """List all groups in the account"""
        path = '/datastream-config-api/v2/log/groups'
        params = {}
        if account_switch_key:
            params['accountSwitchKey'] = account_switch_key
        
        response = self.session.get(urljoin(self.baseurl, path), params=params)
        response.raise_for_status()
        result = response.json()
        return result.get('groups', [])
    
    def list_streams(self, group_id, stream_status=None):
        """List all streams in a group"""
        path = f'/datastream-config-api/v2/log/groups/{group_id}/streams'
        params = {}
        if stream_status:
            params['streamStatus'] = stream_status
        
        response = self.session.get(urljoin(self.baseurl, path), params=params)
        response.raise_for_status()
        return response.json()
    
    def get_stream(self, stream_id, version='latest'):
        """Get details of a specific stream"""
        path = f'/datastream-config-api/v2/log/streams/{stream_id}'
        params = {}
        if version != 'latest':
            params['version'] = version
        
        response = self.session.get(urljoin(self.baseurl, path), params=params)
        response.raise_for_status()
        return response.json()
    
    def list_connectors(self):
        """List all available connectors"""
        path = '/datastream-config-api/v2/log/connectors'
        
        response = self.session.get(urljoin(self.baseurl, path))
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    client = DataStreamClient()
    
    # List groups
    groups = client.list_groups()
    for group in groups:
        print(f"Group: {group.get('groupId')} - {group.get('groupName')}")
