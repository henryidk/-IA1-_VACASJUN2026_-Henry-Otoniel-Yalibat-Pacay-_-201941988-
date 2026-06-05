% Ciudades: departamentos de Guatemala
% Distancias en kilómetros 

:- dynamic ciudad/1, conexion/3.

% --- CIUDADES ---
ciudad(guatemala).
ciudad(antigua).
ciudad(chimaltenango).
ciudad(escuintla).
ciudad(quetzaltenango).
ciudad(huehuetenango).
ciudad(coban).
ciudad(chiquimula).
ciudad(zacapa).
ciudad(puerto_barrios).
ciudad(flores).
ciudad(retalhuleu).

% --- CONEXIONES (origen, destino, distancia_km) ---
% Las conexiones son bidireccionales (ver regla conectado/3)
conexion(guatemala, antigua, 45).
conexion(guatemala, chimaltenango, 54).
conexion(guatemala, escuintla, 60).
conexion(guatemala, coban, 215).
conexion(guatemala, zacapa, 148).
conexion(guatemala, chiquimula, 169).
conexion(antigua, chimaltenango, 20).
conexion(antigua, escuintla, 56).
conexion(chimaltenango, quetzaltenango, 120).
conexion(quetzaltenango, huehuetenango, 94).
conexion(quetzaltenango, retalhuleu, 65).
conexion(escuintla, retalhuleu, 110).
conexion(huehuetenango, coban, 340).
conexion(coban, flores, 360).
conexion(chiquimula, zacapa, 35).
conexion(zacapa, puerto_barrios, 186).
conexion(puerto_barrios, flores, 430).
conexion(coban, chiquimula, 210).

% --- REGLA DE CONECTIVIDAD BIDIRECCIONAL ---
conectado(X, Y, D) :- conexion(X, Y, D).
conectado(X, Y, D) :- conexion(Y, X, D).

% =====================================================================
% BÚSQUEDA DE RUTAS
% ruta(+Origen, +Destino, -Camino, -DistanciaTotal)
% Camino: lista de ciudades recorridas (incluye origen y destino)
% Visitados: lista interna para evitar ciclos
% =====================================================================

% Caso base: ya estamos en el destino
ruta_aux(Destino, Destino, _, [Destino], 0).

% Caso recursivo: avanzar a una ciudad vecina no visitada
ruta_aux(Actual, Destino, Visitados, [Actual|Resto], Distancia) :-
    conectado(Actual, Siguiente, D),
    \+ member(Siguiente, Visitados),
    ruta_aux(Siguiente, Destino, [Siguiente|Visitados], Resto, DistResto),
    Distancia is D + DistResto.

% Punto de entrada: inicializa la lista de visitados con el origen
ruta(Origen, Destino, Camino, Distancia) :-
    ruta_aux(Origen, Destino, [Origen], Camino, Distancia).

% =====================================================================
% RUTA MÁS CORTA Y ORDENAMIENTO
% =====================================================================

% Recopila todas las rutas y las ordena de menor a mayor distancia
todas_las_rutas(Origen, Destino, RutasOrdenadas) :-
    findall(Distancia-Camino, ruta(Origen, Destino, Camino, Distancia), Rutas),
    msort(Rutas, RutasOrdenadas).

% Devuelve únicamente la ruta con menor distancia total
ruta_mas_corta(Origen, Destino, Camino, Distancia) :-
    todas_las_rutas(Origen, Destino, [Distancia-Camino|_]).

% =====================================================================
% UTILIDADES PARA EL BACKEND
% =====================================================================

% Devuelve lista con todas las ciudades registradas
listar_ciudades(Ciudades) :-
    findall(C, ciudad(C), Ciudades).

% Verifica si una ciudad existe en la base de conocimiento
ciudad_valida(Ciudad) :-
    ciudad(Ciudad).

% Verifica si existe al menos una ruta entre dos ciudades
% El corte (!) evita explorar rutas innecesarias una vez encontrada la primera
hay_ruta(Origen, Destino) :-
    ruta(Origen, Destino, _, _), !.
