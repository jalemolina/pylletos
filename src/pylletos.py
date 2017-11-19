#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    File: pylletos.py
    Author: José Alejandro Molina
    Email: yourname@email.com
    Github: https://github.com/yourname
    Description:
"""

import os
import shutil
import subprocess
import sys

try:
    import gi
    gi.require_version('Poppler', '0.18')
    from gi.repository import Poppler
except ImportError:
    print('No se encuentra Poppler de gi.repository')


def organizar(pagina_inicial, pagina_final):
    """
    TODO: Docstring de la funcion
    """

    medio = (pagina_inicial + pagina_final) / 2
    lista_paginas_organizadas = []
    while pagina_final > medio:
        lista_paginas_organizadas.append(pagina_final)
        if pagina_final % 2 == 0:
            while pagina_inicial < medio + 1:
                lista_paginas_organizadas.append(pagina_inicial)
                if pagina_inicial % 2 == 0:
                    pagina_inicial += 1
                    break
                pagina_inicial += 1
        pagina_final -= 1
    return lista_paginas_organizadas


def preparar(n_pages):
    """
    TODO: Docstring de la funcion
    """

    paginas_libres = n_pages % 4
    print("\nAñadiendo páginas en blanco...\n")

    if paginas_libres == 1:
        peb = '{},{},{}'
        peba = 3
    elif paginas_libres == 2:
        peb = '{},{}'
        peba = 2
    elif paginas_libres == 3:
        peb = '{}'
        peba = 1

    comando_paginas_en_blanco = ["pdfjam",
                                 sys.argv[1],
                                 '1-,' + peb,
                                 "--outfile",
                                 "listo.pdf"]
    subprocess.call(comando_paginas_en_blanco)
    return n_pages + peba


def main():
    """
    TODO: Docstring de la funcion
    """

    print("\nProcesando " + sys.argv[1])

    uri = "file://" + os.getcwd() + "/" + sys.argv[1]
    document = Poppler.Document.new_from_file(uri, None)
    n_pages = document.get_n_pages()
    titulo = document.get_properties("title")[0]
    formato = document.get_properties("format")[0]
    autor = document.get_properties("author")[0]
    productor = document.get_properties("producer")[0]
    creador = document.get_properties("creator")[0]

    print("".center(80, "="))
    print(("INFORMACIÓN DE " + sys.argv[1]).center(80, " "))
    print("".center(80, "="))
    print("\tNúmero de páginas: " + str(n_pages))
    print("\tTítulo: " + str(titulo))
    print("\tFormato: " + str(formato))
    print("\tAutor: " + str(autor))
    print("\tProductor: " + str(productor))
    print("\tCreador: " + str(creador))
    print("".center(80, "="))

    if n_pages % 4 != 0:
        numero_de_paginas = preparar(n_pages)
    else:
        numero_de_paginas = n_pages
        shutil.copy(sys.argv[1], 'listo.pdf')

    cantidad_total_hojas = numero_de_paginas // 4
    cantidad_hojas_por_folleto = 5
    cantidad_de_folletos = cantidad_total_hojas // cantidad_hojas_por_folleto
    cantidad_paginas_x_folleto = cantidad_hojas_por_folleto * 4
    lista_final = []

    for i in range(cantidad_de_folletos):
        lista_final.extend(organizar((1 + i * cantidad_paginas_x_folleto),
                                     ((i + 1) * cantidad_paginas_x_folleto)))
    if cantidad_total_hojas % cantidad_hojas_por_folleto != 0:
        ultimo_a = 1 + cantidad_de_folletos * cantidad_paginas_x_folleto
        lista_final.extend(organizar(ultimo_a, numero_de_paginas))

    paginas_ordenadas = str(lista_final)[1:-1].replace(" ", "")
    print("\nPAGINAS")
    print(paginas_ordenadas)
    print("\nLlamando a PDFJAM...\n")
    comando = ["pdfjam",
               "--nup",
               "2x1",
               "listo.pdf",
               paginas_ordenadas,
               "--landscape",
               "--outfile",
               sys.argv[1].partition(".")[0] + "_folleto.pdf"]
    print(comando)
    subprocess.call(comando)
    print("\n¡Listo!")
    os.remove('listo.pdf')

    return 0


if __name__ == '__main__':
    if len(sys.argv) == 2:
        sys.exit(main())
    elif len(sys.argv) > 2:
        print("ERROR: Sobran parámetros\n")
    else:
        print("ERROR: Falta parámetro\n")
        print("""\tNombre_De_Archivo.pdf\n""")
