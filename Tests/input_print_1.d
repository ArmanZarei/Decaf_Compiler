int main() {
    int a;
    int b;
    int c;
    a = ReadInteger();
    b = ReadInteger();
    c = ReadInteger();
    {
        int c;
        c = ReadInteger();
        Print(c);
    }
    Print(a);
    Print(b);
    Print(c);
}