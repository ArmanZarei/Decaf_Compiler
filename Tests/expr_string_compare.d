int main() {
    string a;
    string b;
    string c;
    a = "arman";
    b = "arman";
    c = "ariyan";
    Print(a!=b);
    Print(b!=c);
    b = "ariyan";
    Print(b!=c);
    b = "arman";
    c = "ariyan";
    Print(a==b);
    Print(b==c);
    b = "ariyan";
    Print(b==c);
}