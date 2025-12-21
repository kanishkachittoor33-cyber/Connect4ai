#!/usr/bin/env python3
"""
Script to test all GPT clients using BAML's Client Registry feature.
This script iterates through each GPT client and makes a test call.
"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from baml_client import b
from baml_py import ClientRegistry


# Define all GPT clients with their configurations
GPT_CLIENTS = [
    {
        "name": "Gpt35OpenRouter",
        "provider": "openai-generic",
        "options": {
            "base_url": "https://openrouter.ai/api/v1",
            "api_key": os.environ.get("OPENROUTER_API_KEY"),
            "model": "openai/gpt-3.5-turbo"
        }
    },
    {
        "name": "Gpt5OpenRouter",
        "provider": "openai-generic",
        "options": {
            "base_url": "https://openrouter.ai/api/v1",
            "api_key": os.environ.get("OPENROUTER_API_KEY"),
            "model": "openai/gpt-5"
        }
    },
    {
        "name": "Gptossn41OpenRouter",
        "provider": "openai-generic",
        "options": {
            "base_url": "https://openrouter.ai/api/v1",
            "api_key": os.environ.get("OPENROUTER_API_KEY"),
            "model": "openai/gpt-oss-120b"
        }
    },
    {
        "name": "Gpt4oOpenRouter",
        "provider": "openai-generic",
        "options": {
            "base_url": "https://openrouter.ai/api/v1",
            "api_key": os.environ.get("OPENROUTER_API_KEY"),
            "model": "openai/gpt-4o"
        }
    },
    {
        "name": "CustomGPT5",
        "provider": "openai-responses",
        "options": {
            "model": "gpt-5",
            "api_key": os.environ.get("OPENAI_API_KEY")
        }
    },
    {
        "name": "CustomGPT5Mini",
        "provider": "openai-responses",
        "options": {
            "model": "gpt-5-mini",
            "api_key": os.environ.get("OPENAI_API_KEY")
        }
    },
    {
        "name": "CustomGPT5Chat",
        "provider": "openai",
        "options": {
            "model": "gpt-5",
            "api_key": os.environ.get("OPENAI_API_KEY")
        }
    }
]


def test_client_sync(client_name, provider, options):
    """Test a client synchronously using Client Registry"""
    print(f"\n{'='*60}")
    print(f"Testing client: {client_name}")
    print(f"Provider: {provider}")
    print(f"Model: {options.get('model', 'N/A')}")
    print(f"{'='*60}")
    
    # Check if API key is available
    if 'api_key' in options and not options['api_key']:
        print(f"⚠️  Skipping {client_name}: API key not found in environment")
        return False
    
    try:
        # Create a new client registry
        cr = ClientRegistry()
        
        # Add the client to the registry
        cr.add_llm_client(
            name=client_name,
            provider=provider,
            options=options
        )
        
        # Set it as the primary client
        cr.set_primary(client_name)
        
        # Test with ExtractResume function (override the default client)
        test_resume = """
        John Doe
        john.doe@example.com

        Experience:
        - Software Engineer at Tech Corp (2020-2024)
        - Intern at Startup Inc (2019-2020)

        Skills:
        - Python
        - JavaScript
        - BAML
        """
        
        print(f"Making test call with {client_name}...")
        result = b.ExtractResume(test_resume, baml_options={"client_registry": cr})
        
        print(f"✅ Success with {client_name}!")
        print(f"   Name: {result.name}")
        print(f"   Email: {result.email}")
        print(f"   Skills: {', '.join(result.skills)}")
        return True
        
    except Exception as e:
        print(f"❌ Error with {client_name}: {str(e)}")
        return False


async def test_client_async(client_name, provider, options):
    """Test a client asynchronously using Client Registry"""
    from baml_client.async_client import b as async_b
    
    print(f"\n{'='*60}")
    print(f"Testing client: {client_name}")
    print(f"Provider: {provider}")
    print(f"Model: {options.get('model', 'N/A')}")
    print(f"{'='*60}")
    
    # Check if API key is available
    if 'api_key' in options and not options['api_key']:
        print(f"⚠️  Skipping {client_name}: API key not found in environment")
        return False
    
    try:
        # Create a new client registry
        cr = ClientRegistry()
        
        # Add the client to the registry
        cr.add_llm_client(
            name=client_name,
            provider=provider,
            options=options
        )
        
        # Set it as the primary client
        cr.set_primary(client_name)
        
        # Test with ExtractResume function
        test_resume = """
        John Doe
        john.doe@example.com

        Experience:
        - Software Engineer at Tech Corp (2020-2024)
        - Intern at Startup Inc (2019-2020)

        Skills:
        - Python
        - JavaScript
        - BAML
        """
        
        print(f"Making test call with {client_name}...")
        result = await async_b.ExtractResume(test_resume, baml_options={"client_registry": cr})
        
        print(f"✅ Success with {client_name}!")
        print(f"   Name: {result.name}")
        print(f"   Email: {result.email}")
        print(f"   Skills: {', '.join(result.skills)}")
        return True
        
    except Exception as e:
        print(f"❌ Error with {client_name}: {str(e)}")
        return False


def main():
    """Main function to test all GPT clients"""
    print("GPT Client Testing Script")
    print("=" * 60)
    print(f"Found {len(GPT_CLIENTS)} GPT clients to test\n")
    
    results = []
    
    # Test each client synchronously
    for client_config in GPT_CLIENTS:
        success = test_client_sync(
            client_config["name"],
            client_config["provider"],
            client_config["options"]
        )
        results.append((client_config["name"], success))
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    successful = sum(1 for _, success in results if success)
    failed = len(results) - successful
    
    for client_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {client_name}")
    
    print(f"\nTotal: {len(results)} clients")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"{'='*60}")


async def main_async():
    """Main function to test all GPT clients asynchronously"""
    print("GPT Client Testing Script (Async)")
    print("=" * 60)
    print(f"Found {len(GPT_CLIENTS)} GPT clients to test\n")
    
    results = []
    
    # Test each client asynchronously
    for client_config in GPT_CLIENTS:
        success = await test_client_async(
            client_config["name"],
            client_config["provider"],
            client_config["options"]
        )
        results.append((client_config["name"], success))
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    successful = sum(1 for _, success in results if success)
    failed = len(results) - successful
    
    for client_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {client_name}")
    
    print(f"\nTotal: {len(results)} clients")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"{'='*60}")


if __name__ == "__main__":
    # Check if we should run async version
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--async":
        asyncio.run(main_async())
    else:
        main()

