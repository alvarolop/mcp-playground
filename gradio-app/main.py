import gradio as gr
import requests
import json
import os
from typing import List, Dict, Any
import subprocess
import tempfile

# Configuration
KUBERNETES_MCP_URL = os.getenv("KUBERNETES_MCP_URL", "http://localhost:8080/mcp")
RAG_ENDPOINT = os.getenv("RAG_ENDPOINT", "http://localhost:8000")

# LLM Configuration from environment variables
OLS_PROVIDER_TYPE = os.getenv("OLS_PROVIDER_TYPE", "rhoai_vllm")
OLS_PROVIDER_MODEL_NAME = os.getenv("OLS_PROVIDER_MODEL_NAME", "granite-3-3-8b-instruct")
OLS_PROVIDER_API_URL = os.getenv("OLS_PROVIDER_API_URL", "https://granite-3-3-8b-instruct-maas-apicast-production.apps.prod.rhoai.rh-aiservices-bu.com:443/v1")
OLS_PROVIDER_API_TOKEN = os.getenv("OLS_PROVIDER_API_TOKEN", "e0b0143c4738a56aed654cb7db8ce682")

class KubernetesMCPClient:
    """Simple client for Kubernetes MCP operations"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def get_pods(self, namespace: str = "default") -> Dict[str, Any]:
        """Get pods from a namespace"""
        try:
            result = subprocess.run(
                ["kubectl", "get", "pods", "-n", namespace, "-o", "json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return {"success": True, "data": result.stdout}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_namespaces(self) -> Dict[str, Any]:
        """Get all namespaces"""
        try:
            result = subprocess.run(
                ["kubectl", "get", "namespaces", "-o", "json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return {"success": True, "data": result.stdout}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}

class LLMClient:
    """Client for interacting with the LLM API"""
    
    def __init__(self, api_url: str, api_token: str, model_name: str):
        self.api_url = api_url
        self.api_token = api_token
        self.model_name = model_name
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(self, message: str, context: str = "") -> Dict[str, Any]:
        """Send a chat completion request to the LLM"""
        try:
            # Prepare the prompt with context if provided
            if context:
                full_prompt = f"Context: {context}\n\nUser Question: {message}\n\nPlease provide a helpful response based on the context and your knowledge."
            else:
                full_prompt = message
            
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": "You are an intelligent assistant that helps with Kubernetes deployments, GitOps, and OpenShift configurations. Provide helpful, accurate, and practical advice."},
                    {"role": "user", "content": full_prompt}
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "response": result.get("choices", [{}])[0].get("message", {}).get("content", "No response generated"),
                    "model": self.model_name
                }
            else:
                return {
                    "success": False,
                    "error": f"API request failed with status {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }

# Initialize clients
k8s_client = KubernetesMCPClient(KUBERNETES_MCP_URL)
llm_client = LLMClient(OLS_PROVIDER_API_URL, OLS_PROVIDER_API_TOKEN, OLS_PROVIDER_MODEL_NAME)

def kubernetes_operations(namespace: str, operation: str) -> str:
    """Handle Kubernetes operations"""
    if operation == "get_pods":
        result = k8s_client.get_pods(namespace)
    elif operation == "get_namespaces":
        result = k8s_client.get_namespaces()
    else:
        return f"Unknown operation: {operation}"
    
    if result["success"]:
        return f"✅ Success:\n{result['data']}"
    else:
        return f"❌ Error:\n{result['error']}"

def system_status() -> str:
    """Get comprehensive system status with better structure"""
    
    # 1. Gradio Health
    gradio_status = "✅ Gradio Application: Running and accessible"
    
    # 2. LLM Health and Connection Details
    llm_status = []
    llm_status.append("🤖 LLM Service:")
    
    if OLS_PROVIDER_API_URL:
        llm_status.append(f"   • API URL: {OLS_PROVIDER_API_URL}")
        llm_status.append(f"   • Provider Type: {OLS_PROVIDER_TYPE}")
        llm_status.append(f"   • Model: {OLS_PROVIDER_MODEL_NAME}")
        
        # Test LLM connectivity
        try:
            test_response = requests.get(f"{OLS_PROVIDER_API_URL.replace('/v1', '')}/health", timeout=5)
            if test_response.status_code == 200:
                llm_status.append("   • Connection: ✅ Accessible")
            else:
                llm_status.append(f"   • Connection: ⚠️ Responding with status {test_response.status_code}")
        except Exception as e:
            llm_status.append(f"   • Connection: ❌ Error - {str(e)}")
    else:
        llm_status.append("   • Status: ❌ Not configured")
    
    # 3. MCP Health and Connection Details
    mcp_status = []
    mcp_status.append("☸️ MCP Server:")
    
    if KUBERNETES_MCP_URL:
        mcp_status.append(f"   • URL: {KUBERNETES_MCP_URL}")
        
        # Test MCP connectivity
        try:
            # Use base URL for health check (remove /mcp path)
            health_url = "http://localhost:8080"
            mcp_response = requests.get(f"{health_url}/health", timeout=5)
            if mcp_response.status_code == 200:
                mcp_status.append("   • Health: ✅ Responding")
                
                # Try to list tools
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
                    
                    if tools_response.status_code == 200:
                        tools_data = tools_response.json()
                        if "result" in tools_data and "tools" in tools_data["result"]:
                            tools = tools_data["result"]["tools"]
                            mcp_status.append(f"   • Tools Available: ✅ {len(tools)} tools")
                            mcp_status.append("   • Sample Tools:")
                            for tool in tools[:5]:  # Show first 5 tools
                                mcp_status.append(f"     - {tool.get('name', 'Unknown')}")
                            if len(tools) > 5:
                                mcp_status.append(f"     ... and {len(tools) - 5} more")
                        else:
                            mcp_status.append("   • Tools: ⚠️ Connected but no tools found")
                    else:
                        mcp_status.append(f"   • Tools: ❌ Failed to list tools (HTTP {tools_response.status_code})")
                        
                except Exception as e:
                    mcp_status.append(f"   • Tools: ❌ Error listing tools - {str(e)}")
                    
            else:
                mcp_status.append(f"   • Health: ❌ HTTP {mcp_response.status_code}")
                
        except requests.exceptions.ConnectionError:
            mcp_status.append("   • Health: ❌ Connection refused")
        except requests.exceptions.Timeout:
            mcp_status.append("   • Health: ⏰ Connection timeout")
        except Exception as e:
            mcp_status.append(f"   • Health: ❌ Error - {str(e)}")
    else:
        mcp_status.append("   • Status: ❌ Not configured")
    
    # 4. Kubernetes Access
    k8s_status = []
    k8s_status.append("🔧 Kubernetes Access:")
    
    try:
        kubectl_result = subprocess.run(
            ["kubectl", "version", "--client"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if kubectl_result.returncode == 0:
            k8s_status.append("   • kubectl: ✅ Available")
            k8s_status.append(f"   • Version: {kubectl_result.stdout.strip()}")
        else:
            k8s_status.append("   • kubectl: ❌ Command failed")
            k8s_status.append(f"   • Error: {kubectl_result.stderr.strip()}")
    except FileNotFoundError:
        k8s_status.append("   • kubectl: ❌ Not found in PATH")
    except Exception as e:
        k8s_status.append(f"   • kubectl: ❌ Error - {str(e)}")
    
    # Combine all status information
    full_status = "\n".join([
        "=" * 60,
        "SYSTEM STATUS REPORT",
        "=" * 60,
        "",
        gradio_status,
        "",
        "\n".join(llm_status),
        "",
        "\n".join(mcp_status),
        "",
        "\n".join(k8s_status),
        "",
        "=" * 60
    ])
    
    return full_status

def test_ocp_mcp() -> str:
    """Test OCP MCP Server connectivity"""
    try:
        # Use base URL for health check (remove /mcp path)
        health_url = "http://localhost:8080"
        response = requests.get(f"{health_url}/health", timeout=5)
        if response.status_code == 200:
            return "✅ OCP MCP Server is accessible and responding"
        else:
            return f"⚠️ OCP MCP Server responded with status: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to OCP MCP Server - connection refused"
    except requests.exceptions.Timeout:
        return "⏰ OCP MCP Server connection timed out"
    except Exception as e:
        return f"❌ Error testing OCP MCP Server: {str(e)}"

def list_mcp_tools() -> tuple:
    """List available MCP tools and update the tool selector"""
    print(f"🔍 [MCP DEBUG] Attempting to connect to MCP server at: {KUBERNETES_MCP_URL}")
    
    try:
        # Test connection first
        print(f"🔍 [MCP DEBUG] Testing connection to MCP server...")
        # Use base URL for health check (remove /mcp path)
        health_url = "http://localhost:8080"
        response = requests.get(f"{health_url}/health", timeout=5)
        print(f"🔍 [MCP DEBUG] Health check response: HTTP {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ [MCP DEBUG] Health check failed with status: {response.status_code}")
            return (
                '<div style="background: #ffebee; padding: 10px; border-radius: 5px; margin-bottom: 15px;"><strong>Status:</strong> <span style="color: #c62828;">❌ Cannot connect to MCP server</span></div>',
                ["Select a tool...", "No tools available"],
                "Select a tool..."
            )
        
        # List tools using MCP protocol
        print(f"🔍 [MCP DEBUG] Health check successful, attempting to list tools...")
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
        
        print(f"🔍 [MCP DEBUG] Tools list response: HTTP {tools_response.status_code}")
        
        if tools_response.status_code == 200:
            tools_data = tools_response.json()
            print(f"🔍 [MCP DEBUG] Tools response data: {json.dumps(tools_data, indent=2)}")
            
            if "result" in tools_data and "tools" in tools_data["result"]:
                tools = tools_data["result"]["tools"]
                tool_names = [tool.get("name", "Unknown") for tool in tools]
                print(f"🔍 [MCP DEBUG] Found {len(tool_names)} tools: {tool_names}")
                
                # Ensure the default value is always in the choices
                choices = ["Select a tool..."] + tool_names
                
                # Update status to success
                status_html = f'<div style="background: #e8f5e8; padding: 10px; border-radius: 5px; margin-bottom: 15px;"><strong>Status:</strong> <span style="color: #2e7d32;">✅ Connected to MCP server - {len(tool_names)} tools available</span></div>'
                
                return status_html, choices, "Select a tool..."
            else:
                print(f"⚠️ [MCP DEBUG] No tools found in response: {tools_data}")
                return (
                    '<div style="background: #fff3e0; padding: 10px; border-radius: 5px; margin-bottom: 15px;"><strong>Status:</strong> <span style="color: #ef6c00;">⚠️ Connected but no tools found</span></div>',
                    ["Select a tool...", "No tools available"],
                    "Select a tool..."
                )
        else:
            print(f"❌ [MCP DEBUG] Tools list failed with status: {tools_response.status_code}")
            print(f"🔍 [MCP DEBUG] Response content: {tools_response.text}")
            return (
                f'<div style="background: #ffebee; padding: 10px; border-radius: 5px; margin-bottom: 15px;"><strong>Status:</strong> <span style="color: #c62828;">❌ Failed to list tools: {tools_response.status_code}</span></div>',
                ["Select a tool...", "No tools available"],
                "Select a tool..."
            )
            
    except Exception as e:
        print(f"❌ [MCP DEBUG] Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return (
            f'<div style="background: #ffebee; padding: 10px; border-radius: 5px; margin-bottom: 15px;"><strong>Status:</strong> <span style="color: #c62828;">❌ Error: {str(e)}</span></div>',
            ["Select a tool...", "No tools available"],
            "Select a tool..."
        )

def execute_mcp_tool(tool_name: str, params_json: str) -> str:
    """Execute an MCP tool with the given parameters"""
    if tool_name == "Select a tool..." or not tool_name:
        return "❌ Please select a tool first"
    
    try:
        # Parse parameters
        try:
            params = json.loads(params_json) if params_json.strip() else {}
        except json.JSONDecodeError:
            return "❌ Invalid JSON parameters. Please check your input."
        
        # Execute tool using MCP protocol
        response = requests.post(
            KUBERNETES_MCP_URL,
            headers={"Content-Type": "application/json"},
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": params
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result_data = response.json()
            if "result" in result_data:
                # Format the result nicely
                formatted_result = json.dumps(result_data["result"], indent=2)
                return f"✅ Tool '{tool_name}' executed successfully:\n\n```json\n{formatted_result}\n```"
            elif "error" in result_data:
                return f"❌ Tool '{tool_name}' failed:\n\n```json\n{json.dumps(result_data['error'], indent=2)}\n```"
            else:
                return f"⚠️ Tool '{tool_name}' returned unexpected response:\n\n```json\n{json.dumps(result_data, indent=2)}\n```"
        else:
            return f"❌ HTTP Error {response.status_code}: {response.text}"
            
    except requests.exceptions.Timeout:
        return f"⏰ Tool '{tool_name}' execution timed out"
    except Exception as e:
        return f"❌ Error executing tool '{tool_name}': {str(e)}"

def chat_with_llm(message: str, chat_history: List[Dict[str, str]]) -> tuple:
    """Handle chat with LLM, enriched with MCP data"""
    if not message.strip():
        return chat_history, ""
    
    # Add user message to history
    chat_history.append({"role": "user", "content": message})
    
    # Check if the message is asking for Kubernetes information
    kubernetes_keywords = ['pod', 'pods', 'deployment', 'deployments', 'service', 'services', 'namespace', 'namespaces', 'cluster', 'kubernetes', 'k8s', 'node', 'nodes']
    is_kubernetes_query = any(keyword in message.lower() for keyword in kubernetes_keywords)
    
    if is_kubernetes_query:
        # Use MCP to gather Kubernetes data
        try:
            print(f"🔍 [MCP CHAT] Detected Kubernetes query: {message}")
            
            # Get available tools first
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
            
            if tools_response.status_code == 200:
                tools_data = tools_response.json()
                if "result" in tools_data and "tools" in tools_data["result"]:
                    tools = tools_data["result"]["tools"]
                    print(f"🔍 [MCP CHAT] Found {len(tools)} MCP tools")
                    
                    # Try to get relevant data based on the query
                    kubernetes_data = {}
                    
                    # Check for pods query
                    if any(word in message.lower() for word in ['pod', 'pods']):
                        try:
                            # Determine namespace from message or use default
                            namespace = "default"
                            if "namespace" in message.lower():
                                # Simple extraction - could be improved
                                if "default" in message.lower():
                                    namespace = "default"
                                elif "kube-system" in message.lower():
                                    namespace = "kube-system"
                            
                            pods_response = requests.post(
                                KUBERNETES_MCP_URL,
                                headers={"Content-Type": "application/json"},
                                json={
                                    "jsonrpc": "2.0",
                                    "id": 2,
                                    "method": "tools/call",
                                    "params": {
                                        "name": "pods_list",
                                        "arguments": {"namespace": namespace}
                                    }
                                },
                                timeout=15
                            )
                            
                            if pods_response.status_code == 200:
                                pods_data = pods_response.json()
                                if "result" in pods_data:
                                    kubernetes_data["pods"] = pods_data["result"]
                                    print(f"🔍 [MCP CHAT] Retrieved pods data for namespace: {namespace}")
                        except Exception as e:
                            print(f"⚠️ [MCP CHAT] Error getting pods: {str(e)}")
                    
                    # Check for namespaces query
                    if any(word in message.lower() for word in ['namespace', 'namespaces']):
                        try:
                            namespaces_response = requests.post(
                                KUBERNETES_MCP_URL,
                                headers={"Content-Type": "application/json"},
                                json={
                                    "jsonrpc": "2.0",
                                    "id": 3,
                                    "method": "tools/call",
                                    "params": {
                                        "name": "namespaces_list",
                                        "arguments": {}
                                    }
                                },
                                timeout=15
                            )
                            
                            if namespaces_response.status_code == 200:
                                namespaces_data = namespaces_response.json()
                                if "result" in namespaces_data:
                                    kubernetes_data["namespaces"] = namespaces_data["result"]
                                    print(f"🔍 [MCP CHAT] Retrieved namespaces data")
                        except Exception as e:
                            print(f"⚠️ [MCP CHAT] Error getting namespaces: {str(e)}")
                    
                    # Enhance the prompt with Kubernetes data
                    if kubernetes_data:
                        enhanced_prompt = f"""
User Question: {message}

Kubernetes Cluster Data (retrieved via MCP):
{json.dumps(kubernetes_data, indent=2)}

Please provide a helpful response based on this real-time Kubernetes data and your knowledge. Format the response to be clear and actionable.
"""
                        print(f"🔍 [MCP CHAT] Enhanced prompt with Kubernetes data")
                    else:
                        enhanced_prompt = message
                        print(f"🔍 [MCP CHAT] No Kubernetes data retrieved, using original prompt")
                        
                else:
                    print(f"⚠️ [MCP CHAT] No tools found in MCP response")
                    enhanced_prompt = message
            else:
                print(f"⚠️ [MCP CHAT] Failed to get MCP tools: {tools_response.status_code}")
                enhanced_prompt = message
                
        except Exception as e:
            print(f"❌ [MCP CHAT] Error in MCP integration: {str(e)}")
            enhanced_prompt = message
    else:
        enhanced_prompt = message
    
    # Get LLM response with enhanced prompt
    result = llm_client.chat_completion(enhanced_prompt)
    
    if result["success"]:
        response = result["response"]
        chat_history.append({"role": "assistant", "content": response})
        return chat_history, ""
    else:
        error_msg = f"❌ Error: {result['error']}"
        chat_history.append({"role": "assistant", "content": error_msg})
        return chat_history, ""

def create_demo():
    """Create the beautiful Gradio interface with header and chat"""
    
    with gr.Blocks(
        title="Intelligent CD Chatbot",
        theme=gr.themes.Soft(),  # Fixed light theme - no dark mode switching
        css="""
        .gradio-container {
            max-width: 1400px !important;
        }
        .header-container {
            background: linear-gradient(135deg, #ff8c42 0%, #ffa726 50%, #ff7043 100%);
            color: white;
            padding: 20px;
            border-radius: 0 0 15px 15px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .header-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .header-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .logo {
            width: 50px;
            height: 50px;
            border-radius: 10px;
        }
        .header-title {
            font-size: 2.2em;
            font-weight: bold;
            margin: 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        .header-subtitle {
            font-size: 1.1em;
            opacity: 0.95;
            margin: 5px 0 0 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        .header-right {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .top-controls {
            display: flex;
            gap: 10px;
            align-items: center;
            justify-content: flex-end;
            margin-bottom: 20px;
        }
        .chat-area {
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            padding: 20px;
            background: #f8f9fa;
            height: 600px;
            overflow-y: auto;
        }
        .code-canvas {
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            padding: 20px;
            background: #f8f9fa;
            min-height: 600px;
            overflow-y: auto;
        }
        .chat-input {
            margin-top: 20px;
        }
        """
    ) as demo:
        
        # Beautiful Header with Logo
        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML("""
                <div class="header-container">
                    <div class="header-content">
                        <div class="header-left">
                            <svg class="logo" version="1.0" xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 300 300" preserveAspectRatio="xMidYMid meet">
                                <g transform="translate(0.000000,300.000000) scale(0.100000,-0.100000)" fill="currentColor" stroke="none">
                                    <path d="M1470 2449 c-47 -10 -80 -53 -80 -105 0 -45 26 -88 61 -99 18 -6 19 -14 17 -138 l-3 -132 -37 -3 -38 -3 0 48 c0 43 -4 53 -34 82 -32 31 -35 38 -33 87 2 46 -2 57 -27 83 -36 38 -74 46 -120 27 -70 -29 -86 -125 -30 -177 20 -19 36 -24 79 -24 70 0 95 -22 95 -82 l0 -43 -162 0 c-108 -1 -175 -5 -200 -14 -98 -35 -168 -134 -178 -250 l-5 -69 -44 -11 c-69 -17 -85 -47 -90 -164 -5 -147 17 -194 102 -211 l32 -7 5 -80 c4 -64 11 -90 36 -134 50 -88 141 -140 247 -140 l47 0 0 -135 c0 -122 2 -137 20 -155 11 -11 29 -20 40 -20 21 0 31 8 233 193 l129 117 226 0 c125 0 244 5 264 10 62 18 128 71 162 130 25 44 32 70 36 134 l5 79 44 11 c74 18 86 45 86 186 0 141 -12 168 -86 186 l-44 11 -6 74 c-10 113 -58 187 -153 234 -47 24 -59 25 -218 25 l-168 0 0 40 c0 53 38 91 85 83 60 -10 125 46 125 107 0 38 -30 81 -67 96 -45 19 -83 11 -119 -27 -25 -26 -29 -37 -27 -83 2 -49 -1 -56 -33 -87 -30 -29 -34 -39 -34 -82 l0 -48 -37 3 -38 3 -3 132 c-2 124 -1 132 17 138 35 11 61 54 61 99 0 75 -62 122 -140 105z m65 -79 c27 -30 7 -70 -35 -70 -42 0 -62 40 -35 70 10 11 26 20 35 20 9 0 25 -9 35 -20z m-281 -152 c16 -26 -4 -53 -40 -53 -23 0 -30 5 -32 23 -7 47 47 69 72 30z m556 8 c6 -8 10 -25 8 -38 -6 -42 -78 -32 -78 11 0 37 46 55 70 27z m-4 -376 c182 0 193 -1 225 -23 19 -12 44 -42 57 -67 21 -43 22 -54 22 -330 0 -276 -1 -287 -22 -330 -13 -25 -38 -55 -57 -67 -33 -22 -41 -23 -288 -23 l-253 0 -91 -82 c-50 -46 -109 -98 -130 -116 l-39 -34 0 96 c0 130 -6 136 -134 136 -111 0 -147 18 -183 90 -22 43 -23 54 -23 330 0 277 1 287 23 330 25 50 60 79 106 89 17 3 159 5 314 3 155 -1 368 -2 473 -2z"/>
                                    <path d="M1159 1621 c-80 -80 12 -215 114 -166 52 24 74 79 53 129 -30 71 -114 90 -167 37z"/>
                                    <path d="M1702 1625 c-60 -50 -47 -142 24 -171 45 -19 78 -12 115 26 90 89 -42 226 -139 145z"/>
                                    <path d="M1280 1269 c-10 -17 -6 -25 25 -54 91 -86 299 -86 390 0 31 29 35 37 25 54 -15 28 -31 26 -95 -10 -47 -26 -65 -31 -125 -31 -59 0 -78 5 -127 31 -67 37 -79 38 -93 10z"/>
                                </g>
                            </svg>
                            <div>
                                <div class="header-title">Intelligent CD Chatbot</div>
                                <div class="header-subtitle">AI-Powered GitOps Deployment Assistant</div>
                            </div>
                        </div>
                        <div class="header-right">
                            <div style="font-size: 0.9em; opacity: 0.8;">
                                Powered by <strong>Red Hat AI</strong>
                            </div>
                        </div>
                    </div>
                </div>
                """)
        
        # Top Right Controls
        with gr.Row():
            with gr.Column(scale=1):
                pass  # Left spacer
            with gr.Column(scale=1):
                with gr.Row():
                    # Test OCP MCP Server Button
                    test_mcp_btn = gr.Button("🧪 Test OCP MCP Server", variant="secondary")
        
        # Main Content Area - Two Columns
        with gr.Row():
            # Left Column - Chatbot (40%)
            with gr.Column(scale=2):
                # Tab system for different interfaces
                with gr.Tabs():
                    # Chat Tab
                    with gr.TabItem("💬 Chat"):
                        # Chat Interface
                        chatbot = gr.Chatbot(
                            label="💬 Chat with AI Assistant",
                            height=500,
                            show_label=True,
                            type="messages"
                        )
                        
                        # Chat Input
                        with gr.Row():
                            msg = gr.Textbox(
                                label="Message",
                                placeholder="Ask me about Kubernetes, GitOps, or OpenShift deployments... (Press Enter to send, Shift+Enter for new line)",
                                lines=1,
                                scale=4
                            )
                            send_btn = gr.Button("Send", variant="primary", scale=1)
                        
                        # Clear button
                        clear_btn = gr.Button("Clear Chat", variant="secondary")
                    
                    # MCP Test Tab
                    with gr.TabItem("🧪 MCP Test"):
                        # Status Bar
                        status_indicator = gr.HTML(
                            '<div style="background: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 15px;"><strong>Status:</strong> <span style="color: #666;">Ready to test MCP server</span></div>',
                            label="Status"
                        )
                        
                        # Tool Selector
                        tool_selector = gr.Dropdown(
                            choices=["Select a tool..."],
                            label="Select MCP Tool",
                            value="Select a tool...",
                            interactive=True
                        )
                        
                        # Parameters Section
                        with gr.Group():
                            gr.Markdown("**Parameters:**")
                            params_input = gr.Textbox(
                                label="Parameters (JSON)",
                                placeholder='{"namespace": "default"}',
                                lines=3,
                                value='{}'
                            )
                        
                        # Execute Button
                        execute_btn = gr.Button("Execute Tool", variant="primary", size="lg")
                        
                        # Refresh Tools Button
                        refresh_btn = gr.Button("🔄 Refresh Tools", variant="secondary")
                        
                        # Auto-load tools when tab is selected
                        gr.on(
                            triggers=gr.TabItem("🧪 MCP Test").select,
                            fn=list_mcp_tools,
                            outputs=[status_indicator, tool_selector, tool_selector]
                        )
                    
                    # System Status Tab
                    with gr.TabItem("🔍 System Status"):
                        # Status display area
                        status_display = gr.HTML(
                            '<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0;"><h3>🔍 System Status</h3><p>Click "Check System Status" to view detailed system information...</p></div>',
                            label="System Status"
                        )
                        
                        # Check Status Button
                        check_status_btn = gr.Button("Check System Status", variant="primary", size="lg")
            
            # Right Column - Code Canvas (60%)
            with gr.Column(scale=3):
                # Dynamic content area for System Status, MCP Test results, and other content
                content_area = gr.HTML(
                    '<div class="code-canvas"><h3>📝 Code Canvas</h3><p>Click a button above to see results here, or chat with the AI to generate deployment manifests...</p></div>',
                    label="Content Area"
                )
        
        # Event handlers
        test_mcp_btn.click(
            fn=lambda: f'<div class="code-canvas"><h3>🧪 Test OCP MCP Server</h3><pre>MCP server is integrated into the chat functionality. Ask questions about your Kubernetes cluster in the Chat tab!</pre></div>',
            outputs=content_area
        )
        
        # MCP Test Tab functionality
        refresh_btn.click(
            fn=list_mcp_tools,
            outputs=[status_indicator, tool_selector, tool_selector]
        )
        
        execute_btn.click(
            fn=lambda tool_name, params: f'<div class="code-canvas"><h3>🧪 MCP Tool Execution: {tool_name}</h3><pre>{execute_mcp_tool(tool_name, params)}</pre></div>',
            inputs=[tool_selector, params_input],
            outputs=content_area
        )
        
        # System Status Tab functionality
        check_status_btn.click(
            fn=lambda: f'<div class="code-canvas"><h3>🔍 System Status</h3><pre>{system_status()}</pre></div>',
            outputs=status_display
        )
        
        # Chat functionality
        send_btn.click(
            fn=chat_with_llm,
            inputs=[msg, chatbot],
            outputs=[chatbot, msg]
        )
        
        # Handle Enter key to send message
        msg.submit(
            fn=chat_with_llm,
            inputs=[msg, chatbot],
            outputs=[chatbot, msg]
        )
        
        clear_btn.click(
            fn=lambda: ([], ""),
            outputs=[chatbot, msg]
        )
    
    return demo

def main():
    """Main function to launch the Gradio app"""
    demo = create_demo()
    
    # Launch the app
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True,
        show_error=True
    )

if __name__ == "__main__":
    main()
