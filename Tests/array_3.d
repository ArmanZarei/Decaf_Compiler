int main(){
    int[] a;
    int[] b;
    int i;
    a = NewArray( 10 , int );
    for( i = 0 ; i < 10 ; i = i + 1 ){
        a[i] = i;
    }
    b = a;
    for( i = 0 ; i < 10 ; i = i + 1 ){
        Print( b[i] );
    }
}