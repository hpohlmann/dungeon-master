# 🏰 Dungeon Master

**A context-tracking pre-commit tool for Cursor AI integration.**

Blocks commits until meaningful documentation exists. Creates structured templates that Cursor fills with intelligent content. Enforces quality through automated validation.

```bash
pip install cursor-dungeon-master
dm init
```

---

## ⚔️ How It Works

### 1. **Track Important Files**

Add a simple decorator to mark files for documentation:

```python
# @track_context("auth_service.md")
class AuthService:
    def authenticate(self, token: str) -> bool:
        pass
```

### 2. **Commit Triggers Template Creation**

When you commit, Dungeon Master creates a structured template:

```markdown
# auth_service.py - Context Documentation

## Purpose

<Describe the overall intent and responsibility>

## Key Functions

- **authenticate(token)**: <Explain purpose and usage>
- **generate_token(user_id)**: <Explain purpose and usage>

## Dependencies

- `jwt`: <Why this dependency is needed>
```

### 3. **🛡️ Commit Blocked Until Complete**

```
⚔️ COMMIT BLOCKED: Documentation Required
📜 Templates created: lore/auth_service.md
🧙‍♂️ Use Cursor to complete documentation
```

### 4. **🧙‍♂️ Cursor Fills Templates**

Use Cursor to replace placeholders with meaningful content:

```markdown
## Purpose

Provides JWT-based authentication with secure password hashing
and session management for user login workflows.

## Key Functions

- **authenticate(token)**: Validates JWT tokens and returns user data
- **generate_token(user_id)**: Creates signed JWT tokens for authenticated users
```

### 5. **✅ Validation Passes, Commit Proceeds**

```
🏰 Dungeon Master: All validations passed
📜 Documentation complete and validated
⚡ Commit proceeding...
```

---

## 🎯 Quick Start

```bash
# Install
pip install cursor-dungeon-master

# Initialize in your repo
dm init
pre-commit install

# Mark files for tracking
echo '# @track_context("my_feature.md")' >> src/my_feature.py

# Commit triggers the workflow
git add . && git commit -m "Add new feature"
```

**That's it!** Dungeon Master will guide you through the rest.

---

## 🗡️ Commands

| Command         | Purpose                                      |
| --------------- | -------------------------------------------- |
| `dm init`       | 🏰 Initialize Dungeon Master in repository   |
| `dm update`     | 📜 Create/update templates for tracked files |
| `dm list --all` | 🗺️ Show all tracked files and status         |
| `dm validate`   | 🛡️ Check what would block commits            |
| `dm review`     | 🔮 Manage significant changes                |

---

## 📜 Template Example

**Generated Template:**

```markdown
# auth_service.py - Context Documentation

## Purpose

<Describe the overall intent and responsibility of this file>

## Usage Summary

**File Location**: `src/auth_service.py`

**Key Dependencies**:

- `jwt`: <explain why needed>
- `hashlib`: <explain why needed>

## Key Functions

- **authenticate(self, token)**: <Explain purpose>
- **generate_token(self, user_id)**: <Explain purpose>

## Integration Notes

<How this integrates with the broader system>
```

**After Cursor Completion:**

```markdown
# auth_service.py - Context Documentation

## Purpose

Comprehensive authentication service handling user login, JWT token
management, and secure session tracking. Core security component
for all user authentication workflows.

## Usage Summary

**File Location**: `src/auth_service.py`

**Key Dependencies**:

- `jwt`: Provides JWT encoding/decoding for stateless authentication
- `hashlib`: SHA-256 password hashing for secure credential storage

## Key Functions

- **authenticate(self, token)**: Validates JWT tokens, returns user data or raises AuthError
- **generate_token(self, user_id)**: Creates signed JWT with user claims and expiration

## Integration Notes

Used by API middleware for request authentication. Integrates with
user service for credential validation and session management.
```

---

## 🏺 Project Structure

```
your_project/
├── 📜 lore/                    # Generated documentation
│   ├── auth_service.md         # ✅ Complete
│   ├── api_client.md          # ⚠️ Needs completion
│   └── utils.md               # ✅ Complete
├── 🏹 src/
│   ├── auth.py                # @track_context("auth_service.md")
│   ├── client.js              # @track_context("api_client.md")
│   └── utils.py               # @track_context("utils.md")
└── ⚔️ hooks/
    └── pre_commit_hook.py     # Enforcement engine
```

---

## 🛡️ Validation Rules

| Status         | Rule                           | Action                          |
| -------------- | ------------------------------ | ------------------------------- |
| ⚔️ **BLOCKED** | Template missing               | Creates template, blocks commit |
| ⚔️ **BLOCKED** | Contains `<placeholders>`      | Must complete with Cursor       |
| ⚔️ **BLOCKED** | Significant changes unreviewed | Run `dm review --mark-reviewed` |
| ✅ **PASSES**  | All documentation complete     | Commit proceeds                 |

---

## 🔮 Advanced Features

### 🎲 Change Detection

Automatically detects significant code changes:

```bash
🔮 Significant changes detected:
   📄 auth_service.py
      • New function: validate_permissions()
      • Modified function: authenticate()

💎 Use 'dm review --mark-reviewed' if changes are minor
⚔️ Update documentation if changes affect core functionality
```

### 🧙‍♂️ Language Support

- **🐍 Python**: Full AST analysis with intelligent templates
- **⚡ JavaScript/TypeScript**: Advanced regex parsing
- **🗡️ Other Languages**: Basic analysis with manual completion

### 🏰 Pre-commit Integration

```yaml
repos:
  - repo: local
    hooks:
      - id: dungeon-master
        name: "🏰 Dungeon Master"
        entry: dm validate
        language: python
        always_run: true
```

---

## 🌟 Philosophy

**This isn't auto-documentation.** It's a **structured collaboration** between:

- 🧙‍♂️ **AI (Cursor)** - Provides intelligence and content
- 🏰 **Dungeon Master** - Enforces structure and consistency
- ⚔️ **Developers** - Maintain control and oversight
- 📜 **Documentation** - Stays current through commit-time enforcement

**Result**: Documentation that's meaningful, current, consistent, and enforced.

---

## 🗺️ Development

```bash
git clone https://github.com/yourusername/dungeon-master.git
cd dungeon-master
pip install -e .[dev]
python tests/verify_installation.py
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

**💎 Remember**: This creates a structured way for AI assistants like Cursor to help you maintain accurate, meaningful documentation as part of your development workflow.

🏰 _"In the dungeon of development, proper documentation is your most powerful spell."_
