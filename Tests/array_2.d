int main(){
    int[][] mat;
    int i;
    int j;
    mat = NewArray( 10 , int[] );
    for( i = 0 ; i < 10 ; i = i + 1 ){
        mat[i] = NewArray( 10 , int );
    }
    for( i = 0 ; i < 10 ; i = i + 1 ){
        for( j = 0 ; j < 10 ; j = j + 1 ){
            mat[i][j] = (i+1) * (j+1);
        }
    }
    Print("Mul Table \\n");
    for( i = 0 ; i < 10 ; i = i + 1 ){
        for( j = 0 ; j < 10 ; j = j + 1 ){
            Print(mat[i][j]);
        }
    }
}