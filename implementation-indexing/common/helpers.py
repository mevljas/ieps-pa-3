def find_snippet(document_text: [], indexes: [int]):
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
        result.append(document_text[new_indexes[i]])

    if new_indexes[-1] != len(document_text) - 1:
        result.append('...')

    return " ".join(result)