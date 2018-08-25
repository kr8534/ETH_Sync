def decodeDict(encoded):
    
    b = bytearray()
    b.extend(encoded)

    c0 = str(b[0])
    c1 = str(b[1])
    c4 = str(b[4])
    c5 = str(b[5])
    
    c2 = ""
    if (b[2] == 0):
        c2 = "100"
    elif (b[2] == 1):
        c2 = "200"
    elif (b[2] == 2):
        c2 = "500"
    elif (b[2] == 3):
        c2 = "1000"
    elif (b[2] == 4):
        c2 = "2000"
    else:
        c2 = "5000"

    c3 = ""
    if (b[3] == 0):
        c3 = "1"
    elif (b[3] == 1):
        c3 = "7"
    elif (b[3] == 2):
        c3 = "30"
    else:
        c3 = "365"

    c6 = ""
    if (b[6] == 0):
        c6 = "Male"
    else:
        c6 = "FeMale"

    return c0, c1, c2, c3, c4, c5, c6
    
#print c0, c1, c2, c3, c4, c5

#    b = bytearray()
#    b.extend(decoded[0:7])
#
#    c0 = str(b[0])
#    c1 = str(b[1])
#    c4 = str(b[4])
#    c5 = str(b[5])
#
#    c2 = ""
#    if (b[2] == 0):
#        c2 = "100"
#    elif (b[2] == 1):
#        c2 = "200"
#    elif (b[2] == 2):
#        c2 = "500"
#    elif (b[2] == 3):
#        c2 = "1000"
#    elif (b[2] == 4):
#        c2 = "2000"
#    else:
#        c2 = "5000"
#
#    c3 = ""
#    if (b[3] == 0):
#        c3 = "1"
#    elif (b[3] == 1):
#        c3 = "7"
#    elif (b[3] == 2):
#        c3 = "30"
#    else:
#        c3 = "365"
#
#    c6 = ""
#    if (b[6] == 0):
#        c6 = "Male"
#    else:
#        c6 = "FeMale"
