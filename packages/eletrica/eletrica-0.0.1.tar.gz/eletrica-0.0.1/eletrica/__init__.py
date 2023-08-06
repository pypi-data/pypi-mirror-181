# Bibliotecas necessárias

import cmath
import numpy as np

# Definições

casasDecimais = "{:.6f}"
casasDecimaisAngulo = "{:.2f}"

# Classe comum

class Eletrica():
    def __init__(self, valor):

        # Inicialização

        self.real=0
        self.imag=0

        if (valor): 

            if (type(valor) == str):
                if (valor.find("<")>0):
                    self.real=strToPolar(valor).real
                    self.imag=strToPolar(valor).imag
                else:
                    if (valor.find("j")>0):
                        self.real=strToRect(valor).real
                        self.imag=strToRect(valor).imag
                    else:
                        pass
            else:
                self.real=complex(valor).real
                self.imag=complex(valor).imag

        # Propriedades

        self.polar=RetangularParaPolar(complex(self.real, self.imag))

        if (self.imag >= 0):
            self.retangular=str(casasDecimais.format(self.real)) + "+j" + str(casasDecimais.format(self.imag))
        else:
            self.retangular=str(casasDecimais.format(self.real)) + "-j" + str(casasDecimais.format(self.imag*-1))

        self.conjugado = complex(self.real,self.imag).conjugate()
        self.modulo = (self.real**2 + self.imag**2)**0.5
        self.fase = Graus(cmath.phase(complex(self.real,self.imag)))

    # Operações

    def __add__(self, other):
        return Eletrica(complex(self.real,self.imag) + complex(other.real, other.imag))

    __radd__ = __add__

    def __sub__(self, other):
        return Eletrica(complex(self.real,self.imag) - complex(other.real, other.imag))

    __rsub__ = __sub__

    def __mul__(self, other):
        return Eletrica(complex(self.real,self.imag) * complex(other.real, other.imag))

    __rmul__ = __mul__

    def __truediv__(self, other):
        return Eletrica(complex(self.real,self.imag) / complex(other.real, other.imag))

    def __rtruediv__(self, other):
        return Eletrica(complex(other.real, other.imag) / complex(self.real,self.imag))        

    def __div__(self, other):
        return Eletrica(complex(self.real,self.imag) / complex(other.real, other.imag))

    def __rdiv__(self, other):
        return Eletrica(complex(other.real, other.imag) / complex(self.real,self.imag))  

    def __abs__(self):
        return complex(self.real,self.imag).__abs__()

    def __neg__(self):
        return Eletrica(complex(self.real,self.imag)*-1)

    def __eq__(self, other):
        return self.real == other.real and self.imag == other.imag

    def __gt__(self, other):
        return self.__abs__() > other.__abs__()

    def __le__(self, other):
        return self.__abs__() > other.__abs__()

    def __pow__(self, power):
        return Eletrica(complex(self.real, self.imag)**power)        

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.retangular

    def __repr__(self):
        return self.retangular


# Classe fasor

class Fasor(Eletrica):
    def __init__(self, valor):
        super().__init__(valor)
        
    def conjugado(self):
        resultado = complex(self.real,self.imag).conjugate()
        return Fasor(resultado)          
        
    def __str__(self):
        return self.polar

    def __repr__(self):
        return self.polar

# Classe impedância

class Impedancia(Eletrica):
    def __init__(self, valor):
        super().__init__(valor)
        
    def conjugado(self):
        resultado = complex(self.real,self.imag).conjugate()
        return Impedancia(resultado)          
        
    def __str__(self):
        return self.retangular

    def __repr__(self):
        return self.retangular

# Conversão de ângulos

def Graus(angulo):
    return angulo*180/cmath.pi.__abs__()

def Radianos(angulo):
    return angulo*cmath.pi.__abs__()/180    

# Função para tratar valor no formato a<b°

def strToPolar(z1):
    posAng = z1.find("<")
    modulo, angulo = 0, 0
    modulo, angulo = float(z1[:posAng]), float(z1.replace("°","")[posAng+1:])
    if (modulo):
        return cmath.rect(modulo,Radianos(angulo))
    return 0

# Função para tratar valor no formato a+jb

def strToRect(z1):
    posJ = z1.find("j")
    if (posJ > -1):
        z = z1.replace("j","") + 'j'
    if (z):
        return complex(z)
    return 0

# Conversão Retangular para Polar (com ângulo em graus)

def RetangularParaPolar(valor):
    modulo, angulo = 0, 0
    modulo, angulo = casasDecimais.format(abs(valor)), casasDecimaisAngulo.format(Graus(cmath.phase(valor)))
    valorPolar = str(modulo) + "<" + str(angulo) + "°"
    return valorPolar

# Paralelo

def Paralelo(Z1, Z2):
    return (Z1**-1 + Z2**-1)**-1

# Vetor auxiliar "a"

def a():
    return Fasor("1<120°")    

# Unidades PU

def CorrenteBase(S_MVA, V_KV):
    return S_MVA*1e6/(cmath.sqrt(3)*V_KV*1e3)

def Zpu(Z, S_MVA, V_KV):
    return Impedancia(Z/((V_KV*1e3)**2/(S_MVA*1e6)))

def ZpuNovaBase(Zpu, S_MVA, V_KV, S_MVA_nova, V_KV_nova):
    Zohm = Zpu*((V_KV*1e3)**2/(S_MVA*1e6))
    Zpu_nova = Zohm/((V_KV_nova*1e3)**2/(S_MVA_nova*1e6))
    return Zpu_nova

# Vetores de fase e de sequência

def VetorABC(FaseA,FaseB,FaseC):
    arr = np.array([[FaseA],
                     [FaseB],
                     [FaseC]])  
    return arr  

def Vetor012(Seq0,Seq1,Seq2):
    arr = np.array([[Seq0],
                     [Seq1],
                     [Seq2]])  
    return arr  

def ImprimirVetorPolar(grandeza, vetor, unidade):
    print(grandeza + "A:", vetor[0,0].polar, unidade)     
    print(grandeza + "B:", vetor[1,0].polar, unidade) 
    print(grandeza + "C:", vetor[2,0].polar, unidade) 

def Sequencias(ValorPorFase):
    ax=a()
    arr1 = np.array([[1, 1, 1],
                    [1, ax**2, ax],
                    [1, ax, ax**2]])
    arr1 = np.linalg.inv(arr1)
    arr_012 = np.matmul(arr1,ValorPorFase)
    return arr_012

def Fases(ValorPorSequencia):
    ax=a()
    arr1 = np.array([[1, 1, 1],
                    [1, ax**2, ax],
                    [1, ax, ax**2]])
    arr_abc = np.matmul(arr1,ValorPorSequencia)
    return arr_abc   

# Compensação da corrente para proteção diferencial de transformadores    

def MatrizRotacao(k):
    arr = 1/cmath.sqrt(3)*np.array([[1, -1, 0],
                                    [0,  1, -1],
                                    [-1, 0, 1]])
    return np.linalg.matrix_power(arr, k)

def Compensacao(k, correntes):
    return np.matmul(MatrizRotacao(k),correntes)    

# Faltas

## Falta trifásica (simétrica)

def Icc3f(V, Z1, Zf):
    return V/(Z1 + Zf)

## Falta monofásica

def Icc1f(V, Z0, Z1, Z2, Zf):
    return 3*V/(Z0 + Z1 + Z2 + 3*Zf)

## Falta bifásica

def Icc2f(V, Z1, Z2, Zf):
    I0 = 0
    I1 = V/(Z1 + Z2 + Zf)
    I2 = -1*I1
    return Vetor012(I0, I1, I2)

## Falta bifásica para terra

def Icc2ft(V, Z0, Z1, Z2, Zf, Zft):
    I1 = V/(Z1 + Zf/2 + Paralelo((Z2 + Zf/2), (Z0 + Zf/2 + 3*Zft)))
    I2 = -1*I1*(Z0 + Zf/2 + 3*Zft)/(Z2 + Z0 + Zf + 3*Zft)
    I0 = -1*I1*(Z2 + Zf/2)/(Z2 + Z0 + Zf + 3*Zft)
    return Vetor012(I0, I1, I2)
