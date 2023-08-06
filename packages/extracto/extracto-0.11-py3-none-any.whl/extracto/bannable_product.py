def _bannable_product_1(bans, _0s):
    ban_0 = bans[0]

    for _0 in _0s:
        if _0 in ban_0:
            continue

        yield (_0,)

def _bannable_product_2(bans, _0s, _1s):
    ban_0 = bans[0]
    ban_1 = bans[1]

    for _0 in _0s:
        if _0 in ban_0:
            continue
        for _1 in _1s:
            if _1 in ban_1:
                _1s = [x for x in _1s if not x in ban_1]
                continue
            if _0 in ban_0:
                break

            yield (_0, _1,)

def _bannable_product_3(bans, _0s, _1s, _2s):
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]

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
                if _0 in ban_0 or _1 in ban_1:
                    break

                yield (_0, _1, _2,)

def _bannable_product_4(bans, _0s, _1s, _2s, _3s): # pragma: no cover
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]

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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break

                    yield (_0, _1, _2, _3,)

def _bannable_product_5(bans, _0s, _1s, _2s, _3s, _4s): # pragma: no cover
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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break
                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue
                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3:
                            break

                        yield (_0, _1, _2, _3, _4,)

def _bannable_product_6(bans, _0s, _1s, _2s, _3s, _4s, _5s): # pragma: no cover
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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break
                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue
                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3:
                            break
                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue
                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4:
                                break

                            yield (_0, _1, _2, _3, _4, _5,)

def _bannable_product_7(bans, _0s, _1s, _2s, _3s, _4s, _5s, _6s): # pragma: no cover
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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break
                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue
                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3:
                            break
                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue
                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4:
                                break
                            for _6 in _6s:
                                if _6 in ban_6:
                                    _6s = [x for x in _6s if not x in ban_6]
                                    continue
                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5:
                                    break

                                yield (_0, _1, _2, _3, _4, _5, _6,)

def _bannable_product_8(bans, _0s, _1s, _2s, _3s, _4s, _5s, _6s, _7s): # pragma: no cover
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]
    ban_4 = bans[4]
    ban_5 = bans[5]
    ban_6 = bans[6]
    ban_7 = bans[7]

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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break
                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue
                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3:
                            break
                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue
                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4:
                                break
                            for _6 in _6s:
                                if _6 in ban_6:
                                    _6s = [x for x in _6s if not x in ban_6]
                                    continue
                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5:
                                    break
                                for _7 in _7s:
                                    if _7 in ban_7:
                                        _7s = [x for x in _7s if not x in ban_7]
                                        continue
                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6:
                                        break

                                    yield (_0, _1, _2, _3, _4, _5, _6, _7,)

def _bannable_product_9(bans, _0s, _1s, _2s, _3s, _4s, _5s, _6s, _7s, _8s): # pragma: no cover
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]
    ban_4 = bans[4]
    ban_5 = bans[5]
    ban_6 = bans[6]
    ban_7 = bans[7]
    ban_8 = bans[8]

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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break
                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue
                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3:
                            break
                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue
                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4:
                                break
                            for _6 in _6s:
                                if _6 in ban_6:
                                    _6s = [x for x in _6s if not x in ban_6]
                                    continue
                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5:
                                    break
                                for _7 in _7s:
                                    if _7 in ban_7:
                                        _7s = [x for x in _7s if not x in ban_7]
                                        continue
                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6:
                                        break
                                    for _8 in _8s:
                                        if _8 in ban_8:
                                            _8s = [x for x in _8s if not x in ban_8]
                                            continue
                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7:
                                            break

                                        yield (_0, _1, _2, _3, _4, _5, _6, _7, _8,)

def _bannable_product_10(bans, _0s, _1s, _2s, _3s, _4s, _5s, _6s, _7s, _8s, _9s): # pragma: no cover
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]
    ban_4 = bans[4]
    ban_5 = bans[5]
    ban_6 = bans[6]
    ban_7 = bans[7]
    ban_8 = bans[8]
    ban_9 = bans[9]

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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break
                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue
                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3:
                            break
                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue
                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4:
                                break
                            for _6 in _6s:
                                if _6 in ban_6:
                                    _6s = [x for x in _6s if not x in ban_6]
                                    continue
                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5:
                                    break
                                for _7 in _7s:
                                    if _7 in ban_7:
                                        _7s = [x for x in _7s if not x in ban_7]
                                        continue
                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6:
                                        break
                                    for _8 in _8s:
                                        if _8 in ban_8:
                                            _8s = [x for x in _8s if not x in ban_8]
                                            continue
                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7:
                                            break
                                        for _9 in _9s:
                                            if _9 in ban_9:
                                                _9s = [x for x in _9s if not x in ban_9]
                                                continue
                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8:
                                                break

                                            yield (_0, _1, _2, _3, _4, _5, _6, _7, _8, _9,)

def _bannable_product_11(bans, _0s, _1s, _2s, _3s, _4s, _5s, _6s, _7s, _8s, _9s, _10s): # pragma: no cover
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]
    ban_4 = bans[4]
    ban_5 = bans[5]
    ban_6 = bans[6]
    ban_7 = bans[7]
    ban_8 = bans[8]
    ban_9 = bans[9]
    ban_10 = bans[10]

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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break
                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue
                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3:
                            break
                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue
                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4:
                                break
                            for _6 in _6s:
                                if _6 in ban_6:
                                    _6s = [x for x in _6s if not x in ban_6]
                                    continue
                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5:
                                    break
                                for _7 in _7s:
                                    if _7 in ban_7:
                                        _7s = [x for x in _7s if not x in ban_7]
                                        continue
                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6:
                                        break
                                    for _8 in _8s:
                                        if _8 in ban_8:
                                            _8s = [x for x in _8s if not x in ban_8]
                                            continue
                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7:
                                            break
                                        for _9 in _9s:
                                            if _9 in ban_9:
                                                _9s = [x for x in _9s if not x in ban_9]
                                                continue
                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8:
                                                break
                                            for _10 in _10s:
                                                if _10 in ban_10:
                                                    _10s = [x for x in _10s if not x in ban_10]
                                                    continue
                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9:
                                                    break

                                                yield (_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10,)

def _bannable_product_12(bans, _0s, _1s, _2s, _3s, _4s, _5s, _6s, _7s, _8s, _9s, _10s, _11s): # pragma: no cover
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]
    ban_4 = bans[4]
    ban_5 = bans[5]
    ban_6 = bans[6]
    ban_7 = bans[7]
    ban_8 = bans[8]
    ban_9 = bans[9]
    ban_10 = bans[10]
    ban_11 = bans[11]

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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break
                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue
                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3:
                            break
                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue
                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4:
                                break
                            for _6 in _6s:
                                if _6 in ban_6:
                                    _6s = [x for x in _6s if not x in ban_6]
                                    continue
                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5:
                                    break
                                for _7 in _7s:
                                    if _7 in ban_7:
                                        _7s = [x for x in _7s if not x in ban_7]
                                        continue
                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6:
                                        break
                                    for _8 in _8s:
                                        if _8 in ban_8:
                                            _8s = [x for x in _8s if not x in ban_8]
                                            continue
                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7:
                                            break
                                        for _9 in _9s:
                                            if _9 in ban_9:
                                                _9s = [x for x in _9s if not x in ban_9]
                                                continue
                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8:
                                                break
                                            for _10 in _10s:
                                                if _10 in ban_10:
                                                    _10s = [x for x in _10s if not x in ban_10]
                                                    continue
                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9:
                                                    break
                                                for _11 in _11s:
                                                    if _11 in ban_11:
                                                        _11s = [x for x in _11s if not x in ban_11]
                                                        continue
                                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10:
                                                        break

                                                    yield (_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11,)

def _bannable_product_13(bans, _0s, _1s, _2s, _3s, _4s, _5s, _6s, _7s, _8s, _9s, _10s, _11s, _12s): # pragma: no cover
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]
    ban_4 = bans[4]
    ban_5 = bans[5]
    ban_6 = bans[6]
    ban_7 = bans[7]
    ban_8 = bans[8]
    ban_9 = bans[9]
    ban_10 = bans[10]
    ban_11 = bans[11]
    ban_12 = bans[12]

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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break
                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue
                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3:
                            break
                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue
                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4:
                                break
                            for _6 in _6s:
                                if _6 in ban_6:
                                    _6s = [x for x in _6s if not x in ban_6]
                                    continue
                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5:
                                    break
                                for _7 in _7s:
                                    if _7 in ban_7:
                                        _7s = [x for x in _7s if not x in ban_7]
                                        continue
                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6:
                                        break
                                    for _8 in _8s:
                                        if _8 in ban_8:
                                            _8s = [x for x in _8s if not x in ban_8]
                                            continue
                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7:
                                            break
                                        for _9 in _9s:
                                            if _9 in ban_9:
                                                _9s = [x for x in _9s if not x in ban_9]
                                                continue
                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8:
                                                break
                                            for _10 in _10s:
                                                if _10 in ban_10:
                                                    _10s = [x for x in _10s if not x in ban_10]
                                                    continue
                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9:
                                                    break
                                                for _11 in _11s:
                                                    if _11 in ban_11:
                                                        _11s = [x for x in _11s if not x in ban_11]
                                                        continue
                                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10:
                                                        break
                                                    for _12 in _12s:
                                                        if _12 in ban_12:
                                                            _12s = [x for x in _12s if not x in ban_12]
                                                            continue
                                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11:
                                                            break

                                                        yield (_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12,)

def _bannable_product_14(bans, _0s, _1s, _2s, _3s, _4s, _5s, _6s, _7s, _8s, _9s, _10s, _11s, _12s, _13s): # pragma: no cover
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]
    ban_4 = bans[4]
    ban_5 = bans[5]
    ban_6 = bans[6]
    ban_7 = bans[7]
    ban_8 = bans[8]
    ban_9 = bans[9]
    ban_10 = bans[10]
    ban_11 = bans[11]
    ban_12 = bans[12]
    ban_13 = bans[13]

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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break
                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue
                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3:
                            break
                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue
                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4:
                                break
                            for _6 in _6s:
                                if _6 in ban_6:
                                    _6s = [x for x in _6s if not x in ban_6]
                                    continue
                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5:
                                    break
                                for _7 in _7s:
                                    if _7 in ban_7:
                                        _7s = [x for x in _7s if not x in ban_7]
                                        continue
                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6:
                                        break
                                    for _8 in _8s:
                                        if _8 in ban_8:
                                            _8s = [x for x in _8s if not x in ban_8]
                                            continue
                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7:
                                            break
                                        for _9 in _9s:
                                            if _9 in ban_9:
                                                _9s = [x for x in _9s if not x in ban_9]
                                                continue
                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8:
                                                break
                                            for _10 in _10s:
                                                if _10 in ban_10:
                                                    _10s = [x for x in _10s if not x in ban_10]
                                                    continue
                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9:
                                                    break
                                                for _11 in _11s:
                                                    if _11 in ban_11:
                                                        _11s = [x for x in _11s if not x in ban_11]
                                                        continue
                                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10:
                                                        break
                                                    for _12 in _12s:
                                                        if _12 in ban_12:
                                                            _12s = [x for x in _12s if not x in ban_12]
                                                            continue
                                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11:
                                                            break
                                                        for _13 in _13s:
                                                            if _13 in ban_13:
                                                                _13s = [x for x in _13s if not x in ban_13]
                                                                continue
                                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12:
                                                                break

                                                            yield (_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13,)

def _bannable_product_15(bans, _0s, _1s, _2s, _3s, _4s, _5s, _6s, _7s, _8s, _9s, _10s, _11s, _12s, _13s, _14s): # pragma: no cover
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]
    ban_4 = bans[4]
    ban_5 = bans[5]
    ban_6 = bans[6]
    ban_7 = bans[7]
    ban_8 = bans[8]
    ban_9 = bans[9]
    ban_10 = bans[10]
    ban_11 = bans[11]
    ban_12 = bans[12]
    ban_13 = bans[13]
    ban_14 = bans[14]

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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break
                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue
                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3:
                            break
                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue
                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4:
                                break
                            for _6 in _6s:
                                if _6 in ban_6:
                                    _6s = [x for x in _6s if not x in ban_6]
                                    continue
                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5:
                                    break
                                for _7 in _7s:
                                    if _7 in ban_7:
                                        _7s = [x for x in _7s if not x in ban_7]
                                        continue
                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6:
                                        break
                                    for _8 in _8s:
                                        if _8 in ban_8:
                                            _8s = [x for x in _8s if not x in ban_8]
                                            continue
                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7:
                                            break
                                        for _9 in _9s:
                                            if _9 in ban_9:
                                                _9s = [x for x in _9s if not x in ban_9]
                                                continue
                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8:
                                                break
                                            for _10 in _10s:
                                                if _10 in ban_10:
                                                    _10s = [x for x in _10s if not x in ban_10]
                                                    continue
                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9:
                                                    break
                                                for _11 in _11s:
                                                    if _11 in ban_11:
                                                        _11s = [x for x in _11s if not x in ban_11]
                                                        continue
                                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10:
                                                        break
                                                    for _12 in _12s:
                                                        if _12 in ban_12:
                                                            _12s = [x for x in _12s if not x in ban_12]
                                                            continue
                                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11:
                                                            break
                                                        for _13 in _13s:
                                                            if _13 in ban_13:
                                                                _13s = [x for x in _13s if not x in ban_13]
                                                                continue
                                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12:
                                                                break
                                                            for _14 in _14s:
                                                                if _14 in ban_14:
                                                                    _14s = [x for x in _14s if not x in ban_14]
                                                                    continue
                                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13:
                                                                    break

                                                                yield (_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14,)

def _bannable_product_16(bans, _0s, _1s, _2s, _3s, _4s, _5s, _6s, _7s, _8s, _9s, _10s, _11s, _12s, _13s, _14s, _15s): # pragma: no cover
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]
    ban_4 = bans[4]
    ban_5 = bans[5]
    ban_6 = bans[6]
    ban_7 = bans[7]
    ban_8 = bans[8]
    ban_9 = bans[9]
    ban_10 = bans[10]
    ban_11 = bans[11]
    ban_12 = bans[12]
    ban_13 = bans[13]
    ban_14 = bans[14]
    ban_15 = bans[15]

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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break
                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue
                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3:
                            break
                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue
                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4:
                                break
                            for _6 in _6s:
                                if _6 in ban_6:
                                    _6s = [x for x in _6s if not x in ban_6]
                                    continue
                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5:
                                    break
                                for _7 in _7s:
                                    if _7 in ban_7:
                                        _7s = [x for x in _7s if not x in ban_7]
                                        continue
                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6:
                                        break
                                    for _8 in _8s:
                                        if _8 in ban_8:
                                            _8s = [x for x in _8s if not x in ban_8]
                                            continue
                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7:
                                            break
                                        for _9 in _9s:
                                            if _9 in ban_9:
                                                _9s = [x for x in _9s if not x in ban_9]
                                                continue
                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8:
                                                break
                                            for _10 in _10s:
                                                if _10 in ban_10:
                                                    _10s = [x for x in _10s if not x in ban_10]
                                                    continue
                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9:
                                                    break
                                                for _11 in _11s:
                                                    if _11 in ban_11:
                                                        _11s = [x for x in _11s if not x in ban_11]
                                                        continue
                                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10:
                                                        break
                                                    for _12 in _12s:
                                                        if _12 in ban_12:
                                                            _12s = [x for x in _12s if not x in ban_12]
                                                            continue
                                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11:
                                                            break
                                                        for _13 in _13s:
                                                            if _13 in ban_13:
                                                                _13s = [x for x in _13s if not x in ban_13]
                                                                continue
                                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12:
                                                                break
                                                            for _14 in _14s:
                                                                if _14 in ban_14:
                                                                    _14s = [x for x in _14s if not x in ban_14]
                                                                    continue
                                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13:
                                                                    break
                                                                for _15 in _15s:
                                                                    if _15 in ban_15:
                                                                        _15s = [x for x in _15s if not x in ban_15]
                                                                        continue
                                                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13 or _14 in ban_14:
                                                                        break

                                                                    yield (_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15,)

def _bannable_product_17(bans, _0s, _1s, _2s, _3s, _4s, _5s, _6s, _7s, _8s, _9s, _10s, _11s, _12s, _13s, _14s, _15s, _16s): # pragma: no cover
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]
    ban_4 = bans[4]
    ban_5 = bans[5]
    ban_6 = bans[6]
    ban_7 = bans[7]
    ban_8 = bans[8]
    ban_9 = bans[9]
    ban_10 = bans[10]
    ban_11 = bans[11]
    ban_12 = bans[12]
    ban_13 = bans[13]
    ban_14 = bans[14]
    ban_15 = bans[15]
    ban_16 = bans[16]

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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break
                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue
                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3:
                            break
                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue
                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4:
                                break
                            for _6 in _6s:
                                if _6 in ban_6:
                                    _6s = [x for x in _6s if not x in ban_6]
                                    continue
                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5:
                                    break
                                for _7 in _7s:
                                    if _7 in ban_7:
                                        _7s = [x for x in _7s if not x in ban_7]
                                        continue
                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6:
                                        break
                                    for _8 in _8s:
                                        if _8 in ban_8:
                                            _8s = [x for x in _8s if not x in ban_8]
                                            continue
                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7:
                                            break
                                        for _9 in _9s:
                                            if _9 in ban_9:
                                                _9s = [x for x in _9s if not x in ban_9]
                                                continue
                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8:
                                                break
                                            for _10 in _10s:
                                                if _10 in ban_10:
                                                    _10s = [x for x in _10s if not x in ban_10]
                                                    continue
                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9:
                                                    break
                                                for _11 in _11s:
                                                    if _11 in ban_11:
                                                        _11s = [x for x in _11s if not x in ban_11]
                                                        continue
                                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10:
                                                        break
                                                    for _12 in _12s:
                                                        if _12 in ban_12:
                                                            _12s = [x for x in _12s if not x in ban_12]
                                                            continue
                                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11:
                                                            break
                                                        for _13 in _13s:
                                                            if _13 in ban_13:
                                                                _13s = [x for x in _13s if not x in ban_13]
                                                                continue
                                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12:
                                                                break
                                                            for _14 in _14s:
                                                                if _14 in ban_14:
                                                                    _14s = [x for x in _14s if not x in ban_14]
                                                                    continue
                                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13:
                                                                    break
                                                                for _15 in _15s:
                                                                    if _15 in ban_15:
                                                                        _15s = [x for x in _15s if not x in ban_15]
                                                                        continue
                                                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13 or _14 in ban_14:
                                                                        break
                                                                    for _16 in _16s:
                                                                        if _16 in ban_16:
                                                                            _16s = [x for x in _16s if not x in ban_16]
                                                                            continue
                                                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13 or _14 in ban_14 or _15 in ban_15:
                                                                            break

                                                                        yield (_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15, _16,)

def _bannable_product_18(bans, _0s, _1s, _2s, _3s, _4s, _5s, _6s, _7s, _8s, _9s, _10s, _11s, _12s, _13s, _14s, _15s, _16s, _17s): # pragma: no cover
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]
    ban_4 = bans[4]
    ban_5 = bans[5]
    ban_6 = bans[6]
    ban_7 = bans[7]
    ban_8 = bans[8]
    ban_9 = bans[9]
    ban_10 = bans[10]
    ban_11 = bans[11]
    ban_12 = bans[12]
    ban_13 = bans[13]
    ban_14 = bans[14]
    ban_15 = bans[15]
    ban_16 = bans[16]
    ban_17 = bans[17]

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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break
                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue
                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3:
                            break
                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue
                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4:
                                break
                            for _6 in _6s:
                                if _6 in ban_6:
                                    _6s = [x for x in _6s if not x in ban_6]
                                    continue
                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5:
                                    break
                                for _7 in _7s:
                                    if _7 in ban_7:
                                        _7s = [x for x in _7s if not x in ban_7]
                                        continue
                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6:
                                        break
                                    for _8 in _8s:
                                        if _8 in ban_8:
                                            _8s = [x for x in _8s if not x in ban_8]
                                            continue
                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7:
                                            break
                                        for _9 in _9s:
                                            if _9 in ban_9:
                                                _9s = [x for x in _9s if not x in ban_9]
                                                continue
                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8:
                                                break
                                            for _10 in _10s:
                                                if _10 in ban_10:
                                                    _10s = [x for x in _10s if not x in ban_10]
                                                    continue
                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9:
                                                    break
                                                for _11 in _11s:
                                                    if _11 in ban_11:
                                                        _11s = [x for x in _11s if not x in ban_11]
                                                        continue
                                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10:
                                                        break
                                                    for _12 in _12s:
                                                        if _12 in ban_12:
                                                            _12s = [x for x in _12s if not x in ban_12]
                                                            continue
                                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11:
                                                            break
                                                        for _13 in _13s:
                                                            if _13 in ban_13:
                                                                _13s = [x for x in _13s if not x in ban_13]
                                                                continue
                                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12:
                                                                break
                                                            for _14 in _14s:
                                                                if _14 in ban_14:
                                                                    _14s = [x for x in _14s if not x in ban_14]
                                                                    continue
                                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13:
                                                                    break
                                                                for _15 in _15s:
                                                                    if _15 in ban_15:
                                                                        _15s = [x for x in _15s if not x in ban_15]
                                                                        continue
                                                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13 or _14 in ban_14:
                                                                        break
                                                                    for _16 in _16s:
                                                                        if _16 in ban_16:
                                                                            _16s = [x for x in _16s if not x in ban_16]
                                                                            continue
                                                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13 or _14 in ban_14 or _15 in ban_15:
                                                                            break
                                                                        for _17 in _17s:
                                                                            if _17 in ban_17:
                                                                                _17s = [x for x in _17s if not x in ban_17]
                                                                                continue
                                                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13 or _14 in ban_14 or _15 in ban_15 or _16 in ban_16:
                                                                                break

                                                                            yield (_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15, _16, _17,)

def _bannable_product_19(bans, _0s, _1s, _2s, _3s, _4s, _5s, _6s, _7s, _8s, _9s, _10s, _11s, _12s, _13s, _14s, _15s, _16s, _17s, _18s): # pragma: no cover
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]
    ban_4 = bans[4]
    ban_5 = bans[5]
    ban_6 = bans[6]
    ban_7 = bans[7]
    ban_8 = bans[8]
    ban_9 = bans[9]
    ban_10 = bans[10]
    ban_11 = bans[11]
    ban_12 = bans[12]
    ban_13 = bans[13]
    ban_14 = bans[14]
    ban_15 = bans[15]
    ban_16 = bans[16]
    ban_17 = bans[17]
    ban_18 = bans[18]

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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break
                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue
                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3:
                            break
                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue
                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4:
                                break
                            for _6 in _6s:
                                if _6 in ban_6:
                                    _6s = [x for x in _6s if not x in ban_6]
                                    continue
                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5:
                                    break
                                for _7 in _7s:
                                    if _7 in ban_7:
                                        _7s = [x for x in _7s if not x in ban_7]
                                        continue
                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6:
                                        break
                                    for _8 in _8s:
                                        if _8 in ban_8:
                                            _8s = [x for x in _8s if not x in ban_8]
                                            continue
                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7:
                                            break
                                        for _9 in _9s:
                                            if _9 in ban_9:
                                                _9s = [x for x in _9s if not x in ban_9]
                                                continue
                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8:
                                                break
                                            for _10 in _10s:
                                                if _10 in ban_10:
                                                    _10s = [x for x in _10s if not x in ban_10]
                                                    continue
                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9:
                                                    break
                                                for _11 in _11s:
                                                    if _11 in ban_11:
                                                        _11s = [x for x in _11s if not x in ban_11]
                                                        continue
                                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10:
                                                        break
                                                    for _12 in _12s:
                                                        if _12 in ban_12:
                                                            _12s = [x for x in _12s if not x in ban_12]
                                                            continue
                                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11:
                                                            break
                                                        for _13 in _13s:
                                                            if _13 in ban_13:
                                                                _13s = [x for x in _13s if not x in ban_13]
                                                                continue
                                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12:
                                                                break
                                                            for _14 in _14s:
                                                                if _14 in ban_14:
                                                                    _14s = [x for x in _14s if not x in ban_14]
                                                                    continue
                                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13:
                                                                    break
                                                                for _15 in _15s:
                                                                    if _15 in ban_15:
                                                                        _15s = [x for x in _15s if not x in ban_15]
                                                                        continue
                                                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13 or _14 in ban_14:
                                                                        break
                                                                    for _16 in _16s:
                                                                        if _16 in ban_16:
                                                                            _16s = [x for x in _16s if not x in ban_16]
                                                                            continue
                                                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13 or _14 in ban_14 or _15 in ban_15:
                                                                            break
                                                                        for _17 in _17s:
                                                                            if _17 in ban_17:
                                                                                _17s = [x for x in _17s if not x in ban_17]
                                                                                continue
                                                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13 or _14 in ban_14 or _15 in ban_15 or _16 in ban_16:
                                                                                break
                                                                            for _18 in _18s:
                                                                                if _18 in ban_18:
                                                                                    _18s = [x for x in _18s if not x in ban_18]
                                                                                    continue
                                                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13 or _14 in ban_14 or _15 in ban_15 or _16 in ban_16 or _17 in ban_17:
                                                                                    break

                                                                                yield (_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15, _16, _17, _18,)

def _bannable_product_20(bans, _0s, _1s, _2s, _3s, _4s, _5s, _6s, _7s, _8s, _9s, _10s, _11s, _12s, _13s, _14s, _15s, _16s, _17s, _18s, _19s): # pragma: no cover
    ban_0 = bans[0]
    ban_1 = bans[1]
    ban_2 = bans[2]
    ban_3 = bans[3]
    ban_4 = bans[4]
    ban_5 = bans[5]
    ban_6 = bans[6]
    ban_7 = bans[7]
    ban_8 = bans[8]
    ban_9 = bans[9]
    ban_10 = bans[10]
    ban_11 = bans[11]
    ban_12 = bans[12]
    ban_13 = bans[13]
    ban_14 = bans[14]
    ban_15 = bans[15]
    ban_16 = bans[16]
    ban_17 = bans[17]
    ban_18 = bans[18]
    ban_19 = bans[19]

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
                if _0 in ban_0 or _1 in ban_1:
                    break
                for _3 in _3s:
                    if _3 in ban_3:
                        _3s = [x for x in _3s if not x in ban_3]
                        continue
                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2:
                        break
                    for _4 in _4s:
                        if _4 in ban_4:
                            _4s = [x for x in _4s if not x in ban_4]
                            continue
                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3:
                            break
                        for _5 in _5s:
                            if _5 in ban_5:
                                _5s = [x for x in _5s if not x in ban_5]
                                continue
                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4:
                                break
                            for _6 in _6s:
                                if _6 in ban_6:
                                    _6s = [x for x in _6s if not x in ban_6]
                                    continue
                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5:
                                    break
                                for _7 in _7s:
                                    if _7 in ban_7:
                                        _7s = [x for x in _7s if not x in ban_7]
                                        continue
                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6:
                                        break
                                    for _8 in _8s:
                                        if _8 in ban_8:
                                            _8s = [x for x in _8s if not x in ban_8]
                                            continue
                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7:
                                            break
                                        for _9 in _9s:
                                            if _9 in ban_9:
                                                _9s = [x for x in _9s if not x in ban_9]
                                                continue
                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8:
                                                break
                                            for _10 in _10s:
                                                if _10 in ban_10:
                                                    _10s = [x for x in _10s if not x in ban_10]
                                                    continue
                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9:
                                                    break
                                                for _11 in _11s:
                                                    if _11 in ban_11:
                                                        _11s = [x for x in _11s if not x in ban_11]
                                                        continue
                                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10:
                                                        break
                                                    for _12 in _12s:
                                                        if _12 in ban_12:
                                                            _12s = [x for x in _12s if not x in ban_12]
                                                            continue
                                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11:
                                                            break
                                                        for _13 in _13s:
                                                            if _13 in ban_13:
                                                                _13s = [x for x in _13s if not x in ban_13]
                                                                continue
                                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12:
                                                                break
                                                            for _14 in _14s:
                                                                if _14 in ban_14:
                                                                    _14s = [x for x in _14s if not x in ban_14]
                                                                    continue
                                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13:
                                                                    break
                                                                for _15 in _15s:
                                                                    if _15 in ban_15:
                                                                        _15s = [x for x in _15s if not x in ban_15]
                                                                        continue
                                                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13 or _14 in ban_14:
                                                                        break
                                                                    for _16 in _16s:
                                                                        if _16 in ban_16:
                                                                            _16s = [x for x in _16s if not x in ban_16]
                                                                            continue
                                                                        if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13 or _14 in ban_14 or _15 in ban_15:
                                                                            break
                                                                        for _17 in _17s:
                                                                            if _17 in ban_17:
                                                                                _17s = [x for x in _17s if not x in ban_17]
                                                                                continue
                                                                            if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13 or _14 in ban_14 or _15 in ban_15 or _16 in ban_16:
                                                                                break
                                                                            for _18 in _18s:
                                                                                if _18 in ban_18:
                                                                                    _18s = [x for x in _18s if not x in ban_18]
                                                                                    continue
                                                                                if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13 or _14 in ban_14 or _15 in ban_15 or _16 in ban_16 or _17 in ban_17:
                                                                                    break
                                                                                for _19 in _19s:
                                                                                    if _19 in ban_19:
                                                                                        _19s = [x for x in _19s if not x in ban_19]
                                                                                        continue
                                                                                    if _0 in ban_0 or _1 in ban_1 or _2 in ban_2 or _3 in ban_3 or _4 in ban_4 or _5 in ban_5 or _6 in ban_6 or _7 in ban_7 or _8 in ban_8 or _9 in ban_9 or _10 in ban_10 or _11 in ban_11 or _12 in ban_12 or _13 in ban_13 or _14 in ban_14 or _15 in ban_15 or _16 in ban_16 or _17 in ban_17 or _18 in ban_18:
                                                                                        break

                                                                                    yield (_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15, _16, _17, _18, _19,)


def bannable_product(bans, *args):
    if len(args) == 1: return _bannable_product_1(bans, *args)
    if len(args) == 2: return _bannable_product_2(bans, *args)
    if len(args) == 3: return _bannable_product_3(bans, *args)
    if len(args) == 4: return _bannable_product_4(bans, *args)
    if len(args) == 5: return _bannable_product_5(bans, *args)
    if len(args) == 6: return _bannable_product_6(bans, *args)
    if len(args) == 7: return _bannable_product_7(bans, *args)
    if len(args) == 8: return _bannable_product_8(bans, *args)
    if len(args) == 9: return _bannable_product_9(bans, *args)
    if len(args) == 10: return _bannable_product_10(bans, *args)
    if len(args) == 11: return _bannable_product_11(bans, *args)
    if len(args) == 12: return _bannable_product_12(bans, *args)
    if len(args) == 13: return _bannable_product_13(bans, *args)
    if len(args) == 14: return _bannable_product_14(bans, *args)
    if len(args) == 15: return _bannable_product_15(bans, *args)
    if len(args) == 16: return _bannable_product_16(bans, *args)
    if len(args) == 17: return _bannable_product_17(bans, *args)
    if len(args) == 18: return _bannable_product_18(bans, *args)
    if len(args) == 19: return _bannable_product_19(bans, *args)
    if len(args) == 20: return _bannable_product_20(bans, *args)


    raise Exception('unsupported bannable_product len ' + str(len(args)))
