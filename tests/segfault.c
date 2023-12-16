#include <stddef.h>

void lock()
{

}

void func2()
{
    lock();
    int* i = NULL;
    *i=42;
}

void func1()
{
    func2();
}

int main(int, char*[])
{
    func1();
}