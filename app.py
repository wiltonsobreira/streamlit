# app.py
import streamlit as st
import time
from mysql.connector import Error
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

# título da página e layout
st.set_page_config(page_title="Formulário de Produtos", layout="centered")

def get_db_connection():
    return st.connection(
        "mysql",
        type="sql",
        **st.secrets.mysql
    )

conn = get_db_connection()


@st.cache_data(ttl=3600) 
def get_escope_options() -> list[str]:
    df = conn.query("SELECT DISTINCT nm_escope_product FROM tc_escope_product ORDER BY nm_escope_product;")
    return df['nm_escope_product'].tolist() if not df.empty else []

@st.cache_data(ttl=3600)
def get_product_options(escope: str) -> list[str]:
    if not escope:
        return []
    
    query = "SELECT DISTINCT nm_product FROM tc_product WHERE nm_escope_product = :escope ORDER BY nm_product;"
    df = conn.query(query, params={"escope": escope})
    return df['nm_product'].tolist() if not df.empty else []

def insert_form_data(escope: str, product: str, pm: str, iuds_flag: str):
    """Insere os dados do formulário na tabela"""
    try:
        with conn.session as s:
            s.execute(
                text("INSERT INTO tm_form (nm_escope_product, nm_product, nm_pm, fl_iuds) VALUES (:escope, :product, :pm, :flag);"),
                params={"escope": escope, "product": product, "pm": pm, "flag": iuds_flag}
            )
            s.commit()
        return True, ""
    except (Error, SQLAlchemyError) as e:
        return False, str(e)

def clear_form():
    """Reseta os valores do formulário"""
    st.session_state.selected_escope = ""
    st.session_state.selected_product = ""
    st.session_state.pm_name = ""
    st.session_state.iuds_flag = "Y" 


# --- (UI) ---

st.title("📝 Formulário de Produtos")
st.markdown("Preencha os campos abaixo para registrar um novo item.")

st.subheader("Detalhes do Produto")

# Campo 1
escope_options = get_escope_options()
st.selectbox(
    label="Escopo do Produto",
    options=[""] + escope_options, 
    help="Selecione o escopo geral do produto.",
    key="selected_escope"
)

# Campo 2
is_product_disabled = not bool(st.session_state.selected_escope)

# As opções deste selectbox são carregadas dinamicamente com base no primeiro.
product_options = get_product_options(st.session_state.selected_escope)

st.selectbox(
    label="Produto",
    options=[""] + product_options,
    help="Selecione o produto. Habilitado após escolher um escopo.",
    disabled=is_product_disabled,
    key="selected_product"
)

# Campo 3
st.text_input(
    label="Nome do PM (Product Manager)",
    placeholder="Ex: João da Silva",
    key="pm_name"
)

# Campo 4
st.radio(
    label="Tipo de Operação (fl_iuds)",
    options=['Y', 'N'],
    horizontal=True,
    help="Selecione a flag da operação: (Y)es, (N)o",
    key="iuds_flag"
)

st.divider()

# Botão de submissão
submitted = st.button("🚀 Enviar Registro")

# --- Lógica de Submissão ---

if submitted:
    # Validação dos campos
    if not st.session_state.selected_escope or not st.session_state.selected_product or not st.session_state.pm_name:
        st.warning("Por favor, preencha todos os campos obrigatórios.")
    else:
        # Chama a função para inserir os dados no banco
        success, error_message = insert_form_data(st.session_state.selected_escope, st.session_state.selected_product, st.session_state.pm_name, st.session_state.iuds_flag)
        
        # Mensagem de sucesso/erro exibida temporariamente antes do sleep
        temp_message_placeholder = st.empty()
        if success: temp_message_placeholder.success(f"Registro inserido com sucesso! Produto: '{st.session_state.selected_product}', PM: '{st.session_state.pm_name}'.")
        else: temp_message_placeholder.error(f"Ocorreu um erro ao inserir o registro: {error_message}")

        # Aguarda 2 segundos
        time.sleep(2)

        # diálogo modal para exibir o resultado
        @st.dialog("Status da Operação")
        def show_result_dialog(success_status, msg):
            if success_status:
                st.success(msg)
            else:
                st.error(msg)

            # O botão "OK" limpa o formulário
            if st.button("OK"):
                clear_form()
                st.rerun()

        message = f"Registro inserido com sucesso! Produto: '{st.session_state.selected_product}', PM: '{st.session_state.pm_name}'." if success else f"Ocorreu um erro ao inserir o registro: {error_message}"
        show_result_dialog(success, message)
