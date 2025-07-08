# ----------------------------------------
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @author       : 
# @email        : 
# @time         : 2025/6/23 14:19
# @file         : build_lua_script.py
# @Desc         :
# -----------------------------------------

# import from official
import os
import re
from pathlib import Path
# import from third-party
# import from self-defined

REQUIRE_PATTERN = re.compile(r'''
    \s*                             # Leading whitespace
    (?:local\s+)?                   # Optional 'local' keyword
    (?:(\w+)\s*=\s*)?               # Optional variable name and equal sign
    require\s*                      # 'require' keyword
    \(\s*["\'](.*?)["\']\s*\)       # Module name, using non-greedy matching
''', re.VERBOSE)


def get_dependencies(lua_file_path: Path):
    """
    Extract dependencies from a Lua file
    :param lua_file_path: Path to the Lua file
    :return: List of dependencies (module names)
    """
    try:
        with open(lua_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return [match.group(2) for match in REQUIRE_PATTERN.finditer(content)]
    except FileNotFoundError:
        print(f"Error: File {lua_file_path} not found.")
        return []
    except Exception as e:
        print(f"Error reading file {lua_file_path}: {e}")
        return []

def topological_sort(graph):
    # Build the reversed graph
    reversed_graph = {node: [] for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            reversed_graph[neighbor].append(node)

    in_degree = {node: 0 for node in reversed_graph}
    for node in reversed_graph:
        for neighbor in reversed_graph[node]:
            in_degree[neighbor] = in_degree.get(neighbor, 0) + 1

    queue = [node for node in in_degree if in_degree[node] == 0]
    sorted_nodes = []

    while queue:
        node = queue.pop(0)
        sorted_nodes.append(node)
        if node in reversed_graph:
            for neighbor in reversed_graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    return sorted_nodes  # Directly return the correct order


class LuaBuilder:
    def __init__(self, root: str, output: str, verbose=False, mock=False, debug=False):
        """
        Organize Lua files based on dependencies in a Lua project
        :param root: Directory of the Lua project
        :param output: Path to the output Lua script file
        :param verbose: Whether to print detailed information
        :return:
        """
        self.lua_project_dir = Path(root)
        self.output_file = Path(output)
        self.verbose = verbose
        self.mock = mock
        self.debug = debug

        self.sorted_modules = []

    def _find_module_file(self, module_name):
        """
        Find the path to the module file
        :param module_name: Module name, e.g., 'com/vector'
        :return: Path to the module file
        """
        module_name_strip = module_name.strip()
        if module_name_strip == "":
            raise ValueError("Module name cannot be empty")
        if module_name_strip != module_name:
            raise ValueError("Module name must not contain spaces")
        if ".." in module_name_strip:
            raise ValueError("Module name must not contain '..'")

        # Construct the full path
        file_path = self.lua_project_dir / f"{module_name}.lua"

        return file_path

    def build_dependency_graph(self, root_module):
        """
        Build the dependency graph
        :param root_module: Name of the root module (usually 'global')
        :return: Dependency graph as a dictionary
        """
        graph = {}
        queue = [root_module]

        while queue:
            module = queue.pop(0)
            module_path = self._find_module_file(module)
            if module_path.is_file():
                if module not in graph:
                    dependencies = get_dependencies(module_path)
                    graph[module] = dependencies
                    queue.extend([dep for dep in dependencies if dep not in graph])
            else:
                print(f"Warning: Module file {module_path} not found.")

        return graph

    def check_path(self, entry_point):
        # Check if the Lua project directory exists
        if not self.lua_project_dir.exists():
            raise FileNotFoundError(f"The specified Lua project directory does not exist: {self.lua_project_dir}")

        # Create the parent directory of the output file
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        # Look for the entry_point file
        entry_file_path = self.lua_project_dir / Path(f"{entry_point}.lua")
        if not entry_file_path.is_file():
            raise FileNotFoundError(f"The {entry_point} file was not found in the Lua project directory")

    def merge_content(self) -> str:
        """
        Organize Lua files based on dependencies in entry_point file
        """
        # Initialize the content of the output file
        content = ""
        if self.debug:
            content += "require(\"vscode/console\")\n"
        sorted_modules = self.sorted_modules

        # Iterate through the sorted modules and add the corresponding Lua file content
        for index, module in enumerate(sorted_modules):
            module_path = self._find_module_file(module)
            try:
                if module_path.parent.name == "mock" and not self.mock:
                    if self.verbose:
                        print(f"Skipping: {index+1}/{len(sorted_modules)}: {module_path} [In mock directory, currently compiling for production]")
                    continue
                else:
                    if self.verbose:
                        print(f"Merging: {index+1}/{len(sorted_modules)}: {module_path}")
                with open(module_path, 'r', encoding='utf-8') as file:
                    content += f"-- File: {module_path}\n"
                    # Import content ============================================
                    each_content = file.read()
                    # Remove require statements, as they have already been processed
                    each_content = REQUIRE_PATTERN.sub('', each_content)
                    content += each_content
                    # ============================================================
                    content += f"\n\n"
            except FileNotFoundError:
                print(f"Warning: Module file {module_path} not found.")
            except Exception as e:
                print(f"Warning: Unable to read module {module} ({module_path}): {str(e)}")

        return content

    def output(self, content: str):
        output_file = str(self.output_file)
        # Write the merged content to the output file
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(content)
        except Exception as e:
            raise RuntimeError(f"Unable to write to the output file {output_file}: {str(e)}")

        # If verbose mode is enabled, print the path to the output file
        if self.verbose:
            print(f"The Lua script has been organized and merged based on dependencies to: {output_file}")

    def run(self, entry_point="main"):
        # Perform path checking and build operations
        self.check_path(entry_point)

        # Build the dependency graph
        dependency_graph = self.build_dependency_graph(entry_point)

        # Topological sorting
        self.sorted_modules = topological_sort(dependency_graph)

        # Organize the content
        content = self.merge_content()

        # Perform the output operation
        self.output(content)