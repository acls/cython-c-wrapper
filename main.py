import pyexamples

def main():
    # AVPacket *pkt;
    # 00000000  00 00 00 01 67 4d 40 2a  8d 8d 20 0f 00 44 fc b8  |....gM@*.. ..D..|
    # 00000010  0b 70 10 10 10 20                                 |.p... |
    sps = bytes([ 0x00, 0x00, 0x00, 0x01, 0x67, 0x4d, 0x40, 0x2a,
                  0x8d, 0x8d, 0x20, 0x0f, 0x00, 0x44, 0xfc, 0xb8,
                  0x0b, 0x70, 0x10, 0x10, 0x10, 0x20 ])
    # 00000000  00 00 00 01 68 ee 38 80                           |....h.8.|
    pps = bytes([ 0x00, 0x00, 0x00, 0x01, 0x68, 0xee, 0x38, 0x80 ])

    # Create decoder
    d = pyexamples.VideoDecoder()
    status = d.decode(sps)
    print("sps status {}".format(status))
    status = d.decode(pps)
    print("pps status {}".format(status))

    # with open("/home/acls/src/nio/plugins/imaging/testdata/first_frame.nalu", "rb") as f:
    #     b = bytes([0x00, 0x00, 0x00, 0x01])
    #     fb = f.read()
    #     status = d.decode(b + fb)
    #     print("nalu status {}".format(status))


if __name__ == "__main__":
    main()
