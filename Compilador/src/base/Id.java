package base;

public class Id {
    String lexeme = "";
    public Id(String lexeme) {
        this.lexeme = lexeme;
    }
    
    @Override
    public String toString() {
        return "" + lexeme;
    }
}
