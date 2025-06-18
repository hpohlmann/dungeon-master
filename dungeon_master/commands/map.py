# track_lore("commands/cli-system.md")
"""
Generate a visual map of repository structure.

This module handles creating a file tree map showing relationships between
source files and documentation, saved as map.md in .lore/ directory.
"""

from pathlib import Path

from rich.console import Console
from rich.tree import Tree

from dungeon_master.core.decorator_parser import scan_repository_for_lore_decorators
from dungeon_master.utils.config import get_lore_directory, load_config

console = Console()


def generate_project_tree(repo_path, mapping, lore_root):
    """
    Generate a project tree structure showing tracked files and their documentation.

    Args:
        repo_path (Path): Repository root path
        mapping (dict): Mapping of lore files to tracked files
        lore_root (str): Path to lore directory

    Returns:
        str: Markdown representation of the project tree
    """
    # Create reverse mapping: source file -> lore files
    file_to_lore = {}
    for lore_file, tracked_files in mapping.items():
        for tracked_file in tracked_files:
            if tracked_file not in file_to_lore:
                file_to_lore[tracked_file] = []
            file_to_lore[tracked_file].append(lore_file)

    # Build directory structure
    tree_data = {}

    # Add source files
    for file_path in file_to_lore.keys():
        parts = Path(file_path).parts
        current = tree_data

        for part in parts[:-1]:  # directories
            if part not in current:
                current[part] = {"type": "dir", "children": {}}
            current = current[part]["children"]

        # Add the file
        filename = parts[-1]
        current[filename] = {
            "type": "file",
            "lore_files": file_to_lore.get(file_path, []),
        }

    # Add lore directory structure
    if mapping:
        lore_path = Path(lore_root)
        if "lore" not in tree_data:
            tree_data[lore_path.name] = {"type": "dir", "children": {}}

        for lore_file in mapping.keys():
            parts = Path(lore_file).parts
            current = tree_data[lore_path.name]["children"]

            for part in parts[:-1]:  # directories
                if part not in current:
                    current[part] = {"type": "dir", "children": {}}
                current = current[part]["children"]

            # Add the lore file
            filename = parts[-1]
            current[filename] = {"type": "lore", "tracked_files": mapping[lore_file]}

    return tree_data


def render_tree_markdown(tree_data, prefix="", is_last=True, level=0):
    """
    Render tree data as markdown with proper tree formatting.

    Args:
        tree_data (dict): Tree structure data
        prefix (str): Current line prefix for tree formatting
        is_last (bool): Whether this is the last item in its level
        level (int): Current nesting level

    Returns:
        str: Markdown representation of the tree
    """
    lines = []
    items = list(tree_data.items())

    for i, (name, data) in enumerate(items):
        is_item_last = i == len(items) - 1

        # Choose the appropriate tree character
        if level == 0:
            line_prefix = ""
            next_prefix = ""
        else:
            line_prefix = prefix + ("└── " if is_item_last else "├── ")
            next_prefix = prefix + ("    " if is_item_last else "│   ")

        if data["type"] == "dir":
            lines.append(f"{line_prefix}📁 {name}/")
            if "children" in data and data["children"]:
                lines.extend(
                    render_tree_markdown(
                        data["children"], next_prefix, is_item_last, level + 1
                    )
                )

        elif data["type"] == "file":
            lore_info = ""
            if data.get("lore_files"):
                lore_list = ", ".join(data["lore_files"])
                lore_info = f" *[tracked by {lore_list}]*"

            lines.append(f"{line_prefix}📄 {name}{lore_info}")

        elif data["type"] == "lore":
            tracked_info = ""
            if data.get("tracked_files"):
                tracked_list = ", ".join(data["tracked_files"])
                tracked_info = f" *[tracks {tracked_list}]*"

            lines.append(f"{line_prefix}📋 {name}{tracked_info}")

    return lines


def run_map():
    """
    Generate a visual representation of repository structure.

    Creates:
    - File tree map of all tracked files
    - Shows relationships between source files and documentation
    - Saves output as map.md in .lore/ directory

    Returns:
        bool: True if map generated successfully
    """
    try:
        console.print("📊 [bold green]Generating Repository Map[/bold green] 📊")
        console.print()

        # Load configuration
        config = load_config()
        lore_root = get_lore_directory(config)
        lore_path = Path(lore_root)

        # Scan for decorators
        console.print("🔍 Scanning repository structure...")
        mapping = scan_repository_for_lore_decorators(config=config)

        if not mapping:
            console.print(
                "  [yellow]No track_lore decorators found - creating basic map[/yellow]"
            )
        else:
            console.print(f"  Found [bold]{len(mapping)}[/bold] documented components")

        console.print()

        # Generate tree structure
        repo_path = Path.cwd()
        tree_data = generate_project_tree(repo_path, mapping, lore_root)

        # Create Rich tree for console display
        rich_tree = Tree("📂 [bold]Project Tree[/bold]")

        def add_to_rich_tree(tree_node, data_dict):
            for name, data in data_dict.items():
                if data["type"] == "dir":
                    folder_node = tree_node.add(f"📁 [blue]{name}/[/blue]")
                    if "children" in data and data["children"]:
                        add_to_rich_tree(folder_node, data["children"])

                elif data["type"] == "file":
                    lore_info = ""
                    if data.get("lore_files"):
                        lore_list = ", ".join(data["lore_files"])
                        lore_info = (
                            f" [italic yellow](tracked by {lore_list})[/italic yellow]"
                        )

                    tree_node.add(f"📄 {name}{lore_info}")

                elif data["type"] == "lore":
                    tracked_info = ""
                    if data.get("tracked_files"):
                        tracked_list = ", ".join(data["tracked_files"])
                        tracked_info = (
                            f" [italic cyan](tracks {tracked_list})[/italic cyan]"
                        )

                    tree_node.add(f"📋 [green]{name}[/green]{tracked_info}")

        add_to_rich_tree(rich_tree, tree_data)
        console.print(rich_tree)
        console.print()

        # Generate markdown content
        console.print("📝 Generating map.md...")

        markdown_lines = render_tree_markdown(tree_data)

        # Create full markdown content
        markdown_content = f"""# Repository Map

Generated on: {Path.cwd().name}

## Project Structure

```
{chr(10).join(markdown_lines)}
```

## Documentation Coverage

"""

        if mapping:
            markdown_content += "### Tracked Components\n\n"
            for lore_file, tracked_files in mapping.items():
                markdown_content += f"- **{lore_file}**\n"
                for tracked_file in tracked_files:
                    markdown_content += f"  - `{tracked_file}`\n"
                markdown_content += "\n"
        else:
            markdown_content += "No tracked components found. Add `track_lore` decorators to start documenting.\n\n"

        markdown_content += """## Legend

- 📁 Directory
- 📄 Source file
- 📋 Documentation file
- *[tracked by ...]* - Source file with documentation
- *[tracks ...]* - Documentation file tracking source files

---
*This map is automatically generated by Dungeon Master. Run `dm map` to update.*
"""

        # Save to map.md
        map_file = lore_path / "map.md"

        # Ensure .lore directory exists
        lore_path.mkdir(exist_ok=True)

        map_file.write_text(markdown_content)

        console.print(f"✅ Map generated and saved to [cyan]{lore_root}/map.md[/cyan]")
        console.print()
        console.print("📋 [bold]Map Summary:[/bold]")
        console.print(f"  • [bold]{len(mapping)}[/bold] documented components")
        console.print(
            f"  • [bold]{sum(len(files) for files in mapping.values())}[/bold] tracked source files"
        )
        console.print(f"  • Saved to [cyan]{map_file}[/cyan]")

        return True

    except Exception as e:
        console.print(f"❌ [red]Error generating map: {e}[/red]")
        return False
