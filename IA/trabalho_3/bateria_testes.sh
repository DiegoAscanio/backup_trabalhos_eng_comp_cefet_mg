#!/usr/bin/bash

populacao=100
geracoes=30
mutacao=0.25
n=(6 8 16 32 64 128 256 512)
solucao=$1
quantidade_execucoes=$2
x=10

for tabuleiro in ${n[*]}; do
    echo "======================== n: $tabuleiro"
    python2 n_rainhas.py $solucao $quantidade_execucoes $tabuleiro $populacao $geracoes $mutacao $x
    echo "========================"
done
