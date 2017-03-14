package analisadorlexico;

import java.io.*;
import java.util.*;

public class AnalisadorLexico {
    public static int line = 1; // contador de linhas
    private char ch = ' '; // caractere lido do arquivo
    private FileReader file;

    private Hashtable words = new Hashtable();

    // metodo para inserir palavras reservadas na Hashtable
    private void reserve (Word w) {
        words.put(w.getLexeme(), w);
    }

    public AnalisadorLexico(String fileName) throws FileNotFoundException {
        try {
            file = new FileReader(fileName);
        } catch (FileNotFoundException e) {
            System.out.println("File Not Found!");
            throw e;
        }

        // Insere as palavras reservadas na HashTable

        reserve(new Word("var", Tag.VAR));
        reserve(new Word("begin", Tag.BEGIN));
        reserve(new Word("end", Tag.END));
        reserve(new Word("is", Tag.IS));
        reserve(new Word("int", Tag.INT));
        reserve(new Word("string", Tag.STRING));
        reserve(new Word("if", Tag.IF));
        reserve(new Word("then", Tag.THEN));
        reserve(new Word("else", Tag.ELSE));
        reserve(new Word("do", Tag.DO));
        reserve(new Word("while", Tag.WHILE));
        reserve(new Word("in", Tag.IN));
        reserve(new Word("out", Tag.OUT));
        reserve(new Word("not", Tag.NOT));
        reserve(new Word("or", Tag.OR));
        reserve(new Word("and", Tag.AND));
        reserve(new Word(":=", Tag.ASSIGN));
        reserve(new Word(">=", Tag.GE));
        reserve(new Word("<=", Tag.LE));
        reserve(new Word("<>", Tag.NEQ));
    }

    // le o proximo caractere do arquivo
    private void readch() throws IOException {
        ch = (char) file.read();
    }

    // le o proximo caractere do arquivo e averigua se e igual a c
    private boolean readch(char c) throws IOException {
        readch();
        if (ch != c)
            return false;
        ch = ' ';
        return true;
    }

    public Token scan() throws Exception {
        // Desconsidera delimitadores da entrada
        for (;; readch()) {
            if (ch == ' ' || ch == '\t' || ch == '\r' || ch == '\b')
                continue;
            else if (ch == '\n')
                line ++;
            else
                break;
        }

        switch (ch) {
            // operadores
            case ':':
                if (readch(':'))
                    return Word.assign;
                else
                    return new Token(':');
            case '>':
                if (readch('='))
                    return Word.ge;
                else
                    return new Token('>');
            case '<':
                if (readch('='))
                    return Word.le;
                else if (readch('>'))
                    return Word.ne;
                else
                    return new Token('<');
        }
        // numeros
        if (Character.isDigit(ch)) {
            String integerConst = "";
            do {
                integerConst += ch;
                readch();
            } while (Character.isDigit(ch));
            if (integerConst.charAt(0) != '0' || integerConst.length() == 1) {
                return new IntegerConst(Integer.parseInt(integerConst));
            }
            else {
                throw new Exception("Constante numerica mal formada na linha: "+String.valueOf(line));
            }
        }
        // identificadores que comecam com letra
        if (Character.isLetter(ch)) {
            String id = "";
            do {
                id += ch;
                readch();
            } while (Character.isLetterOrDigit(ch));
            Word w = (Word) words.get(id);
            if (w != null) // palavra existe na hashtable
                return w;
            w = new Word(id, Tag.ID);
            words.put(id, w);
            return w;
        }
        else if (ch == '_') { // identificadores que comecam com _
            String s = "";
            do {
                s += ch;
                readch();
            } while (Character.isLetterOrDigit(ch));
            if (s.length() == 1) {
                throw new Exception("Identificador mal formado na linha: "+String.valueOf(line));
            }
            else {
                Word w = (Word) words.get(s);
                if (w != null) // palavra existe na hashtable
                    return w;
                w = new Word(s, Tag.ID);
                words.put(s, w);
                return w;
            }
        }
        else if (ch == '{') { // literais
            String literal = "";
            if (readch('}')) { // literal mal formado
                throw new Exception("Literal mal formado na linha: "+String.valueOf(line));
            }
            do {
                literal += ch;
                readch();
            } while (ch != '}' && (int) ch != 65535);
            if ((int) ch == 65535)
                throw new Exception("Literal mal formado na linha: "+String.valueOf(line));
            return new Literal(literal);
        }
        else if (ch == '/') { // comentarios de uma linha
            String comentario = "";
            if (readch('/')) {
                do {
                    readch();
                } while (ch != '\n');
            }
            else {
                return new Token('/');
            }
        }
        else if (ch == '%') { // comentarios de mais de uma linha
            do {
                readch();
            } while (ch != '%' && (int) ch != 65535);
            if ((int) ch == 65535)
                throw new Exception("Comentario de multiplas linhas mal formado na linha: "+String.valueOf(line));
        }
        // Caracteres nao especificados
        Token t = new Token(ch);
        ch = ' ';
        return t;
    }

}