from flask import Flask, render_template, request, jsonify, session, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import google.generativeai as genai
import os
import markdown
import threading
import webbrowser

load_dotenv()
app = Flask(__name__)
app.secret_key = "Lesson-Plan-Chat"
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

genai.configure(api_key=os.getenv("GEMINI_API"))
model = genai.GenerativeModel("gemini-2.0-flash")

def historico_msg(historico):
    return [
        {"role": role, "parts": [conteudo]}
        for item in historico
        for role, conteudo in (("user", item["prompt"]), ("model", item["resposta"]))
    ]

def gerar_prompt_inicial(prompt, historico, com_imagem=False):
    if not historico:
        prompt += (" Estar na formatação da Habilidades da BNCC, Objetivos da aula, Avaliação,"
                       " Materiais/Recursos necessários, Referencias para criação do plano."
                       " Caso não esteja informado turma/ano escolar, disciplina/conteúdo,"
                       " me questione o que falta antes de gerar a resposta completa.")
    return prompt

@app.route("/", methods=["GET"])
def index():
    session["historico"] = []
    return render_template("index.html", historico=[])

@app.route("/processar", methods=["POST"])
def generate_prompt():
    file = request.files.get("imagem")
    prompt = request.form.get("prompt", "").strip()

    if not prompt:
        return jsonify({"resposta": "Por favor, digite uma pergunta."})

    try:
        resposta = ""
        imagem_url = None
        historico = session.get("historico", [])

        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            image_ref = genai.upload_file(path=filepath, display_name=filename)
            imagem_url = f"/uploads/{filename}"
            prompt = gerar_prompt_inicial(prompt, historico, com_imagem=True)

            response = model.generate_content([image_ref, prompt])
        else:
            prompt = gerar_prompt_inicial(prompt, historico)
            mensagens = historico_msg(historico)
            mensagens.append({"role": "user", "parts": [prompt]})
            response = model.generate_content(mensagens)

        resposta = markdown.markdown(response.text)
        nova_interacao = {"prompt": prompt, "resposta": resposta}
        if imagem_url:
            nova_interacao["imagem_url"] = imagem_url

        historico.append(nova_interacao)
        session["historico"] = historico

        return jsonify({"resposta": resposta, "historico": historico})

    except Exception as e:
        return jsonify({"resposta": f"Ocorreu um erro ao tentar responder: {str(e)}"})

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1.0, lambda: webbrowser.open_new("http://127.0.0.1:5000")).start()

    app.run(debug=True)