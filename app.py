# app.py
import streamlit as st
import time
from mysql.connector import Error
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

# Configura o título da página e o layout
st.set_page_config(page_title="Formulário de Produtos", layout="centered")

def get_db_connection():
    """Retorna um objeto de conexão do Streamlit."""
    return st.connection(
        "mysql",
        type="sql",
        **st.secrets.mysql
    )

conn = get_db_connection()


@st.cache_data(ttl=3600) # Cache expira em 1 hora (3600 segundos)
def get_escope_options() -> list[str]:
    """Busca todos os escopos de produto da tabela tc_escope_product."""
    df = conn.query("SELECT DISTINCT nm_escope_product FROM tc_escope_product ORDER BY nm_escope_product;")
    # Retorna uma lista de strings, ou uma lista vazia se o dataframe estiver vazio.
    return df['nm_escope_product'].tolist() if not df.empty else []

@st.cache_data(ttl=3600)
def get_product_options(escope: str) -> list[str]:
    """Busca produtos filtrados por um escopo específico."""
    if not escope:
        return [] # Retorna lista vazia se nenhum escopo for fornecido
    
    query = "SELECT DISTINCT nm_product FROM tc_product WHERE nm_escope_product = :escope ORDER BY nm_product;"
    df = conn.query(query, params={"escope": escope})
    return df['nm_product'].tolist() if not df.empty else []

def insert_form_data(escope: str, product: str, pm: str, iuds_flag: str):
    """Insere os dados do formulário na tabela tm_form."""
    try:
        with conn.session as s:
            s.execute(
                text("INSERT INTO tm_form (nm_escope_product, nm_product, nm_pm, fl_iuds) VALUES (:escope, :product, :pm, :flag);"),
                params={"escope": escope, "product": product, "pm": pm, "flag": iuds_flag}
            )
            s.commit()
        return True, ""
    except (Error, SQLAlchemyError) as e:
        # Retorna False e a mensagem de erro em caso de falha
        return False, str(e)

def clear_form():
    """Reseta os valores do formulário no session_state."""
    st.session_state.selected_escope = ""
    st.session_state.selected_product = ""
    st.session_state.pm_name = ""
    st.session_state.iuds_flag = "Y" # Define para o valor padrão


# --- Interface do Usuário (UI) ---

st.title("📝 Formulário de Produtos")
st.markdown("Preencha os campos abaixo para registrar um novo item.")

# Para ter campos dependentes (um habilitando o outro), eles devem estar fora de um st.form.
# st.form impede a re-execução do script a cada interação, o que é necessário para a lógica de habilitação.
st.subheader("Detalhes do Produto")

# Campo 1: Escopo do Produto (ComboBox)
escope_options = get_escope_options()
st.selectbox(
    label="Escopo do Produto",
    options=[""] + escope_options,  # Adiciona uma opção vazia para estado inicial
    help="Selecione o escopo geral do produto.",
    key="selected_escope"
)

# Campo 2: Produto (ComboBox dependente)
# A lógica de habilitação agora funcionará, pois o script re-executa a cada mudança no selectbox acima.
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

# Campo 3: PM (Campo de texto)
st.text_input(
    label="Nome do PM (Product Manager)",
    placeholder="Ex: João da Silva",
    key="pm_name"
)

# Campo 4: Flag IUD (Botões de rádio)
# Radio buttons são ideais para um número pequeno de opções como char(1)
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
        
        # Mensagem de sucesso/erro é exibida temporariamente antes do sleep e do diálogo
        temp_message_placeholder = st.empty()
        if success: temp_message_placeholder.success(f"Registro inserido com sucesso! Produto: '{st.session_state.selected_product}', PM: '{st.session_state.pm_name}'.")
        else: temp_message_placeholder.error(f"Ocorreu um erro ao inserir o registro: {error_message}")

        # 1. Aguarda 2 segundos
        time.sleep(2)

        # 2. Cria um diálogo modal para exibir o resultado
        @st.dialog("Status da Operação")
        def show_result_dialog(success_status, msg):
            if success_status:
                st.success(msg)
            else:
                st.error(msg)

            # 3. O botão "OK" agora limpa o formulário e re-executa o script.
            if st.button("OK"):
                clear_form()
                st.rerun()

        # Define a mensagem e chama o diálogo
        message = f"Registro inserido com sucesso! Produto: '{st.session_state.selected_product}', PM: '{st.session_state.pm_name}'." if success else f"Ocorreu um erro ao inserir o registro: {error_message}"
        show_result_dialog(success, message)
