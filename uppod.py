#!/usr/bin/env python3
# Based on: https://translate.google.com/translate?sl=ru&tl=en
#           &u=https%3A%2F%2Fhms.lostcut.net%2Fviewtopic.php%3Fid%3D80
import base64


def decode(data):
    # internal var hash:String=
    hash_ = '0123456789WGXMHRUZID=NQVBLihbzaclmepsJxdftioYkngryTwuvihv7ec41D6GpBtXx3QJRiN5WwMf=ihngU08IuldVHosTmZz9kYL2bayE'

    data = _decode_tr(data, 'r', 'A')
    data = data.replace('\n', '')
    hash_ = hash_.split('ih')

    if data.endswith('!'):
        data = data[:-1]
        taba = hash_[3]
        tabb = hash_[2]
    else:
        taba = hash_[1]
        tabb = hash_[0]

    i = 0
    while i < len(taba):
        data = data.replace(tabb[i], '__')
        data = data.replace(taba[i], tabb[i])
        data = data.replace('__', taba[i])
        i += 1

    result = base64.b64decode(data).decode('utf-8')
    return result


def _decode_tr(data, ch1, ch2):
    if data[:-1].endswith(ch1) and data[2] == ch2:
        srev = data[::-1]  # reverse string
        try:
            loc3 = int(float(srev[-2:]) / 2)  # get number at end of string
        except ValueError:
            return data
        srev = srev[2:-3]  # get string between ch1 and ch2
        if loc3 < len(srev):
            i = loc3
            while i < len(srev):
                srev = srev[:i] + srev[i+1:]  # remove char at index i
                i += loc3
        data = srev + '!'
    return data


if __name__ == '__main__':
    encoded = [
        '21A8emaoLFCabAuaAb7jNy9nm0VTWMkDpBMjRKCwVIW0rD82NXHAswlb2M9oYm56QEsMXRSGYfLSMcYasQWIk05czv56QrsMXLSQAfpmN6Ybv5vI3wSiYW5ntQu0c9BMrz',
        '02AE0sQ8DYjGcRfscYNvwVQ2QiRI5RfGWMbp3GVTDW5b0j5T7xabDZxaT8fYT1bJ5ntu0o9v0rE',
        '21AEEbNVYym0hTWNZT73Goi8uOniuO9I0uYfGZBQW0peK8F3Nhpk39SQixbJGxS6HnBasF6Z4lGiQPFSe9FFiazf4SQW6fdwnZxOEDZuYf8ESaf=j55TiJ5ntfu0o9v0rZ',
        '03AEamMjR30W9swo72JYniuOI0uYfGBQWY0pe8F3Nhp39SQixKJGxS6HBasF6ZlGinQPFe9FFiaf4SQW6NdwnZxODZuYf8SafN=j5TiJ5ntu0o9v0rG'
    ]
    for s in encoded:
        print(decode(s))
