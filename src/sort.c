#include "sort.h"
#include <stdlib.h>
#include <stdio.h>
static int greater(Item x, Item y, Stats *s) { ++s->comparisons; return x.key > y.key; }
static void assign(Item *dst, Item src, Stats *s) { *dst = src; ++s->moves; }
void insertionSort(Item *a, size_t n, Stats *s) {
    for (size_t i = 1; i < n; ++i) {
        Item value = a[i]; size_t j = i;
        while (j && greater(a[j-1], value, s)) { assign(&a[j], a[j-1], s); --j; }
        if (j != i) assign(&a[j], value, s);
    }
}
static void mergeRec(Item *a, Item *tmp, size_t lo, size_t hi, Stats *s) {
    if (hi-lo < 2) return;
    size_t mid = lo + (hi-lo)/2;
    mergeRec(a,tmp,lo,mid,s); mergeRec(a,tmp,mid,hi,s);
    size_t i=lo,j=mid,k=lo;
    while (i<mid && j<hi) assign(&tmp[k++], greater(a[i],a[j],s) ? a[j++] : a[i++],s);
    while (i<mid) assign(&tmp[k++],a[i++],s);
    while (j<hi) assign(&tmp[k++],a[j++],s);
    for (k=lo;k<hi;++k) assign(&a[k],tmp[k],s);
}
void mergeSort(Item *a, size_t n, Stats *s) {
    if (n<2) return;
    Item *tmp=malloc(n*sizeof *tmp);
    if (!tmp) { fputs("allocation failed\n",stderr); exit(EXIT_FAILURE); }
    mergeRec(a,tmp,0,n,s); free(tmp);
}
void gnomeSort(Item *a, size_t n, Stats *s) {
    size_t i = 1;
    while (i < n) {
        if (!greater(a[i-1], a[i], s)) {
            ++i;
        } else {
            Item tmp = a[i];
            assign(&a[i], a[i-1], s);
            assign(&a[i-1], tmp, s);
            if (i > 1) --i;
            else ++i;
        }
    }
}
