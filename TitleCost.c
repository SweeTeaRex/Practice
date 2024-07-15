
// Simple program to tell you the cost to purchase a specific measurement of flooring 

#include <stdio.h>
#include <math.h>



int main(void)
{
    double legnth;
    double width;
    double cost;


    printf("What is the length measurment? ");
    scanf("%lf", &legnth);
    
    printf("What is the width measurment? ");
    scanf("%lf", &width);

    printf("What is the cost per unit? ");
    scanf("%lf", &cost);
    
    double total;

    total = ((legnth * width) * cost);

    

    printf("The total is $%.2lf \n", total);
    
    
    return 0;


//s

}