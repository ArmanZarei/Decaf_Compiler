class A{
    string name;
    void set(string name){
        this.name = name;
    }

    string get(){
        return name;
    }
}

int main(){
    A[][] arr;
    int i;
    int j;
    arr = NewArray( 2 , A[] );
    for( i = 0 ; i < 2 ; i = i + 1 ){
        arr[i] = NewArray( 2 , A );
    }
    for( i = 0 ; i < 2 ; i = i + 1 ){
        for( j = 0 ; j < 2 ; j = j + 1 ){
            arr[i][j] = new A;
        }
    }
    arr[0][0].set("Arman");
    arr[0][1].set("Ariyan");
    arr[1][0].set("Ali");
    arr[1][1].set("Mohammad");
    for( i = 0 ; i < 2 ; i = i + 1 ){
        for( j = 0 ; j < 2 ; j = j + 1 ){
            Print( arr[i][j].get() );
        }
    }
}