#include "sort.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static unsigned state=20260927u;
static unsigned nextRand(void) {state ^=state<<13; state ^=state>>17; state ^=state<<5; return state;}
static void input(Item *a,size_t n,int shape) {
    for(size_t i=0;i<n;++i) {
        a[i].key=shape==0?(int)(nextRand()%100000u):shape==1?(int)i:shape==2?(int)(n-i):(int)(nextRand()%8u);
        a[i].original=(int)i;
    }
}
int main(void) {
    const size_t sizes[]={1000,2000,4000,8000};
    const char *names[]={"insertion","merge","gnome"};
    const char *shapes[]={"random","sorted","reverse","duplicates"};
    SortFn sorts[]={insertionSort,mergeSort,gnomeSort};
    puts("shape,n,algorithm,time_ms,comparisons,moves,stable");
    for(size_t sh=0;sh<4;++sh) for(size_t si=0;si<4;++si) {
        size_t n=sizes[si]; Item *source=malloc(n*sizeof *source),*work=malloc(n*sizeof *work);
        if(!source||!work) return 1;
        input(source,n,(int)sh);
        for(size_t alg=0;alg<3;++alg) {
            double total=0; Stats s={0,0}; int stable=1;
            for(int rep=0;rep<5;++rep) {
                memcpy(work,source,n*sizeof *work); s=(Stats){0,0};
                clock_t begin=clock(); sorts[alg](work,n,&s); total+=(double)(clock()-begin)*1000.0/CLOCKS_PER_SEC;
                for(size_t k=1;k<n;++k) if(work[k-1].key>work[k].key) return 2;
                for(size_t k=1;k<n;++k) if(work[k-1].key==work[k].key && work[k-1].original>work[k].original) stable=0;
            }
            printf("%s,%zu,%s,%.5f,%llu,%llu,%s\n",shapes[sh],n,names[alg],total/5,s.comparisons,s.moves,stable?"yes":"no");
        }
        free(source);free(work);
    }
    return 0;
}
