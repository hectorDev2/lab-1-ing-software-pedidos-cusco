# Sabor Cusqueño

Proyecto del **Laboratorio 1: Introducción al entorno de desarrollo y Git** de Ingeniería de Software.

Sabor Cusqueño es una aplicación web estática para que una startup de Cusco pueda mostrar comida local y gestionar un pedido básico desde el navegador.

## Funcionalidades

- Visualización de platos típicos de Cusco.
- Agregado de productos al pedido.
- Cálculo automático del total.
- Confirmación y vaciado del pedido.
- Diseño responsive para escritorio y celular.

## Tecnologías

- HTML5 semántico.
- CSS3 con diseño responsive.
- JavaScript vanilla.
- Git y GitHub para el control de versiones.

## Ejecutar el proyecto

No requiere instalación de dependencias ni proceso de build. Abrí `index.html` directamente en un navegador o usá la extensión **Live Server** de Visual Studio Code.

```bash
git clone URL_DEL_REPOSITORIO
cd lab-1-ing-software-pedidos-cusco
```

## Estructura

```text
.
├── app.js       # Menú, carrito y lógica de pedidos
├── index.html   # Estructura principal de la aplicación
├── styles.css   # Estilos y responsive design
└── README.md    # Documentación del proyecto
```

## Flujo de Git utilizado

```bash
git init
git add .
git commit -m "chore: initialize food ordering project"
git remote add origin URL_DEL_REPOSITORIO
git branch -M main
git push -u origin main
```

## Evidencia de commits

El historial del repositorio se puede consultar con:

```bash
git log --oneline --decorate
```

Los commits usan el formato **Conventional Commits** para que el historial sea claro y fácil de revisar.

## Reflexión

### ¿Por qué Git es crítico en proyectos colaborativos?

Git permite que varias personas trabajen sobre el mismo código con trazabilidad. Cada commit representa un cambio acotado que se puede revisar, comparar y recuperar. Además, las ramas permiten desarrollar funcionalidades sin romper la versión estable.

### ¿Qué problemas evita?

Evita perder cambios, sobrescribir accidentalmente el trabajo de otra persona y no saber quién modificó una parte del sistema. También permite volver a una versión anterior cuando una modificación introduce un error.

## PDF del laboratorio

La memoria visual del proyecto está disponible en [`docs/laboratorio-1-sabor-cusqueno.pdf`](docs/laboratorio-1-sabor-cusqueno.pdf). Incluye el caso práctico, fotografías de referencia, una vista conceptual del prototipo, evidencia de commits y la reflexión final.

Para regenerarlo:

```bash
python3 docs/generate_pdf.py
```

Las fotografías de referencia fueron descargadas desde Unsplash y se conservan en `docs/assets/`.
