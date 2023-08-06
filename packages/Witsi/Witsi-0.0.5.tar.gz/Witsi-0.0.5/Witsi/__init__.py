# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 13:17:16 2022

@author: MI19288
"""

import requests
from bs4 import BeautifulSoup
from random import randint
import networkx as nx
import matplotlib.pyplot as plt
#Para fechas
import pandas as pd
from datetime import date
from datetime import timedelta


def url_fecha(job):
    global url
    #Obtenemos la fecha del sistema
    fecha_inicial = str(pd.to_datetime(date.today()) - timedelta(days=2))[:10]
    fecha_final = str(pd.to_datetime(date.today()))[:10]
    #print("-----\n fecha Inicial \n " + fecha_inicial + "\n- fecha Final \n " + fecha_final)

    #Construimos la URL 
    path_scheduling_inicio = 'http://150.100.216.64:8080/scheduling/ejecucionesStatusConsulta?jobname=' 
    path_scheduling_intervalo = '%25&txtFromDate=' + fecha_inicial + '&txtFromTime=00:00&txtToDate=' + fecha_final + '&txtToTime=23:59&nodeid=&foldername=&aplicacion='
    url = path_scheduling_inicio + job + path_scheduling_intervalo

def status_job(job, ODATE):

    url_fecha(job)
    #print("Para el Job: ", job)
    try: 
        table = pd.read_html(url)[1]
        # Se renombra la columna para poder hacer uso de .query 
        table.rename(columns= {'ENDED STATUS': 'ENDED_STATUS'}, inplace=True)

        eje_Ok = table.query('ENDED_STATUS  == "OK" & ODATE == @ODATE')
        eje_NotOK = table.query('ENDED_STATUS  == "NOTOK" & ODATE == @ODATE')
        
        # Si no hay ejecuciones
        if(eje_Ok.shape[0] == 0 and eje_NotOK.shape[0] == 0):
            return veri_ejecutando(job,ODATE)

        #Hay al menos una ejecución OK 
        if(eje_Ok.shape[0] >= 1):
            run_counter = table['RUN COUNTER'].max()
            return (1,url,run_counter)
        if(eje_NotOK.shape[0] > 0 and eje_Ok.shape[0] == 0):
            #print("Proceso cancelado\n El job " + job + " tiene " + str(eje_NotOK.shape[0]) + " cancelaciones para el odate ", ODATE)
            run_counter = table['RUN COUNTER'].max()
            return (0,url, run_counter) 
        # else:
        #     run_counter = table['RUN COUNTER'].max()
        #     return (1,url, run_counter) 
    except:
        return veri_ejecutando(job,ODATE)    

def veri_ejecutando(job,ODATE):
    activo_odate = ODATE - 20000000
    url_eje = "http://150.100.216.64:8080/scheduling/ajF?filtro=" + job

    try:
        table_activo = pd.read_html(url_eje)[0]
        if(table_activo.shape[0] == 0):
            #print("El job " + job + " no está cargado al activo para el odate ", ODATE)
            return (4,url_eje, 0) # -> No tiene por que ejecutar
        ejecutando = table_activo.query('STATUS == "Executing" & ODATE == @activo_odate')
        if(ejecutando.shape[0] == 1):
            return (3,url_eje,0) # 3 -> Ejecutando
        eje_wait = table_activo.query('ODATE == @activo_odate & STATUS == "Wait Condition ¿Que espera para ejecutar?"')
        if(eje_wait.shape[0] >= 1):
            return (2,url_eje, 0) # 2 -> Pendiente de ejecutar
        else: 
            return (4,url_eje, 0)  
    except Exception as e:
        print("Ha ocurrido un error ", e)
        return (5,url_eje, 0) # error 
    
def transformar(lista):
    diccionario ={}
    for letra, numero in lista:
      diccionario[letra] = numero
    return diccionario

def diagramador(jobs, rels, delegados, monitoreo = False, ODATE=20221116, format="pdf",
                     nombre = "Prueba", lista_jobs = []):
    
    if delegados != None:
        dash = lambda x:"shape=octagon" if delegados[x]==1 else ""
    elif len(lista_jobs) > 0:
        dash = lambda x:"shape=octagon" if x in lista_jobs else ""
    else:
        dash = lambda x:"" if type(x)==str else ""
    #Job recibe una tupla con diccionario (0) y tuplas (1)
    #diccionario_jobs= list(jobs.items())
    # Símbolos base.
    conexion = " -> "
    cuerpo = ""
    base_inicio =["strict digraph Ejemplo { \n  rankdir=lR \n splines = ortho \n	node [ fontname=Monospace shape=box style=" + '"'+"filled" +'"' +"]\n"]
    base_fin = "}"
      
    # Color.
    colores = {}
    # Distinción de mallas.
    mallas = list(set(jobs.values()))
    for i in range(len(mallas)):
        colores[mallas[i]] = ('#%06X' % randint(0, 0xFFFFFF))
    #Estatus  
    status_c = {0:"#EC7063", 1:'#AFE1AF', 2:"#BFC9CA", 3:"#F9E79F", 4:"#FFFFFF", 5:"#2471A3"}
    
        #==========================PRUEBA============================
    for key in list(jobs.keys()):
        if monitoreo:
            stat = status_job(key, ODATE)
            key_s = key +" - "+str(stat[2]) if stat[2]  > 1 else key
            #####
            generador = cuerpo + ' {}[label = "{}", color = "{}"URL="{}"penwidth = 5, fillcolor="{}" {}]\n'.format(key, key_s, colores[jobs[key]], stat[1], status_c[stat[0]], dash(key))
            #####
        else:#establecer marcadores para no monitoreo
            # generador = cuerpo + "  " + key + "[color=" + '"'+colores[jobs[key]]+ '"' + "URL=" + '"'+'https://www.google.com.mx'+ '"' + "penwidth = 5 "   +"]\n"
            generador = cuerpo + ' {}[color = "{}"URL="www.google.com"penwidth = 5, fillcolor="{}"{}]\n'.format(key, colores[jobs[key]], colores[jobs[key]]+"70",dash(key))
        # Es aqui Ro.
        base_inicio.append(generador)
      #==========================PRUEBA============================
    for dato in rels:
        generador = "  " + dato[0] + conexion + dato[1]+ "\n"
        base_inicio.append(generador)
      
     #---------------------------------------------------------------------------------------------------------------------------------------------------------
        #-------------------------------------------------                    INICIO                            -----------------------------------------------------
        #---------------------------------------------------     Generación de código de solor estatus     -----------------------------------------------------------
        #---------------------------------------------------------------------------------------------------------------------------------------------------------
    base_legenda_i = "\n  newrank=true\n  subgraph clusterLegend {\n  rank = sink\n  label = "+ '"' +"Código de estatus"+ '"' +"\n  fontsize = 20\n  fontname=Monospace\n  node [ color="+ '"' +"white"+ '"' +" ]\n  {rank=same; key; key2}\n  key [ label=<<table border="+ '"' +"0"+ '"' + " cellpadding="+ '"' +"2"+ '"' + " cellspacing="+ '"' +"0" + '"' + " cellborder="+ '"' +"0"+ '"' +">"
    termino_tabla_c  = "\n  </table>> ]"
    label = "\n  key2 [ label=<<table border="+ '"' +"0"+ '"' + " cellpadding="+ '"' +"2"+ '"' +" cellspacing="+ '"' +"0"+ '"' +" cellborder="+ '"' +"0"+ '"' +">"
    termino_tabla_l = "\n  </table>>]\n"
    base_legenda_f = "}\n  {rank=same;key;key2;}\n "
    #Colores para leyenda.
    num_mallas = len(colores.keys())+ 6 if monitoreo else len(colores.keys())# 6 es el número de los colores base que contemplamos para el estatus del semáforo.
    r = 6 if monitoreo else 0
    
    base_inicio.append(base_legenda_i)
    
    for dato in range(num_mallas):
        color_semaforo=["red","green","gray","yellow","#ffffff","blue"]
        if dato <=5 and monitoreo:
            generador = "\n  <tr><td align="+ '"' +"right" + '"' +"  port="+ '"' +"i" +str(dato+1)+ '"' +"  bgcolor="+ '"' + color_semaforo[dato] + '"' +">  </td></tr>"
            base_inicio.append(generador)
        else:
            color_malla = list(colores.values())
            generador = "\n  <tr><td align="+ '"' +"right" + '"' +"  port="+ '"' +"i" +str(dato+1)+ '"' +"  bgcolor="+ '"' + color_malla[dato - r] + '"' +">  </td></tr>"
            base_inicio.append(generador)
    base_inicio.append(termino_tabla_c)
    base_inicio.append(label)
    
    for dato in range(num_mallas):
        estatus_semaforo=["Ejecuto NotOK","Ejecuto Ok","Pendiente por ejecutar","Ejecutando","No tiene por que ejecutar","Error"]
        if dato <=5 and monitoreo:
            generador = "\n  <tr><td align="+ '"' +"left"+ '"' +"  port="+ '"' +"i" +str(dato+1)+ '"' +">"+ estatus_semaforo[dato] +"</td></tr>"
            base_inicio.append(generador)
        else:
            nombre_malla = list(colores.keys())
            generador = "\n  <tr><td align="+ '"' +"left"+ '"' +"  port="+ '"' +"i" +str(dato+1)+ '"' +">"+nombre_malla[dato - r]+"</td></tr>"
            base_inicio.append(generador)
        
    base_inicio.append(termino_tabla_l)
    
    for dato in range(num_mallas):
        generador = "\n  key:i" +str(dato+1)+ " -> key2:i"+str(dato+1)+ " [style=invis ]"
        base_inicio.append(generador)
    
    base_inicio.append(base_legenda_f)
        #---------------------------------------------------------------------------------------------------------------------------------------------------------
        #-------------------------------------------------                            FIN        -----------------------------------------------------------------
        #---------------------------------------------------------------------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------------------------------------------------------------------  
      
    base_inicio.append(base_fin)
    texto_gv  =str(''.join(base_inicio))
    textfile = open('Job_Malla.gv', 'w')
    textfile.write(texto_gv)
    textfile.close()
    from graphviz import Source
    src = Source.from_file("Job_Malla.gv", encoding="latin-1")
    src.format = format
    src.view(nombre+"."+format, cleanup=True)
    return src

class DiagramadordeMallas:
    """
    Este objeto contiene diversos métodos y atributos que funcionan a través
    del web scrapping de scheduling.
    
    METODOS PRINCIPALES:
        +getMeshDet: Obtiene la relación entre los jobs de una malla.
            -Input: String con el nombre de la malla a buscar.
            -Output: Un diccionario con los jobs como keys y el nombre de la 
            malla como value, y una lista de tuplas con las relaciones entre 
            jobs.
            
        +getMeshesDet: Obtiene la relación entre los jobs de varias mallas.
            -Input: Lista con los nombres de las malla a buscar.
            -Output: Un diccionario con los jobs como keys y el nombre de la 
            malla como value, y una lista de tuplas con las relaciones entre 
            jobs.
                
        +diagramadoMallaNX: Genera la visualización de la o las mallas con networkX.
            -Input: Diccionario generado por getMeshDet o getMeshesDet,
                lista generada por getMeshDet o getMeshesDet,
                "format" con el formato con el que se guardará el archivo 
                (svg por defecto) y "filename" con el nombre con el que se 
                guardará el archivo (por defecto es Mallas).
            -Output: Archivo y visualización con el diagrama 
            (con la extensión seleccionada en format)
            
    ATRIBUTOS:
        +jobs: Diccionario con el nombre de los jobs como keys y el nombre de
        la malla a la que pertenece como value.
        +rels: Lista de tuplas con la relación entre jobs.
        +gnx: Objeto de NetworkX con los jobs como nodos y rels como edges
        +posnx: Posisión como x,y de cada nodo en la gráfica de matplotlib
    """
    
    def __init__(self):
        self.jobs = {}
        self.rels = []
        self.delegados = None
        self.gnx = 0
        self.posnx = 0
        
    def getMeshName(self, jobName):
        url = 'http://150.100.216.64:8080/scheduling/planificacionesConsulta'
        dat = 'jobname='+jobName+'&tablename=&memname=&condicion=&nodo=&owner=&memlib=&aplicacion=&grupo=&descripcion=&calendario=&forzado=&tasktype=&ciclico=&recursoq=&apxdaasjob='
        headers = {
                        'Host': '150.100.216.64:8080',
                        'Connection': 'keep-alive',
                        'Content-Length': '164',
                        'Accept': 'text/html, */*; q=0.01',
                        'X-Requested-With': 'XMLHttpRequest',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'http://150.100.216.64:8080',
                        'Referer': 'http://150.100.216.64:8080/scheduling/planificaciones',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'es-US,es-419;q=0.9,es;q=0.8'
                  }
        
        try:
            page = requests.post(url, headers = headers, data = dat)
            soup = BeautifulSoup(page.text, 'html.parser')
            meshName = soup.find_all('td',{'data-title':'Folder'})
            return meshName[0].string
        except:
            print('No pude acceder a la pagina para checar esta malla:',meshName)
        
    def getMeshDet(self, meshName, dicNodes = {}):
        """
        Webscrapping de scheduling, con lo que se obtienen los jobs y sus relaciones.
        Input:
            +meshName: Nombre de la malla como string
        Output:
            +dicNodes: Diccionario con jobs y su malla perteneciente
            +arrEdges: Lista con las relaciones entre jobs.
        """
        print(meshName)
        url = 'http://150.100.216.64:8080/scheduling/planificacionesConsulta'
        dat = 'jobname=&tablename='+meshName+'&memname=&condicion=&nodo=&owner=&memlib=&aplicacion=&grupo=&descripcion=&calendario=&forzado=&tasktype=&ciclico=&recursoq=&apxdaasjob='
        headers = {
                        'Host': '150.100.216.64:8080',
                        'Connection': 'keep-alive',
                        'Content-Length': '164',
                        'Accept': 'text/html, */*; q=0.01',
                        'X-Requested-With': 'XMLHttpRequest',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'http://150.100.216.64:8080',
                        'Referer': 'http://150.100.216.64:8080/scheduling/planificaciones',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'es-US,es-419;q=0.9,es;q=0.8'
                  }
        
        try:
            page = requests.post(url, headers = headers, data = dat)
            soup = BeautifulSoup(page.text, 'html.parser')
            condicionesCompletas = soup.find_all('td',{'data-title':'Condicion'})
                    
            tuplasCond = []
            
            visited = set()
            inconds = [x for x in condicionesCompletas if x in visited or (visited.add(x) or False)]
            outconds = [x for x in condicionesCompletas if x not in inconds]
            fullconds = inconds + outconds
    
            for condicionIndividual in fullconds:
                condicionSinSeparar = condicionIndividual.string
                condicionSeparada = condicionSinSeparar.split('-TO-')
                if len(condicionSeparada) == 2:
                    tupla = (condicionSeparada[0],condicionSeparada[1],meshName)
                    tuplasCond.append(tupla)
            
            #Se identifica si el job pertenece a la misma UUAA de la malla, se valida tanto 
            #si se trata de una UUAA local o global, si la UUAA del job y la malla es la misma
            #se añade al diccionario la Key = NombreJob con Value = NombreMalla, si las UUAA son
            #distintas, se obtiene el nombre de la malla a la que pertenece le job y se añade al 
            #diccionario
            for tup in tuplasCond:
                if tup[0] not in dicNodes and (tup[0][1:5] == tup[2][5:9] or tup[0][1:4] == tup[2][5:8]):
                    dicNodes[tup[0]] = tup[2]
                elif tup[0] not in dicNodes and (tup[0][1:5] != tup[2][5:9] and tup[0][1:4] != tup[2][5:8]):
                    dicNodes[tup[0]] = self.getMeshName(tup[0])
                    
                if tup[1] not in dicNodes and (tup[1][1:5] == tup[2][5:9] or tup[1][1:4] == tup[2][5:8]):
                    dicNodes[tup[1]] = tup[2]
                elif tup[1] not in dicNodes and (tup[1][1:5] != tup[2][5:9] and tup[1][1:4] != tup[2][5:8]):
                    dicNodes[tup[1]] = self.getMeshName(tup[1])
                
            arrEdges = []    
            for tup in tuplasCond:
                if (tup[0],tup[1]) not in arrEdges and (tup[0] != tup[1]):
                    arrEdges.append((tup[0],tup[1]))
            
            #self.jobs = dicNodes
            #self.rels = arrEdges
            return[dicNodes,arrEdges]         
        except Exception as e:
            print("Ha ocurrido un error ", e)
            print('No pude acceder a la pagina para checar esta malla:',meshName)                                                                                                                                                          
            
    def getMeshesDet(self, meshesName):
        """
        Método para obtener jobs y relaciones entre varias mallas
        Input:
            +meshesName: Lista del nombre de las mallas como string
        Output:
            +dicNodes: Diccionario con jobs y su malla perteneciente
            +arrEdges: Lista con las relaciones entre jobs.
        """
        dicNodes = {}
        self.jobs = dicNodes
        arrEdges = []
        for mesh in meshesName:
            meshDet = self.getMeshDet(mesh)
            dicNodes.update(meshDet[0])
            arrEdges = arrEdges + meshDet[1]
            
        self.jobs = dicNodes
        self.rels = arrEdges
        return (dicNodes,arrEdges)
    
    def diagramadoMallaNX(self, jobs=None, rels=None, delegados = None, monitoreo = False, ODATE=20221116, 
                          figsize=(16,16), font_size=3.3,
                          node_size=600, node_shape="s", file_name="Test.svg",
                          form="svg"):
        """
        Método para diagramar la malla con NetworkX, también cuenta con la función
        de monitoreo de ejecución.
        Input:
            +jobs: Diccionario de los jobs de la malla que se desea diagramar.
            +rels: Relación entre los jobs.
            +monitoreo: Booleano (False por defecto) que permite habilitar
            la monitorización de jobs
            +ODATE: Si monitorización está activa, se requiere el ODATE del día
            que se quiere monitorear
            +figsize: Tupla de números para moldear el tamaño del diagrama 
            (por defecto(16,16))
            +font_size: Tamaño de las etiquetas de los nodos (por defecto 3.3)
            +node_shape: Forma de los nodos, acepta los marcadores de matplotlib 
            (por defecto "s")
            +file_name: Nombre del archivo que se guardará (por defecto "Test.svg")
            +form: Formato con el que se guarda el diagrama (por defecto "svg")
            
        Output:
            G: Objeto de NetworkX con el diagrama, sus respectivos nodos y 
            conexiones.
            
            Diagrama guardado en el formato dado en la misma ruta que el 
            script, además de el diagrama en el notebook.
        
        Colores:
            rojo - Ejecuto NotOK
            verde - Ejecuto Ok
            gris - Pendiente por ejecutar
            amarillo - Ejecutando
            blanco - No tiene por que ejecutar (Es decir, no está cargado en el activo) 
            azul - Error
        """
        if jobs == None:
            jobs = self.jobs
        if rels == None:
            rels = self.rels
        plt.figure(figsize=figsize, dpi = 500)
        
        mallas = list(set(jobs.values())) #color
        colores = {} #color
        for i in range(len(mallas)): #color
            colores[mallas[i]] = ('#%06X' % randint(0, 0xFFFFFF)) #color
            plt.plot(0, 0, marker="s", c = colores[mallas[i]], label = mallas[i])
            
        edge_color = [colores[i] for i in list(jobs.values())]
        
        G = nx.DiGraph()
        #======================================
        #G.add_nodes_from(list(jobs.keys()))
        for k in list(jobs.keys()):
            G.add_node(k, malla = jobs[k])
        
        G.add_edges_from(rels)
        for x in list(G.nodes()):
            if len(G.nodes.data()[x]) != 1:
                G.remove_node(x)
        #=======================================
        if monitoreo:
            colors = {0:"red", 1:"lightgreen", 2:"grey", 3:"yellow", 4:"white", 5:"aqua"}
            status = {0:"Not OK", 1:"OK",2:"Pendiente", 3:"Ejecutando", 4:"No tiene que ejecutar", 5:"ERROR"}
            node_color = [colors[status_job(m, ODATE)[0]] for m in list(G.nodes)]
            for c in list(colors.keys()):
                plt.plot(0,0, marker=".", c = colors[c], label = status[c])
        else:
            node_color="#ffffff"
        
        pos = nx.nx_agraph.pygraphviz_layout(G, prog='dot')
        self.posnx = pos
        
        nx.draw_networkx_labels(G,pos, font_size=font_size)
        
        nx.draw_networkx_nodes(G,pos,node_size=node_size, node_color=node_color,
                               node_shape=node_shape,
                               alpha=0.7, edgecolors = edge_color, linewidths=2.5)
        nx.draw_networkx_edges(G,pos, alpha=1, node_size=node_size,
                               node_shape=node_shape, connectionstyle="arc3")#angle
        
        plt.legend()
        plt.savefig(file_name, format=form)
        plt.show()
        self.gnx = G
        return G
    
    def diagramadorMalla(self, jobs = None, rels = None,delegados = None, monitoreo = False, ODATE=20221116,
                         format="pdf", nombre = "Prueba", lista_jobs = []):
        if jobs == None:
            jobs = self.jobs
        if rels == None:
            rels = self.rels
        if delegados == None:
            delegados = self.delegados
        return diagramador(jobs, rels, delegados, monitoreo=monitoreo, ODATE=ODATE, format=format, nombre = nombre,
                           lista_jobs=lista_jobs)

class DiagramadorDescendente:
    
    def __init__(self):
        self.jobs = {}
        self.rels = []
        self.delegados = None
        self.gnx = 0
        self.posnx = 0
        self.urls = []
        
    def jobsDescendentes(self, jobSolicitado):
        url = 'http://150.100.216.64:8080/scheduling/planificacionesConsulta'
        dat = 'jobname='+jobSolicitado+'&tablename=&memname=&condicion=&nodo=&owner=&memlib=&aplicacion=&grupo=&descripcion=&calendario=&forzado=&tasktype=&ciclico=&recursoq=&apxdaasjob='
    
        headers = {
                        'Host': '150.100.216.64:8080',
                        'Connection': 'keep-alive',
                        'Content-Length': '164',
                        'Accept': 'text/html, */*; q=0.01',
                        'X-Requested-With': 'XMLHttpRequest',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'http://150.100.216.64:8080',
                        'Referer': 'http://150.100.216.64:8080/scheduling/planificaciones',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'es-US,es-419;q=0.9,es;q=0.8'
                  }
        # Código para generar las tuplas
        try:
            page = requests.post(url, headers = headers, data = dat)  # Request
            soup = BeautifulSoup(page.text, 'html.parser')            # Parsear el HTML Response
            condicionesCompletas = soup.find_all(attrs={"data-title": "Condicion"})  # Las tablas con las condiciones tienen el id="tablesorter2", entonces las buscamos
            meshName = ''
            if len(soup.find_all('td',{'data-title':'Folder'})) > 0:
                meshName = soup.find_all('td',{'data-title':'Folder'})[0].string
    
            condicionesSeparadas = []
            tuplasOutcond = []
            
            visited = set()
            inconds = [x for x in condicionesCompletas if x in visited or (visited.add(x) or False)]
            outconds = [x for x in condicionesCompletas if x not in inconds]
            for condicionIndividual in outconds:
                condicionSinSeparar = condicionIndividual.string
                condicionSeparada = condicionSinSeparar.split('-TO-')
                for condicion in condicionSeparada:
                    if condicion != jobSolicitado:
                        condicionesSeparadas.append(condicion)        
            for condicionOut in condicionesSeparadas:
                tupla = (jobSolicitado,condicionOut,meshName)
                tuplasOutcond.append(tupla)
            if len(outconds) == 0:
                tupla = (jobSolicitado,jobSolicitado,meshName)
                tuplasOutcond.append(tupla)
            
            return tuplasOutcond
            
        except:
            print('No se pueden generar los jobs precedentes')
            
    def jobsDescendentesRecursivo(self, jobPrincipal):
        tuplasDefinitivas = []
        tuplas = self.jobsDescendentes(jobPrincipal)
        for tuplaInicial in tuplas:
            tuplasDefinitivas.append(tuplaInicial)
    
        for tuplaIncond in tuplasDefinitivas:
            tuplasNuevas = self.jobsDescendentes(tuplaIncond[1])
            for tupla in tuplasNuevas:
                if tupla not in tuplasDefinitivas:
                    tuplasDefinitivas.append(tupla)   
        
        dicNodes = {tup[0]:tup[2] for tup in tuplasDefinitivas}
        arrEdges = []    
        for tup in tuplasDefinitivas:
            if (tup[0],tup[1]) not in arrEdges and (tup[0] != tup[1]):
                arrEdges.append((tup[0],tup[1]))
        
        self.jobs = dicNodes
        self.rels = arrEdges
        return (dicNodes,arrEdges)
    
    def diagramadoDescNX(self, jobs = None , rels = None, monitoreo = False, ODATE=20221116,
                         figsize=(16,16), font_size=3.3,
                          node_size=600, node_shape="s", file_name="Test.svg",
                          form="svg"):
        if jobs == None:
            jobs = self.jobs
        if rels == None:
            rels = self.rels
        
        plt.figure(figsize=figsize)
        
        mallas = list(set(jobs.values())) #color
        colores = {} #color
        for i in range(len(mallas)): #color
            colores[mallas[i]] = ('#%06X' % randint(0, 0xFFFFFF)) #color
            plt.plot(0, 0, marker="s", c = colores[mallas[i]], label = mallas[i])
            
        edge_color = [colores[i] for i in list(jobs.values())]
        
        G = nx.DiGraph()
        #======================================
        G.add_nodes_from(list(jobs.keys()))
        G.add_edges_from(rels)
        #=======================================
        if monitoreo:
            colors = {0:"red", 1:"lightgreen", 2:"grey", 3:"yellow", 4:"white", 5:"aqua"}
            status = {0:"Not OK", 1:"OK",2:"Pendiente", 3:"Ejecutando", 4:"No tiene que ejecutar", 5:"ERROR"}
            node_color = [colors[status_job(m, ODATE)[0]] for m in list(G.nodes)]
            for c in list(colors.keys()):
                plt.plot(0,0, marker=".", c = colors[c], label = status[c])
        else:
            node_color="#ffffff"
        
        pos = nx.nx_agraph.pygraphviz_layout(G, prog='dot')
        self.posnx = pos
        
        nx.draw_networkx_labels(G,pos, font_size=font_size)
        
        nx.draw_networkx_nodes(G,pos,node_size=node_size, node_color=node_color,
                               node_shape=node_shape,
                               alpha=0.7, edgecolors = edge_color, linewidths=2.5)
        nx.draw_networkx_edges(G,pos, alpha=1, node_size=node_size+100,
                               node_shape=node_shape)
        #=======================================
        #for i in range(num_mallas):
        #    plt.plot(0, 0, marker="s", c = colores[i], label = [*diccionario.keys()][i])
        #=======================================
        plt.legend()
        plt.savefig(file_name, format=form)
        plt.show()
        self.gnx = G
        return G
    
    def diagramadorDesc(self, jobs = None, rels = None,delegados = None, monitoreo = False, ODATE=20221116,
                         format="pdf", nombre = "Prueba", lista_jobs = []):
        if jobs == None:
            jobs = self.jobs
        if rels == None:
            rels = self.rels
        if delegados == None:
            delegados = self.delegados
        return diagramador(jobs, rels, delegados, monitoreo=monitoreo, ODATE=ODATE, format=format, nombre = nombre,
                           lista_jobs=lista_jobs)
    
class DiagramadorAscendente:
    def __init__(self):
        self.jobs = {}
        self.rels = []
        self.delegados = None
        self.gnx = 0
        self.posnx = 0
        
    def jobsAscendentes(self, jobSolicitado):
        # Constantes para hacer el request a Scheduling
        url = 'http://150.100.216.64:8080/scheduling/planificacionesConsulta'
        dat = 'jobname='+jobSolicitado+'&tablename=&memname=&condicion=&nodo=&owner=&memlib=&aplicacion=&grupo=&descripcion=&calendario=&forzado=&tasktype=&ciclico=&recursoq=&apxdaasjob='
    
        headers = {
                        'Host': '150.100.216.64:8080',
                        'Connection': 'keep-alive',
                        'Content-Length': '164',
                        'Accept': 'text/html, */*; q=0.01',
                        'X-Requested-With': 'XMLHttpRequest',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'http://150.100.216.64:8080',
                        'Referer': 'http://150.100.216.64:8080/scheduling/planificaciones',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'es-US,es-419;q=0.9,es;q=0.8'
                  }
        # Código para generar las tuplas
        try:
            page = requests.post(url, headers = headers, data = dat)  # Request
            soup = BeautifulSoup(page.text, 'html.parser')            # Parsear el HTML Response
            condicionesCompletas = soup.find_all(attrs={"data-title": "Condicion"})  # Las tablas con las condiciones tienen el id="tablesorter2", entonces las buscamos
            mallasPorJob = soup.find_all(attrs={"data-title": "Folder"})
            
            condicionesSeparadas = []
            tuplasIncond = []
            mallasArreglo = []
            
            visited = set()
            inconds = [x for x in condicionesCompletas if x in visited or (visited.add(x) or False)]
        
            if inconds == []:
                for condicionCompleta in condicionesCompletas:
                    junta = condicionCompleta.string
                    separada = junta.split('-TO-')
                    if len(separada) == 1:
                        condicionesSeparadas.append(separada[0])
            
            for condicionIndividual in inconds:
                condicionSinSeparar = condicionIndividual.string
                condicionSeparada = condicionSinSeparar.split('-TO-')
                for condicion in condicionSeparada:
                    if condicion != jobSolicitado:
                        condicionesSeparadas.append(condicion)
                        
            for condicionIn in condicionesSeparadas:
                tupla = (condicionIn, jobSolicitado)
                tuplasIncond.append(tupla)
                
            #mallaTupla = (jobSolicitado, mallasPorJob.string)
                
            for malla in mallasPorJob:
                #mallasArreglo.append(malla.string)
                mallaTupla = (jobSolicitado, malla.string)
                if mallaTupla not in mallasArreglo:
                    mallasArreglo.append(mallaTupla)
            
            return tuplasIncond, mallasArreglo
    
            
        except:
            print('No se pueden generar los jobs precedentes')
            
    def jobsAscendentesRecursivo(self, jobPrincipal):
        tuplasDefinitivas = []
        mallasDefinitivas = []
        
        tuplas, mallas = self.jobsAscendentes(jobPrincipal)
        for tuplaInicial in tuplas:
            tuplasDefinitivas.append(tuplaInicial)
        #for malla in mallas:
            #print(malla)
            #mallasDefinitivas.append(malla.string)
    
        for tuplaIncond in tuplasDefinitivas:
            tuplasNuevas, mallasAsc = self.jobsAscendentes(tuplaIncond[0])
            for tupla in tuplasNuevas:
                if tupla not in tuplasDefinitivas:
                    tuplasDefinitivas.append(tupla)
            for mallasAscInd in mallasAsc:
                if mallasAscInd not in mallasDefinitivas:
                    mallasDefinitivas.append(mallasAscInd)
                    
        self.jobs = transformar(mallasDefinitivas)
        self.rels = tuplasDefinitivas
        
        return self.jobs, self.rels
    
    def diagramadorAsc(self, jobs = None, rels = None,delegados = None, monitoreo = False, ODATE=20221116,
                         format="pdf", nombre = "Prueba", lista_jobs = []):
        if jobs == None:
            jobs = self.jobs
        if rels == None:
            rels = self.rels
        if delegados == None:
            delegados = self.delegados
        return diagramador(jobs, rels, delegados, monitoreo=monitoreo, ODATE=ODATE, format=format, nombre = nombre,
                           lista_jobs=lista_jobs)
