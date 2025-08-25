#!/usr/bin/env python3
"""
Test script for the Intelligent CD Chatbot application.
"""

import sys
import os
import requests
import subprocess

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import gradio as gr
        print("✅ Gradio imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Gradio: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Requests: {e}")
        return False
    
    try:
        import json
        print("✅ JSON imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import JSON: {e}")
        return False
    
    print("✅ All imports successful")
    return True

def test_kubernetes_access():
    """Test Kubernetes cluster access."""
    print("\nTesting Kubernetes access...")
    
    try:
        # Test kubectl version
        result = subprocess.run(
            ["kubectl", "version", "--client"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ kubectl is available and working")
            print(f"   Version: {result.stdout.strip()}")
        else:
            print("❌ kubectl command failed")
            print(f"   Error: {result.stderr.strip()}")
            return False
            
    except FileNotFoundError:
        print("❌ kubectl not found in PATH")
        return False
    except subprocess.TimeoutExpired:
        print("❌ kubectl command timed out")
        return False
    except Exception as e:
        print(f"❌ Unexpected error testing kubectl: {e}")
        return False
    
    return True

def test_app_creation():
    """Test that the Gradio app can be created."""
    print("\nTesting app creation...")
    
    try:
        from main import create_demo
        app = create_demo()
        print("✅ Gradio app created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create Gradio app: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Intelligent CD Chatbot Application")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_kubernetes_access,
        test_app_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
