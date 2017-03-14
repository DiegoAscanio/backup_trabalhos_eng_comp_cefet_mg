package analisadorlexico;

public class Word extends Token {
    private String lexeme = "";

    public static final Word assign = new Word(":=", Tag.ASSIGN);
    public static final Word ge = new Word(">=", Tag.GE);
    public static final Word le = new Word("<=", Tag.LE);
    public static final Word ne = new Word("<>", Tag.NEQ);

    public Word(String lexeme, int tag) {
        super(tag);
        this.lexeme = lexeme;
    }

    public String getLexeme() {
        return lexeme;
    }

    @Override
    public String toString() {
        return "" + lexeme;
    }
}
