#!/usr/bin/env python3
"""
Quick setup verification script.
Run this to check if the project is properly set up.
"""

import sys
import os


def check_dependencies():
    """Check if required packages are installed."""
    print("Checking dependencies...")

    packages = {
        'requests': 'REST API calls',
        'mcp': 'Model Context Protocol',
    }

    missing = []
    for package, purpose in packages.items():
        try:
            __import__(package)
            print(f"  ✓ {package} ({purpose})")
        except ImportError:
            print(f"  ✗ {package} ({purpose}) - MISSING")
            missing.append(package)

    return len(missing) == 0


def check_api_key():
    """Check if API key is set."""
    print("\nChecking API key...")
    api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
    if api_key:
        print(f"  ✓ ALPHA_VANTAGE_API_KEY is set")
        return True
    else:
        print(f"  ✗ ALPHA_VANTAGE_API_KEY is not set")
        print(f"    Set it with: export ALPHA_VANTAGE_API_KEY=your_key")
        return False


def check_files():
    """Check if all required files exist."""
    print("\nChecking project files...")

    files = [
        'rest_example/rest_stock_client.py',
        'rest_example/main.py',
        'mcp_example/stock_plugin.py',
        'mcp_example/alphavantage_mcp_plugin.py',
        'mcp_example/main.py',
        'requirements.txt',
        '.env.example',
        'README.md',
        'CLAUDE.md'
    ]

    all_exist = True
    for file in files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            all_exist = False

    return all_exist


def main():
    print("="* 50)
    print("REST vs MCP Stock Data - Setup Verification")
    print("="* 50)

    deps_ok = check_dependencies()
    api_key_ok = check_api_key()
    files_ok = check_files()

    print("\n" + "="* 50)
    if deps_ok and files_ok:
        print("✓ Project structure is good!")
        if not api_key_ok:
            print("⚠ Set API key to run the examples")
        else:
            print("✓ Ready to run examples!")
            print("\nTry:")
            print("  python rest_example/main.py AAPL")
            print("  python mcp_example/main.py AAPL")
    else:
        print("✗ Setup incomplete")
        if not deps_ok:
            print("\nInstall dependencies with:")
            print("  pip install -r requirements.txt")
        if not files_ok:
            print("\nSome project files are missing")
    print("="* 50)

    return 0 if (deps_ok and files_ok) else 1


if __name__ == '__main__':
    sys.exit(main())
