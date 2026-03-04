import math


def distance(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )


def calculate_angle(a, b, c):
    BA = (a[0] - b[0], a[1] - b[1])
    BC = (c[0] - b[0], c[1] - b[1])

    dot = BA[0] * BC[0] + BA[1] * BC[1]

    magBA = math.sqrt(BA[0] ** 2 + BA[1] ** 2)
    magBC = math.sqrt(BC[0] ** 2 + BC[1] ** 2)

    if magBA * magBC == 0:
        return 0

    cos_angle = dot / (magBA * magBC)

    cos_angle = max(-1, min(1, cos_angle))

    angle = math.degrees(math.acos(cos_angle))

    return angle