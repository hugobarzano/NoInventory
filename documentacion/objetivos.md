#Especificación de objetivos  - Primera aproximación

##Objetivos portal web
###Portal web de administración

El portal web de administracion ha de ser capaz de gestionar todo lo relativo a los item del inventario

	-Crear
	-Eliminar
	-Actualizar
	-Solicitar pedido
	-Completar pedido
	-Consultar estado pedido
	-Generar informe

Funcionalidades tecnicas

	-Clasificar items por sus caracteristicas fisicas o funcionales para facilitar su futura localización. 
	-Establecer sistema de clasificación que facilite la localización del item
	-Información sensible (items perecederos, peligrosos, tratamiento especial)
	-Serializar los datos para su facil gestión

Para conseguir estos objetivos será necesario utilizar una api de serialización para trabajar con los datos en un formato estandar(JSON)

###Portal web clientes(opcional)

Entiendase portal web de clientes para posibles aplicaciones de compra-venta sobre catalogo o para empleaos
con menor rango de privilegios.

	-Busqueda en el inventario
	-Reserva
	-Solicitud
	-Compra
	-informacion basica(hoja de especificaciones)
	-Disponibilidad

Consideraciones de cara a producto comercial

	-Inventario público (de cara a compartir con tu lista de amigos que cosas tienes disponibles para prestarles)
	-Inventario público para empresas que trabajen en sectores relacionados. 
	-Control material mediante identificador QR (De cara a poder detectar facilmente items en zonas de trabajo)
	-Detecion de objetos 	

Seria interesante generalizar todo lo posible los modelos a utilziar para la base de datos, dando la posibilidad a cada negocio de crear
las caracteristicas de los items del inventario basandose en las caracteristicas de los objetos que van a manufacturar, de esta manera el abanico
de sectores que puedan interesarse por la aplicación será mayo ya que no estaría centrada en un tipo especifico. 

A medida que avance con el proyecto, modificaré dichos objetivos. 


###Aplicacion Realidad aumentada

Entiendase como aplicación de realidad aumentada una extension del portal web. La aplicación ha de ser capaz de 

	-Detectar items del inventario de manera individual
	-Dar la posibilidad de gestionarlo de igual forma que en el protal web
	-Facilitar la localización de un item especifico en el inventario
	-Avisar al administrador cuando un item especifico ha abandonado el inventario
	-Dar la posibilidad a empleados de registrar nuevos elementos en el inventario de manera sencilla.
	-Detectar items mediante actuadores 
	-Ser capaz de genera pedidos mediante la camara del dispositivo



	
	



















