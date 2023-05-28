from math import log2


def level(points: int) -> int:
    one_review_points = 100

    if points < one_review_points:
        return 0, one_review_points

    level_ = int(log2(points//one_review_points)) + 1

    return level_, 2**level_ * one_review_points


def points_naming(points: int) -> str:
    points_names = ('баллов', 'балл', 'балла', 'балла', 'балла',
                    'баллов', 'баллов', 'баллов', 'баллов', 'баллов')
    return points_names[int(str(points)[-1])]
