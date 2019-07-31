from pathlib import Path
import difflib

if __name__ == "__main__":
    expected_path = Path("stubs/expected")
    generated_path = Path("stubs/generated")

    expected_stubs = sorted(list(expected_path.rglob("*.pyi")))
    generated_stubs = sorted(list(generated_path.rglob("*.pyi")))

    assert len(expected_stubs) == len(generated_stubs), (
            "Number of stubs differs. \n"
            "#Expected (%s) != #Generated (%s)" % (expected_stubs, generated_stubs))

    for e, g in zip(expected_stubs, generated_stubs):
        print("Compare %s with %s" % (e, g))
        with open(e) as ef, open(g) as gf:
            elines = ef.readlines()
            glines = gf.readlines()
            assert elines == glines, "Expected (%s) != Generated (%s): \n" % (e, g) + \
                "".join(list(difflib.ndiff(elines, glines)))
