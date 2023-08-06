import json


def task_bump_version_patch():
    def run():
        with open("package.json", "r") as f:
            d = json.load(f)

        lead, patch = d["version"].rsplit(".", 1)
        d["version"] = lead + "." + str(int(patch) + 1)

        with open("package.json", "w") as f:
            json.dump(d, f, indent=2)

    return {
        "actions": [run],
    }
