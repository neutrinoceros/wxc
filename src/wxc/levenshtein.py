def levenshtein_distance(seq1: str, seq2: str, max_dist: int) -> int:
    """
    Compute the levenshtein distance between seq1 and seq2.
    From https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/

    Parameters
    ----------
    seq1, seq2 : str
        The strings to compute the distance between
    max_dist : integer
        If not None, maximum distance returned (see notes).

    Returns
    -------
    The Levenshtein distance as an integer.

    Notes
    -----
    This computes the Levenshtein distance, i.e. the number of edits to change
    seq1 into seq2. If a maximum distance is passed, the algorithm will stop as soon
    as the number of edits goes above the value. This allows for an earlier break
    and speeds calculations up.
    """
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    max_dist = min(max(size_x, size_y), max_dist)

    if abs(size_x - size_y) > max_dist:
        return max_dist + 1

    matrix = []
    for _ in range(size_x):
        # this somewhat clumsy initialization is intended to avoid
        # side effects of the "smart" way. See
        # >>> matrix = [[0]*size_y]*size_x
        # >>> matrix[0] is matrix[1]
        # True
        matrix.append([0] * size_y)
    for x in range(size_x):
        matrix[x][0] = x
    for y in range(size_y):
        matrix[0][y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1,
                    matrix[x - 1][y - 1],
                    matrix[x][y - 1] + 1,
                )
            else:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1,
                    matrix[x - 1][y - 1] + 1,
                    matrix[x][y - 1] + 1,
                )

        # Early break: the minimum distance is already larger than
        # maximum allow value, can return safely.
        if min(matrix[x]) > max_dist:
            return max_dist + 1
    return matrix[size_x - 1][size_y - 1]
