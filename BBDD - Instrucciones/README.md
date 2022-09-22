# Bioseñales-HW

<p align="center">
<img src="https://user-images.githubusercontent.com/46607004/154055355-a45a597b-4c16-4460-a285-ad0554636bdf.png" alt="drawing" width="200"/>
</p>

La base de datos que está creada en la raspberry pi con la que se está trabajando es POSTGRESQL, por lo que lo primero que hay que hacer,
es instalar POSTGRESQL en el dispositivo, se hace mediante la consola de raspbian (Control + Alt + t).

--> sudo apt install postgresql

Una vez instalado, lo primero es crear un usuario con contraseña, que será el que se use para la copia de datos desde un CSV en Desktop
hacia la Base de Datos. Debido a esto, es necesario darle privilegios de SUperusuario para que no haya problemas.
De nuevo en la consola del terminal:

--> sudo su postgres                         (Te  introduces en la aplicación de POSTGRESQL)
--> psql 			                         (A partir de ahora todas las funciones serán en SQL) 
--> CREATE USER nombre WITH PASSWORD '1234'; (No es obligatorio poner con mayusculas, pero si el ";")
--> ALTER ROLE nombre WITH SUPEUSER;         (Se le dan privilegios de superusuario al usuario recien creada)
--> \du                                      (para observar los usuarios que existen y sus privilegios)

Una vez ya se tiene creado el usuario, se puede proceder a crear una Base de datos (Terminal):

--> CREATE DATABASE nombre_DB;  // Se crea la base de datos

Se crean las tablas que van a ser necesarias, en principio una por sensor (Terminal):

--> CREATE TABLE nombreTable (nombreCol tipodato, nombreCol2 tipodato);

Para visualizar la tabla (Terminal):

--> SELECT * FROM nombreTable;  // No me gusta demasiado la verdad

Para borrar el contenido de la tabla (Terminal):

--> DELETE FROM nombreTable;
