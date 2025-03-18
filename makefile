LIB_DIR = lib

default: pyexamples

pyexamples: setup.py pyexamples.pyx $(LIB_DIR)/libvdecoder.a
	python3 setup.py build_ext --inplace && rm -f pyexamples.c && rm -Rf build

$(LIB_DIR)/libexamples.a:
	make -C $(LIB_DIR) libexamples.a

$(LIB_DIR)/libvdecoder.a:
	make -C $(LIB_DIR) libvdecoder.a

clean:
	make -C $(LIB_DIR) clean
	rm *.so
