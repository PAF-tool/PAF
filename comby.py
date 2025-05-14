import random
import subprocess
from pathlib import Path
from shutil import copyfile
from debugTechParser import extract_function_body



# --------------------------------------------------------------------------
# Run comby in-place on a file
# --------------------------------------------------------------------------
def run_comby(match_tpl: str, rewrite_tpl: str, file_path: Path) -> bool:
    """Try a dry run with comby to see if the pattern exists, then do the in-place replacement."""
    # Check if comby finds any match
    # This is just used for our error handling so that it doesn't fail silently
    preview = subprocess.run(
        ["comby", match_tpl, rewrite_tpl, str(file_path), "-matcher", ".c"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if not preview.stdout:
        return False

    # Apply the change in-place if something matched
    subprocess.run(
        ["comby", match_tpl, rewrite_tpl, str(file_path),
         "-matcher", ".c", "-in-place"],
        check=True
    )
    return True

# --------------------------------------------------------------------------
# Main injection function
# --------------------------------------------------------------------------
def inject_antidebug(
        includes: list[str],
        categories: dict[str, dict[str, list[str]]],  # category -> level -> [snippets]
        file_targets: dict[str, list[str]],           # file -> [func_name]
        selected_categories: list[str],
        density: int 
    ) -> None:
    """
    Inject anti-debug snippets into specified functions with a global overhead level (density).
    Allows repeated use of snippets if not enough are available.
    """

    normalized_categories = {
        k.lower(): {lvl.lower(): v for lvl, v in sub.items()} for k, sub in categories.items()
    }
    normalized_selected = [c.lower() for c in selected_categories]

    if normalized_selected == ["any"]:
        normalized_selected = list(normalized_categories.keys())

    unknown = [cat for cat in normalized_selected if cat not in normalized_categories]
    if unknown:
        print(f"⚠️ Unknown categories: {unknown}")
        return

    for file_path, func_list in file_targets.items():
        original = Path(file_path)
        modified = original.with_name(original.stem + "_modified.c")
        copyfile(original, modified)

        # Collect and shuffle snippet pools
        available = {lvl: [] for lvl in ["low", "medium", "high"]}
        for cat in normalized_selected:
            for lvl in available:
                available[lvl].extend(normalized_categories[cat].get(lvl, []))
        for lst in available.values():
            random.shuffle(lst)

        for func_name in func_list:
            injected_snippets = []

            if density == 0:  # LOW
                if available["low"]:
                    injected_snippets = [random.choice(available["low"])]
            elif density == 1:  # MEDIUM
                if available["medium"]:
                    injected_snippets = [random.choice(available["medium"])]
                elif available["low"]:
                    injected_snippets = [random.choice(available["low"]) for _ in range(2)]
            elif density == 2:  # HIGH
                if available["high"]:
                    injected_snippets = [random.choice(available["high"])]
                elif len(available["low"]) > 0:
                    injected_snippets = [random.choice(available["low"]) for _ in range(3)]
                elif available["medium"] and available["low"]:
                    injected_snippets = [
                        random.choice(available["medium"]),
                        random.choice(available["low"])
                    ]

            if not injected_snippets:
                print(f"⚠️ No suitable anti-debug code for {func_name} (density {density})")
                continue

            combined_body_lines = []
            for snippet in injected_snippets:
                body_lines = extract_function_body(snippet)
                if not body_lines:
                    print(f"⚠️ Could not extract body from snippet for {func_name}")
                    continue
                combined_body_lines.append("{")
                combined_body_lines.extend(body_lines)
                combined_body_lines.append("}")


            body_txt = "\n".join(combined_body_lines)
            match_tpl = f"{func_name}(:[params]):[spaces]{{:[body]}}"
            rewrite_tpl = f"{func_name}(:[params]):[spaces]{{\n{{\n{body_txt}\n}}\n:[body]}}"

        try:
            success = run_comby(match_tpl, rewrite_tpl, modified)
            if not success:
                print(f"⚠️ Function '{func_name}' not found in {modified}. Skipping.")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Comby failed on {func_name} in {modified}: {e}")

        # Add missing includes
        with open(modified, "r") as f:
            lines = f.readlines()

        existing_includes = {line.strip() for line in lines if line.strip().startswith("#include")}
        missing_includes = set(includes) - existing_includes

        if missing_includes:
            insert_idx = next((i for i, line in enumerate(lines)
                               if line.strip() and not line.strip().startswith(("#", "//"))), 0)
            for include in sorted(missing_includes):
                lines.insert(insert_idx, include + "\n")
                insert_idx += 1

            with open(modified, "w") as f:
                f.writelines(lines)

        print(f"✅ Inlined anti-debug code into: {modified}")
