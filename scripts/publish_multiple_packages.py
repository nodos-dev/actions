
import argparse
import json
import os
import subprocess

def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Process GitHub event-related arguments.")

    parser.add_argument("--packages-json", required=True, help="List of tuples with package names, versions and paths in JSON format.")
    parser.add_argument("--tag", required=True, help="Git tag to publish packages against.")
    parser.add_argument("--build-number", required=True, help="Build number to append to the version.")

    # Parse the arguments
    args = parser.parse_args()
    
    # Extract values
    packages_json = args.packages_json
    tag = args.tag
    build_number = args.build_number
    packages = json.loads(packages_json)
    if not isinstance(packages, list):
        raise ValueError("packages_json must be a JSON array of tuples.")
    if not all(isinstance(pkg, list) and len(pkg) == 3 for pkg in packages):
        raise ValueError("Each package must be a tuple with name, version, and path.")

    for pkg in packages:
        if not isinstance(pkg[0], str) or not isinstance(pkg[1], str) or not isinstance(pkg[2], str):
            raise ValueError("Each package tuple must contain strings for name, version, and path.")
        name, version, path = pkg
        print(f"Publishing package: {name}, version: {version}, path in repo: {path}")

    nosman_executable_name = os.env("NOSMAN_EXECUTABLE_NAME")
    nosman_path = f"../../{nosman_executable_name}"
    if not os.path.exists(nosman_path):
        raise FileNotFoundError(f"Nosman executable not found at {nosman_path}")

    for pkg in packages:
        publish_cmd = [
            nosman_path,
            "--workspace", "../../",
            "publish", "--type=generic",
            "--path", pkg[2],
            "--name", pkg[0],
            "--version", pkg[1],
            "--version-suffix", f".b{build_number}",
            "--verbose",
            "--publisher-name", os.getenv("GH_USERNAME"),
            "--publisher-email", os.getenv("GIT_EMAIL"),
            "--tag", tag
        ]
        print(f"Running command: {' '.join(publish_cmd)}")
        result = subprocess.run(publish_cmd, check=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error publishing package {pkg[0]}: {result.stderr}")
        else:
            print(f"Successfully published package {pkg[0]}: {result.stdout}")
    print("All packages processed.")

if __name__ == "__main__":
    main()
