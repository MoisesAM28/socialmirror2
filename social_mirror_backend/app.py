print("🔥 APP.PY FINAL 🔥")
from flask import Flask, request, jsonify
import os
import time
import random
from predict import predecir_emocion

# ==============================
# 🧠 PREGUNTAS
# ==============================
preguntas = [
    "Hola 😊 ¿Cómo te sientes hoy?",
    "Cuéntame algo que te haya hecho feliz",
    "¿Cómo reaccionas cuando algo sale mal?",
    "¿Qué haces cuando estás triste?",
    "¿Qué te preocupa últimamente?",
    "¿Qué te hace sentir tranquilo?",
    "¿Cómo estuvo tu día?",
    "¿Qué te hizo sonreír hoy?",
    "¿Te sientes cansado o con energía?",
    "¿Prefieres estar solo o acompañado cuando estás mal?",
    "¿Qué te motiva a seguir adelante?",
    "¿Hay algo que quisieras cambiar de hoy?",
    "¿Qué haces cuando te enojas?",
    "¿Te sientes estresado últimamente?",
    "¿Qué te ayuda a relajarte?",
    "¿Qué es lo mejor que te ha pasado esta semana?",
    "¿Cómo te describirías en este momento?",
    "¿Qué te gustaría hacer ahora mismo?",
    "¿Te sientes escuchado por los demás?",
    "¿Hay algo que quieras sacar de tu mente?"
]

indice_pregunta = 0

app = Flask(__name__)
os.makedirs("uploads", exist_ok=True)

# ==============================
# 🧠 ANÁLISIS DE TEXTO
# ==============================
def analizar_texto(texto):
    texto = texto.lower()

    if any(p in texto for p in ["hola", "hey", "buenas"]):
        return "saludo"
    elif any(p in texto for p in ["feliz", "bien", "genial", "contento"]):
        return "positivo"
    elif any(p in texto for p in ["triste", "mal", "deprimido"]):
        return "negativo"
    elif any(p in texto for p in ["enojado", "molesto", "furioso"]):
        return "enojo"
    elif any(p in texto for p in ["cansado", "agotado"]):
        return "cansancio"
    elif any(p in texto for p in ["estresado", "presionado"]):
        return "estres"
    else:
        return "neutral"

# ==============================
# ⚠ DETECTAR CONTRADICCIÓN
# ==============================
def detectar_contradiccion(intencion, emocion):
    if intencion == "positivo" and emocion in ["sad", "angry"]:
        return True
    if intencion == "negativo" and emocion == "happy":
        return True
    return False

# ==============================
# 🤖 RESPUESTAS HUMANAS
# ==============================
respuestas_happy = [
    "Qué bien 😄, me alegra escucharlo. ¿Qué lo hizo especial?",
    "Se nota esa buena energía ✨ ¿qué pasó?",
    "Genial 😄 sigue así, ¿quieres contarme más?"
]

respuestas_sad = [
    "Lo siento 😢, aquí estoy para escucharte. ¿Qué pasó?",
    "Parece que no fue un buen momento… ¿quieres hablarlo?",
    "No tienes que guardártelo, cuéntame un poco más 💙"
]

respuestas_angry = [
    "Se nota el enojo 😠 ¿qué ocurrió?",
    "Entiendo… a veces pasa. ¿Qué lo provocó?",
    "Respira un poco 😤 ¿quieres contarme qué pasó?"
]

respuestas_neutral = [
    "Interesante 🤔 cuéntame más.",
    "Ya veo… ¿y cómo te hace sentir eso?",
    "Hmm 🤔 quiero entender mejor, dime más."
]

# ==============================
# 🤖 GENERADOR DE RESPUESTA
# ==============================
def generar_respuesta_realista(texto, emocion):
    intencion = analizar_texto(texto)
    contradiccion = detectar_contradiccion(intencion, emocion)

    # 🎭 SALUDO
    if intencion == "saludo":
        return random.choice([
            "Hola 😊 ¿cómo estás hoy?",
            "Hey 👋 ¿cómo te sientes?",
            "Hola 🙂 me alegra verte, cuéntame algo"
        ])

    # ⚠ CONTRADICCIÓN
    if contradiccion:
        return random.choice([
            "Dices algo diferente a lo que expresas… ¿todo bien realmente?",
            "Parece que hay algo más detrás de lo que dices 🤔 ¿quieres hablarlo?",
            "Tu expresión y tus palabras no coinciden… cuéntame más"
        ])

    # 🎯 RESPUESTAS SEGÚN EMOCIÓN
    if emocion == "happy":
        return random.choice(respuestas_happy)
    elif emocion == "sad":
        return random.choice(respuestas_sad)
    elif emocion == "angry":
        return random.choice(respuestas_angry)
    else:
        return random.choice(respuestas_neutral)

# ==============================
# 🚀 ENDPOINT PRINCIPAL
# ==============================
@app.route("/emocion", methods=["POST"])
def detectar_emocion():
    global indice_pregunta

    print("\n🔥 NUEVA PETICIÓN 🔥")

    try:
        if 'file' not in request.files:
            print("❌ No llegó archivo")
            return jsonify({"error": "No file"}), 400

        file = request.files['file']
        texto = request.form.get("texto", "")

        print(f"💬 Texto: {texto}")

        filename = str(int(time.time())) + ".jpg"
        filepath = os.path.join("uploads", filename)
        file.save(filepath)

        print(f"📸 Imagen guardada en: {filepath}")

        # 🧠 MODELO
        print("➡️ Ejecutando modelo...")
        inicio = time.time()

        try:
            emocion, feedback_modelo = predecir_emocion(filepath)
        except Exception as e:
            print("💥 ERROR EN MODELO:", e)
            emocion = "error"
            feedback_modelo = "Error al procesar la emoción"

        fin = time.time()
        print(f"⏱ Tiempo modelo: {fin - inicio:.2f}s")
        print(f"😊 Emoción detectada: {emocion}")

        # 🤖 RESPUESTA
        respuesta_social = generar_respuesta_realista(texto, emocion)

        pregunta_actual = preguntas[indice_pregunta]

        feedback_final = (
            f"🧠 Pregunta: {pregunta_actual}\n"
            f"💬 Dijiste: '{texto}'\n"
            f"😊 Emoción detectada: {emocion}\n\n"
            f"🤖 Respuesta: {respuesta_social}\n\n"
            f"📊 Análisis del modelo: {feedback_modelo}"
        )

        print("✅ RESPUESTA ENVIADA\n")

        return jsonify({
            "emocion": emocion,
            "feedback": feedback_final,
            "respuesta": respuesta_social
        })

    except Exception as e:
        print("💥 ERROR GENERAL:", e)
        return jsonify({
            "error": "Error interno",
            "detalle": str(e)
        }), 500

# ==============================
# 📌 PREGUNTA ACTUAL
# ==============================
@app.route("/pregunta", methods=["GET"])
def obtener_pregunta():
    global indice_pregunta

    return jsonify({
        "pregunta": preguntas[indice_pregunta],
        "indice": indice_pregunta
    })

# ==============================
# ⏭ SIGUIENTE PREGUNTA
# ==============================
@app.route("/siguiente", methods=["POST"])
def siguiente():
    global indice_pregunta

    indice_pregunta += 1

    if indice_pregunta >= len(preguntas):
        indice_pregunta = 0

    return jsonify({"ok": True})

# ==============================
# 🚀 RUN
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)