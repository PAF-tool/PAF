import sys
from CmdParser import parse_args
from debugTechParser import extract_includes_and_snippets
from comby import inject_antidebug  

def main():
    try:
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
        file_targets, selected_categories, density = parse_args(args)

        # Step 3: Inject anti-debug into specified files/functions
        inject_antidebug(includes, categories, file_targets, selected_categories, density)

    except ValueError as ve:
        print(f"\n❌ Error: {ve}")
        print("\nUsage: ./PAF.py -c <file.c> [functions ...] [-category cat1 cat2 ...] [-d <low|medium|high>]")
        print("Example: ./PAF.py -c example.c main -category time_based -d medium")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
