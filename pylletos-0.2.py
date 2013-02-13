#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       pylletos-0.2.py
#
#       Copyright 2010 Alejandro <ale@ale-laptop>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import sys
import os
import subprocess
import poppler

def main():
    def organizar(pagInicio, pagFinal):
        medio = (pagInicio + pagFinal) / 2
        l = []
        while pagFinal > medio:
            l.append(pagFinal)
            if pagFinal % 2 == 0:
                while pagInicio < medio + 1:
                    l.append(pagInicio)
                    if pagInicio % 2 == 0:
                        pagInicio += 1
                        break
                    pagInicio += 1
            pagFinal -=1
        return l

    def preparar(N):
        #Dicci = "321"
        print "\nAñadiendo páginas en blanco...\n"
        #comandoUnir = ["pdfjoin", "--outfile", "listo.pdf", sys.argv[1], "enBlanco" + Dicci[N-1] + ".pdf"]
        #subprocess.call(comandoUnir)
        ######################################################################################################
        if N == 1:
            peb = '{},{},{}'
            peba = 3
        elif N == 2:
            peb = '{},{}'
            peba = 2
        elif N == 3:
            peb = '{}'
            peba = 1
        comandoPagsEnBlanco = ["pdfjam", sys.argv[1], '1-,' + peb, "--outfile", "listo.pdf"]
        #print comandoPagsEnBlanco
        subprocess.call(comandoPagsEnBlanco)
        #return n_pages + int(Dicci[N-1])
        return n_pages + peba

    print "\nProcesando " + sys.argv[1]

    uri = "file://" + os.getcwd() + "/" + sys.argv[1]
    document = poppler.document_new_from_file (uri, None)
    n_pages = document.get_n_pages()
    titulo = document.get_properties("title")[0]
    formato = document.get_properties("format")[0]
    autor = document.get_properties("author")[0]
    productor = document.get_properties("producer")[0]
    creador = document.get_properties("creator")[0]

    print "\n\t=============================================================="
    print "\t\t\tINFORMACIÓN DE " + sys.argv[1]
    print "\t=============================================================="
    print "\t\tNúmero de páginas: " + str(n_pages)
    print "\t\tTítulo: " + str(titulo)
    print "\t\tFormato: " + str(formato)
    print "\t\tAutor: " + str(autor)
    print "\t\tProductor: " + str(productor)
    print "\t\tCreador: " + str(creador)
    print "\t=============================================================="


    if n_pages%4!=0:
        NumPags = preparar(n_pages%4)
    else:
        NumPags = n_pages


    cth = NumPags/4
    chxf = 5
    CantFolletos = cth / chxf
    cpxf = chxf * 4
    listafinal = []

    for i in range(CantFolletos):
        listafinal.extend(organizar((1+i*cpxf), ((i+1)*cpxf)))
    if cth%chxf != 0:
        ultimoA = 1 + CantFolletos * cpxf
        listafinal.extend(organizar(ultimoA, NumPags))

    c = str(listafinal)[1:-1].replace(" ", "")
    print "\nPAGINAS"
    print c
    print "\nLlamando a PDFJAM...\n"
    #comando = ["pdfnup", "--nup", "2x1", "--pages", c, "--outfile", sys.argv[1] + "_folleto.pdf", "listo.pdf"]
    comando = ["pdfjam", "--nup", "2x1", "listo.pdf", c, "--landscape", "--outfile", sys.argv[1] + "_folleto.pdf"]
    #print comando
    subprocess.call(comando)
    print "\n¡Listo!"

    return 0

if __name__ == '__main__':
    if (len(sys.argv)==2):
        main()
    elif (len(sys.argv)>2):
        print "ERROR: Sobran parámetros\n"
    else:
        print "ERROR: Falta parámetro\n"
        print """\tNombre_De_Archivo.pdf\n"""
