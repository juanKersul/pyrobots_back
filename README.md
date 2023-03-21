# Deploy App

Para utilizar ésta app seguir los siguientes pasos:

1. Clonar el repositorio.
    ```sh
    $ git clone https://github.com/Becarfuliate/Becarfuliate-Back.git
    ```
2. Ubicarse en el directorio Becarfuliate-Back.
    ```sh
    $ cd Becarfuliate-Back/
    ```
    > (Donde se ubica el main.py y directorios de la estructura)

3. Dar permisos al script de deploy.
    ```sh
    $ chmod 700 deployBack.sh
    ```
4. Ejecutar el scritp de deploy.
    ```sh
    $ ./deployBack.sh
    ```
> deployBack.sh es un script que automatiza la **creación del entorno virtual** y **primer despliegue** de esta aplicación. Luego del **primer uso** uso de esta herramienta, se recomienda el despliegue manual de la aplicación, el mismo se encuentra especificado desde el paso 3 de **"Deploy sin script"** (saltar el paso 4). Del mismo modo se recomieda la instalación del gestor **sqlite3** para un acceso cómodo a la base de datos.
    
### Deploy sin script

1. Instalar gestor de bd
    ```sh
    $ sudo apt-get update
    $ sudo apt-get install sqlite3
    ```
2. Crear entorno virtual
    ```sh
    $ sudo apt-get install virtualenv
    $ virtualenv -p /usr/bin/python3 <nombre>
    ```

3. Activar el entorno virtual
    ```sh
    $ source <nombre>/bin/activate
    ```
    > Para desactivar venv: ```$ deactivate```

4. Instalar los requeriments
    ```sh
    $ pip install -r requeriments.txt
    ```
5. Levantar el servidor de FastApi
    ```sh
    $ uvicorn main:app --reload
    ```
6. Consumir las documentaciones de FastAtpi

* http://127.0.0.1:8000/docs
OR
* http://127.0.0.1:8000/redoc

# Endpoints and request

## Indice
* [Login](#login)
    * [Request](#login-request)
    * [Response](#login-response)
* [Register](#register)
    * [Request](#register-request)
    * [Response](#register-response)
* [Verify](#verify)
    * [Request](#verify-request)
    * [Response](#verify-response)
* [Crate Match](#create-match)
    * [Request](#create-match-request)
    * [Response](#create-match-response)
* [Read Matchs](#read-matchs)
    * [Request](#matchs-request)
    * [Response](#matchs-response)
* [Read Robots](#read-robots)
    * [Request](#robots-request)
    * [Response](#robots-response)

## Login

Method: POST
Endpoint: '/login'

### Login Request

Type: Request Body

```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

### Login Response

#### Case: Success Login

Descripción: "Username o email correctos y contraseña correcta"
Status Code: 200 Successful Response

Response Body:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiJ1c2VyIiwiZXhwaXJ5IjoiMjAyMi0xMC0yMiAxMDoyMjoyMS4yNDQyNzYifQ.Lw6VbjurMIzZi9vOl_wrubUXhIAH_NZOkIHQQ8CZFCw"
}
```

#### Case: Incorret Password

Descripción: "Contraseña incorrecta"
Status Code: 400 Bad Request

Response Body:
```json
{
  "detail": "contrasenia incorrecta"
}
```

#### Case: Unverified User

Descripción: "Email no verificado"
Status Code: 400 Bad Request

Response Body:
```json
{
  "detail": "email no verificado"
}
```

#### Case: User Not Exist

Descripción: "No se agrega usuario ni mail, o el usuario o mail no existente"
Status Code: 400 Bad Request

Response Body:
```json
{
  "detail": "no existe el usuario"
}
```


## Register

Method: POST
Endpoint: '/register'

### Register Request

Type: Request Body

```json
{
  "username": "string",
  "password": "string",
  "email": "string"
}
```

### Register Response

#### Case: Register Success

Status Code: 200 Successful Response

Response Body:
```json
{
  "Status": "Usuario agregado con exito"
}
```

#### Case: Password Too Short And Empty Password

Descripción: "Contraseña con menos de 8 caracteres ó vacía"
Status Code: 422 Unprocessable Entity

Response Body:
```json
{
  "detail": [
    {
      "loc": [
        "body",
        "password"
      ],
      "msg": "La longitud mínima es de 8 caracteres.",
      "type": "value_error"
    }
  ]
}
```
#### Case: Password Not Have Special Character

Descripción: "Contraseña sin caracter especial"
Status Code: 422 Unprocessable Entity

Response Body:
```json
{
  "detail": [
    {
      "loc": [
        "body",
        "password"
      ],
      "msg": "Debe contener al menos un caracter especial",
      "type": "value_error"
    }
  ]
}
```
#### Case: Password Not Have Number

Descripción: "Contraseña sin caracter numérico"
Status Code: 422 Unprocessable Entity

Response Body:
```json
{
  "detail": [
    {
      "loc": [
        "body",
        "password"
      ],
      "msg": "Debe contener al menos un numero",
      "type": "value_error"
    }
  ]
}
```
#### Case: Invalid Email And Empty Email

Descripción: "Email inválido ó campo vacío"
Status Code: 422 Unprocessable Entity

Response Body:
```json
{
  "detail": [
    {
      "loc": [
        "body",
        "email"
      ],
      "msg": "Email invalido",
      "type": "value_error"
    }
  ]
}
```

#### Case: Empty Username 

Descripción: "Nombre de usuario vacío"
Status Code: 422 Unprocessable Entity

Response Body:
```json
{
  "detail": [
    {
      "loc": [
        "body",
        "username"
      ],
      "msg": "El usuario no puede ser vacio",
      "type": "value_error"
    }
  ]
}
```


## Verify

Method: GET
Endpoint: '/verify'

### Verify Request

Type: Parameters (_por lo tanto no usa json_)

```
{
  "username": "string",
  "code": 0,
}
```

### Verify Response

#### Case: Verify Success

Descripción: "Se agrega username válido y code"
Status Code: 200 Successful Response

```json
{
  "Status": "Usuario confirmado con exito"
}
```

#### Case: User not exist

Descripicón: "Se quiere verificar un usuario que no existe o vacío"
Status Code: 400 Bad Request

```json
{
  "detail": "El usuario <username> no existe"
}
```

#### Case: Invalid Code

Descripicón: "Code vacío o inválido"
Status Code: 400 Bad Request

```json
{
  "detail": "El usuario <username> no existe"
}
```

## Create Match

Method: POST
Endpoint: '/match/add'

### Create Match Request

Type: Request Body

```json
{
  "name": "string",
  "max_players": 0,
  "min_players": 0,
  "password": "string",
  "n_matchs": 0,
  "n_rounds_matchs": 0,
  "user_creator": "string",
  "token": "string"
}
```

### Create Match Response

#### Case: Match Add Success

Descripción: "Se agregan todos los campos válidos"
Status Code: 200 Successful Response

Response Body:
```json
{
  "Status": "Match added succesfully"
}
```

#### Case: Invalid Max Players

Descripicón: "El máximo de jugadores no está entre 2 y 4"
Status Code: 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "max_players"
      ],
      "msg": "El valor debe estar entre 2 y 4",
      "type": "value_error"
    }
  ]
}
```

#### Case: Invalid Min Players

Descripicón: "El mínimo de jugadores no está entre 2 y 4"
Status Code: 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "min_players"
      ],
      "msg": "El valor debe estar entre 2 y 4",
      "type": "value_error"
    }
  ]
}
```

#### Case: Invalid Num Matchs

Descripicón: "El mínimo de juegos no está entre 1 y 200"
Status Code: 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "n_matchs"
      ],
      "msg": "El valor debe estar entre 1 y 200",
      "type": "value_error"
    }
  ]
}
```

#### Case: Invalid Num Rounds

Descripicón: "El mínimo de rondas no está entre 2 y 10.000"
Status Code: 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "n_rounds_matchs"
      ],
      "msg": "El valor debe estar entre 2 y 10.000",
      "type": "value_error"
    }
  ]
}
```

#### Case: Invalid UserCreator

Descripicón: "El creador de la partida no es un usuario válido"
Status Code: 400 Bad Request

```json
{
  "detail": "El usuario no existe"
}
```

#### Case: Invalid Name

Descripicón: "Nombre de la partida vacío"
Status Code: 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "name"
      ],
      "msg": "El nombre no puede ser vacío",
      "type": "value_error"
    }
  ]
}
```

#### Case: Invalid Type

Descripicón: "Se introduce un str en un campo numérico"
Status Code: 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "max_players"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```


## Read Matchs

Method: GET
Endpoint: '/matchs'

### Matchs Request

Type: Parameters

```json
{
  "token": "string"
}
```

### Matchs Response

#### Case: Match List Success

Descripción: "Se agrega token válido, se listan las partidas"
Status Code: 200 Successful Response

Response Body:
```json
[
  {
    "name": "LichiPa",
    "max_players": 4,
    "min_players": 2,
    "password": "string",
    "n_matchs": 4,
    "n_rounds_matchs": 4,
    "id": 1
  },
  {
    "name": "LichiPa2",
    "max_players": 4,
    "min_players": 2,
    "password": "string",
    "n_matchs": 4,
    "n_rounds_matchs": 4,
    "id": 2
  }
]
```

#### Case: Ivalid Token

Descripicón: "Token no válido"
Status Code: 500 Internal Server Error

```json
Internal Server Error
```

## Read Robots

Method: GET
Endpoint: '/robots'

### Robots Request

Type: Parameters

```json
{
  "token": "string"
}
```

### Robots Response

#### Case: Robot List Success

Descripción: "Se agrega token válido, se listan los robots"
Status Code: 200 Successful Response

Response Body:
```json
[
  {
    "name": "Krlos",
    "avatar": "asdf",
    "matchs_pleyed": 2,
    "matchs_won": 2,
    "avg_life_time": 80,
    "id": 5
  }
]
```

#### Case: Ivalid Token

Descripicón: "Token no válido"
Status Code: 500 Internal Server Error

```json
Internal Server Error
```
