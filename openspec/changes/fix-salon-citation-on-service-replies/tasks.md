## 1. Prompt

- [x] 1.1 En el paso **Informar** de la plantilla inscripción/turno: citar sala si figura y, si `# SALONES` tiene Foto/Video, cerrar con `foto · recorrido` aunque no hayan preguntado el lugar
- [x] 1.2 Reescribir el ejemplo de masajes: tipos/precio/seña, `Se desarrolla en Sala Calma.`, `[foto](/static/salones/calma.jpg) · [recorrido](/static/salones/calma.mp4)`, luego WhatsApp/ID
- [x] 1.3 Ajustar la regla de salones: aplica al informar el servicio/actividad, no solo si preguntan por salones

## 2. Knowledge

- [x] 2.1 En `# SALONES`, aclarar que la plantilla se usa también al informar el servicio o la clase, no solo si preguntan el salón

## 3. Tests

- [x] 3.1 Asserts de prompt: ejemplo con `Sala Calma`, `[foto](/static/salones/calma.jpg)` y `[recorrido](/static/salones/calma.mp4)`
