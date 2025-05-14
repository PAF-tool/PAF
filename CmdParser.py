import os

def parse_args(tokens):
    if not tokens:
        raise ValueError("No arguments provided. Expected: -c <file.c> [functions ...] [-category cat1 cat2 ...] [-d <density>]")

    result = {}
    current_file = None
    categories = None
    density = 1  # Default to medium
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
            if not os.path.isfile(filename):
                raise ValueError(f"File does not exist: {filename}")
            current_file = filename
            result[current_file] = []
        elif token == '-category':
            i += 1
            categories = []
            while i < len(tokens) and not tokens[i].startswith('-'):
                categories.append(tokens[i])
                print(f"📂 Adding category: {tokens[i]}")
                i += 1
            continue  # skip i += 1
        elif token in ('-d', '-density'):
            i += 1
            if i >= len(tokens):
                raise ValueError("Expected a density value after -d or -density (low, medium, high)")
            level = tokens[i].lower()
            if level not in ["low", "medium", "high"]:
                raise ValueError(f"Invalid density value: {level}")
            density = {"low": 0, "medium": 1, "high": 2}[level]
        else:
            if current_file is None:
                raise ValueError(f"Function name '{token}' provided before any -c <file.c>")
            result[current_file].append(token)
        i += 1

    if not result:
        raise ValueError("You must specify at least one file with -c")

    for filename in result:
        if not result[filename]:  # If no function names provided, assume main
            result[filename].append("main")

    if categories is None:
        categories = ["any"]

    # Final summary
    print("✅ Parsed command-line arguments:")
    for file, funcs in result.items():
        print(f"  📝 File: {file}")
        print(f"     ↳ Functions: {', '.join(funcs)}")
    print(f"  📦 Categories: {', '.join(categories)}")
    print(f"  🎛️  Density level: {['LOW', 'MEDIUM', 'HIGH'][density]}")

    return result, categories, density
