# ===============================================================
#
# CURVA DE TRANSFERENCIA DE UM CIRCUITO AMPLIFICADOR COM FILTRO PASSA-FAIXA
#
# Autor: Márcio Augusto Nascimento Atolini
# Data: 03/2023
# 
# ===============================================================

import math
import matplotlib.pyplot as plt

# ===============================================================
# Entrada de variaveis
# ===============================================================
R1 = float(input("Entre com o valor de R1: ")) #2.2e6
C1 = float(input("Entre com o valor de C1: ")) #4.7e-9
R2 = float(input("Entre com o valor de R2: ")) #33e3
C2 = float(input("Entre com o valor de C2: ")) #10e-6
R3 = float(input("Entre com o valor de R3: ")) #2.2e6
C3 = float(input("Entre com o valor de C3: ")) #4.7e-9
R4 = float(input("Entre com o valor de R4: ")) #33e3
C4 = float(input("Entre com o valor de C4: ")) #10e-6
R5 = float(input("Entre com o valor de R5: ")) #2.2e6

freqInicial = 0.1
freqFinal = 20
freqSteps = 0.001

tensaoDCEntrada = 0.7 #float(input('Entre com o valor de tensão DC presente na entrada do circuito: ))' #0.7
alimMin = 0
alimMax = 3.3 - 1.2

# ===============================================================
# Definicao da lista de frequencias angulares com base na lista de 
# frequencias (espectro para o qual se deseja conhecer a resposta do circuito).
# ===============================================================
listaFrequencias = []
listaFreqAngular = []
i = 0
freq = 0

while freq < freqFinal:
  freq = freqInicial +  (i * freqSteps )
  listaFrequencias.append( freq )
  i += 1

for freq in listaFrequencias:
  listaFreqAngular.append( 2 * math.pi * freq )

# ===============================================================
# Calculo da impedancia, Z2, da rede R1-C1 (circuito RC paralelo).
# ===============================================================
AOP1_listaZ2 = []

for freqAngular in listaFreqAngular: 
  AOP1_listaZ2.append( R1 / (math.sqrt( 1 + math.pow( (freqAngular*R1*C1), 2 ) ) )  )

# ===============================================================
# Calculo da impedancia, Z1, da rede R2-C2 (circuito RC série).
# ===============================================================
AOP1_listaZ1 = []

for freqAngular in listaFreqAngular:
  AOP1_listaZ1.append( math.sqrt( math.pow(R2,2) + (1 / math.pow(freqAngular*C2,2)) ) )


# ===============================================================
# Calculo do ganho do primeiro estagio amplificador.
# ===============================================================
AOP1_listaGanho = []

for i in range( 0, len(AOP1_listaZ1) ):
  AOP1_listaGanho.append( 1 + (AOP1_listaZ2[i] / AOP1_listaZ1[i]) )

# ===============================================================
# Calculo, aproximado, das frequencias de corte inferior e superior
# e seus respectivos ganhos.
# ===============================================================
AOP1_ganhoMax = max( AOP1_listaGanho )
AOP1_freqGanhoMax = listaFrequencias[ AOP1_listaGanho.index( AOP1_ganhoMax ) ]


AOP1_ganhoDeCorte = AOP1_ganhoMax * 0.707


AOP1_ganhoFreqCorteInf = 0
AOP1_freqCorteInf = 0
AOP1_decibelFreqCorteInf = 0
i = 0 
while AOP1_listaGanho[i] <= AOP1_ganhoDeCorte:
  if AOP1_listaGanho[i] >= AOP1_ganhoFreqCorteInf:
    AOP1_ganhoFreqCorteInf = AOP1_listaGanho[i]
    AOP1_freqCorteInf = listaFrequencias[ AOP1_listaGanho.index(AOP1_ganhoFreqCorteInf) ]
  i += 1
AOP1_decibelFreqCorteInf = 10 * math.log( AOP1_ganhoFreqCorteInf/AOP1_ganhoMax )


AOP1_ganhoFreqCorteSup = 0
AOP1_freqCorteSup = 0
AOP1_decibelFreqCorteSup = 0
i = len(AOP1_listaGanho)-1
while AOP1_listaGanho[i] <= AOP1_ganhoDeCorte:
  if AOP1_listaGanho[i] >= AOP1_ganhoFreqCorteSup:
    AOP1_ganhoFreqCorteSup = AOP1_listaGanho[i]
    AOP1_freqCorteSup = listaFrequencias[ AOP1_listaGanho.index(AOP1_ganhoFreqCorteSup) ]
  i -= 1
AOP1_decibelFreqCorteSup = 10 * math.log(AOP1_ganhoFreqCorteSup/AOP1_ganhoMax)

# ===============================================================
# Relatório do Primeiro Estágio
# ===============================================================
'''
print(f'Ganho Maximo: {AOP1_ganhoMax:.2f} @{AOP1_freqGanhoMax:.2f}Hz')
print(f'Freq. de corte inferior aproximada: {AOP1_freqCorteInf:.2f}Hz - Ganho nesta frequência: {AOP1_ganhoFreqCorteInf:.2f} ({AOP1_decibelFreqCorteInf:.2f}dB)')
print(f'Freq. de corte superior aproximada: {AOP1_freqCorteSup:.2f}Hz - Ganho nesta frequência: {AOP1_ganhoFreqCorteSup:.2f}  ({AOP1_decibelFreqCorteSup:.2f}dB)')
'''

# ----------------------------------------------------------
# FIGURA 1
# ----------------------------------------------------------
'''
figura1 = plt.figure(1, figsize = (15,5))
#figura1.suptitle('Relatório do Estágio 1')

plotZ2 = plt.subplot(1,2,1)
plotZ2.plot( listaFrequencias, AOP1_listaZ2, label = 'Z2 x Freq', color='blue', linewidth=1, linestyle='solid' )
plt.ylabel('Impedância [Ohms]')
plt.xlabel('Frequencia [Hz]')
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
plt.legend()
plt.grid()
#plt.title('Z2 x Freq')

plotZ1 = plt.subplot(1,2,2)
plotZ1.plot( listaFrequencias, AOP1_listaZ1, label = 'Z1 x Freq', color='blue', linewidth=1, linestyle='solid' )
plt.ylabel('Impedância [Ohms]')
plt.xlabel('Frequencia [Hz]')
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
plt.legend()
plt.grid()
#plt.title('Z1 x Freq')
'''

# ----------------------------------------------------------
# FIGURA 2
# ----------------------------------------------------------
'''
figura2 = plt.figure(2, figsize = (10,5))
#figura2.suptitle('Relatório do Estágio 1')
plotA1 = plt.subplot(1,1,1)
plotA1.plot( listaFrequencias, AOP1_listaGanho, label = 'A1 x Freq', color='blue', linewidth=1, linestyle='solid' )

plotA1.plot( AOP1_freqGanhoMax, AOP1_ganhoMax, marker='o', color='red', label = 'Ganho Máximo' )
str_ganho = '  {:.2f}Hz, {:.2f} (0dB)'.format( AOP1_freqGanhoMax, AOP1_ganhoMax )
plotA1.annotate( str_ganho, xy = (AOP1_freqGanhoMax,AOP1_ganhoMax) )

plotA1.plot( AOP1_freqCorteInf, AOP1_ganhoFreqCorteInf, marker='o', color='black', label = 'Freq. Corte' )
str_ganho = '  {:.2f}Hz, {:.2f} ({:.2f}dB)'.format( AOP1_freqCorteInf, AOP1_ganhoFreqCorteInf, AOP1_decibelFreqCorteInf )
plotA1.annotate (str_ganho, xy = (AOP1_freqCorteInf, AOP1_ganhoFreqCorteInf) )

plotA1.plot( AOP1_freqCorteSup, AOP1_ganhoFreqCorteSup, marker='o', color='black' )#, label = 'Corte Superior' )
str_ganho = '  {:.2f}Hz, {:.2f} ({:.2f}dB)'.format( AOP1_freqCorteSup, AOP1_ganhoFreqCorteSup, AOP1_decibelFreqCorteSup)
plotA1.annotate( str_ganho, xy = (AOP1_freqCorteSup, AOP1_ganhoFreqCorteSup) )

plt.ylabel('Ganho')
plt.xlabel('Frequencia [Hz]')
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
plt.yticks([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70])
#plotA1.title('Estágio 1')
plt.legend()
plt.grid()

#plt.savefig('estagio1.png', format='png')

plt.tight_layout()
plt.show()
'''

# ===============================================================
# Calculo da impedancia Z2, da rede R3-C3 (circuito RC paralelo).
# ===============================================================
AOP2_listaZ2 = []

for freqAngular in listaFreqAngular: 
  AOP2_listaZ2.append( R3 / (math.sqrt( 1 + math.pow( (freqAngular*R3*C3), 2 ) ) )  )

# ===============================================================
# Calculo da impedancia Z1a (parcial), da rede R5-C4 (circuito RC paralelo).
# ===============================================================
AOP2_listaZ1a = []

for freqAngular in listaFreqAngular: 
  AOP2_listaZ1a.append( R5 / (math.sqrt( 1 + math.pow( (freqAngular*R5*C4), 2 ) ) )  )

# ===============================================================
# Calculo da impedancia Z1, da rede R4-Z1a (associação série de impedâncias).
# ===============================================================
AOP2_listaZ1 = []

for z1a in AOP2_listaZ1a:
  AOP2_listaZ1.append( math.sqrt( (math.pow(R4,2) + math.pow(z1a,2)) ) )

# ===============================================================
# Calculo do ganho do segundo estagio amplificador.
# ===============================================================
AOP2_listaGanho = []

for i in range( 0, len(AOP2_listaZ2) ):
  AOP2_listaGanho.append( 1 + (AOP2_listaZ2[i] / AOP2_listaZ1[i]) )

# ===============================================================
# Calculo, aproximado, das frequencias de corte inferior e superior 
# e seus respectivos ganhos.
# ===============================================================
AOP2_ganhoMax = max( AOP2_listaGanho )
AOP2_freqGanhoMax = listaFrequencias[ AOP2_listaGanho.index( AOP2_ganhoMax ) ]


AOP2_ganhoDeCorte = AOP2_ganhoMax * 0.707


AOP2_ganhoFreqCorteInf = 0
AOP2_freqCorteInf = 0
AOP2_decibelFreqCorteInf = 0
i = 0 
while AOP2_listaGanho[i] <= AOP2_ganhoDeCorte:
  if AOP2_listaGanho[i] >= AOP2_ganhoFreqCorteInf:
    AOP2_ganhoFreqCorteInf = AOP2_listaGanho[i]
    AOP2_freqCorteInf = listaFrequencias[ AOP2_listaGanho.index(AOP2_ganhoFreqCorteInf) ]
  i += 1
AOP2_decibelFreqCorteInf = 10 * math.log( AOP2_ganhoFreqCorteInf/AOP2_ganhoMax )


AOP2_ganhoFreqCorteSup = 0
AOP2_freqCorteSup = 0
AOP2_decibelFreqCorteSup = 0
i = len(AOP2_listaGanho)-1
while AOP2_listaGanho[i] <= AOP2_ganhoDeCorte:
  if AOP2_listaGanho[i] >= AOP2_ganhoFreqCorteSup:
    AOP2_ganhoFreqCorteSup = AOP2_listaGanho[i]
    AOP2_freqCorteSup = listaFrequencias[ AOP2_listaGanho.index(AOP2_ganhoFreqCorteSup) ]
  i -= 1
AOP2_decibelFreqCorteSup = 10 * math.log(AOP2_ganhoFreqCorteSup/AOP2_ganhoMax)

# ===============================================================
# Relatório do Segundo Estágio
# ===============================================================
'''
print(f'Ganho Maximo: {AOP2_ganhoMax:.2f} @{AOP2_freqGanhoMax:.2f}Hz')
print(f'Freq. de corte inferior aproximada: {AOP2_freqCorteInf:.2f}Hz - Ganho nesta frequência: {AOP2_ganhoFreqCorteInf:.2f} ({AOP2_decibelFreqCorteInf:.2f}dB)')
print(f'Freq. de corte superior aproximada: {AOP2_freqCorteSup:.2f}Hz - Ganho nesta frequência: {AOP2_ganhoFreqCorteSup:.2f}  ({AOP2_decibelFreqCorteSup:.2f}dB)')
'''

# ----------------------------------------------------------
# FIGURA 1
# ----------------------------------------------------------
'''
figura1 = plt.figure(1, figsize = (15,5))
#figura1.suptitle('Relatório do Estágio 2')

plotZ2 = plt.subplot(1,2,1)
plotZ2.plot( listaFrequencias, AOP2_listaZ2, label = 'Z2 x Freq', color='blue', linewidth=1, linestyle='solid' )
plt.ylabel('Impedância [Ohms]')
plt.xlabel('Frequencia [Hz]')
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
plt.legend()
plt.grid()
#plt.title('Z2 x Freq')

plotZ1 = plt.subplot(1,2,2)
plotZ1.plot( listaFrequencias, AOP2_listaZ1, label = 'Z1 x Freq', color='blue', linewidth=1, linestyle='solid' )
plt.ylabel('Impedância [Ohms]')
plt.xlabel('Frequencia [Hz]')
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
plt.legend()
plt.grid()
#plt.title('Z1 x Freq')
'''

# ----------------------------------------------------------
# FIGURA 2
# ----------------------------------------------------------
'''
figura2 = plt.figure(2, figsize = (10,5))
#figura2.suptitle('Relatório do Estágio 1')
plotA1 = plt.subplot(1,1,1)
plotA1.plot( listaFrequencias, AOP2_listaGanho, label = 'A1 x Freq', color='blue', linewidth=1, linestyle='solid' )

plotA1.plot( AOP2_freqGanhoMax, AOP2_ganhoMax, marker='o', color='red', label = 'Ganho Máximo' )
str_ganho = '  {:.2f}Hz, {:.2f} (0dB)'.format( AOP2_freqGanhoMax, AOP2_ganhoMax )
plotA1.annotate( str_ganho, xy = (AOP2_freqGanhoMax, AOP2_ganhoMax) )

plotA1.plot( AOP2_freqCorteInf, AOP2_ganhoFreqCorteInf, marker='o', color='black', label = 'Freq. Corte' )
str_ganho = '  {:.2f}Hz, {:.2f} ({:.2f}dB)'.format( AOP2_freqCorteInf, AOP2_ganhoFreqCorteInf, AOP2_decibelFreqCorteInf )
plotA1.annotate (str_ganho, xy = (AOP2_freqCorteInf, AOP2_ganhoFreqCorteInf) )

plotA1.plot( AOP2_freqCorteSup, AOP2_ganhoFreqCorteSup, marker='o', color='black' )#, label = 'Corte Superior' )
str_ganho = '  {:.2f}Hz, {:.2f} ({:.2f}dB)'.format( AOP2_freqCorteSup, AOP2_ganhoFreqCorteSup, AOP2_decibelFreqCorteSup)
plotA1.annotate( str_ganho, xy = (AOP2_freqCorteSup, AOP2_ganhoFreqCorteSup) )

plt.ylabel('Ganho')
plt.xlabel('Frequencia [Hz]')
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
plt.yticks([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70])
#plotA1.title('Estágio 1')
plt.legend()
plt.grid()

#plt.savefig('estagio2.png', format='png')

plt.tight_layout()
plt.show()
'''

# ===============================================================
# Calculo do ganho total do circuito (dois estagios em cascata)
# ===============================================================
SAIDA_listaGanho = []

for i in range(0,len(AOP1_listaGanho)):
  SAIDA_listaGanho.append(AOP1_listaGanho[i]*AOP2_listaGanho[i])


SAIDA_ganhoMax = max(SAIDA_listaGanho)
SAIDA_freqGanhoMax = listaFrequencias[SAIDA_listaGanho.index(SAIDA_ganhoMax)]
print(f'Ganho Maximo: {SAIDA_ganhoMax:.2f} @{SAIDA_freqGanhoMax:.2f}Hz')


SAIDA_ganhoDeCorte = SAIDA_ganhoMax * 0.707


SAIDA_ganhoFreqCorteInf = 0
SAIDA_freqCorteInf = 0
SAIDA_decibelFreqCorteInf = 0
i = 0
while SAIDA_listaGanho[i] <= SAIDA_ganhoDeCorte:
  if SAIDA_listaGanho[i] >= SAIDA_ganhoFreqCorteInf:
    SAIDA_ganhoFreqCorteInf = SAIDA_listaGanho[i]
    SAIDA_freqCorteInf = listaFrequencias[SAIDA_listaGanho.index(SAIDA_ganhoFreqCorteInf)]
  i += 1
SAIDA_decibelFreqCorteInf = 10 * math.log(SAIDA_ganhoFreqCorteInf/SAIDA_ganhoMax)
print(f'Freq. de corte inferior aproximada: {SAIDA_freqCorteInf:.2f}Hz - Ganho nesta frequência: {SAIDA_ganhoFreqCorteInf:.2f} ({SAIDA_decibelFreqCorteInf:.2f}dB)') 

SAIDA_ganhoFreqCorteSup = 0
SAIDA_freqCorteSup = 0
SAIDA_decibelFreqCorteSup = 0
i = len(SAIDA_listaGanho)-1
while SAIDA_listaGanho[i] <= SAIDA_ganhoDeCorte:
  if SAIDA_listaGanho[i] >= SAIDA_ganhoFreqCorteSup:
    SAIDA_ganhoFreqCorteSup = SAIDA_listaGanho[i]
    SAIDA_freqCorteSup = listaFrequencias[SAIDA_listaGanho.index(SAIDA_ganhoFreqCorteSup)]
  i -= 1
SAIDA_decibelFreqCorteSup = 10 * math.log(SAIDA_ganhoFreqCorteSup/SAIDA_ganhoMax)
print(f'Freq. de corte superior aproximada: {SAIDA_freqCorteSup:.2f}Hz - Ganho nesta frequência: {SAIDA_ganhoFreqCorteSup:.2f}  ({SAIDA_decibelFreqCorteSup:.2f}dB)')

# ===============================================================
# Análise DC
# Nível de tensão DC na saída do circuito (offset)
# ===============================================================
'''
AOP1_ganhoTensaoDC = 1
AOP1_tensaoDC = tensaoDCEntrada * AOP1_ganhoTensaoDC
print(f'Tensão DC na saída do primeiro estágio: {AOP1_tensaoDC:.2f}V')

AOP2_ganhoTensaoDC = 1 + (R3 / (R5+R4))
AOP2_tensaoDC = AOP1_tensaoDC * AOP2_ganhoTensaoDC
print(f'Tensão DC na saída do segundo estágio: {AOP2_tensaoDC:.2f}V')
'''

# ===============================================================
# Curva de Transferência
# ===============================================================
figura1 = plt.figure(1, figsize = (10,5))
#figura2.suptitle('Curva de Transferência')
plotSaida = plt.subplot(1,1,1)
plotSaida.plot( listaFrequencias, SAIDA_listaGanho, color='blue', linewidth=1, linestyle='solid' )

plotSaida.plot( SAIDA_freqGanhoMax, SAIDA_ganhoMax, marker='o', color='red', label = 'Ganho Máximo' )
str_ganho = '  {:.2f}Hz, {:.2f} (0dB)'.format( SAIDA_freqGanhoMax, SAIDA_ganhoMax )
plotSaida.annotate( str_ganho, xy = (SAIDA_freqGanhoMax, SAIDA_ganhoMax) )

plotSaida.plot( SAIDA_freqCorteInf, SAIDA_ganhoFreqCorteInf, marker='o', color='black', label = 'Freq. Corte' )
str_ganho = '  {:.2f}Hz, {:.2f} ({:.2f}dB)'.format( SAIDA_freqCorteInf, SAIDA_ganhoFreqCorteInf, SAIDA_decibelFreqCorteInf )
plotSaida.annotate (str_ganho, xy = (SAIDA_freqCorteInf, SAIDA_ganhoFreqCorteInf) )

plotSaida.plot( SAIDA_freqCorteSup, SAIDA_ganhoFreqCorteSup, marker='o', color='black' )#, label = 'Corte Superior' )
str_ganho = '  {:.2f}Hz, {:.2f} ({:.2f}dB)'.format( SAIDA_freqCorteSup, SAIDA_ganhoFreqCorteSup, SAIDA_decibelFreqCorteSup)
plotSaida.annotate( str_ganho, xy = (SAIDA_freqCorteSup, SAIDA_ganhoFreqCorteSup) )

plt.ylabel('Ganho')
plt.xlabel('Frequencia [Hz]')
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
plt.yticks([0,500,1000,1500,2000,2500,3000,3500,4000,4500])
plt.title('Curva de Transferência')
plt.legend()
plt.grid()

#plt.savefig('CurvaTransferencia.png', format='png')

plt.tight_layout()
plt.show()


