class List{
    string[] name;
    int cnt;

    void init(int size){
        this.name = NewArray( size , string );
        cnt = 0;
    }

    void add(string name){
        if( cnt == this.name.length() ){
            Print("List is full !!!");
            return;
        }
        this.name[cnt] = name;
        cnt = cnt + 1;
    }

    string search(string key){
        int i;
        for( i = 0 ; i < cnt ; i = i + 1 ){
            if( name[i] == key ){
                return "Found";
            }
        }
        return "Not Found !!!";
    }
}

int main(){
    List l;
    l = new List;
    l.init(5);
    l.add("arman");
    l.add("ariyan");
    Print( l.search("arman") );
    Print( l.search("ali") );
    Print( l.search("Arman") );
    Print("----------------------");
    l.add("X");
    l.add("X");
    l.add("X");
    l.add("X");
    l.add("X");
}