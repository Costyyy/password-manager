import hashlib


def hash_entry(entry_id, ciphertext):
    # combine id and ciphertext so the leaf is unique to both the identity and content of the entry
    data = entry_id.encode() + bytes(ciphertext)
    return hashlib.sha256(data).digest()


def hash_pair(left, right):
    return hashlib.sha256(left + right).digest()


def build_tree(leaves):
    if not leaves:
        return hashlib.sha256(b"empty").digest()

    # work on a copy so the original list is not modified
    layer = list(leaves)

    while len(layer) > 1:
        # if odd number of nodes, duplicate the last one to make it even
        if len(layer) % 2 == 1:
            layer.append(layer[-1])

        layer = [hash_pair(layer[i], layer[i + 1]) for i in range(0, len(layer), 2)]

    return layer[0]


def compute_root(entries):
    # entries is a list of (id, ciphertext) tuples from the database
    if not entries:
        return build_tree([])

    leaves = [hash_entry(entry_id, ciphertext) for entry_id, ciphertext in entries]
    return build_tree(leaves)


def verify(entries, stored_root):
    return compute_root(entries) == stored_root
