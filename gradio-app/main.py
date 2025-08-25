import gradio as gr
import json
import os
import sys
from typing import List, Dict, Any
from llama_stack_client import LlamaStackClient

# Llama Stack Configuration
LLAMA_STACK_URL = os.getenv("LLAMA_STACK_URL", "http://localhost:8321")
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "granite-3-3-8b-instruct")

class ChatTab:
    """Handles chat functionality with Llama Stack LLM"""
    
    def __init__(self, client: LlamaStackClient):
        self.client = client
    
    def chat_completion(self, message: str, chat_history: List[Dict[str, str]]) -> tuple:
        """Handle chat with LLM"""
        if not message.strip():
            return chat_history, ""
        
        # Add user message to history
        chat_history.append({"role": "user", "content": message})
        
        # For now, just use the original message without MCP enhancement
        enhanced_prompt = message
        
        # Get LLM response with enhanced prompt
        result = self.chat_completion_simple(enhanced_prompt)
        
        if result["success"]:
            response = result["response"]
            chat_history.append({"role": "assistant", "content": response})
            return chat_history, ""
        else:
            error_msg = f"❌ Error: {result['error']}"
            chat_history.append({"role": "assistant", "content": error_msg})
            return chat_history, ""
    
    def chat_completion_simple(self, message: str) -> Dict[str, Any]:
        """Send a chat completion request to the Llama Stack LLM"""
        if not self.client:
            return {
                "success": False,
                "error": "Llama Stack LLM client not initialized"
            }
        
        try:
            # Prepare the prompt
            full_prompt = message
            
            # Use Llama Stack for chat completion
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an intelligent assistant that helps with Kubernetes deployments, GitOps, and OpenShift configurations. Provide helpful, accurate, and practical advice."},
                    {"role": "user", "content": full_prompt}
                ],
                model=DEFAULT_LLM_MODEL,
                temperature=0.7,
                max_tokens=1000
            )
            
            return {
                "success": True,
                "response": response.choices[0].message.content,
                "model": "Llama Stack LLM"
            }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Llama Stack LLM error: {str(e)}"
            }


class MCPTestTab:
    """Handles MCP testing functionality with Llama Stack"""
    
    def __init__(self, client: LlamaStackClient):
        self.client = client
    
    def list_toolgroups(self) -> gr.update:
        """List available MCP toolgroups through Llama Stack"""
        print(f"🔍 [MCP DEBUG] Attempting to list MCP toolgroups through Llama Stack...")
        
        # Use the shared client to get tools (which contain toolgroups)
        tools = self.client.tools.list()
        
        # Extract unique toolgroup IDs from tools
        toolgroups = list(set(tool.toolgroup_id for tool in tools))
        print(f"🔍 [MCP DEBUG] Found {len(toolgroups)} toolgroups: {toolgroups}")
        
        return gr.update(choices=toolgroups, value=None)
    
    def get_toolgroup_methods(self, toolgroup_name: str) -> tuple[str, gr.update]:
        """Get methods for a specific toolgroup through Llama Stack"""
        if not toolgroup_name:
            return (
                '<div style="background: #ffebee; padding: 10px; border-radius: 5px; margin-bottom: 15px;"><strong>Status:</strong> <span style="color: #c62828;">❌ Please select a toolgroup first</span></div>',
                gr.update(choices=[], value=None)
            )
        
        print(f"🔍 [MCP DEBUG] Getting methods for toolgroup: {toolgroup_name}")
        
        # Use the shared client to get tools for the specific toolgroup
        tools = self.client.tools.list()
        
        # Filter tools by toolgroup and extract individual tools
        methods = []
        for tool in tools:
            if hasattr(tool, 'toolgroup_id') and tool.toolgroup_id == toolgroup_name:
                # Check if this tool has individual tools/methods
                if hasattr(tool, 'tools') and tool.tools:
                    # Tool contains individual methods
                    for individual_tool in tool.tools:
                        method_name = getattr(individual_tool, 'name', getattr(individual_tool, 'identifier', 'Unknown'))
                        methods.append(method_name)
                else:
                    # This is a direct tool
                    method_name = getattr(tool, 'name', getattr(tool, 'identifier', 'Unknown'))
                    methods.append(method_name)
        
        print(f"🔍 [MCP DEBUG] Found {len(methods)} methods: {methods}")
        
        # Update status to success
        status_html = f'<div style="background: #e8f5e8; padding: 10px; border-radius: 5px; margin-bottom: 15px;"><strong>Status:</strong> <span style="color: #2e7d32;">✅ Found {len(methods)} methods in toolgroup "{toolgroup_name}"</span></div>'
        
        return status_html, gr.update(choices=methods, value=None)
    
    def execute_tool(self, toolgroup_name: str, method_name: str, params_json: str) -> str:
        """Execute an MCP tool through Llama Stack using toolgroup and method"""
        if not toolgroup_name:
            return "❌ Please select a toolgroup first"
        
        if not method_name:
            return "❌ Please select a method first"
        
        try:
            # Parse parameters
            try:
                params = json.loads(params_json) if params_json.strip() else {}
            except json.JSONDecodeError:
                return "❌ Invalid JSON parameters. Please check your input."
            
            # Execute tool through Llama Stack using tool_runtime
            result = self.client.tool_runtime.invoke_tool(
                tool_name=method_name,
                kwargs=params
            )
            
            if result:
                # Extract the actual result data from ToolInvocationResult
                try:
                    # Handle ToolInvocationResult structure
                    if hasattr(result, 'content') and result.content:
                        # Extract text from TextContentItem objects
                        if isinstance(result.content, list):
                            text_parts = []
                            for item in result.content:
                                if hasattr(item, 'text'):
                                    text_parts.append(item.text)
                                else:
                                    text_parts.append(str(item))
                            result_data = '\n'.join(text_parts)
                        else:
                            result_data = str(result.content)
                    elif hasattr(result, 'text'):
                        result_data = result.text
                    elif hasattr(result, 'data'):
                        result_data = result.data
                    else:
                        # Fallback: convert to string representation
                        result_data = str(result)
                    
                    # Try to format as JSON if it's a dict/list, otherwise use string
                    if isinstance(result_data, (dict, list)):
                        formatted_result = json.dumps(result_data, indent=2)
                    else:
                        formatted_result = str(result_data)
                        
                    return f"✅ Method '{method_name}' from toolgroup '{toolgroup_name}' executed successfully:\n\n```\n{formatted_result}\n```"
                except Exception as format_error:
                    # If JSON formatting fails, return as string
                    return f"✅ Method '{method_name}' from toolgroup '{toolgroup_name}' executed successfully:\n\n```\n{str(result)}\n```"
            else:
                return f"❌ Method '{method_name}' from toolgroup '{toolgroup_name}' failed: No result returned"
                
        except Exception as e:
            return f"❌ Error executing method '{method_name}' from toolgroup '{toolgroup_name}': {str(e)}"


class SystemStatusTab:
    """Handles system status functionality"""
    
    def __init__(self, client: LlamaStackClient, llama_stack_url: str):
        self.client = client
        self.llama_stack_url = llama_stack_url
    
    def get_system_status(self) -> str:
        """Get comprehensive system status with better structure"""
        
        # 1. Gradio Health
        gradio_status = "✅ Gradio Application: Running and accessible"
        
        # 2. Llama Stack Server Health and Version
        llama_stack_status = []
        llama_stack_status.append("🚀 Llama Stack Server:")
        llama_stack_status.append(f"   • URL: {self.llama_stack_url}")
        
        try:
            # Get version information
            version_info = self.client.inspect.version()
            llama_stack_status.append(f"   • Version: ✅ {version_info.version}")
            
            # Get health information
            health_info = self.client.inspect.health()
            llama_stack_status.append(f"   • Health: ✅ {health_info.status}")
            
        except Exception as e:
            llama_stack_status.append("   • Status: ❌ Failed to connect to Llama Stack server")
            llama_stack_status.append(f"   • Error: {str(e)}")
        
        # 3. LLM Service (Inference)
        llm_status = []
        llm_status.append("🤖 LLM Service (Inference):")
        
        try:
            # Test LLM connectivity with the correct model name
            test_response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello, this is a test message."}
                ],
                model=DEFAULT_LLM_MODEL,
                temperature=0.7,
                max_tokens=100
            )
            llm_status.append("   • Status: ✅ LLM service responding")
            llm_status.append(f"   • Model: {DEFAULT_LLM_MODEL}")
            llm_status.append(f"   • Response: ✅ Received {len(test_response.choices[0].message.content)} characters")
            
        except Exception as e:
            llm_status.append("   • Status: ❌ Failed to connect to LLM service")
            llm_status.append(f"   • Error: {str(e)}")
        
        # 4. MCP Server
        mcp_status = []
        mcp_status.append("☸️ MCP Server:")
        
        try:
            # List tools to check MCP server connectivity
            tools = self.client.tools.list()
            
            if tools:
                # Extract unique toolgroup IDs
                toolgroups = list(set(tool.toolgroup_id for tool in tools))
                mcp_status.append("   • Status: ✅ MCP server responding")
                mcp_status.append(f"   • Toolgroups: ✅ Found {len(toolgroups)} toolgroup(s)")
                
                # List all toolgroup identifiers as a simple list
                if toolgroups:
                    mcp_status.append("   • Toolgroup IDs:")
                    for toolgroup_id in toolgroups:
                        mcp_status.append(f"      - {toolgroup_id}")
            else:
                mcp_status.append("   • Status: ⚠️ MCP server responding but no toolgroups found")
                mcp_status.append("   • Toolgroups: 0")
                
        except Exception as e:
            mcp_status.append("   • Status: ❌ Failed to connect to MCP server")
            mcp_status.append(f"   • Error: {str(e)}")
        
        # Combine all status information
        full_status = "\n".join([
            "=" * 60,
            "SYSTEM STATUS REPORT",
            "=" * 60,
            "",
            gradio_status,
            "",
            "\n".join(llama_stack_status),
            "",
            "\n".join(llm_status),
            "",
            "\n".join(mcp_status),
            "",
            "=" * 60
        ])
        
        return full_status


def initialize_llama_stack_client() -> tuple[LlamaStackClient, ChatTab, MCPTestTab, SystemStatusTab]:
    """Initialize Llama Stack client and all tab classes"""
    try:
        print(f"🔧 Initializing Llama Stack client with URL: {LLAMA_STACK_URL}")
        llama_stack_client = LlamaStackClient(base_url=LLAMA_STACK_URL)
        print(f"✅ Llama Stack client initialized successfully with URL: {LLAMA_STACK_URL}")
        
        # Initialize tab classes with shared client
        chat_tab = ChatTab(llama_stack_client)
        mcp_test_tab = MCPTestTab(llama_stack_client)
        system_status_tab = SystemStatusTab(llama_stack_client, LLAMA_STACK_URL)
        
        print("✅ All tab classes initialized successfully")
        return llama_stack_client, chat_tab, mcp_test_tab, system_status_tab
        
    except Exception as e:
        print(f"❌ Failed to initialize Llama Stack client: {e}")
        print("❌ Llama Stack client is not available. Application cannot start.")
        print("💡 Please ensure the Llama Stack server is running and accessible.")
        sys.exit(1)


def create_demo(chat_tab: ChatTab, mcp_test_tab: MCPTestTab, system_status_tab: SystemStatusTab):
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
            height: 500px;
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
        
        # Top Right Controls - Removed for cleaner interface
        
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
                            height=300,
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
                        
                        # Toolgroup Selector with Refresh Button
                        with gr.Row():
                            refresh_toolgroups_btn = gr.Button("🔄ToolGroups", variant="secondary", size="md", scale=1)
                            refresh_methods_btn = gr.Button("🔄Methods", variant="secondary", size="md", scale=1)

                        toolgroup_selector = gr.Dropdown(
                            choices=["Select a toolgroup..."],
                            label="Select Toolgroup",
                            value="Select a toolgroup...",
                            interactive=True
                        )

                        method_selector = gr.Dropdown(
                            choices=["Select a method..."],
                            label="Select Method",
                            value="Select a method...",
                            interactive=True
                        )

                        
                        # Parameters Section
                        with gr.Group():
                            # gr.Markdown("**Parameters:**")
                            params_input = gr.Textbox(
                                label="Parameters (JSON)",
                                placeholder='{"namespace": "default"}',
                                lines=3,
                                value='{}'
                            )
                        
                        # Execute Button
                        execute_btn = gr.Button("Execute Method", variant="primary", size="lg")
                    
                    # System Status Tab
                    with gr.TabItem("🔍 System Status"):
                        # Check Status Button
                        check_status_btn = gr.Button("Check System Status", variant="primary", size="lg")
                        
                        # Note for user
                        gr.Markdown("Click the button above to view detailed system information in the right panel.")
            
            # Right Column - Code Canvas (60%)
            with gr.Column(scale=3):
                # Dynamic content area for System Status, MCP Test results, and other content
                content_area = gr.HTML(
                    '<div class="code-canvas"><h3>📝 Code Canvas</h3><p>Click a button above to see results here, or chat with the AI to generate deployment manifests...</p></div>',
                    label="Content Area"
                )
        
        # Event handlers     
        # Refresh Toolgroups Button (next to dropdown)
        refresh_toolgroups_btn.click(
            fn=mcp_test_tab.list_toolgroups,
            outputs=[toolgroup_selector]
        )
        
        # Refresh Methods Button
        refresh_methods_btn.click(
            fn=mcp_test_tab.get_toolgroup_methods,
            inputs=[toolgroup_selector],
            outputs=[status_indicator, method_selector]
        )
        
        execute_btn.click(
            fn=lambda toolgroup, method, params: f'<div class="code-canvas"><h3>🧪 MCP Method Execution: {method}</h3><pre>{mcp_test_tab.execute_tool(toolgroup, method, params)}</pre></div>',
            inputs=[toolgroup_selector, method_selector, params_input],
            outputs=content_area
        )
        
        # System Status Tab functionality
        check_status_btn.click(
            fn=lambda: f'<div class="code-canvas"><h3>🔍 System Status</h3><pre>{system_status_tab.get_system_status()}</pre></div>',
            outputs=content_area
        )
        
        # Chat functionality
        send_btn.click(
            fn=chat_tab.chat_completion,
            inputs=[msg, chatbot],
            outputs=[chatbot, msg]
        )
        
        # Handle Enter key to send message
        msg.submit(
            fn=chat_tab.chat_completion,
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
    # Initialize Llama Stack client and tab classes
    llama_stack_client, chat_tab, mcp_test_tab, system_status_tab = initialize_llama_stack_client()
    
    # Create the Gradio demo with tab instances
    demo = create_demo(chat_tab, mcp_test_tab, system_status_tab)
    
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
