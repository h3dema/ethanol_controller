#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Code by: Henrique Moura
# Last Change: 21/Mar/2016
#
#
#
class Enum():
  '''
    helper function - creates an enumeration

    > Number = Enum('a', 'b', 'c')
    > print Number.a
    0

  '''

  def __init__(self, *keys):
    for k, v in zip(keys, range(len(keys))):
      setattr(self, k, v)

def Enums(*sequential, **named):
  ''' helper function - creates an enumeration '''
  enums = dict(zip(sequential, range(len(sequential))), **named)
  print enums
  return type('Enum', (), enums)


# ############################################
#
#
# uma outra opção é utilizar o módulo enum
# porem enum inicia valores em 1
#
#
# ############################################
# para utilizar enum, é necessário instalar usando
# pip install enum34
# chmod g-wx,o-wx ~/.python-eggs
# 
# no arquivo python declarar:
# from enum import Enum
