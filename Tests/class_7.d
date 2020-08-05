class A{
    void f(){
        Print("A");
    }
    void h(){
        Print("A");
    }
}
class B extends A{
    void f(){
        Print("B");
    }
    void g(){
        Print("B");
    }
}
class C extends B{
    void f(){
        Print("C");
    }
}
int main(){
    A a;
    B b;
    C c;
    a = new A;
    b = new B;
    c = new C;
    a.f();
    a.h();
    b.h();
    c.h();
    Print("--------------");
    b.f();
    b.g();
    c.g();
    Print("---------------");
    c.f();
}