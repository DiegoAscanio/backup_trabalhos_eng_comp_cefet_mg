package analisadorlexico;

public class Token {
    public final int tag; // constante para representar o token

    public Token(int tag) {
        this.tag = tag;
    }

    @Override
    public String toString() {
        return "" + tag;
    }

    public int getTag() {
        return tag;
    }
}