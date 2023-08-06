# Ran when building wheel files for rsm-markup

import subprocess


def build(setup_kwargs):
    subprocess.run(
        "npm install && npm list",
        stdout=subprocess.PIPE,
        check=True,
        shell=True,
        cwd="tree-sitter-rsm",
    )
    subprocess.run(
        "node_modules/.bin/tree-sitter generate",
        stdout=subprocess.PIPE,
        check=True,
        shell=True,
        cwd="tree-sitter-rsm",
    )
    subprocess.run(
        "node_modules/.bin/tree-sitter test",
        stdout=subprocess.PIPE,
        # We need to run this because tree-sitter test creates the .so file in the right
        # place, so it doesn't matter whether the tests fail or pass; thus we use
        # check=False.
        check=False,
        shell=True,
        cwd="tree-sitter-rsm",
    )
    subprocess.run(
        "cp ~/.tree-sitter/bin/rsm.so rsm/",
        stdout=subprocess.PIPE,
        check=True,
        shell=True,
    )


if __name__ == "__main__":
    build(None)
