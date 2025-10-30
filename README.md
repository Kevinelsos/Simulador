# Cliente Simulador RCSS


Este cliente de Robo Cup Soccer Simulator permite recibir un archivo de formación con el que instanciará una serie de procesos, cada uno con un comportamiento distinto dependiendo del comportamiento que se programe.

## Estructura del proyecto
La estructura de los archivos es la siguiente:

~~~ bash
src
├── main.py
├── models.py
├── handler.py
├── behaviors.py
├── cli.py
├── file.py
└── config.py
~~~

Donde cada archivo tiene un motivo especial para su existencia. 

#### Main
*main.py* es el punto de entrada de la aplicación y donde se deja claro el flujo de funcionamiento de esta.
Primero parsea los argumentos de entrada de la aplicación (archivo de formación, ip y puerto del servidor; y delay en la creación de los jugadores),
sigue con la lectura del archivo de formación y transformandolo en una lista de `Player`, 
con esta lista genera una serie de procesos donde el comportamiento de cada uno puede variar dependiendo del `Role` del jugador,
y finalmente ejecuta los procesos creados.

#### Models

*models.py* es el módulo que se encarga de la abstracción de los modelos importantes. Aqui están definidos el `Player` con sus posibles acciones y su `Behavior`,
así como su `Role` y `Client`. El rol es básicamente el tipo de jugador y de este dependerá el comportamiento que tendrá al momento de jugar un partido.
El cliente también es muy importante ya que se encarga de la conexión con el servidor tanto para recibir como para enviar datos.
`Behavior` es una clase abstracta que permite que el jugador pueda tener un comportamiento de los que están definidos en *behaviors.py*

#### Handler
En *handler.py* se manejan todos los procesos jugadores.
Asi que tiene una función base llamada `player_handler` que recibe a un `Player` e inicia su comportamiento. 
También tiene la función para generar todos los procesos que se conectaran al servidor, 
estos los crea en base al método handler antes mencionado

#### Behaviors
*behaviors.py* es el encargado de definir los comportamientos de los jugadores dependiendo de las respuestas que retorna el servidor.
Estos comportamientos son los del GoalKeeper, los Defensas, los medio campistas y los delanteros. este podría ser en un futuro el archivo más complejo, puesto que tiene que parsear el estado del servidor y definir los comportamientos en base a eso.

#### CLI
*cli.py*, como módulo, se encarga del parseo de los argumentos de entrada. Por defecto solo es necesario pasar el archivo de formación, pero se puede pasar también la ip del servidor, el puerto y el delay para crear a los jugadores.

#### File
el módulo *file.py* se encarga de recibir el archivo de formación y parsearlo en los jugadores, creando también sus clientes y adjudicando sus comportamientos a cada uno.

#### Config
en *config.py* se definen los parámetros por defecto de la aplicación, la ip y el puerto del servidor; el timeout del socket y el delay al crear los jugadores.

