for caracter in range(1,101):
    if caracter % 6 == 0:
         print('fizzbuzz')
    elif caracter % 2 == 0:
        print('fizz')
    elif caracter % 3 == 0:
        print('buzz')
    else:
        print(caracter)