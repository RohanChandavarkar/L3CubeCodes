#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<cmath>
#include<iostream>
using namespace std;

class validity
{
private:
int people;
public:
double formula(int p);
void sort(int a[],int x)
{
for(int i=0;i<x-1;i++)
{
for(int j=0;j<x-i-1;j++)
{
if(a[j]>a[j+1])
{
int temp=a[j];
a[j]=a[j+1];
a[j+1]=temp;
}
}
}
}
}v;
double validity::formula(int p)
{
people=p;
int q=(p*(p-1)/2);
double r=1;
double d=364.0/365.0;
for(int i=0;i<q;i++)
{
r=r*d;

}
double res=1.0-r;
return res;
}

int main()
{
int p;
double formprob;
cout<<"Enter the number of people\n";
cin>>p;
if(p<2)
{
cout<<"Please enter the correct input\n";
}
else
{
formprob=v.formula(p);
int trials,repeated,flag=0,tdup;
tdup=repeated=trials=0;
srand(time(NULL));
int birthday[p];
while(1)
{
trials++;
cout<<"Trials\t"<<trials<<"\n";
for(int i=0;i<p;i++)
birthday[i]=(rand()%365)+1;
v.sort(birthday,p);
for(int i=0;i<p;i++)
{
if(birthday[i]==birthday[i-1])
{
flag=1;
break;
}
}
if(flag==1)
{
repeated++;
}
double mpro=(double)repeated/trials;
cout<<"Probability at this point: "<<mpro<<"\n";
if(abs((100*formprob)-(100*mpro))<=0.2)
{
cout<<"Probabiltiy by formula: "<<formprob<<"\n";
cout<<" Number of trials in which birthdays were repeated\n"<<repeated<<"\n";
cout<<"Total number of trials\n"<<trials<<"\n";
cout<<"The birthday paradox is valid\n";
break;
}
}
}
return 0;
}

