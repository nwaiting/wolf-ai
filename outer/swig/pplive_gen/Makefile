all:
	gcc `python-config --cflags` -c pplive_key_generate.c -o pplive_key_generate.o
	gcc `python-config --cflags` -c make_old_key.c -o make_old_key.o
	gcc `python-config --libs` pplive_key_generate.o make_old_key.o -o pplive_key_generate.so
	 
