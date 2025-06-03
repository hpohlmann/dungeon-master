# 🚀 Deployment Scripts

This directory contains scripts for building and deploying Dungeon Master to PyPI.

## 📜 Scripts Overview

### `build_and_deploy.sh` - Full Deployment Script

Comprehensive script with error handling, validation, and interactive prompts.

**Features:**

- ✅ Pre-flight checks (git status, directory validation)
- 🧪 Runs tests before deployment
- 🧹 Cleans build artifacts
- 📦 Builds both wheel and source distributions
- ✅ Validates package integrity
- 🏷️ Optional git tagging
- 🎯 Support for Test PyPI deployment

**Usage:**

```bash
# Deploy to Production PyPI
./scripts/build_and_deploy.sh

# Deploy to Test PyPI
./scripts/build_and_deploy.sh --test-pypi
```

### `quick_deploy.sh` - Rapid Deployment

Minimal script for quick deployments when you're confident everything is ready.

**Features:**

- 🏃‍♂️ Fast execution
- 🧹 Basic cleanup
- 📦 Build and deploy
- ⚡ No interactive prompts

**Usage:**

```bash
./scripts/quick_deploy.sh
```

## 🔧 Prerequisites

Before running these scripts, ensure you have:

1. **PyPI Account**: Register at [pypi.org](https://pypi.org)
2. **API Token**: Create an API token in your PyPI account settings
3. **Twine Configuration**: Configure your credentials

### Setting up PyPI Credentials

**Option 1: API Token (Recommended)**

```bash
# Create ~/.pypirc
[pypi]
username = __token__
password = <your-api-token>

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = <your-test-api-token>
```

**Option 2: Environment Variables**

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=<your-api-token>
```

**Option 3: Interactive (scripts will prompt)**

- Scripts will ask for credentials if not configured

## 📋 Pre-Deployment Checklist

Before deploying a new version:

- [ ] Update version number in `dungeon_master/__init__.py`
- [ ] Update version number in `setup.py`
- [ ] Update `CHANGELOG.md` with release notes
- [ ] Commit all changes
- [ ] Run tests locally
- [ ] Verify documentation is up to date

## 🎯 Deployment Workflow

### For Major Releases

1. **Test on Test PyPI first:**

   ```bash
   ./scripts/build_and_deploy.sh --test-pypi
   ```

2. **Test installation from Test PyPI:**

   ```bash
   pip install --index-url https://test.pypi.org/simple/ cursor-dungeon-master==<version>
   ```

3. **Deploy to Production PyPI:**
   ```bash
   ./scripts/build_and_deploy.sh
   ```

### For Quick Patches

```bash
./scripts/quick_deploy.sh
```

## 🛠️ Troubleshooting

**"Package already exists" error:**

- Check if version number was updated
- Verify you're not re-uploading the same version

**Authentication errors:**

- Verify API token is correct
- Check ~/.pypirc configuration
- Ensure token has upload permissions

**Build failures:**

- Run `python -m build` manually to debug
- Check for syntax errors or missing dependencies
- Ensure all required files are included in MANIFEST.in

**Permission errors:**

- Verify scripts are executable: `chmod +x scripts/*.sh`
- Check virtual environment activation

## 📊 Post-Deployment

After successful deployment:

1. **Verify Installation:**

   ```bash
   pip install cursor-dungeon-master==<new-version>
   ```

2. **Update Documentation:**

   - GitHub README badges
   - Installation instructions
   - Release notes

3. **Create GitHub Release:**

   - Tag the release
   - Upload distribution files
   - Write release notes

4. **Announce:**
   - Social media
   - Documentation updates
   - Notify users/contributors
