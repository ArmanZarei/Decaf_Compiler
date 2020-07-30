class A{
    int x;
    void setX(int a){
        x = a;
    }
}
class B extends A{
    int y;
    void setY(int a){
        y = a;
    }
    void printMul(){
        Print( x * y );
    }
}

int main(){
    B b;
    b = new B;
    b.setX(7);
    b.setY(8);
    b.printMul();
}