#cython: language_level=3

from libc.stdint cimport uintptr_t

# https://cython.readthedocs.io/en/latest/src/userguide/external_C_code.html

cdef extern from "video_decoder.h":
    cdef struct VDecoder:
        pass
    ctypedef unsigned char uint8_t
    VDecoder* decoder_alloc()
    void decoder_free(VDecoder* d)
    int decode(VDecoder* d, long size, uint8_t *data)
    int decode_rgb(VDecoder* d)

cdef class VideoDecoder:
    cdef VDecoder* ptr

    def __cinit__(self):
        print("HERE alloc 01 0x{:x}".format(<uintptr_t>self.ptr))
        self.ptr = decoder_alloc()
        print("HERE alloc 02 0x{:x}".format(<uintptr_t>self.ptr))
        if self.ptr is NULL:
            raise MemoryError

    def __dealloc__(self):
        print("HERE dealloc 01 0x{:x}".format(<uintptr_t>self.ptr))
        if self.ptr is not NULL:
            print("HERE dealloc 02 0x{:x}".format(<uintptr_t>self.ptr))
            decoder_free(self.ptr)
            print("HERE dealloc 03")
            self.ptr = NULL
            print("HERE dealloc 04 0x{:x}".format(<uintptr_t>self.ptr))

    def decode(self, nalu: bytes) -> int:
        print("HERE decode {}".format(<uintptr_t>self.ptr))
        r = decode(self.ptr, len(nalu), nalu)
        print("HERE decode 02")
        return r


    def rgb(self) -> int:
        # TODO: return rgb bytes
        return decode_rgb(self.ptr)


