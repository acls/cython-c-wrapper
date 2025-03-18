#ifndef _VIDEO_DECODER_H_
#define _VIDEO_DECODER_H_

/**
 * A set of helper functions for decoding video by linking against FFmpeg.
 */

#ifdef __cplusplus
extern "C" {
#endif

// #include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>
#include <libswscale/swscale.h>
#include <libavutil/imgutils.h>

#ifdef __cplusplus
};
#endif

#include <stdint.h>
#include <stdbool.h>

#define VID_DECODE_FFMPEG_ERR (-2)
#define VID_DECODE_EOF (-1)
#define VID_DECODE_SUCCESS 0


struct VDecoder {
    AVCodecContext *c;
    AVFrame *frame;

    AVFrame *frame_rgb;
    struct SwsContext *sws_context;
};

struct VDecoder* decoder_alloc();
void decoder_free(struct VDecoder* d);
int decode(struct VDecoder* d, long size, uint8_t *data);

int decode_rgb(struct VDecoder* d);

#endif // _VIDEO_DECODER_H_
