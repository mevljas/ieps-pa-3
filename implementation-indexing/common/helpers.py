def find_snippet(tokens: [], indexes: [int]) -> str:
    """
    Generate snippets from a list of tokens and word indexes.
    :param tokens: list of document tokens
    :param indexes: list of found words indexes
    :return: text snippets
    """
    result = []
    new_indexes = set()
    for index in indexes:
        new_indexes = new_indexes.union(set(range(index - 3, index + 1)))
        new_indexes = new_indexes.union(set(range(index + 1, index + 4)))

    new_indexes = list(new_indexes)
    new_indexes.sort()
    for i in range(0, len(new_indexes)):
        current_index = new_indexes[i]
        if i == 0 and current_index > 0:
            result.append('...')
        elif i > 0 and current_index - new_indexes[i - 1] > 1:
            result.append('...')
        result.append(tokens[new_indexes[i]])

    if new_indexes[-1] != len(tokens) - 1:
        result.append('...')

    return " ".join(result)
