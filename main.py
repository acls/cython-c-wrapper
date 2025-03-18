import pyexamples


import cv2
import numpy as np
import torch
from ultralytics import YOLO

import json
import argparse

# TODO: import vdecoder

# Default
model = "ground.pt"
conf = 0.25
imgsz = 640
maxdet = 10
classes = [
    0,  # person
    1,  # bicycle
    2,  # car
    3,  # motorcycle
    4,  # airplane
    5,  # bus
    6,  # train
    7,  # truck
    8,  # boat
    14,  # bird
    15,  # cat
    16,  # og
    17,  # horse
    18,  # sheep
    19,  # cow
    21,  # bear
]


def main():
    global model
    global conf
    global imgsz
    global maxdet
    global classes

    global device
    global yolo
    # global decoder

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str)
    parser.add_argument("--conf", type=restricted_float)
    parser.add_argument("--imgsz", type=int)
    parser.add_argument("--maxdet", type=int)
    parser.add_argument(  # --classes 0 1 2
        "--classes", nargs="+", help="<Required> Set flag", type=int
    )
    args = parser.parse_args()

    # Overwrite defaults if set.
    if args.model != None:
        model = args.model
    if args.conf != None:
        conf = args.conf
    if args.imgsz != None:
        imgsz = args.imgsz
    if args.maxdet != None:
        maxdet = args.maxdet
    if args.classes != None:
        classes = args.classes

    print("model: {}".format(model))
    print("conf: {}".format(conf))
    print("imgsz: {}".format(imgsz))
    print("maxdet: {}".format(maxdet))
    print("classes: {}".format(classes))

    # setup GPU if available, else default to cpu
    print(torch.cuda.is_available())
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    yolo = YOLO(model)
    yolo.to(device=device)

    snapshotAndClassify()


def restricted_float(x):
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError("{x} not a floating-point literal".format(x=x))
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("{x} not in range [0.0, 1.0]".format(x=x))
    return x


def snapshotAndClassify():
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
    print("sps status {}".format(status)) # -1 is expected since no frame is included.
    status = d.decode(pps)
    print("pps status {}".format(status)) # -1 is expected since no frame is included.

    naluFile = "first_frame.nalu"
    with open(naluFile, "rb") as f:
        prefix = bytes([0x00, 0x00, 0x00, 0x01])
        # decode with prepend bytes
        status = d.decode(prefix + f.read())
        print("nalu decoded {}".format(status == 0))

    imgMat = d.rgb()
    print("imgMat {}".format(imgMat))
    (height, width) = imgMat.shape[:2]

    print("yolo.track 01")
    results = yolo.track(
        imgMat,
        verbose=True,
        imgsz=imgsz,
        max_det=maxdet,
        conf=conf,
        classes=classes,
        device=device,
    )
    print("yolo.track 02")
    detections = []
    MARGIN_SIZE_NORMALIZER = (
        128  # Divide width by this to get appropriate margin for any resolution
    )
    margin = width // MARGIN_SIZE_NORMALIZER
    print("yolo.track 03")
    for r in results:
        if r:
            for box in r.boxes:
                detections.append(
                    {
                        "id": int(box.id),
                        "class_id": int(box.cls),
                        "class": int(box.cls),  # TODO: map class in golang
                        "conf": float(box.conf),
                        "box": [  # [x-min, y-min, x-max, y-max]
                            int(box.data[0][0])
                            - margin,  # make bounding box less tight
                            int(box.data[0][1]) - margin,
                            int(box.data[0][2]) + margin,
                            int(box.data[0][3]) + margin,
                        ],
                    }
                )

    print("publish cameras.id.boxes")
    b = json.dumps(
        {
            "width": width,
            "height": height,
            "detections": detections,
        }
    )
    # await nc.publish("cameras.id.boxes", b.encode("utf-8"))
    print("b: {}".format(b))

if __name__ == "__main__":
    main()
