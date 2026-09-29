#include "../src/sort.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
int main(void) {
    SortFn funcs[]={insertionSort,mergeSort,gnomeSort};
    Item cases[][8]={{{0,0}},{{3,0},{1,1},{3,2},{2,3},{1,4}},{{5,0},{4,1},{3,2},{2,3},{1,4}},{{-2,0},{-2,1},{0,2},{-3,3},{0,4}}};
    size_t lens[]={0,5,5,5};
    for(size_t f=0;f<3;++f) for(size_t c=0;c<4;++c) {
        Item a[8];memcpy(a,cases[c],sizeof a);Stats s={0,0};funcs[f](a,lens[c],&s);
        for(size_t i=1;i<lens[c];++i) {
            assert(a[i-1].key<=a[i].key);
            if(a[i-1].key==a[i].key) assert(a[i-1].original<a[i].original);
        }
    }
    puts("12 algorithm/input checks passed");
}
