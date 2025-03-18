import pyexamples

def main():
    print("HERE 01")
    d = pyexamples.VideoDecoder()
    print("HERE 02")

    d.decode(b"nope")
    print("HERE 03")


if __name__ == "__main__":
    main()
