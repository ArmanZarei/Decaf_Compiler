int main() {
    int a;
    int b;
    int c;
    bool d;
    a = 11;
    b = 9;
    {
        int d;
        c = a*b;
        Print(d=c);
        Print(d);
    }
    Print(c);
    d = a == 11;
    Print(d);
    Print( d = c == 98 );
}