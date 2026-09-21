1er Domian/ports

En esta capa se almacenan las entidades del sistema, en este ToDo en concreto, el sistema trbaja con el nombre de la tarea y su estado de terminada. A su vez, contine la rama ports aqui se definen las interfaces/contratos que se tienen que emplear en la insfraestrcutura

2do use\_case

Aqui se almacena toda la logica de negocio, y los casos de usa que tendra el sistema, en este caso, aqui se alacnen los siguientes casos de uso:

-   crearTarea
-   listarTareas
-   modificarTareas 

los casos de uso se implementan desde los contratos que ya tomo la infraestrtuctura

3er infraestrtuctura
Aqui hay implementaciones concretas, memoeria, base de datos etc. esta capa implementa los contratos y permite que los casos de uso los use

4to interfaces
Aqui se manejan las clases que van atener la interaccion externa del sistema, estas no conocen la logica del neogocio, si como seimplementan

el dominio define el contrato, la infraestructura lo implementa, y los casos 
de uso lo usan
![alt text](image.png)