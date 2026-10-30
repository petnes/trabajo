[P333]
La programación sigue un enfoque competencial y activo. El alumnado ocupa el centro del proceso y el profesorado hace de guía y de evaluador formativo, con la responsabilidad añadida de la seguridad en el taller. El ABP da la estructura general y se complementa con técnicas de aprendizaje cooperativo y con indagación apoyada en simuladores. Cuando un concepto lo requiere, se recurre a la instrucción directa.

[P334]
El proyecto avanza según un ciclo de siete fases que se repite, con distinto alcance, en cada situación de aprendizaje (figura 3). Arranca con la presentación del encargo mediante una pregunta motriz que se mantiene visible todo el curso, cómo garantizar que la huerta reciba el agua que necesita cuando el centro está vacío. Después se analiza el problema, traduciendo la necesidad en requisitos medibles, y se documentan las alternativas posibles. Le siguen el diseño con simulación previa y la construcción del prototipo. Las pruebas sirven para recoger datos y corregir fallos, y el ciclo termina con la comunicación pública y una reflexión sobre lo aprendido.

[P337]
Los equipos son estables, de cuatro personas, y cada integrante tiene un rol. Quien coordina gestiona el plan de trabajo y los plazos, y quien documenta mantiene al día el cuaderno de proyecto y la memoria. Quien se ocupa del material y la seguridad controla el inventario y vigila las normas del taller, mientras que quien verifica diseña las pruebas y registra los resultados. Los roles rotan en cada situación de aprendizaje, así que todo el alumnado pasa por todas las funciones y nadie se queda siempre en labores auxiliares.

[P338]
La instrucción directa también tiene su sitio. Contenidos como el acondicionamiento de la señal de un sensor resistivo, el divisor de tensión, la conversión de la lectura analógica en porcentaje o el relé que aísla el circuito de control del de potencia se explican brevemente antes de que los equipos los apliquen. La secuencia habitual es una explicación corta y una comprobación en el simulador antes de montar y verificar con polímetro. Con ese orden se reduce el riesgo de que la manipulación vaya por delante de la comprensión, algo sobre lo que ya advierten Krajcik y Blumenfeld (2006).

[P339]
Antes de montar nada, circuitos y programas se prueban con simuladores en línea. Esto permite ensayar sin coste ni riesgo y, a la vez, deja ver cómo razona el alumnado. Un montaje simulado se puede compartir y comentar. Solo se pasa al montaje físico cuando el comportamiento simulado cumple los requisitos acordados, y si luego las medidas reales no coinciden con lo simulado, la diferencia se analiza.

[P340]
El trabajo en la huerta, que es donde el sistema se prueba en condiciones reales, se concentra en el bloque doble de los jueves. Allí se hacen la instalación, la medida de la humedad del sustrato, la comprobación de caudales y el ajuste de goteros, con la misma exigencia de registro que en el taller.

[P341]
En cuanto a la seguridad, todo el sistema funciona en muy baja tensión, con un máximo de 12 V en corriente continua, y ningún montaje del alumnado se conecta directamente a la red. Si la instalación definitiva necesita esa conexión, la hace el profesorado o el personal de mantenimiento. Para usar la herramienta de corte, el taladro, la estación de soldadura o la impresora 3D hay que superar antes la lista de control de seguridad del anexo VII.

[P342]
Como el centro es de modelo D, la materia se imparte en euskera, y la terminología técnica se trabaja en euskera y en castellano junto con los términos ingleses más habituales en la documentación técnica y en los entornos de programación. Con ello cada equipo va construyendo un glosario trilingüe que forma parte de la memoria final y cuyo núcleo inicial recoge el anexo VIII.

[P343]
La atención a la diversidad forma parte de la metodología, en la línea del Diseño Universal para el Aprendizaje (CAST, 2018), y no se deja para el final. Cada explicación oral lleva apoyo visual y guion escrito, y las evidencias admiten formatos alternativos. El apartado 3.9 detalla las medidas concretas.

[P345]
La temporalización se ajusta al calendario escolar de Euskadi para el curso 2026-2027 y, con tres sesiones semanales, deja en torno a 101 sesiones efectivas una vez descontados vacaciones y festivos. La secuencia empieza a propósito por la representación gráfica y la electrónica, sin las que el proyecto no podría salir adelante, y el encargo se presenta a comienzos de diciembre. Hasta la defensa de finales de mayo pasan unas 21 semanas lectivas, algo más que la franja de 9 a 18 semanas que Zhang y Ma (2023) asocian a los mejores resultados. La diferencia se explica porque la cuarta situación de aprendizaje tiene una parte importante de instrucción sobre sensores y programación y porque en abril se reservan sesiones de holgura. En junio, el bloque de cierre trata los saberes de tecnología sostenible que el proyecto no cubre, como la arquitectura bioclimática y el transporte, junto con el plan de mantenimiento del sistema y la evaluación final. La figura 4 y la tabla 4 recogen la distribución anual.

[P382]
La tabla 5 recoge semana a semana el cronograma del periodo de proyecto, desde la presentación del encargo hasta la defensa pública. Las sesiones de holgura aparecen señaladas y dan margen para los retrasos habituales del taller sin que se muevan los hitos posteriores.

[P446]
El curso se organiza en seis situaciones de aprendizaje (SA) con la misma pregunta motriz, encadenadas porque cada una deja un resultado que la siguiente necesita. En la tabla 6 figuran el título y el producto final de cada SA, junto con las competencias específicas que trabaja de manera prioritaria.

[P477]
El sistema que construye el alumnado es un lazo de control sencillo, y de su arquitectura dependen muchas decisiones didácticas. El microcontrolador recibe la humedad del sustrato, medida por un sensor capacitivo; la temperatura y la humedad del aire de un sensor ambiental, y la hora de un reloj en tiempo real, que acota la franja en la que se puede regar. Con esa información decide si abre la electroválvula a través de un relé optoacoplado. Y como el agua aportada cambia la humedad del suelo, la salida vuelve a la entrada por vía física (figura 5).

[P480]
Se usa un sensor capacitivo y no uno resistivo, aunque este sea más barato, porque el resistivo se corroe por electrólisis tras pocas semanas en suelo húmedo. El alumnado lo puede comprobar en el aula, y sirve para trabajar la selección de materiales con un caso real.

[P481]
En el algoritmo aparecen dos ideas que el currículo incluye en el bloque de pensamiento computacional. Una es la histéresis. Con un único umbral, el sistema oscilaría alrededor de ese valor y la electroválvula se abriría y cerraría decenas de veces, mientras que con dos, uno inferior que dispara el riego y otro superior que lo detiene, el comportamiento se estabiliza. La otra es la ventana horaria, que impide regar fuera de la franja adecuada aunque la humedad haya bajado. El cuadro 1 recoge el pseudocódigo, y la figura 6, la respuesta del sistema simulado durante cuatro días.

[P522]
Más interesante resulta el hecho de que el algoritmo prevea qué hacer si el sensor falla. Un sensor desconectado da lecturas erráticas que un programa poco cuidadoso tomaría por suelo seco, y la válvula quedaría abierta sin límite. Por eso, ante cualquier lectura imposible, el sistema cierra el riego y registra el error. Esta regla sirve para que el alumnado vea que en cualquier sistema automático hay que definir de antemano cuál es el estado seguro si algo falla.

[P523]
Siguiendo las indicaciones del máster, se desarrollan por extenso la SA3 y la SA5, que se complementan. La SA3 concentra el análisis y la toma de decisiones, que son el núcleo del proceso tecnológico y la parte más difícil de sostener en el aula, porque durante semanas no hay un resultado tangible. La SA5 reúne en cambio la construcción y la validación del prototipo, donde se juntan los problemas de taller y de tiempo con el error técnico. Las dos están en los anexos I y II con el detalle suficiente para llevarlas directamente al aula.

[P525]
Los recursos se organizan en cuatro categorías. Los espacios son el aula taller de Tecnología y el aula de informática, a los que se suma la huerta escolar, siempre dentro del recinto del centro.

En los recursos humanos entran el profesorado de la materia y la consultoría de necesidades educativas especiales, que sigue las adaptaciones, junto con el personal de mantenimiento, para las conexiones eléctricas y de agua, y la comisión de la huerta, que hace de cliente del encargo y participa en la validación final. Puntualmente podría participar alguien del sector agrícola de la comarca para hablar del riego localizado.

[P526]
Los recursos digitales aparecen en la tabla 7. Todos funcionan en el navegador desde los ordenadores del centro, lo que es importante si en el aula de informática no se pueden instalar programas, y permiten el trabajo colaborativo.

[P550]
El material específico se detalla en la tabla 8, con un presupuesto calculado para que cada uno de los seis equipos construya su propio prototipo, más el material común de la instalación definitiva. Las cantidades son orientativas y se pueden ajustar según lo que ya tenga el departamento. No se cuenta el instrumental habitual del aula taller, como los polímetros, la herramienta manual, la estación de soldadura o la impresora 3D.

[P621]
El total, 504 €, es asumible con la dotación anual de un departamento de Tecnología, y baja si se prescinde de la ampliación fotovoltaica o si los equipos comparten la electroválvula durante los ensayos. Una parte del material se queda instalada en la huerta y se amortiza en los cursos siguientes, los componentes electrónicos vuelven al almacén del departamento y se reutilizan.

[P622]
Desde el punto de vista técnico, la propuesta es viable. Los componentes son de uso extendido en el ámbito educativo, con documentación abierta y coste reducido, así que no se depende de un proveedor concreto y reponerlos es sencillo. La muy baja tensión, ya comentada al hablar de la seguridad, deja el montaje dentro de lo que el alumnado puede manipular sin riesgo. La solución, por último, admite distintos grados de complejidad. Un equipo puede, por ejemplo, resolver el encargo con control por umbral y temporización mientras otro añade registro de datos o alimentación fotovoltaica, sin cambiar los requisitos ni los criterios de evaluación.

[P623]
Un proyecto largo, que depende de material físico y de condiciones ambientales reales, tiene riesgos que conviene prever. Los más probables aparecen en la tabla 9 junto con sus medidas de contingencia.

[P653]
Con los recursos del centro y dentro del horario asignado, el plan es realista, aunque tiene un punto frágil en el calendario de la fase final. Por eso la instalación definitiva se programa en abril y no en las últimas semanas del curso, de forma que un imprevisto en la huerta no llegue a comprometer la evaluación.
