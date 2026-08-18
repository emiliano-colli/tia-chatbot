## 1. Copy and layout

- [x] 1.1 Reemplazar el subtítulo del header en `app/static/index.html` por `Preguntame sobre clases de yoga, entrenamiento funcional, talleres, servicios de salud, bienestar y más 🌿`
- [x] 1.2 Ajustar CSS en el mismo archivo: wrap del header (`flex: 1; min-width: 0`), toolbar que envuelve o apila bajo ~480px, input del composer con `min-width: 0`, `overflow-x: hidden` y `min-height: 100dvh` con fallback `100vh`

## 2. Verification

- [x] 2.1 Extender `test_get_root_returns_html` para afirmar el subtítulo nuevo
- [x] 2.2 Correr pytest del test de UI interna
- [x] 2.3 Revisar a ~360px (DevTools o celular): título, subtítulo, “Nueva consulta” y “Enviar” visibles sin scroll horizontal
