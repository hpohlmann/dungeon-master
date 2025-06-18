# Dungeon Master Documentation

**Dungeon Master** is a lightweight pre-commit hook system designed to enforce documentation updates alongside code changes, with first-class integration for Cursor IDE. It ensures your codebase documentation stays current by blocking commits when documentation is missing or outdated.

## 🎯 What Dungeon Master Does

- **Enforces Documentation**: Blocks commits when tracked files are modified but their documentation isn't updated
- **Template-Driven**: Provides structured documentation templates with required sections
- **File Tracking**: Uses simple decorators (`track_lore`) to link source files to documentation
- **Rich CLI**: Beautiful terminal output with clear status indicators and actionable instructions
- **Cursor IDE Integration**: Includes specialized Cursor IDE rules for seamless AI-assisted development workflow

## 🎯 Why Cursor-Specific?

This tool is specifically designed for Cursor IDE users who want to:

- **Leverage AI context**: Documentation is structured to provide rich context for Cursor's AI features
- **Maintain code quality**: Pre-commit hooks ensure documentation stays current with AI-assisted development
- **Streamline workflow**: Cursor rules help the AI understand your documentation standards
- **Scale with teams**: Consistent documentation practices across AI-assisted development teams

## 🚀 Quick Start

1. **Install Dungeon Master**

   ```bash
   pip install cursor-dungeon-master
   ```

2. **Initialize in your project**

   ```bash
   dm init
   ```

3. **Add tracking decorators to your code**

   ```python
   # track_lore("payments.md")
   def process_payment():
       # Your code here
   ```

4. **Create documentation files**

   ```bash
   dm create_lore
   ```

5. **Fill out the documentation templates** (required!)

6. **Check status**
   ```bash
   dm review
   ```

Your commits will now be protected - if you modify tracked files without updating their documentation, the commit will be blocked until you update the docs.

## 📚 Documentation Structure

```
docs/
├── README.md              # This file - overview and quick start
├── getting-started.md     # Detailed setup and first steps
├── commands.md           # Complete CLI command reference
├── workflow.md           # Development workflow and best practices
├── templates.md          # Documentation template guide
├── configuration.md      # Configuration options and customization
├── troubleshooting.md    # Common issues and solutions
└── examples/             # Practical examples and use cases
    ├── python-project/   # Example Python project setup
    ├── typescript-project/ # Example TypeScript project setup
    └── team-workflow/    # Team adoption strategies
```

## 🔗 Key Concepts

### Track Lore Decorators

Mark files that need documentation tracking:

```python
# track_lore("api/payments.md")          # Simple reference
# track_lore("platform/auth/login.md")   # Nested structure
def authenticate_user():
    pass
```

### Documentation Directory

All documentation lives in the `.lore/` directory:

```
.lore/
├── api/
│   └── payments.md
├── platform/
│   └── auth/
│       └── login.md
└── utils.md
```

### Pre-commit Protection

When you modify tracked files, commits are blocked until documentation is updated:

```bash
❌ VALIDATION FAILED
REQUIRED ACTIONS:
  1. UPDATE .lore/api/payments.md TO REFLECT CHANGES IN src/payment.py
🛑 COMMIT BLOCKED: UPDATE DOCUMENTATION BEFORE PROCEEDING
```

## 🎯 Core Commands

| Command          | Purpose                                                  |
| ---------------- | -------------------------------------------------------- |
| `dm init`        | Initialize Dungeon Master in your repository             |
| `dm validate`    | Check documentation status (used by pre-commit hook)     |
| `dm review`      | Display rich documentation status and required actions   |
| `dm create_lore` | Generate documentation templates for tracked files       |
| `dm map`         | Create visual repository structure showing tracked files |

## 🏗️ Documentation Requirements

Every documentation file must include:

- ✅ **Overview**: Clear description of purpose and functionality
- ✅ **Key Functions/Components**: Detailed documentation of main features
- ✅ **Professional Diagrams**: Mermaid.js diagrams showing relationships and flow
- ✅ **Usage Examples**: Concrete examples of how to use the code
- ✅ **Dependencies**: Important relationships and requirements

**Template-only documentation is rejected** - you must fill out all required sections with actual content.

## 🚨 Enforcement Philosophy

Dungeon Master operates on these principles:

1. **Documentation is mandatory** for tracked files
2. **Pre-commit blocking is a feature**, not a bug
3. **Empty templates are technical debt**
4. **Professional diagrams are essential** for understanding
5. **Manual overrides should be extremely rare** and well-justified

## 📖 Next Steps

- **New Users**: Start with [Getting Started Guide](getting-started.md)
- **Team Leaders**: Review [Team Workflow Examples](examples/team-workflow/)
- **Developers**: See [Development Workflow](workflow.md)
- **Advanced Users**: Check [Configuration Options](configuration.md)

## 🆘 Need Help?

- **Common Issues**: See [Troubleshooting Guide](troubleshooting.md)
- **Command Reference**: Full details in [Commands Guide](commands.md)
- **Examples**: Practical setups in [Examples Directory](examples/)

## 🔧 Language Support

Currently supported:

- **Python**: `# track_lore("path/to/doc.md")`
- **TypeScript/JavaScript**: `// track_lore("path/to/doc.md")`

Additional language support can be added through configuration.

---

**Remember**: Dungeon Master protects your project's documentation integrity. Embrace the workflow - your future self and teammates will thank you!
