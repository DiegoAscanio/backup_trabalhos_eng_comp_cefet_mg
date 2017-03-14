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
public class IntegerConst extends Token {
    public final int value;

    public IntegerConst(int value) {
        super(Tag.INTEGER_CONST);
        this.value = value;
    }
    
    @Override
    public String toString() {
        return "" + value;
    }
}
