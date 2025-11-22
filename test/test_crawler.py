#!/usr/bin/env python3

import sys
import os
# Add the project root directory to Python path to allow module imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

import asyncio

import tempfile

import shutil

from mcp_server.server import handle_call_tool, TextContent

def clean_temp_dir(temp_dir):

    # Clean up temporary files

    if os.path.exists(temp_dir):

        shutil.rmtree(temp_dir)

        print(f"\n🧹 Cleaned temporary directory: {temp_dir}")

        

@pytest.mark.asyncio

async def test_complete_crawler():

    print("🔍 Testing complete crawler functionality (with file saving)")

    print("=" * 50)

    

    # Create temporary directory

    temp_dir = "./test_output"

    

    clean_temp_dir(temp_dir)



    os.makedirs(temp_dir, exist_ok=True)

    

    output_dir = ""

    try:

        print(f"📁 Test directory: {temp_dir}")

        

        # Test crawler call

        result = await handle_call_tool("crawl_web_page", {

            "url": os.getenv("TEST_URL", "https://zh.wikipedia.org/wiki/Wikipedia:%E9%A6%96%E9%A1%B5"),

            "save_path": temp_dir,

            "save_screenshot": True,

            "save_pdf": True,

            "generate_markdown": True

        })

        

        print("📤 Crawler execution result:")

        for content in result:

            if hasattr(content, 'text') and "Successfully crawled" in content.text:

                # Extract the output directory from the success message

                output_dir = content.text.split(" to ")[-1]

                print(f"   {content.text}")



        assert output_dir, "Failed to get output directory from crawl result"

        

        # Check generated files

        print(f"\n📄 Checking generated files in {output_dir}:")

        assert os.path.exists(output_dir), f"Output directory {output_dir} was not created."





        expected_files = ["output.html", "output.json", "output.png", "output.pdf", "raw_markdown.md"]

        for file in expected_files:



            file_path = os.path.join(output_dir, file)

            print(f"   Verifying {file}...")

            assert os.path.exists(file_path), f"File {file} was not generated."

            assert os.path.getsize(file_path) > 0, f"File {file} is empty."

            print(f"   ✅ {file} exists and is not empty.")





    except Exception as e:

        print(f"❌ Test failed: {e}")

        import traceback

        traceback.print_exc()

        pytest.fail(f"Test failed with exception: {e}")

    finally:

        # Clean up the specific output directory created by the test

        # shutil.rmtree(output_dir)

        # print(f"\n🧹 Cleaned test run directory: {output_dir}")

        pass


