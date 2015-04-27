# -*- coding: utf-8 -*-

import socket
import sys
import funcoes
import random

#Declaração variáveis/cabeçalhos
host = 'localhost'
port = 5000
tamanhopacote=150
comprimento = 97

#Criando Socket UDP
try:
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Falha ao criar o socket!'
    sys.exit()
 
portClient = 0		#Passando a porta de origem como 0, o S.O. dá uma porta livre. Acessar com cliente.getsockname()[1]
cliente.bind(('',portClient))
portaorigem = cliente.getsockname()[1]

arquivo = open(sys.argv[1],'r')
vetor = arquivo.read().splitlines()


while len(vetor)>1:

	escolha = funcoes.menu(vetor)
	while (escolha==4):
		toshuffle = vetor[0:len(vetor)-1]
		random.shuffle(toshuffle)
		toshuffle.append('-1')
		vetor=toshuffle
		escolha = funcoes.menu(vetor)

	#Estado 0

	dado = int(vetor.pop(0))
        if dado==-1:
		break
	
	#Forçar o erro de bits mudando a soma de verificação	
	if (escolha==2):
		soma=0
	else:
		soma = funcoes.checksum(portaorigem,port,comprimento)

	#Forçando pacotes duplicados
	if (escolha==3):
		seq=1
	else:
		seq=0

	#Encerrando cliente
	if escolha==5:
		sys.exit()

	msg = funcoes.cria_pacote_cliente(portaorigem,port,comprimento,soma,seq,dado)
	
	try :
		#Enviando datagrama ao servidor
		cliente.sendto(msg, (host, port))
	except socket.error, msg:
		print 'Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1]
		sys.exit()


	#Estado 1
	# Recebendo mensagem do servidor
	d = cliente.recvfrom(tamanhopacote)
	data = d[0]
	addr = d[1]

	if not data: 
		break

	portaorigemservidor=int(data[0:16],2)
	portadestinoservidor=int(data[16:32],2)
	comprimentoservidor=int(data[32:48],2)
	ackservidor=int(data[48:49],2)
	seqservidor=int(data[49:50],2)
	somaservidor=int(data[50:66],2)

	verificasoma=funcoes.checksum(portaorigemservidor,portadestinoservidor,comprimentoservidor)

	while (somaservidor!=verificasoma or (ackservidor==1 and seqservidor==1)):

		soma = funcoes.checksum(portaorigem,port,comprimento)
		seq = 0
		msg = funcoes.cria_pacote_cliente(portaorigem,port,comprimento,soma,seq,dado)
		cliente.sendto(msg,(host,port))		

		# Recebendo mensagem do servidor
		d = cliente.recvfrom(tamanhopacote)
		data = d[0]
		addr = d[1]

		portaorigemservidor=int(data[0:16],2)
		portadestinoservidor=int(data[16:32],2)
		comprimentoservidor=int(data[32:48],2)
		ackservidor=int(data[48:49],2)
		seqservidor=int(data[49:50],2)
		somaservidor=int(data[50:66],2)

		verificasoma=funcoes.checksum(portaorigemservidor,portadestinoservidor,comprimentoservidor)

		if not data: 
			break

	#Estado 2

	escolha = funcoes.menu(vetor)
	while (escolha==4):
		toshuffle = vetor[0:len(vetor)-1]
		random.shuffle(toshuffle)
		toshuffle.append('-1')
		vetor=toshuffle
		escolha = funcoes.menu(vetor)

	dado = int(vetor.pop(0))
        if dado==-1:
		break

	#Forçar o erro de bits mudando a soma de verificação
	if (escolha==2):
		soma=0
	else:
		soma = funcoes.checksum(portaorigem,port,comprimento)
	
	#Forçando pacotes duplicados
	if (escolha==3):
		seq=0
	else:
		seq=1

	#Encerrando cliente
	if escolha==5:
		sys.exit()


	msg = funcoes.cria_pacote_cliente(portaorigem,port,comprimento,soma,seq,dado)

	try :
		#Enviando datagrama ao servidor
		cliente.sendto(msg, (host, port))
	except socket.error, msg:
		print 'Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1]
		sys.exit()

	#Estado 3
	# Recebendo mensagem do servidor
	d = cliente.recvfrom(tamanhopacote)
	data = d[0]
	addr = d[1]

	if not data: 
		break

	portaorigemservidor=int(data[0:16],2)
	portadestinoservidor=int(data[16:32],2)
	comprimentoservidor=int(data[32:48],2)
	ackservidor=int(data[48:49],2)
	seqservidor=int(data[49:50],2)
	somaservidor=int(data[50:66],2)

	verificasoma=funcoes.checksum(portaorigemservidor,portadestinoservidor,comprimentoservidor)

	while (somaservidor!=verificasoma or (ackservidor==1 and seqservidor==0)):

		soma = funcoes.checksum(portaorigem,port,comprimento)
		seq = 1
		msg = funcoes.cria_pacote_cliente(portaorigem,port,comprimento,soma,seq,dado)
		cliente.sendto(msg,(host,port))		

		# Recebendo mensagem do servidor
		d = cliente.recvfrom(tamanhopacote)
		data = d[0]
		addr = d[1]

		portaorigemservidor=int(data[0:16],2)
		portadestinoservidor=int(data[16:32],2)
		comprimentoservidor=int(data[32:48],2)
		ackservidor=int(data[48:49],2)
		seqservidor=int(data[49:50],2)
		somaservidor=int(data[50:66],2)

		verificasoma=funcoes.checksum(portaorigemservidor,portadestinoservidor,comprimentoservidor)

		if not data: 
			break

cliente.close()
