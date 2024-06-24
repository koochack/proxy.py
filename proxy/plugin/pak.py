def scrambleHost(headerHost, shift):
    bArray = bytearray(headerHost)
    colonIdx = bArray.find(b':')
    host = bArray[:colonIdx]
    if shift == "left":
        host.append(host.pop(0))
    if shift == "right":
        host.insert(0, host.pop(-1))
    both = host + bArray[colonIdx:]
    return bytes(both)

pak = b'salam:443'
print(scrambleHost(pak, "right"))
