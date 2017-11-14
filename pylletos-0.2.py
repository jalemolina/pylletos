#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       pylletos-0.2.py
#
#       Copyright 2016 Alejandro Molina <jalemolina arroba gmail dot com>
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
import shutil
import subprocess
import poppler

def main():
    def organizar(pagIricio, pagFinal):
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
            pagFinal -= 1
        return l

    def preparar(N):
        #Dicci = "321"
        print "\nAñadiendo páginas en blanco...\n"
        #comandoUnir = ["pdfjoin",
                        #"--outfile",
                        #"listo.pdf",
                        #sys.argv[1],
                        #"enBlanco" + Dicci[N-1] + ".pdf"]
        #subprocess.call(comandoUnir)
        ########################################################################
        if N == 1:
            peb = '{},{},{}'
            peba = 3
        elif N == 2:
            peb = '{},{}'
            peba = 2
        elif N == 3:
            peb = '{}'
            peba = 1
        comandoPagsEnBlanco = ["pdfjam",
                               sys.argv[1],
                               '1-,' + peb,
                               "--outfile",
                               "listo.pdf"]
        #print comandoPagsEnBlanco
        subprocess.call(comandoPagsEnBlanco)
        #return n_pages + int(Dicci[N-1])
        return n_pages + peba

    print "\nProcesando " + sys.argv[1]

    uri = "file://" + os.getcwd() + "/" + sys.argv[1]
    document = poppler.document_new_from_file(uri, None)
    n_pages = document.get_n_pages()
    titulo = document.get_properties("title")[0]
    formato = document.get_properties("format")[0]
    autor = document.get_properties("author")[0]
    productor = document.get_properties("producer")[0]
    creador = document.get_properties("creator")[0]

    print "\n".center(80, "=")
    print ("INFORMACIÓN DE " + sys.argv[1]).center(80, " ")
    print "\t".center(80, "=")
    print ("Número de páginas: " + str(n_pages)).ljust(5, " ")
    print ("Título: " + str(titulo)).ljust(5, " ")
    print ("Formato: " + str(formato)).ljust(5, " ")
    print ("Autor: " + str(autor)).ljust(5, " ")
    print ("Productor: " + str(productor)).ljust(5, " ")
    print ("Creador: " + str(creador)).ljust(5, " ")
    print "".center(80, "=")


    if n_pages%4 != 0:
        NumPags = preparar(n_pages%4)
    else:
        NumPags = n_pages
        shutil.copy(sys.argv[1], 'listo.pdf')


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
    #comando = ["pdfnup",
               #"--nup",
               #"2x1",
               #"--pages",
               #c,
               #"--outfile",
               #sys.argv[1] + "_folleto.pdf",
               #"listo.pdf"]
    comando = ["pdfjam",
               "--nup",
               "2x1",
               "listo.pdf",
               c,
               "--landscape",
               "--outfile",
               sys.argv[1].partition(".")[0] + "_folleto.pdf"]
    #print comando
    subprocess.call(comando)
    print "\n¡Listo!"
    os.remove('listo.pdf')

    return 0

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main()
    elif len(sys.argv) > 2:
        print "ERROR: Sobran parámetros\n"
    else:
        print "ERROR: Falta parámetro\n"
        print """\tNombre_De_Archivo.pdf\n"""
