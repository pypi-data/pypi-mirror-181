import itertools

def bannable_product_2(bans, ws, xs):
    ban_w = bans[0]
    ban_x = bans[1]

    for w in ws:
        if w in ban_w:
            continue
        for x in xs:
            if x in ban_x:
                xs = [x for x in xs if not x in ban_x]
                continue

            if w in ban_w:
                break

            yield (w, x)

def bannable_product_3(bans, ws, xs, ys):
    ban_w = bans[0]
    ban_x = bans[1]
    ban_y = bans[2]

    for w in ws:
        if w in ban_w:
            continue
        for x in xs:
            if x in ban_x:
                xs = [x for x in xs if not x in ban_x]
                continue

            if w in ban_w:
                break

            for y in ys:
                if y in ban_y:
                    ys = [y for y in ys if not y in ban_y]
                    continue

                if x in ban_x or w in ban_w:
                    break

                yield (w, x, y)

def bannable_product_4(bans, ws, xs, ys, zs):
    ban_w = bans[0]
    ban_x = bans[1]
    ban_y = bans[2]
    ban_z = bans[3]

    for w in ws:
        if w in ban_w:
            continue
        for x in xs:
            if x in ban_x:
                xs = [x for x in xs if not x in ban_x]
                continue

            if w in ban_w:
                break

            for y in ys:
                if y in ban_y:
                    ys = [y for y in ys if not y in ban_y]
                    continue

                if x in ban_x or w in ban_w:
                    break

                for z in zs:
                    if z in ban_z:
                        zs = [z for z in zs if not z in ban_z]
                        continue

                    if y in ban_y or x in ban_x or w in ban_w:
                        break
                    yield (w, x, y, z)

def bannable_product_5(bans, _0s, _1s, _2s, _3s, _4s):
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]
    ban_4 = bans[4]

    for _0 in _0s:
        if _0 in ban_0:
            continue

        for _1 in _1s:
            if _1 in ban_1:
                _1s = [x for x in _1s if not x in ban_1]
                continue

            if _0 in ban_0:
                break

            for _2 in _2s:
                if _2 in ban_2:
                    _2s = [x for x in _2s if not x in ban_2]
                    continue

                if _1 in ban_1 or _0 in ban_0:
                    break

                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue

                    if _2 in ban_2 or _1 in ban_1 or _0 in ban_0:
                        break

                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue

                        if _3 in ban_3 or _2 in ban_2 or _1 in ban_1 or _0 in ban_0:
                            break

                        yield (_0, _1, _2, _3, _4)


def bannable_product_6(bans, _0s, _1s, _2s, _3s, _4s, _5s):
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]
    ban_4 = bans[4]
    ban_5 = bans[5]

    for _0 in _0s:
        if _0 in ban_0:
            continue

        for _1 in _1s:
            if _1 in ban_1:
                _1s = [x for x in _1s if not x in ban_1]
                continue

            if _0 in ban_0:
                break

            for _2 in _2s:
                if _2 in ban_2:
                    _2s = [x for x in _2s if not x in ban_2]
                    continue

                if _1 in ban_1 or _0 in ban_0:
                    break

                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue

                    if _2 in ban_2 or _1 in ban_1 or _0 in ban_0:
                        break

                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue

                        if _3 in ban_3 or _2 in ban_2 or _1 in ban_1 or _0 in ban_0:
                            break

                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue

                            if _4 in ban_4 or _3 in ban_3 or _2 in ban_2 or _1 in ban_1 or _0 in ban_0:
                                break

                            yield (_0, _1, _2, _3, _4, _5)

def bannable_product_7(bans, _0s, _1s, _2s, _3s, _4s, _5s, _6s):
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]
    ban_4 = bans[4]
    ban_5 = bans[5]
    ban_6 = bans[6]

    for _0 in _0s:
        if _0 in ban_0:
            continue

        for _1 in _1s:
            if _1 in ban_1:
                _1s = [x for x in _1s if not x in ban_1]
                continue

            if _0 in ban_0:
                break

            for _2 in _2s:
                if _2 in ban_2:
                    _2s = [x for x in _2s if not x in ban_2]
                    continue

                if _1 in ban_1 or _0 in ban_0:
                    break

                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue

                    if _2 in ban_2 or _1 in ban_1 or _0 in ban_0:
                        break

                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue

                        if _3 in ban_3 or _2 in ban_2 or _1 in ban_1 or _0 in ban_0:
                            break

                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue

                            if _4 in ban_4 or _3 in ban_3 or _2 in ban_2 or _1 in ban_1 or _0 in ban_0:
                                break

                            for _6 in _6s:
                                if _6 in ban_6:
                                    _6s = [x for x in _6s if not x in ban_6]
                                    continue

                                if _5 in ban_5 or _4 in ban_4 or _3 in ban_3 or _2 in ban_2 or _1 in ban_1 or _0 in ban_0:
                                    break

                                yield (_0, _1, _2, _3, _4, _5, _6)

def bannable_product(bans, *args):
    if len(args) == 1:
        return itertools.product(*args)

    if len(args) == 2:
        return bannable_product_2(bans, *args)

    if len(args) == 3:
        return bannable_product_3(bans, *args)

    if len(args) == 4:
        return bannable_product_4(bans, *args)

    if len(args) == 5:
        return bannable_product_5(bans, *args)

    if len(args) == 6:
        return bannable_product_6(bans, *args)

    if len(args) == 7:
        return bannable_product_7(bans, *args)

    raise Exception('unsupported len ' + str(len(args)))

    return itertools.product(*args)

