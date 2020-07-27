int main() {
    int a;
    int b;
    a = 10;
    while ( a >= 0 ){
        a = a-1;
        if( a == 5 ){
            break;
        }
        Print(a);
    }
    Print("Should Print from 9 to 6");
    Print("-------------------");
     a = 10;
    while ( a >= 0 ){
        a = a-1;
        if( a == 3 )
            break;
        Print(a);
    }
    Print("Should Print from 9 to 4");
    Print("-------------------");
    a = 0;
    while( a < 10 ){
        b = 0;
        while( b < 10 ){
            Print(a);
            Print(b);
            Print("-----");
            if( b == 4 ){
                break;
            }
            b = b + 1;
        }
        a = a + 1;
    }
    Print("-------------------");
    for( a = 0 ; a < 10 ; a = a + 1 ){
        Print( a );
        if( a == 7 ){
            break;
        }
    }
    Print("a should be : 0 -> 7");
    Print("----------------------------");
    for( a = 0 ; a < 10 ; a = a + 1 ){
        for( b = 0 ; b < 10 ; b = b + 1 ){
            Print(a);
            Print(b);
            Print("----");
            if(b == 3){
                break;
            }
        }
    }
}