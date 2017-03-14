package analisadorlexico;

public class Literal extends Token {

    public final String value;

    public Literal(String value) {
        super(Tag.LITERAL);
        this.value = value;
    }

    public String getValue() {
        return value;
    }

    @Override
    public String toString() {
        return "" + value;
    }
}