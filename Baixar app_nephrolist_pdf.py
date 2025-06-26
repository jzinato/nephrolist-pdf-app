
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Leitor de PDFs - NephroList", layout="centered")

st.title("📄 Leitor de Evoluções Clínicas - NephroList")
st.markdown("Envie um PDF gerado pelo prontuário eletrônico para extrair dados clínicos estruturados.")

uploaded_file = st.file_uploader("Escolha um arquivo PDF", type=["pdf"])

if uploaded_file:
    # Simulação de extração (dados fixos para exemplo)
    dados = {
        "Nome": "Vera Ondina Marcos",
        "Setor": "CTG 4",
        "Leito": "19",
        "Idade": "82",
        "Data_Admissao": "2025-06-23",
        "Motivo_Internacao": "Febre e tremores em paciente dialítica",
        "Diagnostico": "Infecção de cateter de hemodiálise",
        "Situacao_Atual": "Afebril, vertigem postural, PA 90x60",
        "Dialise": "Sim / Crônico",
        "Peso": "65",
        "Plano": "Suspender Anlodipino e Furosemida. HD + ATB guiado por vancocinemia.",
        "Preceptor": "Gabriel Silqueira",
        "Residente": "Marcela Oliveira",
        "Desfecho": "Alta",
        "Data_Desfecho": "2025-06-28"
    }

    df = pd.DataFrame([dados])
    st.success("✅ Dados extraídos com sucesso!")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Baixar dados como CSV", csv, "dados_extraidos_nephrolist.csv", "text/csv")

