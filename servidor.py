# -*- coding: utf-8 -*-

import socket
import sys
import funcoes
import os

#Declaração de variáveis/cabeçalhos 
host = 'localhost'  
port = 5000
tamanhopacote=150
comprimentoservidor=66		#pacote = 16 porta origem + 16 porta destino + 16 comprimento + 1 ack + 1 seq + 16 checksum
dadosrecebidos=[]
dadosrecebidosordem=[]
dadosduplicados=[]
dadoscorrompidos=[]
dado=0
i=0

print "\nIniciando Servidor..."

#Criando Socket UDP
try :
	servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print '\nSocket criado com sucesso!'
except socket.error, msg :
	print '\nFalha ao criar o socket. Código do erro: ' + str(msg[0]) + '. Mensagem: ' + msg[1]
	sys.exit()

#Amarrando socket ao localhost e porta definidos
try:
	servidor.bind((host, port))
except socket.error , msg:
	print '\nBind falhou. Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1]
	sys.exit()
print '\nBind do Socket completo!'


#Para saber se é a primeira vez que passa pelo estado
oncethru=0

while 1:
	
	#Estado 0

	# Recebendo dados do cliente (dados, endereço)
	d = servidor.recvfrom(tamanhopacote)
	data = d[0]
	addr = d[1]
     
	if not data: 
		break

	i+=1
	os.system('clear')
	print "\n------------------------------------------"
	print "\tEnvio do",i,"º pacote"
	print "------------------------------------------"

	#Extraindo dados do pacote
	portaorigem=int(data[0:16],2)
	portadestino=int(data[16:32],2)
	comprimento=int(data[32:48],2)
	checksum=int(data[48:64],2)
	seq = int(data[64:65],2)
	dadoanterior=dado
	dado=int(data[65:97],2)

	soma = funcoes.checksum(portaorigem,portadestino,comprimento)
	
	if (seq==1):
		print "\nPacote ["+str(dadoanterior)+"] duplicado! Descartando e re-solicitando..."
		dadosduplicados.append(dadoanterior)
	if (soma!=checksum):
		print "\nPacote ["+str(dado)+"] com erro de bits! Descartando e re-solicitando..."
		dadoscorrompidos.append(dado)
	while (seq==1 or soma!=checksum):
		if (oncethru==1):
			try :
				#Enviando mensagem ao cliente informando pacote duplicado/corrompido
				servidor.sendto(msg, addr)
			except socket.error, msg:
				print 'Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1]
				sys.exit()

		
		# Recebendo dados do cliente (dados, endereço)
		d = servidor.recvfrom(tamanhopacote)
		data = d[0]
		addr = d[1]
	     
		if not data: 
			break

		#Extraindo dados do pacote
		portaorigem=int(data[0:16],2)
		portadestino=int(data[16:32],2)
		comprimento=int(data[32:48],2)
		checksum=int(data[48:64],2)
		seq = int(data[64:65],2)
		dadoanterior=dado
		dado=int(data[65:97],2)

		soma = funcoes.checksum(portaorigem,portadestino,comprimento)

	if (seq==0 and soma==checksum):
		dadosrecebidos.append(dado)
		dadosrecebidosordem.append(dado)
		dadosrecebidosordem.sort()
		print "\nPacote ["+str(dado)+"] recebido corretamente!"
		print "\nPacotes recebidos até o momento:"
		print dadosrecebidos
		print "\nPacotes recebidos (em ordem):"
		print dadosrecebidosordem
		print "\nPacotes duplicados:"
		print dadosduplicados
		print "\nPacotes corrompidos:"
		print dadoscorrompidos
		msg = funcoes.cria_pacote_servidor(servidor.getsockname()[1],port,comprimentoservidor,1,0)
		try :
			#Enviando mensagem ao cliente
			servidor.sendto(msg, addr)
		except socket.error, msg:
			print 'Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1]
			sys.exit()
		oncethru=1


	#Estado 1
	# Recebendo dados do cliente (dados, endereço)
	d = servidor.recvfrom(tamanhopacote)
	data = d[0]
	addr = d[1]
     
	if not data: 
		break

	#Extraindo dados do pacote
	portaorigem=int(data[0:16],2)
	portadestino=int(data[16:32],2)
	comprimento=int(data[32:48],2)
	checksum=int(data[48:64],2)
	seq = int(data[64:65],2)
	dadoanterior=dado
	dado=int(data[65:97],2)

	soma = funcoes.checksum(portaorigem,portadestino,comprimento)

	i+=1
	os.system('clear')
	print "\n------------------------------------------"
	print "\tEnvio do",i,"º pacote"
	print "------------------------------------------"

	if (seq==0):
		print "\nPacote ["+str(dadoanterior)+"] duplicado! Descartando e re-solicitando..."
		dadosduplicados.append(dadoanterior)
	if (soma!=checksum):
		print "\nPacote ["+str(dado)+"] com erro de bits! Descartando e re-solicitando..."
		dadoscorrompidos.append(dado)
	while (seq==0 or soma!=checksum):
		try :
			#Enviando mensagem ao cliente
			servidor.sendto(msg, addr)
		except socket.error, msg:
			print 'Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1]
			sys.exit()
		
		# Recebendo dados do cliente (dados, endereço)
		d = servidor.recvfrom(tamanhopacote)
		data = d[0]
		addr = d[1]
	     
		if not data: 
			break

		#Extraindo dados do pacote
		portaorigem=int(data[0:16],2)
		portadestino=int(data[16:32],2)
		comprimento=int(data[32:48],2)
		checksum=int(data[48:64],2)
		seq = int(data[64:65],2)
		dadoanterior=dado
		dado=int(data[65:97],2)

		soma = funcoes.checksum(portaorigem,portadestino,comprimento)

	if (seq==1 and soma==checksum):
		dadosrecebidos.append(dado)
		dadosrecebidosordem.append(dado)
		dadosrecebidosordem.sort()
		print "\nPacote ["+str(dado)+"] recebido corretamente!"
		print "\nPacotes recebidos até o momento:"
		print dadosrecebidos
		print "\nPacotes recebidos (em ordem):"
		print dadosrecebidosordem
		print "\nPacotes duplicados:"
		print dadosduplicados
		print "\nPacotes corrompidos:"
		print dadoscorrompidos

		msg = funcoes.cria_pacote_servidor(servidor.getsockname()[1],port,comprimentoservidor,1,1)
		try :
			#Enviando mensagem ao cliente informando pacote duplicado/corrompido
			servidor.sendto(msg, addr)
		except socket.error, msg:
			print 'Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1]
			sys.exit()

servidor.close()
