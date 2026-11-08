# DRIPCORNER.ES · Anuncio vertical 9:16 · 45 s

Kit de producción. Las escenas 1–5 (animación 3D con personajes) se generan con una
herramienta de vídeo IA (Veo, Kling, Runway, Sora, Hailuo…) usando los prompts de abajo.
La escena 6 (cierre de marca) ya está renderizada en `output/escena6_dripcorner_cierre.mp4`
y se puede regenerar con `python3 scripts/end_card.py`.

Subtítulos listos: `subtitulos_dripcorner.srt`.

---

## Personajes (usar SIEMPRE la misma descripción en cada prompt para mantener la coherencia)

- **LEO (protagonista):** chico de 17 años, piel morena clara, pelo negro corto con degradado,
  mandíbula marcada, mirada segura. Sudadera negra lisa oversize, pantalón cargo gris,
  zapatillas blancas y grises modernas, cadena plateada gruesa, bandolera negra de cuero.
- **DANI:** chico de 16 años, pelo castaño oscuro rizado, sonrisa amplia, camiseta blanca lisa.
  Personaje original: no copiar el parecido de ninguna persona real.
- **LUCÍA:** chica de 16 años, pelo castaño largo con coleta alta, top beige y chaqueta vaquera.

> Truco de coherencia: genera primero una imagen de referencia de cada personaje y úsala
> como *image reference / character reference* en todas las escenas.

**Estilo base para añadir al final de cada prompt:**
`stylized 3D animation, Pixar-like cinematic quality, expressive realistic facial animation,
soft global illumination, shallow depth of field, smooth cinematic camera, vertical 9:16, 4K`

---

## Escena 1 · El aula (0–5 s)

**Prompt:** Modern American high school classroom, warm afternoon light through large windows.
Several teenagers chatting at their desks. DANI (curly dark hair, plain white t-shirt) leans back
and talks, shrugging, slightly annoyed. LUCÍA nods next to him. Slow dolly-in toward Dani.

| Tiempo | Personaje | Diálogo |
|---|---|---|
| 0.3–2.6 | DANI | «Tío, es que las marcas buenas están carísimas.» |
| 2.7–4.8 | LUCÍA | «Ya ves… imposible ir bien vestido.» |

## Escena 2 · Entra el protagonista (5–12 s)

**Prompt:** The classroom door swings open, LEO walks in confidently (black oversized hoodie,
grey cargo pants, modern white-grey sneakers, thick silver chain, black leather crossbody bag).
Everyone turns their heads. Slow-motion close-ups: sneakers stepping, silver chain catching the
light, crossbody bag, then a low-angle shot of Leo's confident face. Low-angle tracking shot.

| Tiempo | Personaje | Diálogo |
|---|---|---|
| 8.5–10.5 | LUCÍA (susurrando) | «Madre mía… ¿has visto a Leo?» |

## Escena 3 · Conversación (12–20 s)

**Prompt:** Leo sits down; Dani and Lucía turn toward him, surprised and curious. Over-the-shoulder
shots alternating between faces, natural reactions, Leo smiles calmly and answers with confidence.

| Tiempo | Personaje | Diálogo |
|---|---|---|
| 12.2–14.0 | DANI | «Bro, ¿de dónde sacas todo eso?» |
| 14.1–15.8 | LUCÍA | «¿Cuánto te ha costado?» |
| 16.0–19.7 | LEO | «Menos de lo que crees. Todo de DRIPCORNER.ES.» |

## Escena 4 · Salida del instituto (20–29 s)

**Prompt:** Golden-hour sunset, Leo walks out of the high school main entrance with Dani and Lucía,
slow motion, wide full-body shot from the front, then close-ups of hoodie, chain and sneakers,
lens flare, warm cinematic color grading.

| Tiempo | Personaje | Diálogo |
|---|---|---|
| 21.0–25.0 | LEO (voz en off) | «Calidad, estilo y precios que sí puedes pagar.» |

## Escena 5 · Estilo de vida (29–38 s)

**Prompt:** Leo leans against a sleek black luxury sports car (no visible logos or badges) in a
modern parking lot at dusk, speaks directly to camera with a confident smile. Then quick montage:
modern city skyline at night, sports cars driving by, neon urban streets.

| Tiempo | Personaje | Diálogo |
|---|---|---|
| 29.5–33.5 | LEO (a cámara) | «Si quieres ir a otro nivel, ya sabes dónde mirar.» |

## Escena 6 · Promoción final (38–45 s): ya renderizada ✅

`output/escena6_dripcorner_cierre.mp4`: transición con barras diagonales, logo DRIPCORNER.ES
animado letra a letra, «TU ESTILO, A OTRO NIVEL», «DESCUBRE DRIPCORNER.ES» y «LINK EN LA BIO»
con pulsos sincronizados al beat (140 BPM).

*Opcional:* antes del logo, 1–2 s de planos rápidos de tus productos reales (fotos de la tienda).

---

## Voces y lip-sync

1. Genera las voces con ElevenLabs u otra herramienta similar: voces juveniles, **español de España**.
2. Si tu generador de vídeo no hace lip-sync, aplícalo después (Kling Lip Sync, Hedra, Sync Labs…).

## Montaje final (CapCut / Premiere / DaVinci)

1. Pon en orden los clips de las escenas 1–5 y añade `escena6_dripcorner_cierre.mp4` al final.
2. Importa `subtitulos_dripcorner.srt` y aplícales el estilo: tipografía gruesa, blanca con borde
   negro y la palabra clave en amarillo (#FFD600).
3. Música: beat urbano/trap sin copyright, a unos 140 BPM, con la voz por encima (ducking).
4. Exporta en 1080×1920, 30 fps. No debe salir ningún nombre ni marca de agua de otras cuentas.

## Notas

- Usa personajes originales. Imitar a una persona real (por ejemplo, un futbolista famoso) en un
  anuncio puede violar sus derechos de imagen e insinuar un patrocinio que no existe.
- Pasa lo mismo con el coche: un deportivo negro genérico sin logos evita problemas de marca registrada.
