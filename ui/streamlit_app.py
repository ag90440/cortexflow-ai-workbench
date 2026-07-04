import json
import requests
import streamlit as st

API = st.sidebar.text_input('API URL', 'http://localhost:8000')
st.set_page_config(page_title='CortexFlow AI Workbench', layout='wide')
st.title('CortexFlow AI Workbench')
st.caption('RAG, agents, MCP, evals, memory, multi-agent workflows, RL strategy tuning, and AI system design in one portfolio app.')
mode = st.sidebar.selectbox('Mode', ['Chat', 'RAG Query', 'Agent', 'Multi-Agent', 'MCP Tools', 'EvalOps', 'System Design'])

if mode == 'Chat':
    message = st.text_area('Message', 'Explain how production RAG should be evaluated')
    if st.button('Send'):
        response = requests.post(f'{API}/chat', json={'message': message, 'session_id': 'ui-session'}).json()
        st.write(response['answer'])
        st.json(response)

if mode == 'RAG Query':
    question = st.text_area('Question', 'How does CortexFlow handle safe tool execution?')
    strategy = st.selectbox('Retrieval strategy', ['hybrid', 'bm25', 'tfidf', 'keyword'])
    if st.button('Ask RAG'):
        response = requests.post(f'{API}/rag/query', json={'question': question, 'strategy': strategy, 'top_k': 5}).json()
        st.write(response['answer'])
        st.json(response['metrics'])
        st.dataframe(response['citations'])

if mode == 'Agent':
    goal = st.text_area('Goal', 'Design a customer support knowledge agent and create an incident ticket if risk is high')
    approved = st.checkbox('Approve risky actions')
    if st.button('Run Agent'):
        response = requests.post(f'{API}/agent/run', json={'goal': goal, 'approved': approved}).json()
        st.write(response['final_answer'])
        st.json(response)

if mode == 'Multi-Agent':
    objective = st.text_area('Objective', 'Design an enterprise policy Q&A assistant with evals and permissions')
    if st.button('Run Team'):
        response = requests.post(f'{API}/multiagent/run', json={'objective': objective}).json()
        st.write(response['final_answer'])
        st.json(response)

if mode == 'MCP Tools':
    method = st.selectbox('Method', ['initialize', 'tools/list', 'resources/list', 'prompts/list'])
    if st.button('Call MCP'):
        response = requests.post(f'{API}/mcp', json={'method': method, 'params': {}}).json()
        st.json(response)

if mode == 'EvalOps':
    if st.button('Run RAG Eval'):
        response = requests.post(f'{API}/eval/run').json()
        st.metric('Overall', response['score'])
        st.json(response['metrics'])
        st.dataframe(response['rows'])

if mode == 'System Design':
    requirement = st.text_area('Requirement', 'Build a private enterprise knowledge assistant with tool calling and approval workflow')
    if st.button('Create Blueprint'):
        response = requests.post(f'{API}/system-design/blueprint', json={'requirement': requirement}).json()
        st.json(response)
