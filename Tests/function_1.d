int fact( int a ){
    if( a == 1 ){
        return 1;
    }
    return a * fact( a - 1 );
}

int fib( int n ){
    if ( n == 1 || n == 2 ){
        return 1;
    }
    return fib( n-1 ) + fib( n - 2);
}

int main() {
    Print( fact(4) );
    Print( fib(8) );
}