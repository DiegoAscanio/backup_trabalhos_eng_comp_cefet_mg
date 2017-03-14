package analisadorlexico;

public class IntegerConst extends Token {
    public final int value;

    public IntegerConst(int value) {
        super(Tag.INTCONST);
        this.value = value;
    }

    public int getValue() {
        return value;
    }

    @Override
    public String toString() {
        return "" + value;
    }
}
