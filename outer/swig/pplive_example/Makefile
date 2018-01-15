all:
	gcc `python-config --cflags` -c make_example.c -o make_example.o
	gcc `python-config --cflags` -c pplive_example.c -o pplive_example.o
	gcc `python-config --libs` pplive_example.o make_example.o -o pplive_example.so
