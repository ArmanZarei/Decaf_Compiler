int main(){
    double[] a;
    string[] b;
    bool[] c;
    a = NewArray( 2 , double );
    b = NewArray( 2 , string );
    c = NewArray( 2 , bool );
    a[0] = 24.42;
    a[1] = 11.35;
    b[0] = "Arman";
    b[1] = "Ariyan";
    c[0] = true;
    c[1] = false;
    Print( a[0] , " - " , a[1] );
    Print( b[0] , " - " , b[1] );
    Print( c[0] , " - " , c[1] );
}