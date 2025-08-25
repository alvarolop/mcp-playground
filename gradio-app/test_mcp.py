#!/usr/bin/env python3
"""
Test script to verify MCP server connection
"""

import requests
import json
import os

# Configuration
KUBERNETES_MCP_URL = os.getenv("KUBERNETES_MCP_URL", "http://localhost:8080/mcp")

def test_mcp_connection():
    """Test MCP server connection"""
    print(f"🔍 Testing MCP connection to: {KUBERNETES_MCP_URL}")
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        health_response = requests.get("http://localhost:8080/health", timeout=5)
        print(f"   Health check: HTTP {health_response.status_code}")
        if health_response.status_code == 200:
            print("   ✅ Health endpoint accessible")
        else:
            print(f"   ⚠️ Health endpoint returned {health_response.status_code}")
    except Exception as e:
        print(f"   ❌ Health check failed: {str(e)}")
    
    # Test 2: Tools list
    print("\n2. Testing tools list...")
    try:
        tools_response = requests.post(
            KUBERNETES_MCP_URL,
            headers={"Content-Type": "application/json"},
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            },
            timeout=10
        )
        print(f"   Tools list: HTTP {tools_response.status_code}")
        
        if tools_response.status_code == 200:
            tools_data = tools_response.json()
            print("   ✅ Tools list successful")
            if "result" in tools_data and "tools" in tools_data["result"]:
                tools = tools_data["result"]["tools"]
                print(f"   📋 Found {len(tools)} tools:")
                for tool in tools[:5]:
                    print(f"      - {tool.get('name', 'Unknown')}")
                if len(tools) > 5:
                    print(f"      ... and {len(tools) - 5} more")
            else:
                print("   ⚠️ No tools found in response")
                print(f"   Response: {json.dumps(tools_data, indent=2)}")
        else:
            print(f"   ❌ Tools list failed: {tools_response.text}")
            
    except Exception as e:
        print(f"   ❌ Tools list failed: {str(e)}")
    
    # Test 3: Call a specific tool
    print("\n3. Testing pods_list tool...")
    try:
        pods_response = requests.post(
            KUBERNETES_MCP_URL,
            headers={"Content-Type": "application/json"},
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "pods_list",
                    "arguments": {"namespace": "default"}
                }
            },
            timeout=15
        )
        print(f"   Pods list: HTTP {pods_response.status_code}")
        
        if pods_response.status_code == 200:
            pods_data = pods_response.json()
            print("   ✅ Pods list successful")
            if "result" in pods_data:
                print("   📋 Pods data retrieved")
                # Print a sample of the data
                result = pods_data["result"]
                if isinstance(result, dict) and "content" in result:
                    content = result["content"]
                    if content and len(content) > 0:
                        print(f"   📄 Content type: {type(content[0])}")
                        if hasattr(content[0], 'get'):
                            print(f"   📄 Content keys: {list(content[0].keys())}")
            else:
                print("   ⚠️ No result in response")
                print(f"   Response: {json.dumps(pods_data, indent=2)}")
        else:
            print(f"   ❌ Pods list failed: {pods_response.text}")
            
    except Exception as e:
        print(f"   ❌ Pods list failed: {str(e)}")

if __name__ == "__main__":
    test_mcp_connection()
