CC = gcc -fPIC

default: libexamples.a

libexamples.a: examples.o
	ar rcs $@ $^
examples.o: examples.c examples.h
	$(CC) -c $<


libvdecoder.a: video_decoder.o
	ar rcs $@ $^
video_decoder.o: video_decoder.c video_decoder.h
	$(CC) -c $< -Lavcodec -Lavutil -Lswscale

clean:
	rm *.o *.a
