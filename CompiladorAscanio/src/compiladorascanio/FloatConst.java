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
public class FloatConst extends Token {
    public final float value;

    public FloatConst(float value) {
        super(Tag.FLOAT_CONST);
        this.value = value;
    }

    @Override
    public String toString() {
        return "" + value;
    }
}
