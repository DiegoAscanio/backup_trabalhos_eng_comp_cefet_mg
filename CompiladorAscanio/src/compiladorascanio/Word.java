/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package compiladorascanio;

/**
 *
 * @author diego
 */
public class Word extends Token {
    private String lexeme = "";
    
    public static final Word and = new Word(Tag.AND, "&&");
    public static final Word or = new Word(Tag.OR, "||");
    public static final Word eq = new Word(Tag.EQ, "=");
    public static final Word neq = new Word(Tag.NEQ, "!=");
    public static final Word ge = new Word(Tag.GE, ">=");
    public static final Word le = new Word(Tag.LE, "<=");
    public static final Word assign = new Word(Tag.ASSIGN, ":=");

    public Word(int tag, String s) {
        super(tag);
        this.lexeme = s;
    }

    public String getLexeme() {
        return lexeme;
    }
    
    @Override
    public String toString() {
        return "" + this.lexeme;
    }
}
