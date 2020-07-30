class A{
    void f(){
        Print("From Class");
    }
    void g(){
        f();
    }
}
void f(){
    Print("From Global");
}

int main(){
    A a;
    a = new A;
    a.g();
}