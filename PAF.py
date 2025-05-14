import sys
from CmdParser import parse_args
from debugTechParser import extract_includes_and_snippets
from comby import inject_antidebug  # Replace with actual file name if not named yet

def main():
    # Step 1: Extract includes and categorized snippets
    includes, categories = extract_includes_and_snippets("antiDebug.c")
    #{
    #"time_based": {
    #    "low": [func1_code, func2_code],
    #    "high": [func3_code],
    #},
    #"process_scan_based": {
    #    "medium": [func4_code],
    #}
    #}
    # Step 2: Parse command-line arguments
    args = sys.argv[1:]
    file_targets, selected_categories , density = parse_args(args)
    # Step 3: Inject anti-debug into specified files/functions
    inject_antidebug(includes, categories, file_targets, selected_categories, density)

if __name__ == "__main__":
    main()
