int main() {
    bool a;
    bool b;
    int c;
    a = true;
    b = false;
    c = 2;
    if( a ){
        Print("a is true");
        if( b ){
            Print("it shouldn't print this !");
        }else{
            Print("it should print this -> else b");
        }
    }
    if( !a ){
        Print("it shouldn't print this !");
    }else{
        Print("it should print this -> else !a");
    }
    if( c == 5 || a != false ){
        Print("Congrat. !");
    }
    if( c == 5 || a != true ){
        Print("it shouldn't print this !");
    }
}