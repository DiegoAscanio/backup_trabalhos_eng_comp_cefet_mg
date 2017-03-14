/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package compiladorascanio;

import java.io.FileNotFoundException;

/**
 *
 * @author diego
 */
public class CompiladorAscanio {
    public static void main (String [] args) throws FileNotFoundException, Exception {
        String fileName = args[0];
        Lexer l = new Lexer(fileName);
        Env e = new Env(null);
        Token t = null;
        
        System.out.println("Sequencia de tokens identificadas: ");
        do {
            t = l.scan();
            System.out.println(t.tag+", "+t);
            e.put(t, new Id(t.toString()));
        } while (t.tag != 65535); // EOF
        
        System.out.println("Simbolos instalados na tabela de simbolos: ");
        System.out.println(e);
    }
}
