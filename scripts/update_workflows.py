#!/usr/bin/env python3
"""
Update workflow files in plugin repositories based on templates.

This script reads the repositories.json configuration file and updates
the build.yml workflow file in each repository/branch with the appropriate
template, applying repository-specific configuration.
"""

import argparse
import json
import os
import sys
import subprocess
import tempfile


def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the output."""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False
    )
    if check and result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    return result


def get_repo_config(repo_path):
    """
    Fetch repository-specific configuration from .nodos/workflow_config.json
    in the plugin repository.
    """
    config_path = os.path.join(repo_path, '.nodos', 'workflow_config.json')
    
    default_config = {
        'build_number_offset': 0,
        'linux_enabled': True,
        'windows_enabled': True
    }
    
    if not os.path.exists(config_path):
        print(f"  No config file found at {config_path}, using defaults")
        return default_config
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            # Merge with defaults
            return {**default_config, **config}
    except (json.JSONDecodeError, FileNotFoundError, PermissionError, OSError) as e:
        print(f"  Error reading config file: {e}, using defaults")
        return default_config


def apply_template_substitutions(template_content, repo_config):
    """
    Apply repository-specific substitutions to the workflow template.
    
    Placeholders:
    - __BUILD_NUMBER_OFFSET__: Starting build number offset
    - __LINUX_ENABLED__: Whether Linux builds are enabled
    - __WINDOWS_ENABLED__: Whether Windows builds are enabled
    """
    content = template_content
    
    # Replace build number offset
    build_offset = repo_config.get('build_number_offset', 0)
    content = content.replace('__BUILD_NUMBER_OFFSET__', str(build_offset))
    
    # Replace linux/windows enabled flags
    linux_enabled = str(repo_config.get('linux_enabled', True)).lower()
    windows_enabled = str(repo_config.get('windows_enabled', True)).lower()
    content = content.replace('__LINUX_ENABLED__', linux_enabled)
    content = content.replace('__WINDOWS_ENABLED__', windows_enabled)
    
    return content


def update_repository_workflow(repo, branch, workflow_template, token, dry_run=False):
    """
    Update the workflow file in a specific repository/branch.
    """
    print(f"\nProcessing {repo} (branch: {branch})")
    
    # Read the template file
    template_path = workflow_template
    if not os.path.exists(template_path):
        print(f"  Error: Template file not found: {template_path}")
        return False
    
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Create a temporary directory for cloning
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_dir = os.path.join(tmpdir, 'repo')
        
        # Clone the repository
        # Note: Token is passed via environment variable to avoid exposure in logs
        clone_url = f"https://github.com/{repo}.git"
        print(f"  Cloning repository...")
        
        # Configure git credentials temporarily
        env = os.environ.copy()
        env['GIT_TERMINAL_PROMPT'] = '0'
        
        result = subprocess.run(
            [
                'git', 'clone',
                '--depth', '1',
                '--branch', branch,
                f'https://x-access-token:{token}@github.com/{repo}.git',
                repo_dir
            ],
            capture_output=True,
            text=True,
            check=False,
            env=env
        )
        
        if result.returncode != 0:
            print(f"  Failed to clone repository (branch might not exist)")
            return False
        
        # Get repository-specific configuration
        repo_config = get_repo_config(repo_dir)
        print(f"  Config: {repo_config}")
        
        # Apply template substitutions
        workflow_content = apply_template_substitutions(template_content, repo_config)
        
        # Ensure .github/workflows directory exists
        workflows_dir = os.path.join(repo_dir, '.github', 'workflows')
        os.makedirs(workflows_dir, exist_ok=True)
        
        # Write the workflow file
        workflow_path = os.path.join(workflows_dir, 'build.yml')
        
        # Check if file needs updating
        needs_update = True
        if os.path.exists(workflow_path):
            with open(workflow_path, 'r') as f:
                current_content = f.read()
            needs_update = current_content != workflow_content
        
        if not needs_update:
            print(f"  Workflow file is already up to date")
            return True
        
        if dry_run:
            print(f"  [DRY RUN] Would update workflow file")
            return True
        
        with open(workflow_path, 'w') as f:
            f.write(workflow_content)
        
        # Configure git
        run_command('git config user.name "nodos-bot"', cwd=repo_dir)
        run_command('git config user.email "bot@nodos.dev"', cwd=repo_dir)
        
        # Check if there are changes
        result = run_command('git status --porcelain', cwd=repo_dir)
        if not result.stdout.strip():
            print(f"  No changes to commit")
            return True
        
        # Commit and push
        run_command('git add .github/workflows/build.yml', cwd=repo_dir)
        run_command(
            'git commit -m "Update build workflow from actions repository"',
            cwd=repo_dir
        )
        print(f"  Pushing changes...")
        run_command(f'git push origin {branch}', cwd=repo_dir)
        
        print(f"  Successfully updated workflow")
        return True


def main():
    parser = argparse.ArgumentParser(
        description='Update plugin repository workflow files from templates'
    )
    parser.add_argument(
        '--config',
        default='repositories.json',
        help='Path to repositories configuration file'
    )
    parser.add_argument(
        '--token',
        help='GitHub token for authentication (or set GITHUB_TOKEN env var)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    parser.add_argument(
        '--repo',
        help='Only update this specific repository (format: owner/repo)'
    )
    parser.add_argument(
        '--branch',
        help='Only update this specific branch (requires --repo)'
    )
    
    args = parser.parse_args()
    
    # Get GitHub token
    token = args.token or os.environ.get('GITHUB_TOKEN')
    if not token:
        print("Error: GitHub token not provided. Use --token or set GITHUB_TOKEN env var")
        sys.exit(1)
    
    # Read repositories configuration
    if not os.path.exists(args.config):
        print(f"Error: Configuration file not found: {args.config}")
        sys.exit(1)
    
    with open(args.config, 'r') as f:
        config = json.load(f)
    
    repositories = config.get('repositories', [])
    
    # Filter by repo/branch if specified
    if args.repo:
        repositories = [r for r in repositories if r['repo'] == args.repo]
        if args.branch:
            repositories = [r for r in repositories if r['branch'] == args.branch]
    
    if not repositories:
        print("No repositories to process")
        sys.exit(0)
    
    print(f"Processing {len(repositories)} repository/branch combinations")
    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
    
    success_count = 0
    fail_count = 0
    
    for repo_config in repositories:
        repo = repo_config['repo']
        branch = repo_config['branch']
        workflow_template = repo_config['workflow_template']
        
        try:
            success = update_repository_workflow(
                repo,
                branch,
                workflow_template,
                token,
                dry_run=args.dry_run
            )
            if success:
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"  Error processing {repo}/{branch}: {e}")
            fail_count += 1
    
    print(f"\n{'='*60}")
    print(f"Summary: {success_count} succeeded, {fail_count} failed")
    print(f"{'='*60}")
    
    if fail_count > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
