#include <stddef.h>

void lock()
{

}

void func2(int* result)
{
    lock();
    *result=42;
}

void func1()
{
  int *i = NULL;
  func2(i);
}

int main(int, char*[])
{
    func1();
}