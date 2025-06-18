# Dungeon Master CLI Command Reference

This document provides a comprehensive reference for all Dungeon Master CLI commands, their options, usage patterns, and example outputs.

## 📋 Command Overview

| Command | Purpose | Frequency |
|---------|---------|-----------|
| [`dm init`](#dm-init) | Initialize Dungeon Master in repository | Once per project |
| [`dm validate`](#dm-validate) | Validate documentation status (pre-commit) | Automatic |
| [`dm review`](#dm-review) | Display documentation status with rich formatting | Daily |
| [`dm create_lore`](#dm-create_lore) | Generate documentation templates | As needed |
| [`dm map`](#dm-map) | Generate visual repository structure | Weekly/monthly |

## 🚀 dm init

Initialize the Dungeon Master environment in your repository.

### Usage
```bash
dm init
```

### Actions Performed
- Creates `.lore/` directory for documentation
- Creates `.cursor/rules/` directory for IDE integration
- Copies Cursor rule templates for workflow guidance
- Generates `dmconfig.json` configuration file
- Creates `dmcache.json` for state tracking
- Updates `.gitignore` to exclude cache files
- Sets up pre-commit hook for validation

### Example Output
```
✨ Initializing Dungeon Master ✨

📁 Creating directory structure...
  ✅ Created .lore/ directory
  ✅ Created .cursor/rules/ directory

📝 Creating configuration files...
  ✅ Created dmconfig.json
  ✅ Created dmcache.json

🔮 Setting up gitignore...
  ✅ Updated .gitignore to exclude dmcache.json

🧙 Setting up Cursor rules...
  ✅ Copied dungeon_master_workflow.mdc to .cursor/rules/
  ✅ Copied dungeon_master_enforcement.mdc to .cursor/rules/
  ✅ Copied dungeon_master_commands.mdc to .cursor/rules/
  ✅ Copied dungeon_master_template.mdc to .cursor/rules/

Initialization complete! Your project is now protected by Dungeon Master.
```

### Files Created
```
your-project/
├── .lore/                                    # Documentation directory
├── .cursor/rules/                           # IDE integration rules
│   ├── dungeon_master_workflow.mdc         # Workflow guide
│   ├── dungeon_master_enforcement.mdc      # Enforcement rules
│   ├── dungeon_master_commands.mdc         # Command reference
│   └── dungeon_master_template.mdc         # Template guide
├── dmconfig.json                           # Configuration
├── dmcache.json                            # State tracking (gitignored)
└── .git/hooks/pre-commit                   # Pre-commit hook
```

### Next Steps After Init
1. Add `track_lore` decorators to your code
2. Run `dm create_lore` to generate templates
3. Fill out documentation templates
4. Test with `dm review`

---

## 🔍 dm validate

Core pre-commit hook functionality that verifies documentation is up-to-date. This runs automatically before each commit.

### Usage
```bash
dm validate
```

### Validation Checks
- ✅ Each tracked file has corresponding documentation
- ✅ Changed tracked files have updated documentation  
- ✅ Documentation contains actual content (not just templates)
- ✅ Required sections are completed
- ✅ Professional diagrams are included

### Success Output
```
🔒 Validating Documentation 🔒

🔍 Checking git staged changes...
  Found 2 changed files with track_lore decorators

📝 Checking documentation status...
  ✓ src/api/payment.py → .lore/payments.md UPDATED
  ✓ src/models/user.py → .lore/users.md UPDATED

✅ VALIDATION PASSED
All documentation is up-to-date!
```

### Failure Output
```
🔒 Validating Documentation 🔒

🔍 Checking git staged changes...
  Found 4 changed files with track_lore decorators

📝 Checking documentation status...
  ✓ src/models/user.py → .lore/users.md UPDATED
  ✓ src/api/payouts.py → .lore/payments-platform/payouts.md UPDATED
  ✗ src/api/payment.py → .lore/payments.md NOT UPDATED
  ✗ src/auth/login.py → .lore/auth/login.md TEMPLATE ONLY

❌ VALIDATION FAILED

REQUIRED ACTIONS:
  1. UPDATE .lore/payments.md TO REFLECT CHANGES IN src/api/payment.py
     REVIEW ALL FILES TRACKED BY THIS LORE FILE:
     - src/api/payment.py
     - src/api/payment_processor.py
     
  2. COMPLETE .lore/auth/login.md TEMPLATE WITH ACTUAL DOCUMENTATION
     REVIEW ALL FILES TRACKED BY THIS LORE FILE:
     - src/auth/login.py
     
     MISSING REQUIRED SECTIONS: Overview, Key Functions/Components, Diagrams

🛑 COMMIT BLOCKED: UPDATE DOCUMENTATION BEFORE PROCEEDING
```

### When It Runs
- Automatically during `git commit`
- Manually when you run `dm validate`
- Can be integrated into CI/CD pipelines

---

## 📊 dm review

Display documentation status using rich formatting with detailed information about what needs attention.

### Usage
```bash
dm review [options]
```

### Options
```
--mark-reviewed <file>    Mark a file as reviewed (EMERGENCY USE ONLY)
```

### Standard Output
```
🔍 Documentation Review 🔍

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Lore File                      ┃ Tracked Files                              ┃ Status              ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ .lore/payments.md              │ src/api/payment.py [changed]               │ NEEDS UPDATE       │
│                               │ src/api/payment_processor.py                  │                      │
├───────────────────────────────┼────────────────────────────────────────────────┼──────────────────────────┤
│ .lore/payments-platform/      │ src/api/payouts.py                            │ UP TO DATE         │
│ payouts.md                    │                                                │                      │
├───────────────────────────────┼────────────────────────────────────────────────┼──────────────────────────┤
│ .lore/users.md                │ src/models/user.py                             │ UP TO DATE         │
├───────────────────────────────┼────────────────────────────────────────────────┼──────────────────────────┤
│ .lore/auth/login.md           │ src/auth/login.py                              │ TEMPLATE ONLY      │
└───────────────────────────────┴────────────────────────────────────────────────┴──────────────────────────┘

❗ REQUIRED ACTIONS:
  → UPDATE .lore/payments.md TO REFLECT CHANGES IN src/api/payment.py
    REVIEW THESE FILES TO UNDERSTAND THE ENTIRE SYSTEM:
    - src/api/payment.py
    - src/api/payment_processor.py
    
  → COMPLETE .lore/auth/login.md TEMPLATE WITH ACTUAL DOCUMENTATION
    REVIEW THESE FILES TO UNDERSTAND THE ENTIRE SYSTEM:
    - src/auth/login.py
```

### Status Indicators
- **🟢 UP TO DATE**: Documentation is current with code changes
- **🟡 TEMPLATE ONLY**: Documentation file exists but contains only template content
- **🔴 NEEDS UPDATE**: Tracked files have changed but documentation hasn't been updated
- **⚠️ MISSING**: Tracked files reference non-existent documentation

### Manual Review Override

**⚠️ CRITICAL WARNING: USE WITH EXTREME CAUTION**

```bash
dm review --mark-reviewed <file>
```

This override should **ONLY** be used when:
- File changes are truly minor (formatting, typos)
- You've thoroughly reviewed both code and documentation
- You can confidently confirm documentation remains accurate

**Example:**
```bash
# Only for genuinely minor changes
dm review --mark-reviewed src/api/payment.py
```

**Never use for:**
- Behavior changes
- New features
- API modifications
- When rushing deadlines

---

## 🔮 dm create_lore

Generate documentation templates for all `track_lore` decorators found in the codebase.

### Usage
```bash
dm create_lore [lore_file]
```

### Parameters
- `lore_file` (optional): Create only a specific documentation file

### Actions
- Scans codebase for `track_lore` decorators
- Creates missing documentation files
- Generates subdirectories as needed
- Populates files with standard templates

### Example Output
```
🔮 Creating Lore Files 🔮

🔍 Scanning for track_lore decorators...
  Found 5 unique lore files referenced in code

📝 Checking documentation status...
  ✅ .lore/payments.md (exists)
  ✅ .lore/payments-platform/payouts.md (exists)
  ✅ .lore/users.md (exists)
  ❌ .lore/config.md (missing)
  ❌ .lore/auth/login.md (missing)
  
📁 Creating necessary directories...
  ✅ Created .lore/auth/ directory
  
📑 Creating missing lore files with templates...
  ✅ Created .lore/config.md with documentation template
  ✅ Created .lore/auth/login.md with documentation template

✨ Complete! All lore files are now created.
⚠️ WARNING: FILL OUT ALL TEMPLATES WITH ACTUAL DOCUMENTATION BEFORE COMMITTING.
```

### Creating Specific Files
```bash
# Create only a specific documentation file
dm create_lore api/payments.md
```

### What Happens Next
1. Templates are created with placeholder content
2. You must fill out all required sections
3. Run `dm review` to check progress
4. Templates are detected and rejected during validation until completed

---

## 🗺️ dm map

Generate a visual representation of repository structure showing relationships between source files and documentation.

### Usage
```bash
dm map
```

### Actions
- Scans repository for tracked files
- Maps relationships between code and documentation
- Creates visual tree structure
- Saves output to `.lore/map.md`

### Example Output
```
📊 Generating Repository Map 📊

🔍 Scanning repository structure...

📂 Project Tree:
├── 📁 src/
│  ├── 📄 api/
│  │  ├── 📄 payment.py (tracked by .lore/payments.md)
│  │  ├── 📄 payment_processor.py (tracked by .lore/payments.md)
│  │  └── 📄 payouts.py (tracked by .lore/payments-platform/payouts.md)
│  ├── 📄 models/
│  │  └── 📄 user.py (tracked by .lore/users.md)
│  ├── 📄 auth/
│  │  └── 📄 login.py (tracked by .lore/auth/login.md)
│  └── 📄 main.py (tracked by .lore/app.md)
├── 📁 tests/
│  └── 📄 test_payment.py
└── 📁 .lore/
   ├── 📄 payments.md
   ├── 📁 payments-platform/
   │  └── 📄 payouts.md
   ├── 📄 users.md
   ├── 📁 auth/
   │  └── 📄 login.md
   └── 📄 app.md

✅ Map generated and saved to .lore/map.md
```

### Use Cases
- Understanding documentation coverage
- Onboarding new team members
- Identifying documentation gaps
- Planning documentation structure
- Architecture reviews

---

## 🔄 Common Command Workflows

### Initial Project Setup
```bash
# Set up Dungeon Master
dm init

# Add track_lore decorators to your code
# (manual step - edit your source files)

# Generate documentation templates
dm create_lore

# Fill out templates
# (manual step - edit .lore/*.md files)

# Check status
dm review

# Test the system
git add .
git commit -m "Set up documentation system"
```

### Daily Development Workflow
```bash
# Check what needs attention
dm review

# Work on code...
# Update documentation...

# Validate before committing
dm validate

# Commit changes
git add .
git commit -m "Feature with documentation"
```

### Documentation Maintenance
```bash
# Generate repository overview
dm map

# Check for missing documentation
dm create_lore

# Review current status
dm review

# Address any issues...
```

---

## 🚨 Error Handling

### Common Errors and Solutions

#### Not Initialized
```
❌ Error: Dungeon Master not initialized in this repository.
Run `dm init` to set up Dungeon Master.
```
**Solution**: Run `dm init` in your project root.

#### Invalid Decorator Format
```
⚠️ Warning: Invalid track_lore format in src/api/payment.py:
# track_lore(payments.md)
Should be: # track_lore("payments.md")
```
**Solution**: Add quotes around the file path.

#### Missing Documentation Files
```
❌ Error: Documentation file not found: .lore/payments.md
Referenced in: src/api/payment.py
```
**Solution**: Run `dm create_lore` to generate missing files.

#### Pre-commit Hook Failure
```
❌ Pre-commit hook failed: Documentation validation failed.
Run `dm validate` for details.
```
**Solution**: Run `dm validate` to see specific issues, then address them.

---

## ⚙️ Environment Variables

Configure Dungeon Master behavior through environment variables:

```bash
export DM_CONFIG_PATH="/path/to/custom/config.json"    # Custom config location
export DM_LORE_DIR="docs"                             # Custom documentation directory
export DM_DISABLE_COLORS="true"                       # Disable colored output
export DM_LOG_LEVEL="debug"                          # Set logging level
```

---

## 🔗 Integration with Other Tools

### CI/CD Pipeline
```yaml
# GitHub Actions example
- name: Validate Documentation
  run: |
    dm validate
    if [ $? -ne 0 ]; then
      echo "Documentation validation failed"
      exit 1
    fi
```

### IDE Integration
- Cursor rules are automatically installed with `dm init`
- Set up file watchers to run `dm review` on save
- Create code snippets for `track_lore` decorators

### Git Hooks
```bash
# Additional hooks can be added to .git/hooks/
# Example: pre-push hook
#!/bin/sh
dm validate || exit 1
```

---

For more information about specific workflows and best practices, see:
- [Development Workflow Guide](workflow.md)
- [Troubleshooting Guide](troubleshooting.md)
- [Configuration Options](configuration.md)