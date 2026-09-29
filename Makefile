CC = gcc
CFLAGS = -std=c17 -O2 -Wall -Wextra -pedantic
SORT = src/sort.c

.PHONY: all run test clean
all: test

src/main.out: src/main.c $(SORT) src/sort.h
	$(CC) $(CFLAGS) -o $@ src/main.c $(SORT)

tests/test_sort.out: tests/test_sort.c $(SORT) src/sort.h
	$(CC) $(CFLAGS) -o $@ tests/test_sort.c $(SORT)

run: src/main.out
	./src/main.out

test: tests/test_sort.out
	./tests/test_sort.out

clean:
	rm -f src/*.out tests/*.out
