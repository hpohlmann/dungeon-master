# Dungeon Master

A context-tracking pre-commit tool designed for **Cursor AI integration**. Creates a structured workflow where Cursor collaborates with developers to maintain accurate, up-to-date repository documentation.

## 🎯 Core Philosophy

**This is NOT an auto-documentation generator.** Instead, Dungeon Master is a **scaffolding and enforcement system** that:

- 🛡️ **Blocks commits** when tracked files lack proper context documentation
- 📋 **Generates templates** with Cursor-specific placeholders and instructions
- ✅ **Validates completion** to ensure meaningful documentation exists
- 🔄 **Enforces consistency** through structured, commit-aware workflows

## How It Works

### 1. **File Tracking**

Add a simple decorator to any file you want to track:

```python
# @track_context("auth_service.md")

class AuthService:
    def authenticate(self, token: str) -> bool:
        # Your code here
        pass
```

### 2. **Template Generation**

When you commit a tracked file, Dungeon Master creates a template in `/dungeon_master/`:

```markdown
# auth_service.py - Context Documentation

> **Instructions for Cursor**: This is a context template. Please replace all placeholder text in parentheses with meaningful documentation. Remove this instruction block when complete.

## Purpose

(Describe the overall intent and responsibility of this file. This Python module contains 1 class(es) and 10 function(s). What problem does it solve? What is its role in the larger system?)

## Usage Summary

**File Location**: `src/auth_service.py`

**Key Dependencies**:
(Review and document the purpose of these key imports:)

- `jwt`: (explain why this dependency is needed)
- `hashlib`: (explain why this dependency is needed)

## Key Functions or Classes

**Classes:**

- **AuthService**: (Describe the purpose and responsibility of this class)

**Key Functions:**

- **authenticate(self, token)**: (Explain what this function does and when it's used)
- **generate_token(self, user_id)**: (Explain what this function does and when it's used)
```

### 3. **Commit Blocking**

The commit is **blocked** with a helpful message:

```
🛡️  COMMIT BLOCKED: Context Documentation Required
================================================================
📝 New context templates created:
   • dungeon_master/auth_service.md

🎯 Next Steps:
   1. Use Cursor to complete the context documentation
   2. Fill in all placeholder text marked with parentheses
   3. Remove the 'Instructions for Cursor' block when done
   4. Commit again once documentation is complete
```

### 4. **Cursor Integration**

Use Cursor to fill out the template with meaningful content:

```markdown
## Purpose

This module provides a comprehensive authentication service for handling user login,
token management, and session tracking. It serves as the core security component
for user authentication workflows, implementing JWT-based authentication with
secure password hashing and session management capabilities.

## Usage Summary

**Primary Use Cases**:

- User authentication and login workflows
- JWT token generation and validation
- Password hashing and verification
- Session management and tracking

**Key Dependencies**:

- `jwt`: Provides JWT token encoding/decoding functionality
- `hashlib`: Used for secure SHA-256 password hashing
```

### 5. **Validation & Success**

Once completed, the commit proceeds with updated documentation:

```
✅ Dungeon Master Context Tracking: All validations passed
   📊 Processed 1 tracked file(s)
   📝 Updated 1 context document(s)
   🎯 Repository context documentation is up to date!
```

## 🚀 Quick Start

### Installation

```bash
pip install dungeon-master
```

### Initialize

```bash
dm init
pre-commit install
```

### Track Files

Add the tracking decorator to any important file:

```python
# @track_context("my_component.md")
```

### Commit Workflow

1. **Commit tracked files** → Templates created, commit blocked
2. **Use Cursor** to fill templates with meaningful documentation
3. **Commit again** → Validation passes, documentation updated

## 📋 CLI Commands

### Process Templates

```bash
# Create templates for staged files
dm update

# Process specific files
dm update src/auth.py src/utils.py
```

### Check Status

```bash
# List tracked files and their documentation status
dm list --all

# Validate what would block commits
dm validate
```

### Initialize Repository

```bash
# Set up Dungeon Master in current repo
dm init
```

## 🔍 Validation Rules

Commits are blocked when context documents:

- ❌ **Don't exist** (templates need to be created)
- ❌ **Contain placeholders** like `(Describe the purpose...)`
- ❌ **Have instruction blocks** for Cursor still present
- ❌ **Lack meaningful content** beyond template structure

✅ **Commits proceed** when all tracked files have complete, validated documentation.

## 🏗️ Template Structure

Generated templates include:

- **Purpose**: Overall intent and responsibility
- **Usage Summary**: File location, use cases, dependencies
- **Key Functions/Classes**: Main components with descriptions
- **Usage Notes**: Patterns, gotchas, considerations
- **Dependencies & Integration**: How it fits in the system
- **Changelog**: Auto-maintained history

## 📁 Directory Structure

```
your_project/
├── dungeon_master/           # Generated context documents
│   ├── auth_service.md       # ✓ Completed by Cursor
│   ├── api_client.md         # ⚠️ Needs completion
│   └── utils.md              # ✓ Completed
├── src/
│   ├── auth.py              # @track_context("auth_service.md")
│   ├── client.js            # @track_context("api_client.md")
│   └── utils.py             # @track_context("utils.md")
├── hooks/
│   └── pre_commit_hook.py   # Pre-commit enforcement
└── .pre-commit-config.yaml
```

## 🎨 Language Support

- **Python** (.py) - Full AST analysis for intelligent templates
- **JavaScript/TypeScript** (.js, .ts, .jsx, .tsx) - Regex-based parsing
- **Other Languages** - Basic file analysis with manual completion

## ⚙️ Configuration

### Pre-commit Integration

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/yourusername/dungeon-master
    rev: v0.1.0
    hooks:
      - id: dungeon-master
```

Or for local development:

```yaml
repos:
  - repo: local
    hooks:
      - id: dungeon-master
        name: Dungeon Master Context Tracking
        entry: python hooks/pre_commit_hook.py
        language: system
        pass_filenames: false
        always_run: true
```

## 🧠 Philosophy: AI-Assisted Documentation

Dungeon Master creates a **structured integration point** where:

- 🤖 **AI (Cursor)** provides the intelligence and content
- 🛠️ **The system** provides structure, enforcement, and consistency
- 👨‍💻 **Developers** maintain control and oversight
- 📈 **Documentation** stays current through commit-time enforcement

This approach ensures documentation is:

- **Meaningful** (written by AI that understands code)
- **Current** (updated every time code changes)
- **Consistent** (follows the same structure)
- **Enforced** (can't be skipped or forgotten)

## 🔧 Development

### Setup

```bash
git clone https://github.com/yourusername/dungeon-master.git
cd dungeon-master
pip install -e .[dev]
```

### Test

```bash
python verify_installation.py
make test
```

### Demo

```bash
make demo  # See the system in action
```

## 🗺️ Roadmap

- [ ] **Git Integration**: Better change detection and diff analysis
- [ ] **AI Enhancement**: Integration with multiple AI providers
- [ ] **Configuration**: Customizable templates and validation rules
- [ ] **Analytics**: Documentation coverage and quality metrics
- [ ] **IDE Plugins**: Direct integration with VSCode, IntelliJ, etc.

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

This tool is designed to evolve with AI coding practices. Contributions welcome for:

- Enhanced language support
- Better validation logic
- Improved template generation
- AI provider integrations

---

**💡 Remember**: This isn't about generating docs automatically—it's about creating a structured way for AI assistants like Cursor to help you maintain accurate, meaningful documentation as part of your development workflow.
