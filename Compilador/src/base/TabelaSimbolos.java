package base;

import java.util.Hashtable;
import analisadorlexico.Word;
import analisadorlexico.Token;

public class TabelaSimbolos {
    private Hashtable table;
    protected TabelaSimbolos anterior;

    public TabelaSimbolos(TabelaSimbolos anterior) {
        this.table = new Hashtable();
        this.anterior = anterior;
    }

    public void put(Token w, Id i) {
        table.put(w,i);
    }

    public Id get(Token w) {
        for (TabelaSimbolos ts = this; ts != null; ts = ts.anterior) {
            Id found = (Id) ts.table.get(w);
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
