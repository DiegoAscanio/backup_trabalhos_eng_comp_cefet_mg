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
