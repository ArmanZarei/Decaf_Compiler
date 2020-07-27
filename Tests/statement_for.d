int main() {
    int a;
    int b;
    for( a = 0 ; a < 10 ; a = a + 1 ){
        Print( a );
    }
    Print("----------------------------");
    for( a = 0 ; a < 10 ; a = a + 1 ){
        for( b = 0 ; b < 10 ; b = b + 1 ){
            Print(a);
            Print(b);
            Print("----");
        }
    }
    Print("---------------------");
    a = 3;
    for( ; a < 10 ; ){
        Print( a );
        a = a + 1;
    }
    Print("******************");
    a = 7;
    for( ; a < 10 ; a = a + 1 ){
        Print( a );
    }
}