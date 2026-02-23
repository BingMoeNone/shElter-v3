#!/usr/bin/env python3
"""
Security scan script for dependency vulnerabilities and code quality
"""

import subprocess
import sys
import os
import json
from datetime import datetime


def run_command(cmd, shell=True):
    """Run a command and return the output"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            check=False
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": 1
        }


def install_deps():
    """Install security scanning dependencies"""
    print("Installing security scanning dependencies...")
    deps = [
        "safety",
        "bandit",
        "black",
        "flake8",
        "isort"
    ]
    
    for dep in deps:
        result = run_command(f"uv add {dep}")
        if result["returncode"] != 0:
            print(f"Failed to install {dep}: {result['stderr']}")
            return False
    return True


def scan_dependencies():
    """Scan dependencies for vulnerabilities"""
    print("\n=== Scanning Dependencies for Vulnerabilities ===")
    result = run_command("uv run safety check --json")
    
    if result["returncode"] == 0:
        print("✓ No dependency vulnerabilities found")
        return []
    else:
        try:
            vulnerabilities = json.loads(result["stdout"])
            print(f"✗ Found {len(vulnerabilities)} vulnerabilities")
            return vulnerabilities
        except json.JSONDecodeError:
            print(f"✗ Failed to parse safety output: {result['stderr']}")
            return []


def scan_code_security():
    """Scan code for security issues"""
    print("\n=== Scanning Code for Security Issues ===")
    result = run_command("uv run bandit -r src -f json")
    
    if result["returncode"] == 0:
        print("✓ No security issues found in code")
        return []
    else:
        try:
            issues = json.loads(result["stdout"])["results"]
            print(f"✗ Found {len(issues)} security issues in code")
            return issues
        except (json.JSONDecodeError, KeyError):
            print(f"✗ Failed to parse bandit output: {result['stderr']}")
            return []


def check_code_format():
    """Check code format with Black"""
    print("\n=== Checking Code Format ===")
    result = run_command("uv run black --check src")
    
    if result["returncode"] == 0:
        print("✓ Code is formatted correctly")
        return True
    else:
        print("✗ Code needs formatting")
        return False


def check_code_style():
    """Check code style with Flake8"""
    print("\n=== Checking Code Style ===")
    result = run_command("uv run flake8 src")
    
    if result["returncode"] == 0:
        print("✓ No code style issues found")
        return True
    else:
        print("✗ Code style issues found:")
        print(result["stdout"])
        return False


def check_import_order():
    """Check import order with isort"""
    print("\n=== Checking Import Order ===")
    result = run_command("uv run isort --check src")
    
    if result["returncode"] == 0:
        print("✓ Import order is correct")
        return True
    else:
        print("✗ Import order needs fixing")
        return False


def generate_report(vulnerabilities, security_issues, code_format, code_style, import_order):
    """Generate a security scan report"""
    report = {
        "scan_time": datetime.now().isoformat(),
        "dependencies": {
            "vulnerabilities": vulnerabilities,
            "count": len(vulnerabilities)
        },
        "code_security": {
            "issues": security_issues,
            "count": len(security_issues)
        },
        "code_quality": {
            "format_correct": code_format,
            "style_correct": code_style,
            "import_order_correct": import_order
        },
        "summary": {
            "status": "PASS" if all([
                len(vulnerabilities) == 0,
                len(security_issues) == 0,
                code_format,
                code_style,
                import_order
            ]) else "FAIL"
        }
    }
    
    # Save report to file
    report_dir = "security_reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    report_file = os.path.join(report_dir, f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n=== Scan Report Generated ===")
    print(f"Report saved to: {report_file}")
    print(f"Scan Status: {report['summary']['status']}")
    
    return report


def main():
    """Main function"""
    print("Security Scan Script")
    print("=" * 40)
    
    # Install dependencies
    if not install_deps():
        print("Failed to install dependencies. Exiting.")
        sys.exit(1)
    
    # Run scans
    vulnerabilities = scan_dependencies()
    security_issues = scan_code_security()
    code_format = check_code_format()
    code_style = check_code_style()
    import_order = check_import_order()
    
    # Generate report
    report = generate_report(vulnerabilities, security_issues, code_format, code_style, import_order)
    
    # Exit with appropriate code
    if report['summary']['status'] == "FAIL":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
