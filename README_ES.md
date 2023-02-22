# Kraken

<h1 align="center">
  <br>
  <img src="static/kraken-logo-background.jpg" alt="Kraken">
</h1>

<h4 align="center">Kraken, una webshell modular y multi-lenguaje desarrollada por @secu_x11.</h4>

<p align="center">
  <a href="#versión">Versión</a> •
  <a href="#requirimientos">Requerimientos</a> •
  <a href="#soporte">Soporte</a> •
  <a href="#instalación">Instalación</a> •
  <a href="#guía-de-uso">Guía de Uso</a> •
  <a href="#ejemplos">Ejemplos</a> •
  <a href="#contribuciones">Contribuciones</a> •
  <a href="#bugs">Bugs</a>
</p>

<p align="center">
  <a href="https://github.com/kraken-ng/Kraken/blob/main/README.md">Ingles</a> •
  <a href="https://github.com/kraken-ng/Kraken/blob/main/README_ES.md">Español</a>
</p>

---

## Versión

1.0.0 - [Version changelog](CHANGELOG.md)

## Requerimientos

Para poder utilizar la herramienta, primero se deben satisfacer los siguientes requerimientos:

- **python3.8** (>= 3.8): la herramienta contiene elementos sintácticos que tan sólo estan disponibles en las versiones >= de Python 3.8.
- **pip**: en el archivo [requirements.txt](requirements.txt) se encuentran el conjunto de librerias que son necesarias instalar para que la herramienta funcione. Es importante que la versión de pip vaya ligada a la de Python, pues de otra forma no funcionarán las librerias.
- **docker** (>= 20.10.12): debido a que se deben "cross-compilar" los módulos en Java, pues no se ha encontrado otra forma de hacerlo, se ha optado por utilizar contenedores de Docker para realizar este proceso de la forma más elegante y limpia posible.

Aunque no es un requerimiento, **se recomienda** utilizar la herramienta en un sistema operativo Linux pues, de esta forma, se asegura (dentro de lo esperado), el correcto funcionamiento.

## Soporte

Por un lado, Kraken esta soportado en diferentes tecnologías y versiones. A continuación se detalla un listado acerca de dónde los agentes de Kraken estan soportados:

- **PHP (php):**
  - 5.4, 5.5, 5.6
  - 7.0, 7.1, 7.2, 7.3, 7.4
  - 8.0, 8.1, 8.2
- **JAVA (jsp):**
  - 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17
- **.NET (aspx):**
  - 3.5
  - 4.0
  - 4.5, 4.5.1, 4.5.2
  - 4.6, 4.6.1, 4.6.2
  - 4.7, 4.7.1, 4.7.2
  - 4.8

Por el otro lado, es posible consultar el listado de versiones y tecnologias que soporta cada módulo de Kraken. Se puede consultar [aquí](https://github.com/kraken-ng/modules/blob/main/README.md).

No obstante, puedes comprobar (manualmente) la compatibilidad de los módulos a través de la utilidad: [check_syntax](https://github.com/kraken-ng/utils/blob/main/check_syntax/README.md).

## Instalación

A continuación se explica el proceso de instalación de los requerimientos, no es obligatorio hacerlo de esta forma, pero si se **RECOMIENDA** para evitar posibles errores o fallos inesperados durante el uso de Kraken:

En primer lugar se comienza instalando [Conda](https://docs.conda.io/projects/conda/en/stable/) o [Miniconda](https://docs.conda.io/en/latest/miniconda.html). Esta herramienta nos permitirá gestionar diferentes "entornos" python aislados entre sí y con diferentes librerias y dependencias. El proceso de instalación es muy sencillo, y se puede seguir aquí: [Linux](https://conda.io/projects/conda/en/stable/user-guide/install/linux.html) o [Windows](https://conda.io/projects/conda/en/stable/user-guide/install/windows.html)

Una vez se tenga instalado conda, se crea un entorno para Kraken:

```shell
conda create -n kraken python=3.8
conda activate kraken
```

> Utilizando este método, no es necesario especificar ni la versión de Python ni de Pip, así como tampoco tendremos problemas de visibilidad con las librerias python instaladas, ya que todo se queda en el entorno virtual creado con conda.

Después se procede a clonar el repositorio e instalar las dependencias:

```shell
git clone --recurse-submodules https://github.com/kraken-ng/Kraken.git
cd Kraken
pip install -r requirements.txt
python kraken.py -h
```

> Es muy importante clonar el repositorio y los **submódulos** existentes ya que, los componentes de Kraken estan repartidos en diferentes repositorios. De otra forma, Kraken no funcionará correctamente.

El siguiente requerimiento, Docker, se puede evitar en caso de usar las versiones PHP y/o ASPX de los agentes de Kraken. En el caso de usar Java es necesario instalar docker para poder compilar los módulos. Aunque, se recomienda seguir con la instalación para tener todos los requerimientos instalados.

Continuando con la instalación, se procede a instalar **Docker**. Esta herramienta se puede descargar, o bien del gestor de paquetes, o de la [página oficial](https://docs.docker.com/engine/install/). En principio el proceso de instalación es sencillo y guiado. Al final, simplemente se debe añadir nuestro usuario al grupo de docker y reiniciar, para que pueda descargar y levantar los contenedores. Esto se puede hacer con:

```shell
sudo usermod -aG docker $USER
```

Adiccionalmente, como dependencia **opcional** y recomendada (que depende del uso que vayas a darle a la herramienta), se propone la herramienta **Docker-Compose**, que será necesaria exclusivamente para desplegar los entornos de desarrollo y/o pruebas. Se puede instalar de la [página oficial](https://docs.docker.com/compose/install/) o, durante la instalación de Docker, a través de los repositorios con (sino se ha instalado antes):

```shell
sudo apt install docker-compose-plugin
```

## Guía de Uso

Tras haber completado la fase de instalación, se comienza con el uso de la herramienta:

```
usage: kraken.py [-h] [-g] [-c] [-m {st,c2}] -p PROFILE -k {raw,container} [-d] [-l]

Kraken, a modular multi-language webshell (coded by @secu_x11)

optional arguments:
  -h, --help            show this help message and exit
  -g, --generate        Generate a webshell (php/jsp/aspx)
  -c, --connect         Connect to a deployed webshell
  -m {st,c2}, --mode {st,c2}
                        Mode of operation with agent
  -p PROFILE, --profile PROFILE
                        Filepath of Connection Profile to use
  -k {raw,container}, --compiler {raw,container}
                        Name of the compiler to use
  -d, --debug           Turn ON Debug Mode
  -l, --log             Log all executed commands and outputs

```

Primero, se debe subir un agente para poder comunicarse con él utilizando Kraken. Los agentes se encuentran bajo el directorio [agents](https://github.com/kraken-ng/agents) y existen 2 tipos: **standard** y **c2** que dependen del modo de funcionamiento que se desee utilizar (para saber más información consultar la wiki).

Tras subir el agente y disponer de la URL con la ruta donde se ha subido, se debe crear un **Perfil de Conexión**. El proceso de creación de perfiles de conexión se encuentra detallado en la wiki. No obstante, puedes consultar algunos ya existentes [aquí](https://github.com/kraken-ng/utils/tree/main/req2profile/examples).

Una vez creado el perfil de conexión, el segundo paso es conectarse con el agente, esto se puede hacer con el siguiente comando (dependiendo del agente utilizado se especificará un modo u otro):

```shell
python kraken.py --connect --mode <MODO> --profile <RUTA_DEL_PERFIL>
```

Tras conectarse con el agente, Kraken cargará los módulos que se pueden utilizar con el agente en cuestión y arrojará una prompt. A través de la prompt se pueden consultar los módulos disponibles pulsando la tecla `<ESPACIO>` o directamente con el comando `help`.

## Ejemplos

A modo de ejemplo, se utilizará el entorno de pruebas LAMP. Un agente **STANDARD** será desplegado en el contenedor de PHP 8.

Primero, se despliegan los contenedores con Docker Compose:

```
(kraken) secu@x11:~/Kraken$ docker compose -f envs/php/docker-compose.yml up -d
[+] Running 4/4
 ⠿ Network php_apps       Created                                                             0.0s
 ⠿ Container php5-apache  Started                                                             0.6s
 ⠿ Container php7-apache  Started                                                             0.6s
 ⠿ Container php8-apache  Started                                                             0.4s
```

> Durante el despliegue con Docker Compose se copia el Agente Standard al directorio del servicio web automáticamente, así que no tenemos que subirlo manualmente.

El segundo paso es crear o elegir un perfil de conexión para comunicarnos con el agente desplegado. En este caso, como estamos utilizando un entorno de pruebas, se utilizará su correspondiente perfil de conexión: [profile_testing_php_linux_st.json](https://github.com/kraken-ng/utils/blob/main/req2profile/examples/profile_testing_php_linux_st.json).

```json
{
  "client" : {
    "url" : "http://localhost:8000/agent_st.php",
    "skip_ssl": false,
    "method" : "POST",
    "headers" : {
      "Host" : "localhost:8000",
      "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    },
    "cookies" : {},
    "fields" : {},
    "message" : {
      "secret" : {
        "type" : "COOKIE",
        "key" : "X-Authorization",
        "value" : "P4ssw0rd!"
      },
      "data" : {
        "type" : "FIELD",
        "key" : "data"
      }
    }
  },
  "server" : {
    "type" : "FIELD",
    "key" : "data"
  }
}
```

En este perfil, podemos configurar todos los parámetros de conexión para ajustarlo a nuestras necesidades. No obstante, si se realizan cambios (como por ejemplo la contraseña), estos deben reflejarse en el agente:

```php
public  $REQUEST_METHOD    = "POST";
private $PASSWORD_TYPE     = "COOKIE";
private $PASSWORD_KEY      = "X-Authorization";
private $PASSWORD_VALUE    = "P4ssw0rd!";
private $REQUEST_DATA_TYPE = "FIELD";
private $REQUEST_DATA_KEY  = "data";
private $RESPONSE_DATA_KEY = "data";
```

> Para este ejemplo, no se modificará ningún dato, ya que se utiliza un entorno de pruebas para PHP. Pero **se recomienda** modificar esta información cuando se use fuera de un entorno de pruebas.

Finalmente, con el perfil de conexión listo, se procede a conectarse con el agente:

```
(kraken) secu@x11:~/Kraken$ python kraken.py -c -m st -p utils/req2profile/examples/profile_testing_php_linux_st.json -k raw
(ST) www-data@c48827a1b2ac:/var/www/html$ help

+------------+--------+-----------------------------------------------------------------------------------+-----------------+
|  Command   |  Type  |                                    Description                                    |     Authors     |
+------------+--------+-----------------------------------------------------------------------------------+-----------------+
|    exit    |  Core  |                          Ends the session with the agent                          |    @secu_x11    |
|    help    |  Core  | Displays the available commands or information of a command passed as an argument |    @secu_x11    |
|    cat     | Module |                                 Read file contents                                |    @secu_x11    |
|     cd     | Module |                              Change working directory                             |    @secu_x11    |
|   chmod    | Module |                 Change file permissions of file or multiple files                 |    @secu_x11    |
|     cp     | Module |                            Copy file or multiple files                            |    @secu_x11    |
|  download  | Module |                       Download a remote file to a local path                      |    @secu_x11    |
|  execute   | Module |                  Execute a binary or command and retrieve output                  |    @secu_x11    |
|    find    | Module |                      Find files of directory using a pattern                      |    @secu_x11    |
|    grep    | Module |                  Search for files whose content matches a pattern                 |    @secu_x11    |
|     id     | Module |              Displays information about the currently logged-in user              |    @secu_x11    |
|     ls     | Module |                             List files or directories                             |    @secu_x11    |
|   mkdir    | Module |                      Create directories and/or subdirectories                     | @r1p, @secu_x11 |
|  netstat   | Module |              Show listening ports, arp table and machine's net routes             |    @secu_x11    |
|     ps     | Module |                     List the processes running on the machine                     |    @secu_x11    |
|    pspy    | Module |                          Monitor processes on the machine                         |    @secu_x11    |
|     rm     | Module |                           Remove file or multiple files                           |    @secu_x11    |
|  sysinfo   | Module |                  Get basic system info about compromised machine                  |    @secu_x11    |
| tcpconnect | Module |                                Connect to TCP Port                                |    @secu_x11    |
|   touch    | Module |               Change the date of an existing file or multiple files               |    @secu_x11    |
|   upload   | Module |                       Upload a local file to remote filepath                      |    @secu_x11    |
|  webinfo   | Module |                Get basic web server info about compromised machine                |    @secu_x11    |
+------------+--------+-----------------------------------------------------------------------------------+-----------------+

(ST) www-data@c48827a1b2ac:/var/www/html$ help touch                                                                                    
usage: touch datetime [files [files ...]]

Change the date of an existing file or multiple files

positional arguments:
  datetime  Date represented in 'd/m/Y-H:i:s' format
  files     File/s to change date

Examples:
  touch 01/01/2022-00:00:00 example.txt
  touch 01/01/2022-00:00:00 /tmp/passwd
  touch 01/01/2022-00:00:00 ../test_1.txt ../test_2.txt
  touch 01/01/2022-00:00:00 C:/Windows/Tasks/example.txt

(ST) www-data@c48827a1b2ac:/var/www/html$ sysinfo                                                                                       
Hostname: c48827a1b2ac
IP: 172.19.0.2
OS: Linux c48827a1b2ac 5.15.0-58-generic #64-Ubuntu SMP Thu Jan 5 11:43:13 UTC 2023 x86_64
User: www-data
Path: /var/www/html/agent_st.php
Version: 8.0.25

(ST) www-data@c48827a1b2ac:/var/www/html$ cd ..                                                                                         
(ST) www-data@c48827a1b2ac:/var/www$ ls

                
  drwxr-xr-x  1      root      root      4096   2022/11/15 04:13:21  .      
  drwxr-xr-x  1      root      root      4096   2022/11/15 04:13:21  ..     
  drwxrwxrwx  1      www-data  www-data  4096   2023/02/21 22:58:28  html   

(ST) www-data@c48827a1b2ac:/var/www$ exit

```

También es posible utilizar el modo **C2** como se muestra a continuación:

```
(kraken) secu@x11:~/Kraken$ python kraken.py -c -m c2 -p utils/req2profile/examples/profile_testing_php_linux_c2.json -k raw
[*] Detected new cookie: "PHPSESSID" = "deaa1240ada8f3afe949f5fc070bfab3"
(C2) www-data@c48827a1b2ac:/var/www/html$ help                                                                                          
+-----------------+--------+-----------------------------------------------------------------------------------+-----------------+
|     Command     |  Type  |                                    Description                                    |     Authors     |
+-----------------+--------+-----------------------------------------------------------------------------------+-----------------+
|       exit      |  Core  |                          Ends the session with the agent                          |    @secu_x11    |
|       help      |  Core  | Displays the available commands or information of a command passed as an argument |    @secu_x11    |
|   list_modules  |  Core  |                          List modules loaded in the agent                         |    @secu_x11    |
|   load_module   |  Core  |        Load a new agent module/s (use 'all' to load all available modules)        |    @secu_x11    |
|  unload_module  |  Core  |     Unload an existing agent module/s (use 'all' to unload all loaded modules)    |    @secu_x11    |
| refresh_modules |  Core  |          Refresh module status from agent (update agent's memory in use)          |    @secu_x11    |
|  clean_modules  |  Core  |                              Unload all agent modules                             |    @secu_x11    |
|       cat       | Module |                                 Read file contents                                |    @secu_x11    |
|        cd       | Module |                              Change working directory                             |    @secu_x11    |
|      chmod      | Module |                 Change file permissions of file or multiple files                 |    @secu_x11    |
|        cp       | Module |                            Copy file or multiple files                            |    @secu_x11    |
|     download    | Module |                       Download a remote file to a local path                      |    @secu_x11    |
|     execute     | Module |                  Execute a binary or command and retrieve output                  |    @secu_x11    |
|       find      | Module |                      Find files of directory using a pattern                      |    @secu_x11    |
|       grep      | Module |                  Search for files whose content matches a pattern                 |    @secu_x11    |
|        id       | Module |              Displays information about the currently logged-in user              |    @secu_x11    |
|        ls       | Module |                             List files or directories                             |    @secu_x11    |
|      mkdir      | Module |                      Create directories and/or subdirectories                     | @r1p, @secu_x11 |
|     netstat     | Module |              Show listening ports, arp table and machine's net routes             |    @secu_x11    |
|        ps       | Module |                     List the processes running on the machine                     |    @secu_x11    |
|       pspy      | Module |                          Monitor processes on the machine                         |    @secu_x11    |
|        rm       | Module |                           Remove file or multiple files                           |    @secu_x11    |
|     sysinfo     | Module |                  Get basic system info about compromised machine                  |    @secu_x11    |
|    tcpconnect   | Module |                                Connect to TCP Port                                |    @secu_x11    |
|      touch      | Module |               Change the date of an existing file or multiple files               |    @secu_x11    |
|      upload     | Module |                       Upload a local file to remote filepath                      |    @secu_x11    |
|     webinfo     | Module |                Get basic web server info about compromised machine                |    @secu_x11    |
+-----------------+--------+-----------------------------------------------------------------------------------+-----------------+

(C2) www-data@c48827a1b2ac:/var/www/html$ list_modules                                                                                  
+----+------+----------+------+
| ID | Name | Filepath | Date |
+----+------+----------+------+
+----+------+----------+------+
Total memory in use: 0 B

(C2) www-data@c48827a1b2ac:/var/www/html$ load_module sysinfo ls id cd                                                                  
[*] Loaded module 'sysinfo' successfully
[*] Loaded module 'ls' successfully
[*] Loaded module 'id' successfully
[*] Loaded module 'cd' successfully

(C2) www-data@c48827a1b2ac:/var/www/html$ list_modules                                                                                  
+------------+---------+----------------------------------+---------------------+
|     ID     |   Name  |             Filepath             |         Date        |
+------------+---------+----------------------------------+---------------------+
| 523453412  | sysinfo | modules/sysinfo/sysinfo.php8.php | 2023/02/22 00:12:57 |
| 1915659346 |    ls   |      modules/ls/ls.php8.php      | 2023/02/22 00:12:57 |
| 238096256  |    id   |      modules/id/id.php8.php      | 2023/02/22 00:12:57 |
| 1992344736 |    cd   |      modules/cd/cd.php8.php      | 2023/02/22 00:12:57 |
+------------+---------+----------------------------------+---------------------+
Total memory in use: 7.82 KB

(C2) www-data@c48827a1b2ac:/var/www/html$ sysinfo                                                                                       
Hostname: c48827a1b2ac
IP: 172.19.0.2
OS: Linux c48827a1b2ac 5.15.0-58-generic #64-Ubuntu SMP Thu Jan 5 11:43:13 UTC 2023 x86_64
User: www-data
Path: /var/www/html/agent_c2.php
Version: 8.0.25

(C2) www-data@c48827a1b2ac:/var/www/html$ cd ..                                                                                         
(C2) www-data@c48827a1b2ac:/var/www$ ls                                                                                                 
                
  drwxr-xr-x  1      root      root      4096   2022/11/15 04:13:21  .      
  drwxr-xr-x  1      root      root      4096   2022/11/15 04:13:21  ..     
  drwxrwxrwx  1      www-data  www-data  4096   2023/02/21 22:58:28  html   

(C2) www-data@c48827a1b2ac:/var/www$ unload_module id                                                                                   
[*] Unloaded module 'id' successfully

(C2) www-data@c48827a1b2ac:/var/www$ list_modules                                                                                       
+------------+---------+----------------------------------+---------------------+
|     ID     |   Name  |             Filepath             |         Date        |
+------------+---------+----------------------------------+---------------------+
| 523453412  | sysinfo | modules/sysinfo/sysinfo.php8.php | 2023/02/22 00:12:57 |
| 1915659346 |    ls   |      modules/ls/ls.php8.php      | 2023/02/22 00:12:57 |
| 1992344736 |    cd   |      modules/cd/cd.php8.php      | 2023/02/22 00:12:57 |
+------------+---------+----------------------------------+---------------------+
Total memory in use: 6.63 KB

(C2) www-data@c48827a1b2ac:/var/www$ clean_modules                                                                                      
[*] Clean modules from agent successfully

(C2) www-data@c48827a1b2ac:/var/www$ list_modules                                                                                       
+----+------+----------+------+
| ID | Name | Filepath | Date |
+----+------+----------+------+
+----+------+----------+------+
Total memory in use: 0 B

(C2) www-data@c48827a1b2ac:/var/www$ exit                                                                                               
```

Para más información o consultar la guía de uso avanzado, visitar la wiki del proyecto.

## Contribuciones

Para contribuir en el proyecto: ya sea con nuevos agentes, modulos u otras funcionalidades, visita la wiki del proyecto. La sección de contribuciones detallará todo el proceso a realizar para cada caso de contribución.

## Bugs

Si se identifica algún error o anomalía con los agentes de Kraken, los módulos o con la propia herramienta, por favor, abrir un **issue** y se intentará solucionar ASAP.

