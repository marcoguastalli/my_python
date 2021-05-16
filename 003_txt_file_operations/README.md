# txt file operations
'r' read
'w' write
'a' append

Si a cualquiera de los anteriores le añadimos un “+” se convierte en modo de escritura y lectura.
Pero ambos (“r+”) y (“w+”) trabajan de manera diferente.
Al utilizar (“w+”) si el archivo existe será truncado, es decir, se borrara todo su contenido y se sobreescribirá en el.
No es así el caso de (“r+”). (a+) permanece igual, solo que al agregarle un + si el fichero no existe sera creado.

Recuerda que tanto “w” como “w+” van a truncar los archivos en caso de existir, por lo que si abres un file existente el mismo será sobrescrito y perderás su contenido.

### inspiring links
https://pythones.net/archivos-en-python-3/
