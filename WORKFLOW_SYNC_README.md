# Plugin Workflow Sync System

This directory contains the workflow synchronization system for plugin repositories.

## Overview

The system automatically syncs build workflow files from this repository to all plugin repositories, ensuring they stay in sync and up-to-date.

## Files

### Template Files

- `plugin_build.yml.dev` - Workflow template for `dev` branches
- `plugin_build.yml.nodos-1.3` - Workflow template for `nodos-1.3` branches
- `plugin_build.yml.nodos-1.2` - Workflow template for `nodos-1.2` branches

These templates contain placeholders that are replaced with repository-specific values:
- `__BUILD_NUMBER_OFFSET__` - Starting build number offset for the repository
- `__LINUX_ENABLED__` - Whether Linux builds are enabled (true/false)
- `__WINDOWS_ENABLED__` - Whether Windows builds are enabled (true/false)

### Configuration Files

- `repositories.json` - Maps repositories and branches to their workflow templates
- `.nodos-template/workflow_config.json` - Example repository-specific configuration

### Scripts

- `scripts/update_workflows.py` - Python script that performs the workflow synchronization

### Workflows

- `.github/workflows/update_workflow.yml` - GitHub Actions workflow that runs the sync

## How It Works

1. When changes are pushed to template files or configuration in this repository, the `update_workflow.yml` workflow is triggered
2. The workflow runs `update_workflows.py` which:
   - Reads `repositories.json` to get the list of repositories/branches to update
   - For each repository/branch:
     - Clones the repository
     - Reads the repository-specific configuration from `.nodos/workflow_config.json`
     - Applies the template substitutions
     - Writes the result to `.github/workflows/build.yml`
     - Commits and pushes the changes
3. Plugin repositories are updated automatically with the latest workflow files

## Repository-Specific Configuration

Each plugin repository can have a `.nodos/workflow_config.json` file with the following structure:

```json
{
  "build_number_offset": 0,
  "linux_enabled": true,
  "windows_enabled": true
}
```

**Fields:**
- `build_number_offset` (number): Offset to add to GitHub's `run_number` for build numbering. Default: 0
- `linux_enabled` (boolean): Whether Linux builds are enabled for this repository. Default: true
- `windows_enabled` (boolean): Whether Windows builds are enabled for this repository. Default: true

If the configuration file doesn't exist, default values are used (all enabled, no offset).

## Adding a New Plugin Repository

1. Add an entry to `repositories.json` for each branch you want to sync:

```json
{
  "repo": "nodos-dev/new-plugin",
  "branch": "dev",
  "workflow_template": "plugin_build.yml.dev"
}
```

2. Optionally, create `.nodos/workflow_config.json` in the plugin repository with custom settings

3. Push the changes to this repository, which will trigger the automatic sync

## Manual Workflow Sync

You can manually trigger the workflow sync from the Actions tab:

1. Go to Actions → Update Plugin Workflows
2. Click "Run workflow"
3. Optionally specify:
   - A specific repository to update (e.g., `nodos-dev/audio`)
   - A specific branch (requires repository)
   - Dry run mode to preview changes without applying them

## Template Customization

To customize the workflow templates:

1. Edit the appropriate `plugin_build.yml.*` file
2. Use placeholders (`__PLACEHOLDER__`) for repository-specific values
3. Update `scripts/update_workflows.py` if you add new placeholders
4. Push changes to trigger automatic sync

## Testing

To test changes without affecting production:

1. Use the workflow dispatch option with dry-run mode enabled
2. Or test with a specific repository/branch first
3. Check the logs to see what changes would be made

## Notes

- The workflow files in plugin repositories should NOT be edited directly
- Changes should be made to the templates in this repository
- The sync system uses the `CI_TOKEN` secret for authentication
- Failed syncs will be reported in the workflow logs
