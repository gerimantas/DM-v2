"""
Code Analyzer for the AI Programming Assistant.
Provides static analysis of Python code.
"""
import ast
import re
from typing import Dict, List, Any


class CodeAnalyzer:
    """
    Analyzes Python code to identify potential issues and metrics.
    Uses a combination of AST parsing and pattern matching.
    """
    
    def __init__(self):
        """Initialize the code analyzer."""
        # Common anti-patterns to check for
        self.anti_patterns = {
            "bare_except": re.compile(r'except\s*:'),
            "global_vars": re.compile(r'^(?!\s*(def|class)).*=.*$', re.MULTILINE),
            "mutable_defaults": re.compile(r'def\s+\w+\s*\(.*=\s*(\[\]|\{\}|\(\)).*\)'),
        }
    
    def analyze(self, code: str) -> Dict[str, Any]:
        """
        Analyze the provided Python code.
        
        Args:
            code: The Python code to analyze as a string.
            
        Returns:
            Dictionary containing analysis results.
        """
        result = {
            "issues": [],
            "complexity": "Unknown",
            "line_count": 0,
            "function_count": 0,
            "class_count": 0
        }
        
        # Basic metrics
        result["line_count"] = len(code.split('\n'))
        
        # Check for syntax errors first
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            result["issues"].append(f"Syntax error: {str(e)}")
            return result
        
        # Count functions and classes
        result["function_count"] = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
        result["class_count"] = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
        
        # Detect anti-patterns
        self._check_anti_patterns(code, result)
        
        # Check variable naming
        self._check_variable_naming(tree, result)
        
        # Calculate code complexity (simplified)
        complexity = self._calculate_complexity(tree)
        if complexity < 5:
            result["complexity"] = "Low"
        elif complexity < 10:
            result["complexity"] = "Medium"
        else:
            result["complexity"] = "High"
        
        return result
    
    def _check_anti_patterns(self, code: str, result: Dict[str, Any]) -> None:
        """
        Check for common anti-patterns in the code.
        
        Args:
            code: The code to check.
            result: The result dictionary to update.
        """
        # Check for bare except
        if self.anti_patterns["bare_except"].search(code):
            result["issues"].append("Uses bare 'except:' without specifying exceptions")
        
        # Check for mutable default arguments
        if self.anti_patterns["mutable_defaults"].search(code):
            result["issues"].append("Uses mutable default argument (list, dict, etc.)")
        
        # Check for unnecessary global variables
        if len(self.anti_patterns["global_vars"].findall(code)) > 3:
            result["issues"].append("Possible excessive use of global variables")
    
    def _check_variable_naming(self, tree: ast.AST, result: Dict[str, Any]) -> None:
        """
        Check for proper variable naming conventions.
        
        Args:
            tree: The AST tree of the code.
            result: The result dictionary to update.
        """
        for node in ast.walk(tree):
            # Check variable assignments
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                # Variables should use snake_case
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.id) and not node.id.isupper():
                    result["issues"].append(f"Variable '{node.id}' does not follow snake_case convention")
            
            # Check function definitions
            if isinstance(node, ast.FunctionDef):
                # Functions should use snake_case
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    result["issues"].append(f"Function '{node.name}' does not follow snake_case convention")
            
            # Check class definitions
            if isinstance(node, ast.ClassDef):
                # Classes should use CamelCase
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    result["issues"].append(f"Class '{node.name}' does not follow CamelCase convention")
    
    def _calculate_complexity(self, tree: ast.AST) -> int:
        """
        Calculate a simplified cyclomatic complexity of the code.
        
        Args:
            tree: The AST tree of the code.
            
        Returns:
            An integer representing the code complexity.
        """
        complexity = 0
        
        for node in ast.walk(tree):
            # Count control flow statements
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                complexity += 1
            
            # Count boolean operations
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
