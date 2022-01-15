from pathlib import Path
import difflib

if __name__ == "__main__":
    expected_path = Path("stubs/expected")
    generated_path = Path("stubs/generated")

    rel_expected_stubs = sorted([p.relative_to(expected_path) for p in expected_path.rglob("*.pyi")])
    rel_generated_stubs = sorted([p.relative_to(generated_path) for p in generated_path.rglob("*.pyi")])

    assert rel_expected_stubs == rel_generated_stubs, (
            "List of stub files do not match: \n"
            "./%s/ \t[ \n\t%s\n]\n"
            "is different from expected one:\n"
            "./%s/ \t[ \n\t%s\n]\n" % (
                generated_path, "\n\t".join(map(str, rel_generated_stubs)),
                expected_path, "\n\t".join(map(str, rel_expected_stubs))
            )
    )

    for rel_sub_path in rel_expected_stubs:
        e = expected_path / rel_sub_path
        g = generated_path / rel_sub_path
        print("Compare %s with %s" % (e, g))
        with open(e, encoding='utf-8') as ef, open(g, encoding='utf-8') as gf:
            elines = ef.readlines()
            glines = gf.readlines()
            assert elines == glines, "Expected (%s) != Generated (%s): \n" % (e, g) + \
                                     "".join(list(difflib.ndiff(elines, glines)))
