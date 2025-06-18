# 🏰 Dungeon Master

**A context-tracking pre-commit tool for Cursor integration.**

Blocks commits until meaningful documentation exists. Creates structured templates that Cursor fills with intelligent content. Enforces quality through automated validation.

```bash
pip install cursor-dungeon-master
dm init
```

---

## 🚀 Quick Start

```bash
# Install
pip install cursor-dungeon-master

# Initialize in your repository
dm init

# Mark files for tracking by adding a comment
echo '# track_lore("my_feature.md")' >> src/my_feature.py

# Commit triggers the workflow
git add . && git commit -m "Add new feature"
```

That's it! Dungeon Master will create documentation templates and block commits until they're complete.

---

## 🗡️ Commands

| Command          | Purpose                                   |
| ---------------- | ----------------------------------------- |
| `dm init`        | Initialize Dungeon Master in repository   |
| `dm create-lore` | Create/update templates for tracked files |
| `dm review`      | Show all tracked files and their status   |
| `dm validate`    | Check what would block commits            |
| `dm map`         | Generate repository structure map         |

---

## ⚔️ How It Works

1. **Track Files**: Add `# track_lore("filename.md")` comments to important files
2. **Commit**: When you commit, templates are created in `.lore/` directory
3. **Complete**: Use Cursor to fill template placeholders
4. **Validate**: Commits are blocked until documentation is complete

### Example Template

```markdown
# my_feature.py - Context Documentation

## Overview

[PLEASE FILL OUT: Overview]

## Key Functions/Components

[PLEASE FILL OUT: Functions/Components]

## Dependencies

[PLEASE FILL OUT: Dependencies]
```

---

## 🛡️ Validation

Commits are blocked when:

- Documentation templates are missing
- Templates contain `[PLEASE FILL OUT: ...]` placeholders
- Significant code changes haven't been reviewed

---

## 🌟 Why Use This?

- **Enforced Documentation**: No more outdated or missing docs
- **AI-Friendly Structure**: Templates work perfectly with Cursor
- **Pre-commit Integration**: Automatic validation before commits
- **Language Support**: Python, JavaScript, TypeScript, and more

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

🏰 _"In the dungeon of development, proper documentation is your most powerful spell."_
