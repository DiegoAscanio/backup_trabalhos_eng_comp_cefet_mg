function [ x, and, or, w_and, w_or, w_i_and, w_i_or ] = perceptron()
    error = 1;
    n = 0.20;
    x = [0 0 0;
         0 0 1;
         0 1 0;
         0 1 1;
         1 0 0;
         1 0 1;
         1 1 0;
         1 1 1];
     y_d_and = [0; 0; 0; 0; 0; 0; 0; 1];
     and = zeros(8,1);
     y_d_or = [0; 1; 1; 1; 1; 1; 1; 1];
     or = zeros(8,1);
     % cria pesos iniciais aleatorios
     w = arrayfun(@(x)(0.5 - rand), zeros(4,1)); % 3 pesos + bias
     w_i_and = w;
     
     % rna and - treinamento da rede
     e = 0; % e - esperado
     while e ~= 1 % enquanto nao se alcancam os valores esperados
         e = 1;
         index = randperm(8);
         for i = 1:8
             % selecao de uma entrada aleatoria - por causa do randperm ali em cima
             x_i = horzcat([1], x(index(i),1:3)); % x0, x1, x2, x3 - concatenacao horizontal necessaria, para incluir bias
             y_d = y_d_and(index(i)); % y desejado para a operacao AND
             net = 0;
             for j = 1:4
                 net = net + w(j)*x_i(j); % calculo da rede
             end
             if net > 0
                 y = 1;
             else
                 y = 0;
             end
             error = y_d - y;
             if error ~= 0
                 for j = 1:4
                     w(j) = w(j) + n*error*x_i(j);
                 end
                 e = 0;
             end
         end
     end
     % apos treinamento da rede - averiguacao do funcionamento
     for i = 1:8
         x_i = horzcat([1], x(i,1:3));
         net = 0;
         for j = 1:4
             net = net + w(j)*x_i(j); % calculo da rede
         end
         if net > 0
             y = 1;
         else
             y = 0;
         end
         and(i) = y;
     end
     w_and = w;
     
     w = arrayfun(@(x)(0.5 - rand), zeros(4,1)); % 3 pesos + bias
     w_i_or = w;
     % rna or - treinamento da rede
     e = 0; % e - esperado
     while e ~= 1 % enquanto nao se alcancam os valores esperados
         e = 1;
         index = randperm(8);
         for i = 1:8
             x_i = horzcat([1], x(index(i),1:3)); % x0, x1, x2, x3 - concatenacao horizontal necessaria, para incluir bias
             y_d = y_d_or(index(i)); % y desejado para a operacao OR
             net = 0;
             for j = 1:4
                 net = net + w(j)*x_i(j); % calculo da rede
             end
             if net > 0
                 y = 1;
             else
                 y = 0;
             end
             error = y_d - y;
             if error ~= 0
                 for j = 1:4
                     w(j) = w(j) + n*error*x_i(j);
                 end
                 e = 0;
             end
         end
     end
     % apos treinamento da rede - averiguacao do funcionamento
     for i = 1:8
         x_i = horzcat([1], x(i,1:3));
         net = 0;
         for j = 1:4
             net = net + w(j)*x_i(j); % calculo da rede
         end
         if net > 0
             y = 1;
         else
             y = 0;
         end
         or(i) = y;
     end
     w_or = w;
end
