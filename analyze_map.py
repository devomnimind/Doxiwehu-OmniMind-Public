import json
import os
from collections import defaultdict


def analyze():
    # Load map
    if not os.path.exists("omnimind_structure_map.json"):
        print("Map not found.")
        return

    with open("omnimind_structure_map.json", "r") as f:
        data = json.load(f)

    # Convert to easier structure
    # Map: path -> {imports: [], concepts: []}
    files = data

    # 1. Build Dependency Graph (Who imports whom?)
    # Since imports are usually module names (e.g. 'src.cognitive.npu_metrics'), we need to match them to filepaths or at least module names.
    # Simplified: We treat import strings as edges.

    imported_modules = set()
    file_modules = {}  # path -> module_name

    for path, info in files.items():
        # Heuristic for module name from path
        # ./src/governance/npu_metrics.py -> src.governance.npu_metrics
        rel = os.path.relpath(path, ".")
        if rel.startswith("src/"):
            mod = rel.replace("/", ".").replace(".py", "")
            file_modules[path] = mod

        for imp in info["imports"]:
            imported_modules.add(imp)

    # 2. Dead Code Detection
    # If a file in src/ defines a module that is NEVER imported, it MIGHT be dead code (or an entry point).
    potential_dead = []
    for path, mod in file_modules.items():
        if mod not in imported_modules and not path.endswith("main.py") and "scripts" not in path:
            potential_dead.append(path)

    # 3. Specific Clusters
    iit_phi_scripts = [p for p, i in files.items() if "COGNITION" in i["concepts"]]
    membrane_scripts = [
        p
        for p, i in files.items()
        if "membrane" in p.lower() or "world_membrane" in str(i["imports"])
    ]
    validation_scripts = [p for p, i in files.items() if "scripts/science_validation" in p]

    # Check connections
    membrane_connected_to_validation = False
    for v_script in validation_scripts:
        info = files[v_script]
        if any("membrane" in imp for imp in info["imports"]):
            membrane_connected_to_validation = True

    # 4. Islands (Clusters with no incoming or outgoing links to main system)
    # Simplified: Files with 0 imports from src and 0 imports to them
    islands = []
    for path, info in files.items():
        # internal imports
        internal_deps = [i for i in info["imports"] if i.startswith("src")]
        if not internal_deps:
            # and is not imported by anyone?
            mod = file_modules.get(path)
            if mod and mod not in imported_modules:
                islands.append(path)

    print("--- ANALYSIS REPORT ---")
    print(f"Total Files Scanned: {len(files)}")
    print(f"\n[POTENTIAL DEAD CODE] (Not imported by others in src/): {len(potential_dead)}")
    for p in potential_dead[:10]:
        print(f"  - {p}")

    print(f"\n[IIT/PHI CLUSTER] ({len(iit_phi_scripts)} files)")
    for p in iit_phi_scripts[:5]:
        print(f"  - {p}")

    print(f"\n[MEMBRANE CONNECTIVITY]")
    print(f"  - Membrane Scripts: {len(membrane_scripts)}")
    print(
        f"  - Connected to Validation Scripts? {'YES' if membrane_connected_to_validation else 'NO'}"
    )

    print(f"\n[ISLANDS OF KNOWLEDGE] (No internal deps, not imported)")
    for p in islands[:10]:
        print(f"  - {p}")


if __name__ == "__main__":
    analyze()
