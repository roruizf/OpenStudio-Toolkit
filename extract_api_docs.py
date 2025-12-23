"""
Script to extract API documentation from OpenStudio-Toolkit codebase.
This script analyzes all Python files and extracts:
- Function names and signatures
- Docstrings
- Return attributes (for dict/dataframe functions)
- Incomplete attributes (set to None)
"""

import ast
import os
from pathlib import Path
from typing import List, Dict, Any, Set
import json

class FunctionAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        
    def visit_FunctionDef(self, node):
        func_info = {
            'name': node.name,
            'lineno': node.lineno,
            'args': [arg.arg for arg in node.args.args],
            'returns': ast.unparse(node.returns) if node.returns else None,
            'docstring': ast.get_docstring(node),
            'attributes': [],
            'incomplete_attributes': []
        }
        
        # Look for dictionary returns in the function body
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Dict):
                for key, value in zip(stmt.keys, stmt.values):
                    if isinstance(key, ast.Constant):
                        attr_name = key.value
                        # Check if value is None
                        is_none = isinstance(value, ast.Constant) and value.value is None
                        func_info['attributes'].append(attr_name)
                        if is_none:
                            func_info['incomplete_attributes'].append(attr_name)
        
        self.functions.append(func_info)
        self.generic_visit(node)

def analyze_file(file_path: Path) -> Dict[str, Any]:
    """Analyze a single Python file and extract function information."""
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read())
            analyzer = FunctionAnalyzer()
            analyzer.visit(tree)
            return {
                'file': str(file_path),
                'functions': analyzer.functions
            }
        except Exception as e:
            return {
                'file': str(file_path),
                'error': str(e),
                'functions': []
            }

def main():
    # Base directory
    base_dir = Path('/mnt/c/Users/rober/OneDrive/8_DEVELOPMENT/OpenStudio-Toolkit/src/openstudio_toolkit')
    
    # Find all Python files
    py_files = list(base_dir.rglob('*.py'))
    py_files = [f for f in py_files if '__pycache__' not in str(f)]
    
    results = []
    for py_file in sorted(py_files):
        rel_path = py_file.relative_to(base_dir.parent)
        print(f"Analyzing: {rel_path}")
        result = analyze_file(py_file)
        result['relative_path'] = str(rel_path)
        results.append(result)
    
    # Save results
    output_file = '/mnt/c/Users/rober/OneDrive/8_DEVELOPMENT/OpenStudio-Toolkit/api_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nAnalysis complete! Results saved to: {output_file}")
    print(f"Total files analyzed: {len(results)}")
    total_functions = sum(len(r['functions']) for r in results)
    print(f"Total functions found: {total_functions}")

if __name__ == '__main__':
    main()
