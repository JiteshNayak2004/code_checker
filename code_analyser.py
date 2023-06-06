import ast
import pylint.lint
from jinja2 import Template
from pylint.reporters.text import TextReporter
from io import StringIO


def parse_python_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
        return ast.parse(code)


def calculate_cyclomatic_complexity(node):
    # Calculate cyclomatic complexity for a given node in the AST
    complexity = 1  # Initialize with 1 for the default path

    if isinstance(node, ast.If):
        # Increase complexity for each if condition
        complexity += len(node.orelse)

    if isinstance(node, ast.For) or isinstance(node, ast.While):
        # Increase complexity for each loop
        complexity += 1

    for child in ast.iter_child_nodes(node):
        complexity += calculate_cyclomatic_complexity(child)

    return complexity


def calculate_code_duplication(node):
    # Calculate code duplication for a given node in the AST
    # In this example, we'll count the number of duplicated lines of code
    code_lines = []

    if isinstance(node, ast.FunctionDef):
        # Collect all lines of code in the function
        code_lines = [node.lineno for node in ast.walk(node) if isinstance(node, ast.stmt)]

    duplicated_lines = len(code_lines) - len(set(code_lines))

    return duplicated_lines


def calculate_code_length(node):
    # Calculate code length for a given node in the AST
    if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
        # Count the number of lines in the function or class definition
        return node.body[-1].lineno - node.lineno + 1
    else:
        return 0


def calculate_function_complexity(node):
    # Calculate function complexity for a given node in the AST
    if isinstance(node, ast.FunctionDef):
        # Calculate complexity based on the number of parameters and depth of nesting
        parameter_count = len(node.args.args)
        nesting_depth = max(
            calculate_function_complexity(child) for child in node.body if isinstance(child, ast.FunctionDef)
        )
        return parameter_count + nesting_depth
    else:
        return 0


def analyze_python_file(file_path):
    tree = parse_python_file(file_path)

    metrics = {
        'cyclomatic_complexity': calculate_cyclomatic_complexity(tree),
        'code_duplication': calculate_code_duplication(tree),
        'code_length': calculate_code_length(tree),
        'function_complexity': calculate_function_complexity(tree),
    }

    lint_report_stream = StringIO()
    reporter = TextReporter(lint_report_stream)
    pylint.lint.Run([file_path], reporter=reporter, exit=False)
    lint_report = lint_report_stream.getvalue()

    report_template = Template(
        """
        Code Quality Analysis Report
        ----------------------------

        Metrics:
        - Cyclomatic Complexity: {{ metrics.cyclomatic_complexity }}
        - Code Duplication: {{ metrics.code_duplication }}
        - Code Length: {{ metrics.code_length }}
        - Function Complexity: {{ metrics.function_complexity }}

        Linting Results:
        {{ lint_report }}
        """
    )

    report = report_template.render(metrics=metrics, lint_report=lint_report)
    return report


# Example usage
file_path = r'C:\Users\91636\Desktop\sunil_project\bing.py'
analysis_report = analyze_python_file(file_path)
print(analysis_report)
