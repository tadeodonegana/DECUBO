# DECUBO: Diminuta Evaluación Cultural Bonaerense

DECUBO es un benchmark diseñado para evaluar la comprensión contextual de modelos de lenguaje en textos literarios situados en la Provincia de Buenos Aires, Argentina. Este proyecto se centra en la evaluación de las capacidades de los LLMs (Modelos de Lenguaje de Gran Escala) para interpretar referencias culturales, geográficas y lingüísticas específicas de la región bonaerense.

## Descripción

Los modelos de lenguaje han mostrado un desempeño destacado en tareas de procesamiento de texto, pero su efectividad varía significativamente según el contexto cultural y lingüístico. DECUBO aborda esta problemática mediante un corpus literario compuesto por textos de autores bonaerenses, evaluando cinco modelos de lenguaje prominentes:

- GPT-4
- Claude 2.1
- Llama 3 70B
- Llama 3 8B
- Mistral 7B

### Objetivos

1. **Evaluar sesgos culturales y lingüísticos** en LLMs.
2. **Medir la comprensión de textos literarios regionales.**
3. **Analizar el rendimiento de los modelos en tareas culturalmente situadas.**

## Estructura del Proyecto

- **Corpus de Textos:** Selección de 20 textos literarios representativos de la región bonaerense.
- **Dataset de Preguntas:** 68 preguntas de opción múltiple diseñadas para evaluar la comprensión contextual de los textos.
- **Modelos Evaluados:** Pruebas realizadas con cinco LLMs utilizando Amazon Bedrock.

## Resultados

Los resultados preliminares y ajustados muestran un rendimiento superior de GPT-4 y Llama 3 70B con una precisión de más del 90%. Los modelos más pequeños exhibieron limitaciones significativas, especialmente en la interpretación de referencias culturales y geográficas.

| Modelo     | Precisión Ajustada |
|------------|--------------------|
| GPT-4      | 93.10%             |
| Llama 3 70B| 91.18%             |
| Claude 2.1 | 72.06%             |
| Mistral 7B | 70.59%             |
| Llama 3 8B | 66.18%             |

## Uso del Benchmark

El benchmark está diseñado en formato CSV siguiendo el modelo de MMLU, con columnas que incluyen las preguntas, opciones de respuesta y la respuesta correcta.

### Paper

Puedes encontrar el paper [aqui]().
