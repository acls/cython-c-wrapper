
#include "video_decoder.h"

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
// #include <string.h>

#include <libavcodec/avcodec.h>
#include <libswscale/swscale.h>
#include <libavutil/imgutils.h>


int decoder_init(struct VDecoder* d) {
    const AVCodec *codec;

    codec = avcodec_find_decoder(AV_CODEC_ID_H264);
    if (!codec) {
        fprintf(stderr, "Codec not found\n");
        return -1;
    }

    d->c = avcodec_alloc_context3(codec);
    if (!d->c) {
        fprintf(stderr, "Could not allocate video codec context\n");
        return -1;
    }

    if (avcodec_open2(d->c, codec, NULL) < 0) {
        fprintf(stderr, "Could not open codec\n");
        return -1;
    }

    d->frame = av_frame_alloc();
    if (!d->frame) {
        fprintf(stderr, "Could not allocate video frame\n");
        return -1;
    }

    return 0;
}

void decoder_free(struct VDecoder* d) {
    avcodec_free_context(&d->c);
    av_frame_free(&d->frame);
}

static
int decode_packet(struct VDecoder *d, AVPacket *pkt) {
    if (avcodec_send_packet(d->c, pkt) < 0) {
        return -1;
    }
    if (avcodec_receive_frame(d->c, d->frame) < 0) {
        return -1;
    }
    return 0;
}

int decode(struct VDecoder* d, long size, uint8_t *data) {
    int ret;
    AVPacket *pkt;
    pkt = av_packet_alloc();
    if (!pkt)
        return -1;
    pkt->size = size;
    pkt->data = data;

    ret = decode_packet(d, pkt);
    fprintf(stderr, "d->frame 2 height %d width %d.\n", d->frame->height, d->frame->width);

    av_packet_unref(pkt);

    return ret;
}

// NOTE: not sure if this function works...
static AVFrame *
allocate_rgb_image(AVCodecContext *codec_context)
{
    int32_t status;
    AVFrame *frame_rgb;

    frame_rgb = av_frame_alloc();
    if (frame_rgb == NULL) {
        return NULL;
    }

    frame_rgb->format = AV_PIX_FMT_RGBA;
    frame_rgb->width = codec_context->width;
    frame_rgb->height = codec_context->height;

    status = av_image_alloc(frame_rgb->data,
                            frame_rgb->linesize,
                            frame_rgb->width,
                            frame_rgb->height,
                            AV_PIX_FMT_RGBA,
                            32);
    if (status < 0) {
        av_frame_free(&frame_rgb);
        return NULL;
    }

    return frame_rgb;
}

// NOTE: not sure if this function works...
uint8_t *decode_rgb(struct VDecoder* d)
{
    fprintf(stderr, "decode_rgb 01\n");
    int status;

    if (d->frame_rgb == NULL ||
        d->frame_rgb->width != d->frame->width ||
        d->frame_rgb->height != d->frame->height) {

        fprintf(stderr, "decode_rgb 02\n");
        // Recreate rgb frame.
        if (d->frame_rgb != NULL) {
            av_frame_free(&d->frame_rgb);
        }
        d->frame_rgb = allocate_rgb_image(d->c);
        assert(d->frame_rgb != NULL);

        fprintf(stderr, "decode_rgb 03\n");
        // Recreate sws context.
        if (d->sws_context != NULL) {
            sws_freeContext(d->sws_context);
        }
        d->sws_context = sws_getContext(d->c->width,
                                     d->c->height,
                                     d->c->pix_fmt,
                                     d->c->width,
                                     d->c->height,
                                     AV_PIX_FMT_RGBA,
                                     SWS_BILINEAR,
                                     NULL,
                                     NULL,
                                     NULL);
        assert(d->sws_context != NULL);
    }
    fprintf(stderr, "decode_rgb 04\n");

    // convert color space from YUV420 to RGBA
    status = sws_scale(d->sws_context,
                        (const uint8_t * const *)(d->frame->data),
                        d->frame->linesize,
                        0,
                        d->c->height,
                        d->frame_rgb->data,
                        d->frame_rgb->linesize);
    fprintf(stderr, "decode_rgb 05\n");
    if (status < 0) {
        fprintf(stderr, "decode_rgb 05b\n");
        return NULL;
    }

    fprintf(stderr, "decode_rgb 06\n");
    return d->frame_rgb->data[0];

    // av_freep(d->frame_rgb->data);
    // av_frame_free(&frame_rgb);
    // sws_freeContext(sws_context);
}

