qntfam = int(input('quantas pessoas você tem na familia? '))
totaldes = 0

for i in range(1, qntfam + 1):
    totaldesindiv = 0  # Resetar aqui
    di = int(input('quantas despesas a pessoa %i tem? ' % i))
    for y in range(1, di + 1):
        dic = float(input('qual o custo da despesa %i ' % y))
        totaldesindiv += dic
    print('\n pessoa %i tem %.2f reais gastos \n' % (i, totaldesindiv))
    totaldes -= totaldesindiv  # Subtrair despesas da pessoa

for i in range(1, qntfam + 1):
    si = float(input('qual o salário da pessoa %i? ' % i))
    totaldes += si  # Adiciona salário ao orçamento

print('o seu orçamento total é %.2f reais.' % totaldes)
