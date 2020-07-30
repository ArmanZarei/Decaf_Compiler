class A{
    int x;
    int getX(){
        return x;
    }
    void setX( int a ){
        x = a;
    }
    void increment(){
        this.x = this.x + 1;
    }
    void mul( int a , int c ){
        this.x = a * c;
    }
}

int main(){
    A a;
    a = new A;
    a.setX( 35 );
    Print( a.getX() );
    a.increment();
    Print( a.getX() );
    a.mul( 2 , 4 );
    Print( a.getX() );
}