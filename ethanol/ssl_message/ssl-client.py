#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  implementação de ssl-client.c em python

  FOR TESTING ONLY
"""
import ssl
from socket import socket, AF_INET, SOCK_STREAM
from random import randint

from msg_hello import send_msg_hello
from msg_ping import send_msg_ping
from msg_common import SERVER_PORT

server = ("localhost", SERVER_PORT)

# cert = ssl_sock.getpeercert(True) # << False, if the certificate was not validated, the dict is empty.
# # mostra certificado em binário. não existe módulo no python (padrão) que faça esta decodificação
# print "certificado: ", cert

'''
  MSG HELLO
'''
num_tries = randint(1, 5)
print "enviando %d mensagem(s) de hello" % num_tries
for i in range(num_tries):
    print "envio de Hello #%d" % i
    ret = send_msg_hello(server, i)
    print "resposta: ", ret.m_id, ret.rtt
print "\n\n\n"

'''
  MSG PING
'''
num_tries = randint(1, 21)
pckt_size = randint(64, 512)
print "enviando %d pings de %d bytes" % (num_tries, pckt_size)
ret = send_msg_ping(server, id=1, num_tries=num_tries, p_size=pckt_size)
for p in ret:
    print p.m_id, p.rtt
