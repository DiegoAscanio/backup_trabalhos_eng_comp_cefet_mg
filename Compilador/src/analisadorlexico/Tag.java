package analisadorlexico;

public class Tag {
    public final static int
    // palavras reservadas
    VAR = 256,
    BEGIN = 257,
    END = 258,
    IS = 259,
    INT = 260,
    STRING = 261,
    IF = 262,
    THEN = 263,
    ELSE = 264,
    DO = 265,
    WHILE = 266,
    IN = 267,
    OUT = 268,
    NOT = 269,
    OR = 270,
    AND = 271,
    // operadores e pontuacao
    ASSIGN = 272,
    GE = 273,
    LE = 274,
    NEQ = 275,
    // outros tokens
    INTCONST=276,
    LITERAL=277,
    ID=278;
}
