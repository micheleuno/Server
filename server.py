import socket
import re
import sys
import codecs
try:
    import urllib.request
except ImportError:
    import urllib2


print("Servidor HTTP Iniciado")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 9100))
s.listen(1)

def ObtenerDirectorio2(str):
  pos1 = str.find(" /") 
  pos2 = str.find("HTTP")
  Directorio = str[pos1+1:pos2-1]
  return Directorio

def ObtenerDirectorio(str):
  pos1 = str.find(" /") 
  pos2 = str.find("HTTP")
  Directorio = str[pos1+1:pos2-1]  
  #
  if sys.version_info < (2, 8): #Segun la version de python
    Directorio =  urllib2.unquote(Directorio) #Encodear en caso de espacios
    Directorio = Directorio.decode('latin-1') #y cosas raras (python menor a 3)
    Directorio = Directorio.encode('utf-8')     
  else:
    Directorio =  urllib.request.unquote(Directorio)
  return Directorio;

def ObtenerProtocolo(str):
  pos1 = str.find("HTTP") 
  pos2 = str.find("\r")
  Protocolo = str[pos1:pos2]
  protocolo = SacarTexto(Protocolo)
  return Protocolo;

def ObtenerMetodo(str): 
  pos2 = str.find("/")
  Metodo = str[0:pos2-1]
  Metodo = SacarTexto(Metodo)
  return Metodo;

def ObtenerHost(str):
  pos1 = str.find("Host:") 
  pos2 = str.find("Accept")
  Host = str[pos1+6:pos2]
  Host = SacarTexto(Host)
  return Host;

def ObtenerIdioma(str):
  pos1 = str.find("age:") 
  pos2 = str.find("Con") 
  Idioma = str[pos1+5:pos2-1]
  Idioma = Idioma[0:pos2-1]
  Idioma = Idioma.replace("\r", "")
  Idioma = SacarTexto(Idioma)
  return Idioma;

def ObtenerAceptado(str):
  pos1 = str.find("Accept:") 
  pos2 = str.find(";q")
  Aceptado = str[pos1+8:pos2]
  Aceptado = SacarTexto(Aceptado)
  return Aceptado;

def SacarTexto(str): #Sacar posibles retunrs y saltos de linea
  str = str.replace("\r", "")
  str = str.replace("\n", "")
  return str

def CrearJSON(protocolo,metodo,host,idioma,aceptado,path):
  JSON =('X-RequestEcho: {"path": "'+path+'", "protocol": "'+protocolo
    +'", "method": "'+metodo +'", "headers": {"Accept": "'+aceptado
    +'", "Accept-Language": "'+idioma+'", "Host": "'+host+'"}'+'}')
  return JSON

while True:
  client_connection, client_address = s.accept()
  request = client_connection.recv(1024) #obtener request
  mensaje = request.decode('utf-8') #Codificar a String
  path=ObtenerDirectorio(mensaje)
  Directorio =(ObtenerDirectorio2(mensaje))
  Protocolo = (ObtenerProtocolo(mensaje))
  Metodo = (ObtenerMetodo(mensaje))
  Host = (ObtenerHost(mensaje))
  Idioma = (ObtenerIdioma(mensaje))
  Aceptado = (ObtenerAceptado(mensaje))
  JSON = CrearJSON(Protocolo,Metodo,Host,Idioma,Aceptado,Directorio)
  try:
    file_object = open("documentRoot/"+path, "r") 
    message =("HTTP/1.1 200 OK\n"
       +JSON+"\n"
       +"\n" 
       +file_object.read()+"\n");
  except IOError:
    message = ("HTTP/1.1 404 NOT FOUND\n"
       +JSON)   
  client_connection.sendall(message.encode('utf-8'))
  client_connection.close() 