import shlex

def tokenize_command_line_string_to_args(command_line):
    tokens = shlex.split(command_line)
    return tokens[1:] if tokens else []

def parse_args(tokens):
    if not tokens:
        raise ValueError("No arguments provided. Expected: -c <file.c> [functions ...] [-category cat1 cat2 ...]")

    result = {}
    current_file = None
    categories = None
    density = 1  # Default density is medium
    i = 0

    while i < len(tokens):
        token = tokens[i]
        if token == '-c':
            i += 1
            if i >= len(tokens):
                raise ValueError("Expected a filename after -c")
            filename = tokens[i]
            if not filename.endswith('.c'):
                raise ValueError(f"Invalid C file name: {filename}")
            current_file = filename
            result[current_file] = []
        elif token == '-category':
            i += 1
            categories = []
            while i < len(tokens) and not tokens[i].startswith('-'):
                categories.append(tokens[i])
                print(f"Adding category: {tokens[i]}")
                i += 1
            continue  # skip normal i += 1
        elif token == '-d' or token == '-density':
            i += 1
            if i >= len(tokens):
                raise ValueError("Expected a density value after -d or -density (low,medium,high)")
            if tokens[i].lower() not in ["low", "medium", "high"]:
                raise ValueError(f"Invalid density value: {tokens[i]}")
            match tokens[i].lower():
                case "low":
                    density = 0
                case "medium":
                    density = 1
                case "high":
                    density = 2

        else:
            if current_file is None:
                raise ValueError(f"Function name '{token}' provided before any -c <file.c>")
            result[current_file].append(token)
        i += 1

    for filename in result:
        if not result[filename]:
            result[filename].append("main")

    if categories is None:
        categories = ["any"]

    return result, categories , density

