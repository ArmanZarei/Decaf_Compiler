int main() {
    string a;
    string b;
    string c;
    a = "arman";
    b = "ariyan";
    c = "ali";
    Print(a);
    Print(b);
    Print(c);
    Print("------------");
    a = b;
    b = c;
    Print(a);
    Print(b);
    Print(c);
    Print("------------");
    a = b;
    c = b;
    b = a;
    Print(a);
    Print(b);
    Print(c);
}