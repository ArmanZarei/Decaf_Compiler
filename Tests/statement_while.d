int main() {
    int a;
    int b;
    a = 10;
    while ( a >= 0 ){
        Print(a);
        a = a-1;
    }
    Print("-------------------");
    a = 0;
    while( a < 10 ){
        b = 0;
        while( b < 10 ){
            Print(a);
            Print(b);
            Print("-----");
            b = b + 1;
        }
        a = a + 1;
    }
}