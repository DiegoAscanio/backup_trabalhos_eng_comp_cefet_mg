/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package compiladorascanio;

import java.util.*;

/**
 *
 * @author diego
 * 
 * Tabela de Símbolos
 * 
 */
public class Env {
    private Hashtable table;
    protected Env prev;

    public Env(Env prev) {
        table = new Hashtable();
        this.prev = prev;
    }
    
    public void put (Token w, Id i) {
        table.put(w, i);
    }
    
    public Id get(Token w) {
        for (Env e = this; e != null; e = e.prev) {
            Id found = (Id) e.table.get(w);
            if (found != null)
                return found;
        }
        return null;
    }

    @Override
    public String toString() {
        String str = "";
        for (Object o : this.table.keySet()) {
            str += o + ", " + this.table.get(o) + '\n';
        }
        return str;
    }
    
}
