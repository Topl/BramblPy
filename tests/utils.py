import os


def assert_equal(x, y):
    assert x == y
    assert not (x != y)


def assert_not_equal(x, y):
    assert x != y
    assert not (x == y)


def read_crypto_test_vectors(fname, maxels=0, delimiter=None):
    assert delimiter is not None and isinstance(delimiter, bytes)
    vectors = []
    path = os.path.join(os.path.dirname(__file__), "data", fname)
    with open(path, "rb") as fp:
        for line in fp:
            line = line.rstrip()
            if line and line[0] != b"#"[0]:
                splt = [x for x in line.split(delimiter)]
                if maxels:
                    splt = splt[:maxels]
                vectors.append(tuple(splt))
    return vectors
