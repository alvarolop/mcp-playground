import json
import threading
import requests
from sseclient import SSEClient
import time

# --- Global State and Configuration ---
SERVER_URL = "http://localhost:3000"
SSE_URL = f"{SERVER_URL}/sse"
MESSAGES_URL = f"{SERVER_URL}/messages"
SESSION_ID = None
STOP_EVENT = threading.Event()
REQUEST_ID = 1 # A simple counter for JSON-RPC requests
EXPECTING_TOOL_NAMES = False  # Flag to track when we're expecting just tool names
EXPECTING_TOOL_INFO = False  # Flag to track when we're expecting tool info for filtering
REQUESTED_TOOL_NAME = None  # Store the requested tool name for filtering

# --- SSE Listener Thread ---
def sse_listener():
    """Listens for events on the SSE stream and handles the session."""
    global SESSION_ID, EXPECTING_TOOL_NAMES, EXPECTING_TOOL_INFO, REQUESTED_TOOL_NAME

    print("Connecting to SSE stream...")
    try:
        client = SSEClient(SSE_URL)
        for event in client:
            if STOP_EVENT.is_set():
                break

            event_data = event.data
            if not event_data:
                continue
            
            # The initial event to establish the session
            if event_data.startswith("/messages?sessionId="):
                session_id = event_data.split("=")[1]
                SESSION_ID = session_id
                print(f"Session established. Session ID: {SESSION_ID}")
                print("You can now send commands from the main thread.")
            else:
                try:
                    data = json.loads(event_data)
                    
                    # Check if this is a response to tools/list and we're expecting just names
                    if EXPECTING_TOOL_NAMES and 'result' in data and 'tools' in data['result']:
                        print("\n--- Tool Names ---")
                        for tool in data['result']['tools']:
                            print(f"• {tool['name']}")
                        print(f"Total: {len(data['result']['tools'])} tools")
                        EXPECTING_TOOL_NAMES = False
                    # Check if this is a response to tools/list and we're expecting tool info for filtering
                    elif EXPECTING_TOOL_INFO and 'result' in data and 'tools' in data['result']:
                        tool_found = False
                        for tool in data['result']['tools']:
                            if tool['name'] == REQUESTED_TOOL_NAME:
                                print(f"\n--- Tool Info for '{REQUESTED_TOOL_NAME}' ---")
                                print(json.dumps(tool, indent=2))
                                tool_found = True
                                break
                        
                        if not tool_found:
                            print(f"\nTool '{REQUESTED_TOOL_NAME}' not found.")
                        
                        EXPECTING_TOOL_INFO = False
                        REQUESTED_TOOL_NAME = None
                    else:
                        print(f"\n[EVENT RECEIVED]:\n{json.dumps(data, indent=2)}")
                        
                except json.JSONDecodeError:
                    print(f"\n[RAW EVENT RECEIVED]:\n{event_data}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to SSE stream: {e}")
        STOP_EVENT.set()
    finally:
        print("SSE listener stopped.")

# --- Command Sender Function ---
def send_command(method: str, params: dict):
    """Sends a JSON-RPC command via HTTP POST and returns the request ID."""
    global REQUEST_ID
    if not SESSION_ID:
        print("Error: No session ID available. Make sure the SSE listener is running.")
        return None

    payload = {
        "jsonrpc": "2.0",
        "id": REQUEST_ID,
        "method": method,
        "params": params,
    }

    try:
        response = requests.post(
            f"{MESSAGES_URL}?sessionId={SESSION_ID}",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        print(f"Command '{method}' sent successfully. Server response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending command: {e}")
    
    current_request_id = REQUEST_ID
    REQUEST_ID += 1
    return current_request_id

# --- New Functionality: List and Show Tool Info ---
def list_tool_names():
    """Lists only the names of available tools."""
    global EXPECTING_TOOL_NAMES
    print("Requesting tool names...")
    EXPECTING_TOOL_NAMES = True  # Set flag to expect tool names
    send_command("tools/list", {})

def show_tool_info(tool_name: str):
    """Shows detailed information for a specific tool by filtering the tools/list response."""
    global EXPECTING_TOOL_INFO, REQUESTED_TOOL_NAME
    print(f"Requesting info for tool: {tool_name}")
    EXPECTING_TOOL_INFO = True  # Set flag to expect tool info for filtering
    REQUESTED_TOOL_NAME = tool_name  # Store the requested tool name
    send_command("tools/list", {})  # Call tools/list and filter the response

# --- Main Application Logic ---
if __name__ == "__main__":
    listener_thread = threading.Thread(target=sse_listener)
    listener_thread.daemon = True
    listener_thread.start()

    while not SESSION_ID and not STOP_EVENT.is_set():
        time.sleep(1)

    if not SESSION_ID:
        print("Failed to establish session. Exiting.")
        exit()

    while not STOP_EVENT.is_set():
        print("\n--- Available Actions ---")
        print("1. List all tools with full info")
        print("2. List just the tool names")
        print("3. Show detailed info for one tool")
        print("4. Execute a tool")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            send_command("tools/list", {})
        elif choice == "2":
            list_tool_names()
        elif choice == "3":
            tool_name = input("Enter the tool name (e.g., 'list_applications'): ")
            show_tool_info(tool_name)
        elif choice == "4":
            tool_name = input("Enter the tool name to execute: ")
            params_input = input("Enter parameters as a JSON string (e.g., '{\"location\": \"New York\"}'): ")
            
            # Handle empty parameters gracefully
            if not params_input.strip():
                arguments = {}
                print("No parameters provided, using empty parameters.")
            else:
                try:
                    arguments = json.loads(params_input)
                except json.JSONDecodeError:
                    print("Invalid JSON format for parameters. Please try again.")
                    continue
            
            # Execute the tool using the correct MCP protocol format
            tool_params = {
                "name": tool_name,
                "arguments": arguments
            }
            send_command("tools/call", tool_params)
        elif choice == "5":
            print("Exiting...")
            STOP_EVENT.set()
        else:
            print("Invalid choice. Please try again.")

    listener_thread.join(timeout=5)
    print("Application finished.")