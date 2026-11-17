#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>

int main(){
    int n;
    printf("enter no of particles :");
    scanf("%d",&n);
    double k=15.0;
    double x0=0.8;
   
    double (*pos)[2] = malloc(n*sizeof(*pos));
    double (*force)[2] = calloc(n,sizeof(*force));


    for(int i=0;i<n;i++){
    pos[i][0] = 10.0*rand()/RAND_MAX;
    pos[i][1] = 10.0*rand()/RAND_MAX;
}

clock_t start = clock();

for(int i=0;i<n;i++){
    for(int j=i+1;j<n;j++){

        double dx = pos[i][0] -pos[j][0];
        double dy = pos[i][1] -pos[j][1];
        double x = sqrt(dx*dx + dy*dy);
        force[i][0] += -k*dx*(x-x0)/x;
        force[i][1] += -k*dy*(x-x0)/x;
        
        force[j][0] += k*dx*(x-x0)/x;
        force[j][1] += k*dy*(x-x0)/x;

}}
clock_t end = clock();
 double elasped = (double)(end - start)/CLOCKS_PER_SEC;
   double sumx =0;
   double sumy=0;
    for(int i=0;i<n;i++){

        sumx += force[i][0];
        sumy += force[i][1];
    }
   size_t memory = sizeof(*pos) +n*sizeof(*force);
   printf("Time elapsed : %.15f\n",elasped); 
   printf("Total force in x direction :%f\n",sumx);
   printf("Total force in y direction :%f\n",sumy);
    printf("Memory %zu\n",memory);
    
    
    
    free(pos);
    free(force);
    return 0;
}