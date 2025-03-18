#cython: language_level=3

import numpy as np
import cv2

# https://cython.readthedocs.io/en/latest/src/userguide/external_C_code.html

cdef extern from "video_decoder.h":
    cdef struct VDecoder:
        pass
    ctypedef unsigned char uint8_t
    int decoder_init(VDecoder* d)
    void decoder_free(VDecoder* d)
    int decode(VDecoder* d, long size, uint8_t *data)
    uint8_t *decode_rgb(VDecoder* d)

cdef class VideoDecoder:
    cdef VDecoder d

    def __cinit__(self):
        decoder_init(&self.d)

    def __dealloc__(self):
        decoder_free(&self.d)

    def decode(self, nalu: bytes) -> int:
        return decode(&self.d, len(nalu), nalu)

    def rgb(self) -> bytes:
        frame = decode_rgb(&self.d)

        print("frame {}".format(len(frame)))
        np_array = np.frombuffer(frame, np.uint8)
        return cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)

