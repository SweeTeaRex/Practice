
// Program that tells you Pi to the nth digit


#include <stdio.h>




int main(void)
{
    int place;

    printf("How many places?\n");
    scanf("%i", &place);

    double pi = 3.14159265358979323846;
    
    
    printf("Pi is %.*lf \n", place, pi);
    
    return 0;


}