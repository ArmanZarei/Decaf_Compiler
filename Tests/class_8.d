class A{
    void f(){
        Print("A");
    }
}
class B extends A{
    void f(){
        Print("B");
    }
}
int main(){
    A a;
    B b;
    (a = b = new B).f();
}