
# 📚 Lesson Plan Chat

Este é um projeto de chatbot com interface web, que ajuda a montar planos de aula com base na BNCC. Ele usa a API Gemini da Google para entender perguntas com ou sem imagem, e responde de forma organizada com tópicos como Habilidades da BNCC, Objetivos, Avaliação, Materiais e Referências.
Esse app foi feito para facilitar a vida de professores, pedagogos ou qualquer pessoa que precisa criar um plano de aula de forma rápida e completa. Basta digitar uma pergunta ou anexar uma imagem (como uma atividade), e o chatbot responde com sugestões detalhadas.

## Tecnologias usadas

- Python com Flask (backend)
- HTML, CSS e JavaScript (frontend)
- API Google Gemini (modelo generativo de IA)
- Markdown (formatação das respostas)
- Reconhecimento de voz (speech-to-text no navegador)
- Upload de imagem para interpretação pela IA

## Como rodar o projeto

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/lesson-plan-chat.git
cd lesson-plan-chat
```

2. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` com sua chave da API Gemini:
```
GEMINI_API=sua_chave_aqui
```

5. Rode o app:
```bash
python app.py
```

6. O app vai abrir automaticamente no navegador. Se não abrir, acesse:
```
http://127.0.0.1:5000
```

## Como usar o Lesson Plan Chat

- Escreva uma pergunta como: *"Crie um plano de aula sobre frações para o 6º ano."*
- Você pode anexar uma imagem de um conteúdo também.
- Clique no botão de microfone para ditar a pergunta se preferir.
- O sistema vai responder com um plano de aula estruturado.
