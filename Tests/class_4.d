class A{
    int x;
    void setX(int a){
        x = a;
    }
    void prettyPrint(){
        Print( "Parent : " , x );
    }
}
class B extends A{
    void prettyPrint(){
        Print( "Child : " , x );
    }
}
int main(){
    B b;
    B bb;
    b = new A;
    bb = new B;
    b.setX(7);
    bb.setX(7);
    b.prettyPrint();
    bb.prettyPrint();
}