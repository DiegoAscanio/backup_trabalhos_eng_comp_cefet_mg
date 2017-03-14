/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package compiladorascanio;

import java.io.*;
import java.util.*;

/**
 *
 * @author diego
 */
public class Lexer {
    public static int line = 1; // Contador de linhas
    private char ch = ' '; // caractere lido do arquivo
    private FileReader file;
    
    private Hashtable words = new Hashtable();
    
    /* metodo de insercao de palavras reservadas na hashtable */
    private void reserve (Word w) {
        words.put(w.getLexeme(), w); // lexema - chava para entrada na tabela
    }
    
    // construtor
    public Lexer (String fileName) throws FileNotFoundException, Exception {
        try {
            file = new FileReader(fileName);
        }
        catch (FileNotFoundException e) {
            System.err.println("Arquivo "+fileName+" nao encontrado! ");
            throw e;
        }
        
        // insercao das palavras reservadas da linguagem na tabela
        reserve(new Word(Tag.APP, "app"));
        reserve(new Word(Tag.START, "start"));
        reserve(new Word(Tag.STOP, "stop"));
        reserve(new Word(Tag.INTEGER, "integer"));
        reserve(new Word(Tag.REAL, "real"));
        reserve(new Word(Tag.IF, "if"));
        reserve(new Word(Tag.THEN, "then"));
        reserve(new Word(Tag.ELSE, "else"));
        reserve(new Word(Tag.REPEAT, "repeat"));
        reserve(new Word(Tag.UNTIL, "until"));
        reserve(new Word(Tag.END, "end"));
        reserve(new Word(Tag.WHILE, "while"));
        reserve(new Word(Tag.DO, "do"));
        reserve(new Word(Tag.READ, "read"));
        reserve(new Word(Tag.WRITE, "write"));
    }
    
    private void readch() throws IOException {
        ch = (char) file.read();
    }
    
    private boolean readch(char c) throws IOException {
        readch();
        if (ch != c)
            return false;
        ch = ' ';
        return true;
    }
    
    public Token scan() throws IOException, Exception {
        // Desconsidera delimitadores na entrada
        for (;; readch()) {
            if (ch == ' ' || ch == '\t' || ch == '\r' || ch == '\b')
                continue;
            else if (ch == '\n')
                line ++;
            else
                break;
        }
        // operadores
        switch (ch) {
            case '&':
                if (readch('&'))
                    return Word.and;
                else
                    return new Token('&');
            case '|':
                if (readch('|'))
                    return Word.or;
                else
                    return new Token('|');
            case ':':
                if (readch('='))
                    return Word.assign;
                else
                    return new Token(':');
            case '=':
                readch();
                return Word.eq;
            case '!':
                if (readch('='))
                    return Word.neq;
                else
                    return new Token('!');
            case '>':
                if (readch('='))
                    return Word.ge;
                else
                    return new Token('>');
            case '<':
                if (readch('='))
                    return Word.le;
                else
                    return new Token('<');
        }
        
        // Numeros
        if (Character.isDigit(ch)) {
            boolean real = false;
            int vInt = 0;
            float vFloat = 0;
            int casasDecimais = -1;
            do {
                if (!real) {
                    vInt = 10*vInt + Character.digit(ch, 10);
                    
                }
                else {
                    vFloat += Character.digit(ch, 10)*Math.pow(10, casasDecimais);
                    casasDecimais --;
                }
                if (readch('.')) {
                    vFloat += vInt;
                    real = true;
                    readch();
                }
            } while (Character.isDigit(ch));
            
            if (real)
                return new FloatConst(vFloat);
            return new IntegerConst(vInt);
        }
        
        // Comentarios
        if (ch == '%') {
            do {
                readch();
            } while (ch != '\n');
        }
        
        // Literais
        if (ch == '{') {
            StringBuffer sb = new StringBuffer();
            do {
                readch();
                sb.append(ch);
            } while (ch != '}' && ch != '\n');
            if (ch != '}') {
                throw new Exception ("Erro na linha: "+line+"! Literal mal formado!");
            }
            String s = sb.toString();
            Word w = (Word) words.get(s);
            if (w != null)
                return w;
            w = new Word(Tag.LITERAL, s);
            words.put(s, w);
            return w;
        }
        
        // Identificadores
        if (Character.isLetter(ch) || ch == '_') {
            StringBuffer sb = new StringBuffer();
            do {
                sb.append(ch);
                readch();
            } while (Character.isLetterOrDigit(ch) || ch == '_');
            
            String s = sb.toString().toLowerCase();
            Word w = (Word) words.get(s);
            if (w != null)
                return w;
            w = new Word(Tag.IDENTIFIER, s);
            words.put(s, w);
            return w;
        }
        
        // caracteres não especificados
        Token t = new Token(ch);
        ch = ' ';
        return t;
    }
}
