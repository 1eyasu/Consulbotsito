#Colors :D
#f2f4ff PRIMER PLANO
#a9d3ff OBJETOS
#96c5f7 FONDO DE OBJETOS
#93acb5 FRAMES
#6c756b FORMULARIO
import requests
from requests.auth import HTTPBasicAuth
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import Toplevel, StringVar, messagebox
import os
from email.mime.base import MIMEBase
from email import encoders
import glob
import time
from datetime import datetime, timedelta
import asyncio
import psutil
import dropbox
import webbrowser
import shutil
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading

def Cerrar(myForm):
    myForm.destroy()

def crear_icono():
    # Crear el ícono
    icon_image = Image.open(currentWorkingDirectory+r'\consulbotsito.ico')
    draw = ImageDraw.Draw(icon_image)
    draw.rectangle((0, 0, 64, 64), fill=(70, 162, 175))  # Color personalizado
    draw.text((10, 25), "App", fill="white")  # Texto en el ícono

    def mostrar_ventana():
        root.deiconify()  # Restaurar la ventana

    def salir_programa():
        icon.stop()  # Detener el ícono
        root.destroy()  # Cerrar la ventana principal

    # Menú del ícono
    menu = Menu(
        MenuItem('Mostrar ventana', mostrar_ventana),
        MenuItem('Salir', salir_programa)
    )

    # Crear el ícono y asociar el menú
    icon = Icon('App', icon_image, menu=menu)
    icon.run()
my_counter = 0
calculo_ancho = 0
calculo_alto = 0
calculo_fuente = 0
version_app = 0.5
#Metodo para acceder a URLS
def acceder_url(opcion):
    if opcion == 1:
        try:
            # Abrir la URL en el navegador predeterminado
            webbrowser.open('https://www.dropbox.com/developers')
            print(f"Se ha abierto la URL: https://www.dropbox.com/developers")
        except Exception as e:
            print(f"Error al abrir la URL: {str(e)}")
    elif opcion == 2:
        try:
            # Abrir la URL en el navegador predeterminado
            client_id = etrDropbox1.get()
            
            webbrowser.open('https://www.dropbox.com/oauth2/authorize?client_id=' + client_id +'&token_access_type=offline&response_type=code')
            print(f"Se ha abierto la URL: 'https://www.dropbox.com/oauth2/authorize?client_id={client_id}&token_access_type=offline&response_type=code'")
        except Exception as e:
            print(f"Error al abrir la URL: {str(e)}")
#Metodo para obtener token de acceso
def obtener_token_acceso():
    try:
        CLIENT_ID = etrDropbox1.get().strip()
        CLIENT_SECRET = etrDropbox2.get().strip()
        AUTHORIZATION_CODE  = etrDropbox3.get().strip()

        # Endpoint para obtener tokens
        url = "https://api.dropbox.com/oauth2/token"

        # Cuerpo de la solicitud
        data = {
            'code': AUTHORIZATION_CODE,
            'grant_type': 'authorization_code',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        # Enviar la solicitud POST
        respuesta = requests.post(url, data=data)

        # Manejar la respuesta
        if respuesta.status_code == 200:
            tokens = respuesta.json()
            #print("Access Token:", tokens['access_token'])
            #print("Refresh Token:", tokens['refresh_token'])        
            #print (respuesta.json().get('refresh_token'))
            #etrDropbox4.insert(0, respuesta.json().get('refresh_token'))
            string_token = f"{tokens['refresh_token']}"
            etrDropbox4.delete(0, tk.END)
            etrDropbox4.insert(0, string_token)
            #return respuesta.json().get('refresh_token')
            Estatus("Se ha generado el token, guarde y reinicie la app para aplicar")
            return tokens['refresh_token']

        else:
            print("Error:", respuesta.status_code, respuesta.text)
            Estatus("Error:", respuesta.status_code, respuesta.text)
            return None

    except Exception as e:
        Estatus("Error:" + str(e) + " Campos incorrectos/incompletos", False)
#metodo para renovar token de acceso
def renovar_access_token(refresh_token):    
    CLIENT_ID = etrDropbox1.get().strip()
    CLIENT_SECRET = etrDropbox2.get().strip()
    #CLIENT_ID = '0g9e8t8h4ptmgk6'
    #CLIENT_SECRET = 'fh31zsfp1tdg2sj'
    #refresh_token = 'qRpKT8mIPuIAAAAAAAAAAQjZVbr-1y8huS5Uyru5Woprbqh_PMYMLhKzNTQmJGBqsIMeFlzP5UMAAAAAAAAAASbCADFVBL0dzNfQELdjJCFGPpZunE1feJOBUZgWeX9hB9ZFsTv05nEAAAAAAAAAAUjthUbDR2l6n4_GcHmgEhy2cX9_ESwScIZTtBy8E8hOSSKmfNnZUE4AAAAAAAAAAavhpPusfsy_puMQY9MRYBJnKGrJ6_-yXKKNvSVK3QTosl.u.AFrJt4seSJ3RTe11_p8kTUDfUpsioKW2XKnKJOKdGZUoOoePJwD5RseKEI-5QjaIH7en8VISYJyxXSNRoC8rUy2xycIVZcqi5DjupQVgob4qCR-A_wvjqLLH1Wn763u8OeiYAkvWN_tGD9QaPb5rmDHdwuF7i5qhDRAvuDqFkvgw1NIvV8YABQi9hPwkROJ5gh1BIxvFJsj_uWzZ0PAuq0wvHmCCCo-oZIfiqanoZ_Lgl_st5cD0XrTeFNfnRAUisydDEJ6nQnRVNgqZcjWCFXAJf0YTwFt5SRETmq18PqRlerW-4q1eMInW1P7AEn6kceippPMeBiUR_4iSHHyhPU8Wso7dGPtMWSDMmMgQeG_4P7gUzvzHJbsVN_VdKd3RgE_yFh8HR5LbVhhsQsphLHpgFmIxkJjTOjzmABclqVHKtwnO7QPDp3vhKgau_2BiG6jJgnUtyfVKJcfHN43aTDAw4RgQZXQSylFIJzyQO9cFu1EzmWduQhy1GMfZurhlRJjZiyWDxGqJQezN7EpgyUV841G2FmbICvAyJb04_U-qkq2GAlFWqn2Tz0LvSwWhhV_Xl0lqTYL0TjLqqrzR_DAi2bZ32Jx6_TpYXpvtB_yhyEIsYRr1MrY_Gi7dutKkeQ5p0O5PMUy0uK7-H5Y__SFdnLWjuTXZv93QvjCK0J4iSgM8-wpbc8tphzOxJPVR62Tbu0kV3rUdki4FUaR_64CfjRzB8l8httRJBg5ShC7YWv2FZS1O-87lEXaNDFQHaElDVDkR0aDTujDkLSamqCfhCUVXA8j_n7OcT5yieMjuZ3wNAx_qqCIaTf9LNqg9trC4SvBbEUdzeogJdXcYRrI5bhvsAk8CnoWo0kmU1PRIFew-jh3cAXd0JUl8Tkez7k-5Oamxwb_rPU298Ujv3C3q_UaEunzBVPyRI9-56hq7YU9jbzvxnL0sClNM5eqUTHsikHtDvHMUj--a5s0tdkgBjsv34iuacyxa5aJsQtRDoo_Rl2t11b73izEY9azd0ZrN094fxk4j-zZeV75CsSs22xHAjLut0NEmw11DxQhoqBca38hGPqrv7zJ1jp3TIbtT5hx2SKHg3f3gnRTefnCzADNt24vsBONevBlAWMLccrRJ6X41e3rA_IqOdmA1NYG5eInsKCXSwahNk6qUAJfLnbfDVsBNKzePUKCrGD52mz4Ksxi3satLeJNzDMIbxr_FH9aAMBF9k0tS8aob7sF7-SJWMMxWJ4LkB5m6SM_VJ68sexNOXRZuFqflOwWL5gRhyEGheNk2y2lsDIH5U6iA'
    print(f"CLIENT_ID: {CLIENT_ID}, CLIENT_SECRET: {CLIENT_SECRET}")
    print(f"Refresh Token enviado: {refresh_token.strip()}")
    
    url = "https://api.dropbox.com/oauth2/token"

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token.strip()
    }

    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    respuesta = requests.post(url, data=data, auth=auth)

    if respuesta.status_code == 200:
        tokens = respuesta.json()
        access_token = tokens.get('access_token')
        print(f"Nuevo Access Token: {access_token}")
        return access_token
    else:
        print("Error al renovar el access token:", respuesta.status_code, respuesta.text)
        return None
#Metodo que usando el token de acceso obtiene el estado de el espacio usado y disponible de dropbox
def obtener_estado_dropbox(access_token):
    try:
        dbx = dropbox.Dropbox(access_token)

        # Consultar espacio disponible y utilizado
        cuenta = dbx.users_get_space_usage()
        usado = cuenta.used / (1024 ** 2)  # Convertir a MB
        total = cuenta.allocation.get_individual().allocated / (1024 ** 2)  # Convertir a MB

        print(f"Espacio usado: {usado:.2f} MB\nEspacio total: {total:.2f} MB")
        return f"Espacio usado: {usado:.2f} MB\nEspacio total: {total:.2f} MB"
        
    except dropbox.exceptions.AuthError:
        print("Error: el token es inválido o ha caducado.")
        return "Error de autenticación con Dropbox."
    except Exception as e:
        print("Error específico:", str(e))
        return f"Error al consultar Dropbox: {str(e)}"
#Metodo para verificar servicios en ejecucion a traves de los procesos
def verificar_servicios(servicios):
    servicios_en_ejecucion = []
    servicios_no_encontrados = []

    for servicio in servicios:
        servicio_encontrado = False
        for proceso in psutil.process_iter(['name']):
            if proceso.info['name'].lower() == servicio.lower():
                servicios_en_ejecucion.append(servicio)
                servicio_encontrado = True
                break
        if not servicio_encontrado:
            servicios_no_encontrados.append(servicio)

    return servicios_en_ejecucion, servicios_no_encontrados
#metodo para buscar logs existentens en una lista
def logSearcher(lista_rutas, extension):
    archivos_encontrados = []  # Lista para almacenar las rutas de los archivos encontrados

    for ruta in lista_rutas:
        # Usar glob para buscar archivos con la extensión especificada dentro de cada directorio
        patron = os.path.join(ruta, f"*.{extension}")
        archivos = glob.glob(patron)  # Esto devuelve una lista de archivos que coinciden
        archivos_encontrados.extend(archivos)  # Agregar los archivos encontrados a la lista principal
    #print("tarea ejecutada")
    return archivos_encontrados
#Metodo para cortar los logs encontrados en una carpeta de respaldo
def copiar_archivos_carpetas_logs(rutas, destino_base):
    try:
        # Asegurarse de que la carpeta destino "Respaldo logs" exista
        carpeta_respaldo = os.path.join(destino_base, "Backup Logs")
        os.makedirs(carpeta_respaldo, exist_ok=True)

        for ruta_carpeta in rutas:
            # Verificar si la ruta es una carpeta válida
            if os.path.isdir(ruta_carpeta):
                # Buscar todos los archivos .log en la carpeta dada
                for archivo in os.listdir(ruta_carpeta):
                    ruta_archivo = os.path.join(ruta_carpeta, archivo)
                    
                    # Verificar si es un archivo .log
                    if os.path.isfile(ruta_archivo) and archivo.lower().endswith('.log'):
                        # Crear subcarpeta correspondiente en "Respaldo logs"
                        carpeta_origen = os.path.basename(ruta_carpeta)
                        carpeta_destino = os.path.join(carpeta_respaldo, carpeta_origen)
                        os.makedirs(carpeta_destino, exist_ok=True)

                        # Mover el archivo al destino
                        archivo_destino = os.path.join(carpeta_destino, archivo)
                        shutil.move(ruta_archivo, archivo_destino)
                        print(f"Archivo movido: {ruta_archivo} -> {archivo_destino}")
            else:
                Estatus(f"La ruta no es una carpeta válida: {ruta_carpeta}")
                print(f"La ruta no es una carpeta válida: {ruta_carpeta}")

        print("Operación completada.")
    except Exception as e:
        Estatus(f"Ocurrió un error: {str(e)}")
        print(f"Ocurrió un error: {str(e)}")
#Metodo para leer el archivo de configuracion
def leer_archivo(ruta):
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        return contenido
    except FileNotFoundError:
        Estatus("Error: El archivo en la ruta '{ruta}' no existe.")
        print(f"Error: El archivo en la ruta '{ruta}' no existe.")
    except IOError:
        Estatus("Error: No se pudo leer el archivo en la ruta '{ruta}'.")
        print(f"Error: No se pudo leer el archivo en la ruta '{ruta}'.")
#Metodo para envio de email con toda la informacion
def SendMessage(semail, remail, password, attachments, asuntoCorreo, servidorCorreo, puerto, listaAdtg):
    #global rutas_resultado
    # Sender and receiver information
    sender_email = semail
    receiver_emails = remail  # List of recipients
    password = password
    emailmesagge = ""
    if var_check_hora.get() == 1:
        asuntoCorreo = asuntoCorreo + " " + str(datetime.now())
    if etrDropbox4.get() != "":
        datos_de_dropbox = str(obtener_estado_dropbox(renovar_access_token(str(etrDropbox4.get()))))
    else:
        lblEstatus.configure(text="Error registre datos de dropbox nuevamente")
        return
    # Create the email message
    message = MIMEMultipart()
    message["Subject"] = asuntoCorreo
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_emails)  # Join the list of emails
    texto_ADTG = ""
    for item in listaAdtg:
        texto_ADTG = texto_ADTG + "\n " + item 
    #for i in attachments:
    #   emailmesagge = emailmesagge + "\n" + attachments[i] +  leer_archivo(attachments[i])
    en_ejecucion, no_encontrados = verificar_servicios([lbServicios.get(i) for i in range(lbServicios.size())])
    if no_encontrados == "":
        no_encontrados = "Ninguno"
    if attachments != "":
        for archivo in attachments:
            emailmesagge += f"\n{archivo}\n{leer_archivo(archivo)}\n"
    else:
        emailmesagge = "Ninguno"
    # Create the plain-text and HTML version of your message
    text = f"=====================================\n=====================================\nLog de agentes encontrados:\n=====================================\n=====================================\n{emailmesagge}\n=====================================\n=====================================\nServicios en ejecucion:=====================================\n=====================================\n{en_ejecucion}\n=====================================\n=====================================\nServicios fuera de funcionamiento:=====================================\n=====================================\n{no_encontrados}\n=====================================\n=====================================\nInformacion dropbox:=====================================\n=====================================\n{datos_de_dropbox}\n=====================================\n=====================================\nADTG encontrados:=====================================\n=====================================\n{texto_ADTG}"
    html = f"""\
    <html>
    <body>
        <p>{emailmesagge}</p>        
        <p>Servicios en ejecucion:{en_ejecucion}</p>
        <p>Servicios no encontrados:{no_encontrados}</p>
    </body>
    </html>
    """
    # Attach the plain-text and HTML parts
    part1 = MIMEText(text, "plain")
    #part2 = MIMEText(html, "html")
    message.attach(part1)
    #message.attach(part2)
    # Attach files
    attachments = attachments  # List of files to attach
    for file in attachments:
        try:
            with open(file, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={file}",
            )
            message.attach(part)
        except FileNotFoundError:
            Estatus("Attachment {file} not found. Skipping.")
            print(f"Attachment {file} not found. Skipping.")

    # Send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(servidorCorreo, puerto, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_emails, message.as_string())
    contenido = list(lbRutas.get(0, tk.END))
    copiar_archivos_carpetas_logs(contenido, etrrutas2.get())
#Metodo para guardar todo en archivo de configuracion
def saveData():
    global var_check_hora
    email = etrCorreo.get()
    passw = etrContraseña.get()
    timet = etrhora.get()
    Rutas = [lbRutas.get(i) for i in range(lbRutas.size())]
    Destinatarios = [lbdestinatarios.get(i) for i in range(lbdestinatarios.size())]
    servidorCorreo = etrServidorCorreo.get() 
    puertoCorreo = etrPuerto.get()
    asuntoCorreo = etrAsunto.get()
    Servicios = [lbServicios.get(i) for i in range(lbServicios.size())]
    app_key = etrDropbox1.get()
    secret_key = etrDropbox2.get()
    refresh_token = etrDropbox4.get()
    ruta_backup = etrrutas2.get()
    if var_check_hora.get() == 1:
        checkHora = 1
    else:
        checkHora = 0
    if email and passw and timet and Rutas and Destinatarios and servidorCorreo and puertoCorreo and Servicios and asuntoCorreo and Servicios and ruta_backup:    
        if app_key or secret_key or refresh_token:
            if app_key and secret_key and refresh_token:
                # Save the data to a text file
                with open("form_data.txt", "w") as file:
                    file.write(f"Email: {email}\npassw: {passw}\ntimet: {timet}\nRutas: {Rutas} \nDestinatarios: {Destinatarios} \nServidor de Correo: {servidorCorreo}\nPuerto: {puertoCorreo}\nServicios: {Servicios}\nAsunto: {asuntoCorreo}\nHoraMarcada: {checkHora}\nApp_Key: {app_key}\nSecret_Key: {secret_key}\nToken: {refresh_token}\nRuta_Backup: {ruta_backup}")
                Estatus("Datos guardados correctamente reinicie la aplicacion para aplicar los cambios.", False)
            else:
                Estatus("Por favor rellene todos los campos.", False)
                return "break" 
        else:
            # Save the data to a text file
            with open("form_data.txt", "w") as file:
                file.write(f"Email: {email}\npassw: {passw}\ntimet: {timet}\nRutas: {Rutas} \nDestinatarios: {Destinatarios} \nServidor de Correo: {servidorCorreo}\nPuerto: {puertoCorreo}\nServicios: {Servicios}\nAsunto: {asuntoCorreo}\nHoraMarcada: {checkHora}\nApp_Key: {app_key}\nSecret_Key: {secret_key}\nToken: {refresh_token}\nRuta_Backup: {ruta_backup}")
            Estatus("Datos guardados correctamente reinicie la aplicacion para aplicar los cambios.", False)

    else:
        Estatus("Por favor rellene todos los campos.")
        return "break" 
#Metodo para cargar data desde archivo de configuracion
def load_data():
    try:
        with open("form_data.txt", "r") as file:
            lines = file.readlines()
            rutas_encontradas = False
            destinatarios_encontrados = False
            servicios_encontrados = False
            
            for line in lines:
                if line.startswith("Email:"):
                    etrCorreo.insert(0, line.strip().split(": ")[1])
                elif line.startswith("passw:"):
                    etrContraseña.insert(0, line.strip().split(": ")[1])
                elif line.startswith("timet:"):
                    etrhora.insert(0, line.strip().split(": ")[1])
                elif line.startswith("Servidor de Correo:"):
                    etrServidorCorreo.insert(0, line.strip().split(": ")[1])
                elif line.startswith("Puerto:"):
                    etrPuerto.insert(0, line.strip().split(": ")[1])
                elif line.startswith("Asunto:"):
                    etrAsunto.insert(0, line.strip().split(": ")[1])
                elif line.startswith("Rutas:"):
                    try:
                        rutas = eval(line.strip().split(": ")[1])
                        for ruta in rutas:
                            lbRutas.insert(tk.END, ruta)
                        rutas_encontradas = True
                    except Exception as e:
                        Estatus("Error al cargar rutas", f"No se pudo cargar las rutas: {e}")
                        print("Error al cargar rutas", f"No se pudo cargar las rutas: {e}")
                elif line.startswith("Destinatarios:"):
                    try:
                        destinatarios = eval(line.strip().split(": ")[1])
                        for destinatario in destinatarios:
                            lbdestinatarios.insert(tk.END, destinatario)
                        destinatarios_encontrados = True
                    except Exception as e:
                        Estatus("Error al cargar destinatarios", f"No se pudo cargar los destinatarios: {e}")
                        print("Error al cargar destinatarios", f"No se pudo cargar los destinatarios: {e}")
                elif line.startswith("Servicios:"):
                    try:
                        servicios = eval(line.strip().split(": ")[1])
                        for servicio in servicios:
                            lbServicios.insert(tk.END, servicio)
                        servicios_encontrados = True
                    except Exception as e:
                        Estatus("Error al cargar los servicios", f"No se pudo cargar los servicios: {e}")
                        print("Error al cargar los servicios", f"No se pudo cargar los servicios: {e}")
                elif line.startswith("HoraMarcada: "):
                    try:                        
                        valorCargador = int(line.strip().split(": ")[1])
                        var_check_hora.set(valorCargador)
                    except Exception as e:
                        Estatus("Error al cargar los servicios", f"No se pudo cargar los servicios: {e}")
                        print("Error en check box hora", f"No se pudo cargar el estado del check box: {e}")
                elif line.startswith("App_Key: "):
                    etrDropbox1.insert(0, line.strip().split(": ")[1])
                elif line.startswith("Secret_Key: "):
                    etrDropbox2.insert(0, line.strip().split(": ")[1])
                elif line.startswith("Token: "):
                    etrDropbox4.insert(0, line.strip().split(": ")[1])
                elif line.startswith("Ruta_Backup: "):
                    etrrutas2.insert(0, line.strip().split(": ")[1])
            if not rutas_encontradas or not destinatarios_encontrados or not servicios_encontrados:
                Estatus("Advertencia", "No se encontraron rutas o destinatarios en el archivo.")
                print("Advertencia", "No se encontraron rutas o destinatarios en el archivo.")
            
    except FileNotFoundError:
        Estatus("Archivo no encontrado", "No se encontró el archivo form_data.txt.")
        print("Archivo no encontrado", "No se encontró el archivo form_data.txt.")
#Metodo para abrir ventana de apertura de dialogo de hora (no esta en uso actualmente)
def open_time_picker(entry):
    def set_time():
        hour = hour_var.get()
        minute = minute_var.get()
        entry.delete(0, tk.END)
        entry.insert(0, f"{hour}:{minute}")
        picker.destroy()

    picker = Toplevel(root)
    picker.title("Select Time")

    hour_var = StringVar(value="00")
    minute_var = StringVar(value="00")

    # Hour selection
    tk.Label(picker, text="Hour:").grid(row=0, column=0, padx=5, pady=5)
    hour_entry = tk.Spinbox(picker, from_=0, to=23, wrap=True, textvariable=hour_var, width=5)
    hour_entry.grid(row=0, column=1, padx=5, pady=5)

    # Minute selection
    tk.Label(picker, text="Minute:").grid(row=1, column=0, padx=5, pady=5)
    minute_entry = tk.Spinbox(picker, from_=0, to=59, wrap=True, textvariable=minute_var, width=5)
    minute_entry.grid(row=1, column=1, padx=5, pady=5)

    # Button to set the selected time
    set_button = tk.Button(picker, text="Set Time", command=set_time)
    set_button.grid(row=2, columnspan=2, pady=10)

#metodo para limpiar entry al intentar copiar letras en caja de texto especifica
def clear_entry(event):
    event.widget.delete(0, tk.END)
    return "break"
#Metodo para sumar un item en un listbox
def sumarItem(listBox, entry):
    count = listBox.size() + 1
    if entry.get() != "" and not entry.get() == " ":
        listBox.insert(count, entry.get())
        Estatus(f"Agregado {entry.get()}", False)
        entry.delete(0, tk.END)
    else:
        Estatus("No hay valor que agregar, esta vacio o es invalido", False)  
    return
#Metodo para restar un item en un listbox
def restarItem(listBox):
    seleccion = listBox.curselection()  # Obtener el índice (o índices) seleccionados
    if seleccion:  # Verificar si hay una selección
        indice = seleccion[0] # Primer índice seleccionado  
        Estatus(f"Eliminado {listBox.get(seleccion)}", False)  
        listBox.delete(indice)
    else:
        Estatus("No hay valor que eliminar seleccionado, esta vacio o es invalido", False)  
    return

#Variables y codigo del formulario

currentWorkingDirectory = os.getcwd()

color1 = "#6c756b"
color2 = "#93acb5"
color3 = "#96c5f7"
color4 = "#a9d3ff"
color5 = "#f2f4ff"

root = tk.Tk()
root.title ("Colsulbotsito " + str(version_app))
root.resizable(False, False)
root.state('iconic')

root.configure(bg=color1)
#Metodo para ajustar tamaño de objetos tkinter dinamicamente dependiendo de la resolucion de la pantalla obtenida en la ejecucion inicial del programa
def ajustar_tamano():
    global calculo_alto, calculo_ancho, calculo_fuente

    ancho_pantalla_origen = 1920
    alto_pantalla_origen = 1080
    #fuente_origen = 12
    calculo_ancho = (root.winfo_screenwidth() / (ancho_pantalla_origen * 100)) * 100
    calculo_alto = (root.winfo_screenheight() / (alto_pantalla_origen * 100)) * 100

    calculo_fuente = calculo_alto

ajustar_tamano()
window_height = int(920 * calculo_alto)
window_width = int(950 * calculo_ancho)
print ("Valor alto " + str(calculo_alto) + " alto actual: " + str(window_height))

# Función para minimizar al ícono de la barra de herramientas
def minimizar_a_icono():
    root.withdraw()  # Oculta la ventana completamente (incluido el ícono de la barra de tareas)

# Interceptar el evento de minimizar la ventana
def minimizar_con_evento():
    root.withdraw()  # Ocultar ventana completamente
    # La lógica para el ícono en la barra ya está manejada por pystray
minimizar_a_icono()
root.protocol("WM_DELETE_WINDOW", minimizar_a_icono)  # Si cierran la ventana, se oculta

thread_icono = threading.Thread(target=crear_icono)
thread_icono.daemon = True
thread_icono.start()
#ajustar_tamano(root, ancho_relativo=0.3, alto_relativo=0.3)

#Metodo para abrir manual de usuario
def url_manual():
    webbrowser.open('Manual.pdf')

#Metodo con creditos del desarrollador y acceso al manual
def Creditos():
    global version_app

    smallMessageBox = Toplevel(root, bg=color3)
    smallMessageBox.title(" Información")
    smallMessageBox.resizable(False, False)
    center_screen(smallMessageBox, 360, 130)

    try:
        smallMessageBox.iconbitmap(currentWorkingDirectory+r'\consulbotsito.ico')
    except:
        smallMessageBox.iconbitmap(currentWorkingDirectory+r'\consulbotsito.ico')
    lblCreditosReales = tk.Label(smallMessageBox, text="Programa Original de José Timaure \nDesarrollador: José Timaure\nVersión: " + str(version_app), font=('Arial', 12, 'bold'), bg=color3, fg='white')
    lblCreditosReales.grid(column=0, row=0, pady=0, sticky='n', padx=42)
    button_manual = tk.Button(smallMessageBox, text="Manual", command=lambda: url_manual(), font=('Arial', 12, 'bold underline'), bg=color3, fg='white', borderwidth=0)
    button_manual.grid(column=0, row=1, pady=0, sticky='n', padx=42)
    #lbl3.configure(text='Asegurese que Fecha/Año y el rango sean correctos,\n haga click  en el boton procesar. En caso de que el rango \n de dias sea muy alto el proceso puede tomar su tiempo.')
    #imagen = tk.Label(smallMessageBox, image=currentWorkingDirectory + r"\Consulbotsito.ico")
    #imagen.grid(column=0, row=2, sticky = 'n')
    btnCerrar = tk.Button(smallMessageBox, text="Cerrar", command=lambda: Cerrar(smallMessageBox), bg=color2, borderwidth=0, fg='white', font=('Arial', 12, 'bold'))
    btnCerrar.grid(column=0, row=2, sticky='n', padx=0, pady=1)
#Metodo para actualizar la etiqueta de la barra de estado
def Estatus(texto, concatenar = True):
    global my_counter
    #if not concatenar:
    #    concatenar = True
    if concatenar == True:
        if my_counter >= 2: 
            my_counter = 0
        if my_counter == 0:
            lblEstatus.configure(text=texto)
        else:    
            lblEstatus.configure(text=lblEstatus.cget("text")+ " " + texto)
        my_counter += 1
    else:
        lblEstatus.configure(text=texto)
#Metodo para centrar pantalla dependiendo de la resolucion actual de pantalla
def center_screen(form, width, height):    
    #gets the coordinates of the center of the screen
    global screen_height, screen_width, x_cordinate, y_cordinate
    screen_width = form.winfo_screenwidth()
    screen_height = form.winfo_screenheight()
    # Coordinates of the upper left corner of the window to make the window appear in the center
    x_cordinate = int((screen_width/2) - (width/2))
    y_cordinate = int((screen_height/2) - (height/2))
    form.geometry("{}x{}+{}+{}".format(width, height, x_cordinate, y_cordinate))
center_screen(root, window_width, window_height)
#Frame de datos de correo y su etiqueta
frCorreo = tk.Frame(root, width=window_width-14, height=int(340 * calculo_alto), bg=color2)
frCorreo.grid(row=0, column=0, padx=7, pady=int(7*calculo_alto), rowspan=6, columnspan=5)
frCorreo2 = tk.Frame(root, width=window_width-14, height=int(30 * calculo_alto), bg=color3)
frCorreo2.grid(row=0, column=0, padx=7, pady=int(7*calculo_alto), rowspan=6, columnspan=5, sticky="N")
lblframeCorreo = tk.Label(root, text="Datos de correo", bg=color3, fg='white', font=("Arial", int((14 * calculo_fuente)-(14*0.15)),"bold"))
lblframeCorreo.grid(row=0, column=0, padx=0, pady=int(7*calculo_alto), columnspan=6, sticky="N")
#Caja de texto de correo y su equiteta
lblCorreo = tk.Label(root, text="Correo origen:", bg=color2, fg='white', font=("Arial", int(12 * calculo_fuente),"bold"))
lblCorreo.grid(row=1, column=0, padx=1, pady=0, sticky="E")
etrCorreo = tk.Entry(root, borderwidth=0, width=int(25 * calculo_ancho), font=("Arial", int(12 * calculo_fuente)), bg="#70A0AF", fg="white")
etrCorreo.grid(row=1, column=1, padx=1, pady=0)
#Caja de texto de contraseña y su equiteta
lblContraseña = tk.Label(root, text="Contraseña correo de origen:", bg=color2, fg='white', font=("Arial", int(12 * calculo_fuente),"bold"))
lblContraseña.grid(row=2, column=0, padx=1, pady=0,sticky="E")
etrContraseña = tk.Entry(root, show="☻", borderwidth=0, width=int(25 * calculo_ancho), font=("Arial", int(12 * calculo_fuente), "bold"), bg="#70A0AF", fg="white")
etrContraseña.grid(row=2, column=1, padx=1, pady=0)
#Caja de texto de servidor correo y su equiteta
lblServidorCorreo = tk.Label(root, text="Servidor de correo:", bg=color2, fg='white', font=("Arial", int(12 * calculo_fuente),"bold"))
lblServidorCorreo.grid(row=3, column=0, padx=1, pady=0,sticky="E")
etrServidorCorreo = tk.Entry(root, borderwidth=0, width=int(25 * calculo_ancho), font=("Arial", int(12 * calculo_fuente)), bg="#70A0AF", fg="white")
etrServidorCorreo.grid(row=3, column=1, padx=1, pady=0)
#Caja de texto de puerto y su equiteta
lblPuerto = tk.Label(root, text="Puerto de servidor:", bg=color2, fg='white', font=("Arial", int(12 * calculo_fuente),"bold"))
lblPuerto.grid(row=4, column=0, padx=1, pady=0,sticky="E")
etrPuerto = tk.Entry(root, borderwidth=0, width=int(25 * calculo_ancho), font=("Arial", int(12 * calculo_fuente)), bg="#70A0AF", fg="white")
etrPuerto.grid(row=4, column=1, padx=1, pady=0)
#Caja de texto de puerto y su equiteta
lblAsunto = tk.Label(root, text="Asunto correo:", bg=color2, fg='white', font=("Arial", int(12 * calculo_fuente),"bold"))
lblAsunto.grid(row=5, column=0, padx=1, pady=1,sticky="E")
etrAsunto = tk.Entry(root, borderwidth=0, width=int(25 * calculo_ancho), font=("Arial", int(12 * calculo_fuente)), bg="#70A0AF", fg="white")
etrAsunto.grid(row=5, column=1, padx=1, pady=1)
var_check_hora = tk.IntVar()
cbxHora = tk.Checkbutton(root, text="Hora", variable=var_check_hora, fg='white',bg=color2, borderwidth=0, onvalue=1, offvalue=0, highlightcolor=color2,highlightbackground=color2, selectcolor=color1, activebackground=color2, activeforeground='white', highlightthickness=0,disabledforeground='white', font=("Arial", int(12 * calculo_fuente), "bold"),indicatoron=False, relief="flat", command = lambda: Estatus("Se agregara/eliminara hora y fecha al asunto", False))
cbxHora.grid(row=5, column=1, sticky="E")

#Listbox destinatarios y su etiqueta
etrdestinatarios = tk.Entry(root, borderwidth=0, width=int(25 * calculo_ancho), font=("Arial", int(12 * calculo_fuente)), bg="#70A0AF", fg="white")
etrdestinatarios.grid(row=1, column=3, padx=1, pady=0)
lbldestinatarios = tk.Label(root, text="Destinatarios:", bg=color2, fg='white', font=("Arial", int(12 * calculo_fuente),"bold"))
lbldestinatarios.grid(row=1, column=2, padx=1, pady=0,sticky="E")
lbdestinatarios = tk.Listbox(root, activestyle='dotbox', borderwidth=0, width=int(25 * calculo_ancho),height=int(10*calculo_alto), font=("Arial", int(12 * calculo_fuente)), bg="#70A0AF", fg="white")
lbdestinatarios.grid(row=2, column=3, padx=1, pady=0, rowspan=5, sticky="N")
sumarDestinatarios_button = tk.Button(root, text="+", command=lambda:sumarItem(lbdestinatarios, etrdestinatarios), borderwidth=0, bg="#96c5f7", font=("Arial", int(12 * calculo_fuente), "bold"), fg="white", width=1, height=1)
sumarDestinatarios_button.grid(row=2, column=4, pady=0, padx=0, sticky='NW', rowspan=4)
restarDestinatarios_button = tk.Button(root, text="-", command=lambda:restarItem(lbdestinatarios), borderwidth=0, bg="#96c5f7", font=("Arial", int(12 * calculo_fuente), "bold"), fg="white", width=1, height=1)
restarDestinatarios_button.grid(row=2, column=4, pady=int(70 * calculo_alto),padx=0, sticky='NW', rowspan=4)

#Frame de datos de configuraciones adicionales
frmconfig = tk.Frame(root, width=window_width-14, height=int(470 * calculo_alto), bg=color2)
frmconfig.grid(row=9, column=0, padx=7, pady=0, rowspan=8, columnspan=5)
frmconfig2 = tk.Frame(root, width=window_width-14, height=int(30 * calculo_alto), bg=color3)
frmconfig2.grid(row=9, column=0, padx=7, pady=0, rowspan=6, columnspan=5, sticky="N")
lbl_datos_adicionales = tk.Label(root, text="Datos adicionales", bg=color3, fg='white', font=("Arial", int((14 * calculo_fuente)-(14*0.15)),"bold"))
lbl_datos_adicionales.grid(row=9, column=0, padx=0, pady=0, columnspan=5, sticky="N")

#Caja de texto de hora y su etiqueta
def validar_entrada(texto):
    # Permitir que el Entry esté vacío
    if texto == "":
        return True
    # Verificar que la longitud no exceda los 5 caracteres (formato ##:##)
    if len(texto) > 5:
        return False
    # Verificar que los dos primeros caracteres sean números
    if len(texto) <= 2 and not texto.isdigit():
        return False
    # Asegurar que el tercer carácter sea ':'
    if len(texto) == 3 and texto[2] != ":":
        return False
    # Verificar que los caracteres después del ':' sean números
    if len(texto) > 3:
        parte_inferior = texto[3:]
        if not parte_inferior.isdigit():
            return False
    return True
    
vcmd = root.register(validar_entrada)
lblhora = tk.Label(root, text="Hora ejecucion:", bg=color2, fg='white', font=("Arial", int(12 * calculo_fuente),"bold"))
lblhora.grid(row=10, column=0, padx=1, pady=1,sticky="E")
etrhora = tk.Entry(root, validate="key", validatecommand=(vcmd, "%P"), borderwidth=0, width=int(25*calculo_ancho), font=("Arial", int(12 * calculo_fuente)), bg="#70A0AF", fg="white")
etrhora.grid(row=10, column=1, padx=1, pady=1)

'''
etrhora.bind("<Button-1>", lambda event: open_time_picker(etrhora))
etrhora.bind("<Key>", clear_entry)
'''
#List box servicios y su etiqueta
etrServicios = tk.Entry(root, borderwidth=0, width=int(25 * calculo_ancho), font=("Arial", int(12 * calculo_fuente)), bg="#70A0AF", fg="white")
etrServicios.grid(row=11, column=1, padx=1, pady=0)
lblServicios = tk.Label(root, text="Servicios:", bg=color2, fg='white', font=("Arial", int(12 * calculo_fuente),"bold"))
lblServicios.grid(row=11, column=0, padx=1, pady=0,sticky="E")
lbServicios = tk.Listbox(root, activestyle='dotbox', borderwidth=0, width=int(25 * calculo_ancho), height=5, font=("Arial", int(12 * calculo_fuente)), bg="#70A0AF", fg="white")
lbServicios.grid(row=12, column=1, padx=1, pady=0, rowspan=1, sticky="N")
sumarServicio_button = tk.Button(root, text="+", command=lambda:sumarItem(lbServicios, etrServicios), borderwidth=0, bg="#96c5f7", font=("Arial", int(12 * calculo_fuente), "bold"), fg="white", height=1, width=1)
sumarServicio_button.grid(row=12, column=2, pady=0, padx=0, sticky='NW', rowspan=1)
restarServicio_button = tk.Button(root, text="-", command=lambda:restarItem(lbServicios), borderwidth=0, bg="#96c5f7", font=("Arial", int(12 * calculo_fuente), "bold"), fg="white", height=1, width=1)
restarServicio_button.grid(row=12, column=2, pady=int(60 * calculo_alto),padx=0, sticky='NW', rowspan=1)
#List box rutas y su etiqueta
etrrutas = tk.Entry(root, borderwidth=0, width=int(25 * calculo_ancho), font=("Arial", int(12*calculo_fuente)), bg="#70A0AF", fg="white")
etrrutas.grid(row=10, column=3, padx=1, pady=0)
lblrutas = tk.Label(root, text="Rutas:", bg=color2, fg='white', font=("Arial", int(12 * calculo_fuente),"bold"))
lblrutas.grid(row=10, column=2, padx=1, pady=0,sticky="E")
lbRutas = tk.Listbox(root, activestyle='dotbox', borderwidth=0, width=int(25 * calculo_ancho), height=5, font=("Arial", int(12 * calculo_fuente)), bg="#70A0AF", fg="white")
lbRutas.grid(row=11, column=3, padx=1, pady=0, rowspan=2, sticky="N")
sumarRuta_button = tk.Button(root, text="+", command=lambda:sumarItem(lbRutas, etrrutas), borderwidth=0, bg="#96c5f7", font=("Arial", int(12 * calculo_fuente), "bold"), fg="white", height=1, width=1)
sumarRuta_button.grid(row=11, column=4, pady=0, padx=0, sticky='NW', rowspan=2)
restarRuta_button = tk.Button(root, text="-", command=lambda:restarItem(lbRutas), borderwidth=0, bg="#96c5f7", font=("Arial", int(12 * calculo_fuente), "bold"), fg="white", height=1, width=1)
restarRuta_button.grid(row=11, column=4, pady=int(60* calculo_alto),padx=0, sticky='NW', rowspan=4)
#Ruta de backup
etrrutas2 = tk.Entry(root, borderwidth=0, width=int(25 * calculo_ancho), font=("Arial", int(12 * calculo_fuente)), bg="#70A0AF", fg="white")
etrrutas2.grid(row=11, column=3, padx=1, pady=int(120*calculo_alto), sticky="N", rowspan=5)
lblrutas2 = tk.Label(root, text="Ruta Backup:", bg=color2, fg='white', font=("Arial", int(12 * calculo_fuente),"bold"))
lblrutas2.grid(row=11, column=2, padx=1, pady=int(120*calculo_alto),sticky="NE",rowspan=5)


#Barra DRopbox
frdropbox = tk.Frame(root, width=window_width - 14, height=int(30*calculo_alto), bg=color3)
frdropbox.grid(row=12, column=0, padx=0, pady=0, rowspan=1, columnspan=5, sticky="S")
lbldropboxtitle = tk.Label(root, text="Configuracion Dropbox", bg=color3, fg='white', font=("Arial", int((14 * calculo_fuente)-(14*0.15)),"bold"))
lbldropboxtitle.grid(row=12, column=0, padx=0, pady=int(4 * calculo_alto), columnspan=5, sticky="S")
#Boton URL Paso 1 configuracion dropbox
url1_button = tk.Button(root, text="URL App Key/Secret Key", command=lambda: acceder_url(1), borderwidth=0, bg="#96c5f7", font=("Arial", int(12 * calculo_fuente), "bold"), fg="white")
url1_button.grid(row=13, pady=0,padx=5, column=0, columnspan=2, sticky="S")
#Caja de texto de dropboxtoken y su etiqueta
lbldropbox1 = tk.Label(root, text="App key Dropbox:", bg=color2, fg='white', font=("Arial", int(12 * calculo_fuente),"bold"))
lbldropbox1.grid(row=14, column=0, padx=1, pady=int(15*calculo_alto),sticky="SE")
etrDropbox1 = tk.Entry(root, borderwidth=0, width=int(25 * calculo_ancho), font=("Arial", int(12 * calculo_fuente), "bold"), bg="#70A0AF", fg="white", show="☻")
etrDropbox1.grid(row=14, column=1, padx=1, pady=int(15*calculo_alto), sticky="S")
#Caja de texto de dropboxtoken y su etiqueta
lbldropbox2 = tk.Label(root, text="App secret Dropbox:", bg=color2, fg='white', font=("Arial", int(12 * calculo_fuente),"bold"))
lbldropbox2.grid(row=15, column=0, padx=1, pady=int(15*calculo_alto),sticky="SE")
etrDropbox2 = tk.Entry(root, borderwidth=0, width=int(25 * calculo_ancho), font=("Arial", int(12 * calculo_fuente), "bold"), bg="#70A0AF", fg="white", show="☻")
etrDropbox2.grid(row=15, column=1, padx=1, pady=int(15*calculo_alto), sticky="S")
#Boton URL Paso 2 configuracion dropbox
url2_button = tk.Button(root, text="URL Token", command=lambda: acceder_url(2), borderwidth=0, bg="#96c5f7", font=("Arial", int(12 * calculo_fuente), "bold"), fg="white")
url2_button.grid(row=13, pady=0,padx=5, column=2, columnspan=2, sticky="S")
#Caja de texto de dropboxtoken y su etiqueta
lbldropbox3 = tk.Label(root, text="Token Validacion:", bg=color2, fg='white', font=("Arial", int(12 * calculo_fuente),"bold"))
lbldropbox3.grid(row=14, column=2, padx=1, pady=int(15*calculo_alto),sticky="SE")
etrDropbox3 = tk.Entry(root, borderwidth=0, width=int(25 * calculo_ancho), font=("Arial", int(12 * calculo_fuente), "bold"), bg="#70A0AF", fg="white", show="☻")
etrDropbox3.grid(row=14, column=3, padx=1, pady=int(15 * calculo_alto), sticky="S")

lbldropbox4 = tk.Label(root, text="Token Resultante:", bg=color2, fg='white', font=("Arial", int(12 * calculo_fuente),"bold"))
lbldropbox4.grid(row=15, column=2, padx=1, pady=int(15*calculo_alto),sticky="SE")
etrDropbox4 = tk.Entry(root, borderwidth=0, width=int(25 * calculo_ancho), font=("Arial", int(12 * calculo_fuente), "bold"), bg="#70A0AF", fg="white", show="☻")
etrDropbox4.grid(row=15, column=3, padx=1, pady=int(15*calculo_alto), sticky="S")
registrar_button = tk.Button(root, text="Registrar", command=lambda: obtener_token_acceso(), borderwidth=0, bg="#96c5f7", font=("Arial", int(12 * calculo_fuente), "bold"), fg="white")
registrar_button.grid(row=16, pady=int(5 * calculo_alto),padx=5, column=0, columnspan=2)
#Boton de guardado de informacion en archivo txt
submit_button = tk.Button(root, text="Guardar/Actualizar", command=saveData, width=int(30 * calculo_ancho), borderwidth=0, bg="#96c5f7", font=("Arial", int(12 * calculo_fuente), "bold"), fg="white")
submit_button.grid(row=17, columnspan=5, pady=int(7*calculo_alto))

frEstatus = tk.Frame(root, width=window_width, height=int(50 * calculo_alto), bg=color2)
frEstatus.grid(row=18, column=0, padx=0, pady=int(7*calculo_alto), rowspan=1, columnspan=5, sticky="S")
lblEstatus = tk.Label(root, text="", bg=color2, fg='white', font=("Arial", int((14 * calculo_fuente)-(14*0.15)),"bold"))
lblEstatus.grid(row=18, column=0, padx=0, pady=int(7*calculo_alto), columnspan=5)
help_button = tk.Button(root, text="?", command=lambda: Creditos(), borderwidth=0, bg="#96c5f7", font=("Arial", int(12 * calculo_fuente), "bold"), fg="white")
help_button.grid(row=18, columnspan=5, pady=int(7*calculo_alto),padx=5, sticky="E")
#test_button = tk.Button(root, text="T", command=lambda: obtener_estado_dropbox(renovar_access_token(etrDropbox4.get())), borderwidth=0, bg="#96c5f7", font=("Arial", 12, "bold"), fg="white")
#test_button.grid(row=20, columnspan=5, pady=5,padx=5, sticky="W")
#test_button = tk.Button(root, text="T", command=lambda: obtener_estado_dropbox(renovar_access_token(obtener_token_acceso())), borderwidth=0, bg="#96c5f7", font=("Arial", 12, "bold"), fg="white")
#test_button.grid(row=20, columnspan=5, pady=5,padx=5, sticky="W")

try:    
    root.iconbitmap(currentWorkingDirectory+r'\consulbotsito.ico')
except Exception as e:
    lblEstatus.configure(text="Icono no encontrado, se cargo icono por defecto.")

try:
    load_data()    
    print("Datos cargados")
except:
    print("No hay datos que cargar")
def MyTimer():
    import time
    from datetime import datetime, timedelta
#Ejecuta metodos sin colgar la app
async def ejecutar_tarea_diaria(hora_objetivo, metodo):
    global my_counter
    while True:
        ahora = datetime.now()
        objetivo = ahora.replace(hour=hora_objetivo.hour, minute=hora_objetivo.minute, second=hora_objetivo.second, microsecond=0)
        
        if objetivo < ahora:
            # Si la hora objetivo ya pasó, calcula para el día siguiente
            objetivo += timedelta(days=1)
        
        tiempo_restante = (objetivo - ahora).total_seconds()
        print(f"Esperando {int(tiempo_restante)} segundos para la próxima ejecución...")
        my_counter = 0
        Estatus("Bienvenido, proxima ejecucion en: " + str(int(tiempo_restante)) + " segundos")
        await asyncio.sleep(tiempo_restante)  # Pausa asíncrona sin bloquear el programa
        metodo()  # Ejecuta el método cuando llega la hora objetivo

# Integración entre asyncio y Tkinter
def iniciar_asyncio_en_tk(root, asyncio_loop):
    # Ejecuta el bucle de eventos de asyncio cada cierto tiempo dentro del mainloop de Tkinter
    def tick():
        asyncio_loop.stop()
        asyncio_loop.run_forever()
        root.after(100, tick)  # Llama a tick repetidamente
    root.after(100, tick)

# Configuración del programa
def metodoEjecucion():
    global listaRutas, rutas_resultado
    listaRutas = [lbRutas.get(i) for i in range(lbRutas.size())]
    rutas_resultado = logSearcher(listaRutas, "log")
    hora_objetivo = datetime.strptime(etrhora.get(), "%H:%M").time()        
    lista_destinatarios = [lbdestinatarios.get(i) for i in range(lbdestinatarios.size())]
    Lista_Rutas = logSearcher(listaRutas, "log")
    Lista_Rutas2 = logSearcher(listaRutas, "adtg")
    verificar_servicios([lbServicios.get(i) for i in range(lbServicios.size())])
    asyncio.create_task(ejecutar_tarea_diaria(hora_objetivo, lambda:SendMessage(
        etrCorreo.get(),
        lista_destinatarios,
        etrContraseña.get(),
        Lista_Rutas,
        etrAsunto.get(),
        etrServidorCorreo.get(),
        int(etrPuerto.get()),
        Lista_Rutas2
        )))

#Metodo main
async def main():
    try:
        metodoEjecucion()
        nombres_procesos = (p.name() for p in psutil.process_iter())
        # Verificar si "Consulbotsito.exe" está en los nombres de los procesos
        contador_procesos = 0 
        for nombre in nombres_procesos:
            if nombre == "Consulbotsito.exe":
                contador_procesos += 1
                if contador_procesos > 1:
                    Cerrar(root)
                    break  # Si se encuentra el proceso, salimos del bucle
    except Exception as e:
        Estatus("Error al cargar archivo de datos: " + str(e), False)
        
        


asyncio_loop = asyncio.get_event_loop()
iniciar_asyncio_en_tk(root, asyncio_loop)
asyncio_loop.create_task(main())

root.mainloop()