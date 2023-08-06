""" Helper methods. """


def bytestring(arr):
    """Join an array of bytes into a bytestring. Unlike `bytes()`, this method supports a mixed array with integers and bytes."""
    return b"".join([i if isinstance(i, bytes) else bytes([i]) for i in arr])


def bytearray_to_bits(bytearray):
    """Convert a bytearray to a list of set bits."""
    bits = []
    j = 0
    for byte in bytearray:
        for i in range(8):
            if byte & (1 << i):
                bits.append(j)
            j += 1
    return bits


def version_decode(version):
    """Decode the version number to a string."""
    v1 = (version >> 30) & 3
    v2 = (version >> 20) & 1023
    v3 = (version >> 10) & 1023
    v4 = version & 1023

    if v1 == 0:
        v1 = "U"
    elif v1 == 1:
        v1 = "D"
    elif v1 == 2:
        v1 = "P"
    elif v1 == 3:
        v1 = "R"

    return "%s%s.%s.%s" % (v1, v2, v3, v4)


def pdo_to_can(pdo, node_id=1):
    """Convert a PDO-ID to a CAN-ID."""
    return ((pdo << 14) + 0x40 + node_id).to_bytes(4, byteorder="big").hex()


def can_to_pdo(can, node_id=1):
    """Convert a CAN-ID to a PDO-ID."""
    return (int(can, 16) - 0x40 - node_id) >> 14
