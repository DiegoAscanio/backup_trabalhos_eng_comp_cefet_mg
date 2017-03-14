package base;

import analisadorlexico.AnalisadorLexico;
import analisadorlexico.Tag;
import analisadorlexico.Token;
import analisadorlexico.Word;

public class Main {
    public static void main (String [] args) throws Exception {
        String fileName = args[0];
        AnalisadorLexico al = new AnalisadorLexico(fileName);
        Token t = null;
        TabelaSimbolos ts = new TabelaSimbolos(null);
        int nivelEscopo = 0;

        System.out.println("Sequencia de tokens identificados: ");
        do {
            t = al.scan();
            System.out.println(t.tag+", "+t);
            if (t instanceof Word) {
                if (t.getTag() == Tag.BEGIN || t.getTag() == Tag.THEN || t.getTag() == Tag.DO) { // Comeco de Escopo
                    nivelEscopo ++;
                    ts = new TabelaSimbolos(ts);
                }
                if (t.getTag() == Tag.ELSE) { // Fim de um Escopo - Comeco de um novo
                    System.out.printf("Tabela de Simbolos no nível %d:\n", nivelEscopo);
                    System.out.println(ts);
                    ts = ts.anterior;
                    nivelEscopo --;
                    ts = new TabelaSimbolos(ts);
                    nivelEscopo ++;
                }
                if (t.getTag() == Tag.END || t.getTag() == Tag.WHILE) { // Fim de um Escopo - Retorno ao Anterior
                    System.out.printf("Tabela de Simbolos no nível %d:\n", nivelEscopo);
                    System.out.println(ts);
                    ts = ts.anterior;
                    nivelEscopo --;
                }
                ts.put(t, new Id(t.toString()));
            }
        } while (t.tag != 65535); // EOF
        System.out.printf("Tabela de Simbolos no nível %d:\n", nivelEscopo);
        System.out.println(ts);
    }
}
