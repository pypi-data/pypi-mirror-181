from flatten_everything import flatten_everything


def group_lists_with_intersections(list_, keep_duplicates=False):
    results = [tuple(x) for x in list_]
    results2 = results.copy()
    for r in results:
        rset = set(r)
        newresults2 = []
        for r2 in results2:
            inter = tuple(rset.intersection(set(r2)))
            if inter:
                appe = r + r2
                appe = tuple(set(appe))
                newresults2.append(tuple(sorted(appe)))
            else:
                newresults2.append(tuple(sorted(r2)))

        results2 = newresults2.copy()
        results2 = [x for x in results2 if x]
        results2 = list(set(results2))
    if keep_duplicates:
        flattened = tuple(flatten_everything(results))
        results2 = [
            tuple(flatten_everything([[y] * flattened.count(y) for y in x]))
            for x in results2
        ]
    return results2

