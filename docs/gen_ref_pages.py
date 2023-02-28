"""Generate the code reference pages and navigation.

Source: https://mkdocstrings.github.io/recipes/#automatic-code-reference-pages
"""

import pathlib

import mkdocs_gen_files
import typeguard


@typeguard.typechecked
def main() -> None:
    """MKDocs generation."""
    nav = mkdocs_gen_files.nav.Nav()  # type: ignore[no-untyped-call]

    for path in sorted(pathlib.Path("src").rglob("*.py")):
        module_path = path.relative_to("src").with_suffix("")
        doc_path = path.relative_to("src").with_suffix(".md")
        full_doc_path = pathlib.Path("reference", doc_path)

        parts = tuple(module_path.parts)

        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")
            full_doc_path = full_doc_path.with_name("index.md")
        elif parts[-1] == "__main__":
            continue

        nav[parts] = doc_path.as_posix()

        with mkdocs_gen_files.open(full_doc_path, "w") as file:
            ident = ".".join(parts)
            file.write(f"::: {ident}")

        mkdocs_gen_files.set_edit_path(full_doc_path, path)

    with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())


main()
