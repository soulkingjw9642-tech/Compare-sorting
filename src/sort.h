#ifndef SORT_H
#define SORT_H
#include <stddef.h>
typedef struct { int key; int original; } Item;
typedef struct { unsigned long long comparisons, moves; } Stats;
typedef void (*SortFn)(Item *, size_t, Stats *);
void insertionSort(Item *, size_t, Stats *);
void mergeSort(Item *, size_t, Stats *);
void gnomeSort(Item *, size_t, Stats *);
#endif
