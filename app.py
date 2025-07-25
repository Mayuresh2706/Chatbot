from flask import Flask,jsonify,request,render_template,session,url_for,redirect
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import requests
import mysql.connector
import json

users = {'admin': 'admin123'}

app = Flask(__name__)
app.secret_key  = 'new_session'

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Mayuresh1',
    database='AI_Chatbot'
)

cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT question, answer FROM Training_Data")
rows = cursor.fetchall()

Questions = [row['question'] for row in rows]
Answers = [row['answer'] for row in rows]


@app.route('/',methods = ['GET','POST'])
def home():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        if users.get(u) == p:
            session['user'] = u
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

Model = SentenceTransformer('all-MiniLM-L6-v2')
Encoder = Model.encode(Questions, normalize_embeddings=True)
index = faiss.IndexFlatIP(Encoder.shape[1])
index.add(np.array(Encoder))

@app.route('/chat', methods=['POST'])

def chat():
    input_text = request.json.get('input', '')
    query_vector = Model.encode(input_text, normalize_embeddings=True)
    D, I = index.search(np.array([query_vector]), k=3)

    similarity = D[0][0]
    best_answer_index = I[0][0]

    cursor.execute("SELECT question, answer FROM history WHERE user = %s ORDER BY created_at DESC LIMIT 1", (session['user'],))
    chat_history_rows = cursor.fetchall()
        
    if similarity< 0.90:
        history = "\n".join([f'"User": "{row["question"]}"\n"Bot": "{row["answer"]}"' for row in chat_history_rows])
        faq_text = "\n".join([f'"Q": "{Questions[i]}"\n"A": "{Answers[i]}"' for i in I[0]])
        
        response = requests.post('http://localhost:11434/api/generate/',
                    json={
                        "model": "phi",
                        "stream": False,
                        "num_predict": 50,
                        "prompt" : f'''
You are a helpful and concise support bot trained to answer e-Invoicing-related questions based on FAQs.

Answer the question below clearly and concisely in 1–2 sentences. Act like its a conversation not a FAQ.

User Question:
{input_text}

Recent Chat History (optional):
{history}

Relevant FAQs:
{faq_text}

Only output your answer — do not repeat the question or include 'User' or 'Bot' tags.

'''}
)
        if response.status_code == 200:
                ollama = response.json()
                ollama = ollama['response']
                cursor.execute("INSERT INTO history (user, question, answer) VALUES (%s, %s, %s)",
                (session['user'], input_text, ollama))
                conn.commit()
                return jsonify({'answer': ollama,'recommended questions': [Questions[i] for i in I[0]][1:4]})
        else:
            return ("Error: " + response.text, 500)
        
    cursor.execute("INSERT INTO history (user, question, answer) VALUES (%s, %s, %s)",
                   (session['user'], input_text, Answers[best_answer_index]))
    conn.commit()
    return jsonify({'answer': Answers[best_answer_index],'recommended questions': [Questions[i] for i in I[0]][1:4]})

    
if __name__ == '__main__':
    app.run(port = 5000,debug=True)
