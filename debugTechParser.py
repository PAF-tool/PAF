import re
from collections import defaultdict

def extract_includes_and_snippets(file_path):
    includes = []
    snippets = defaultdict(lambda: defaultdict(list))  # category -> subcategory -> list of functions

    current_category = None
    current_subcategory = None

    with open(file_path, "r") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Collect includes
        if line.startswith("#include"):
            includes.append(line)
            i += 1
            continue

        # Detect category
        category_match = re.match(r'//\s*===\s*(\w+)\s*===', line)
        if category_match:
            current_category = category_match.group(1).lower()
            current_subcategory = None  # reset subcategory on new category
            i += 1
            continue

        # Detect subcategory
        subcategory_match = re.match(r'//\s*==\s*(LOW|MEDIUM|HIGH)\s*==', line, re.IGNORECASE)
        if subcategory_match:
            current_subcategory = subcategory_match.group(1).lower()
            i += 1
            continue

        # Detect function start
        if current_category and current_subcategory and re.match(r'\b[a-zA-Z_][a-zA-Z0-9_ \*\t]*\b\([^\)]*\)\s*\{', line):
            func_lines = []
            brace_count = 0

            # Start collecting from here
            while i < len(lines):
                current_line = lines[i]
                func_lines.append(current_line)

                brace_count += current_line.count("{")
                brace_count -= current_line.count("}")

                i += 1

                if brace_count == 0:
                    break

            full_func = "".join(func_lines)
            snippets[current_category][current_subcategory].append(full_func)
            continue

        i += 1

    return includes, snippets


def get_func_call_from_definition(func_code):
    match = re.search(r'void\s+([a-zA-Z_]\w*)\s*\(', func_code)
    return f"{match.group(1)}();" if match else None
def extract_function_body(func_code):
    """
    Extracts and returns the full body of a C function.
    """
    lines = func_code.splitlines()
    body_lines = []
    brace_level = 0
    in_body = False

    for line in lines:
        if "{" in line and not in_body:
            in_body = True
            brace_level += line.count("{")
            continue  # skip the opening brace line

        if in_body:
            brace_level += line.count("{")
            brace_level -= line.count("}")
            if brace_level == 0:
                break
            body_lines.append("    " + line.strip())

    return body_lines
