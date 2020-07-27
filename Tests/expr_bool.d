int main() {
    bool a;
    bool b;
    bool c;
    a = true;
    b = false;
    c = false;
    Print(!a);
    Print(!!a);
    Print(a || b);
    Print(b || c);
    Print(a && b);
    Print(c && b);
    Print(a && true);
    Print(a && false);
    Print(a == b);
    Print(b == c);
}