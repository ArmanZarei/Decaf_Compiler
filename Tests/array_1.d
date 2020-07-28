int main(){
    int [] a;
    int n;
    int i;
    n = ReadInteger();
    a = NewArray( n , int );
    for( i = 0 ; i < n ; i = i + 1 ){
        a[i] = ReadInteger();
    }
    Print("---------------------");
    for( i = n-1 ; i >= 0 ; i = i - 1){
        Print(a[i]);
    }
}