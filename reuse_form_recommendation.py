# app.py
from configparser import NoSectionError
import streamlit as st
import time
from mysql.connector import Error
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import re
from unicodedata import normalize

# =============================================================================
#  css to hide sidebar
# =============================================================================

st.markdown("""
<style>
    .css-1d391kg {display: none}
    .css-1rs6os {display: none}
    .css-17eq0hr {display: none}
    [data-testid="stSidebar"] {display: none}
    [data-testid="collapsedControl"] {display: none}
    .css-1cypcdb {margin-left: 0rem !important}
    .css-18e3th9 {padding-left: 1rem !important}
</style>
""", unsafe_allow_html=True)


# =============================================================================
#  set title and layout
# =============================================================================

st.set_page_config(
    page_title="Indicação de Produto para Reúso", 
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =============================================================================
#  transform_snake_case
# =============================================================================

def transform_snake_case(string_to_transform: str) -> str:

    # Remove accents from characters
    normalized_string = normalize('NFKD', string_to_transform).encode(
        'ASCII', 'ignore').decode('utf-8')

    # Replace spaces and special characters with underscores
    snake_case_string = re.sub(r'[^a-zA-Z0-9]+', '_', normalized_string)

    # Remove leading and trailing underscores
    snake_case_string = snake_case_string.strip('_')

    # Convert to lowercase
    snake_case_string = snake_case_string.lower()

    return snake_case_string

def is_valid_email(email: str) -> bool:
    """Valida o formato de um e-mail usando regex."""
    if not email:
        return False
    # Padrão de regex para validar e-mail
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# =============================================================================
#  connection db
# =============================================================================

def get_db_connection():
    """Retorna um objeto de conexão do Streamlit."""
    return st.connection(
        "mysql",
        type="sql",
        **st.secrets.mysql
    )

conn = get_db_connection()


# =============================================================================
#  get list options
# =============================================================================

@st.cache_data(ttl=3600)
def get_product_scope_options() -> list[str]:
    """Busca todos os nm_product_scope da tabela tc_product_scope."""
    df = conn.query("SELECT DISTINCT nm_product_scope FROM tc_product_scope ORDER BY nm_product_scope;")
    # Retorna uma lista de strings, ou uma lista vazia se o dataframe estiver vazio.
    return df['nm_product_scope'].tolist() if not df.empty else []

@st.cache_data(ttl=3600)
def get_product_use_method_options() -> list[str]:
    """Busca todos os nm_product_use_method da tabela tc_product_use_method."""
    df = conn.query("SELECT DISTINCT nm_product_use_method FROM tc_product_use_method ORDER BY nm_product_use_method;")
    # Retorna uma lista de strings, ou uma lista vazia se o dataframe estiver vazio.
    return df['nm_product_use_method'].tolist() if not df.empty else []

@st.cache_data(ttl=3600)
def get_support_tier_options() -> list[str]:
    """Busca todos os ds_support_tier da tabela tc_support_tier."""
    df = conn.query("SELECT DISTINCT ds_support_tier FROM tc_support_tier ORDER BY ds_support_tier;")
    # Retorna uma lista de strings, ou uma lista vazia se o dataframe estiver vazio.
    return df['ds_support_tier'].tolist() if not df.empty else []

# =============================================================================
#  insert data
# =============================================================================

def insert_form_data(ds_email_sender: str, 
                     cd_product: str, 
                     nm_product: str, 
                     nm_product_use_method: str, 
                     ds_other_product_use_method: str, 
                     nm_product_scope: str, 
                     ds_other_product_scope: str, 
                     nm_squad_owner: str, 
                     fl_squad_owner_financas: str,
                     ds_email_product_manager: str,
                     ds_email_tech_lead: str,
                     ds_sn_st_product: str,
                     fl_support: str,
                     ds_support_tier: str,
                     fl_allow_inner_source: str,
                     url_git_repository: str,
                     fl_user_documentation: str,
                     url_user_documentation: str,
                     fl_inner_source_documentation: str,
                     url_inner_source_documentation: str,
                     fl_iu_digital_store: str,
                     url_iu_digital_store: str,
                     fl_video_user_product: str,
                     url_video_user_product: str,
                     fl_video_inner_source: str,
                     url_video_inner_source: str,
                     dt_release_product: str,
                     nr_user_squads: str,
                     ds_name_user_squads: str):
    """Insere os dados do formulário na tabela tm_form_recommendation."""
    try:
        with conn.session as s:
            s.execute(
                text("""INSERT INTO tm_form_recommendation (
                ds_email_sender,
                cd_product,
                nm_product,
                nm_product_use_method,
                ds_other_product_use_method, 
                nm_product_scope, 
                ds_other_product_scope, 
                nm_squad_owner, 
                fl_squad_owner_financas,
                ds_email_product_manager,
                ds_email_tech_lead,
                ds_sn_st_product,
                fl_support,
                ds_support_tier,
                fl_allow_inner_source,
                url_git_repository,
                fl_user_documentation,
                url_user_documentation,
                fl_inner_source_documentation,
                url_inner_source_documentation,
                fl_iu_digital_store,
                url_iu_digital_store,
                fl_video_user_product,
                url_video_user_product,
                fl_video_inner_source,
                url_video_inner_source,
                dt_release_product,
                nr_user_squads,
                ds_name_user_squads
                ) VALUES (
                :ds_email_sender, 
                :cd_product, 
                :nm_product, 
                :nm_product_use_method, 
                :ds_other_product_use_method, 
                :nm_product_scope, 
                :ds_other_product_scope, 
                :nm_squad_owner, 
                :fl_squad_owner_financas,
                :ds_email_product_manager,
                :ds_email_tech_lead,
                :ds_sn_st_product,
                :fl_support,
                :ds_support_tier,
                :fl_allow_inner_source,
                :url_git_repository,
                :fl_user_documentation,
                :url_user_documentation,
                :fl_inner_source_documentation,
                :url_inner_source_documentation,
                :fl_iu_digital_store,
                :url_iu_digital_store,
                :fl_video_user_product,
                :url_video_user_product,
                :fl_video_inner_source,
                :url_video_inner_source,
                :dt_release_product,
                :nr_user_squads,
                :ds_name_user_squads);"""),
                params={"ds_email_sender": ds_email_sender, 
                        "cd_product": cd_product, 
                        "nm_product": nm_product,
                        "nm_product_use_method": nm_product_use_method,
                        "ds_other_product_use_method": ds_other_product_use_method,
                        "nm_product_scope": nm_product_scope,
                        "ds_other_product_scope": ds_other_product_scope,
                        "nm_squad_owner": nm_squad_owner,
                        "fl_squad_owner_financas": fl_squad_owner_financas,
                        "ds_email_product_manager": ds_email_product_manager,
                        "ds_email_tech_lead": ds_email_tech_lead,
                        "ds_sn_st_product": ds_sn_st_product,
                        "fl_support": fl_support,
                        "ds_support_tier": ds_support_tier,
                        "fl_allow_inner_source": fl_allow_inner_source,
                        "url_git_repository": url_git_repository,
                        "fl_user_documentation": fl_user_documentation,
                        "url_user_documentation": url_user_documentation,
                        "fl_inner_source_documentation": fl_inner_source_documentation,
                        "url_inner_source_documentation": url_inner_source_documentation,
                        "fl_iu_digital_store": fl_iu_digital_store,
                        "url_iu_digital_store": url_iu_digital_store,
                        "fl_video_user_product": fl_video_user_product,
                        "url_video_user_product": url_video_user_product,
                        "fl_video_inner_source": fl_video_inner_source,
                        "url_video_inner_source": url_video_inner_source,
                        "dt_release_product": dt_release_product,
                        "nr_user_squads": nr_user_squads,
                        "ds_name_user_squads": ds_name_user_squads}
            )
            s.commit()
        return True, ""
    except (Error, SQLAlchemyError) as e:
        # Retorna False e a mensagem de erro em caso de falha
        return False, str(e)

# =============================================================================
#  clear form
# =============================================================================

def clear_form():
    """Reseta os valores do formulário no session_state."""
    st.session_state.ds_email_sender = ""
    st.session_state.nm_product = ""
    st.session_state.selected_use_method = []
    st.session_state.ds_other_product_use_method = ""
    st.session_state.selected_scope = []
    st.session_state.ds_other_product_scope = ""
    st.session_state.nm_squad_owner = ""
    st.session_state.fl_squad_owner_financas = None
    st.session_state.ds_email_product_manager = ""
    st.session_state.ds_email_tech_lead = ""
    st.session_state.ds_sn_st_product = ""
    st.session_state.fl_support = None
    st.session_state.ds_support_tier = ""
    st.session_state.fl_allow_inner_source = None
    st.session_state.url_git_repository = ""
    st.session_state.fl_user_documentation = None
    st.session_state.url_user_documentation = ""
    st.session_state.fl_inner_source_documentation = None
    st.session_state.url_inner_source_documentation = ""
    st.session_state.fl_iu_digital_store = None
    st.session_state.url_iu_digital_store = ""
    st.session_state.fl_video_user_product = None
    st.session_state.url_video_user_product = ""
    st.session_state.fl_video_inner_source = None
    st.session_state.url_video_inner_source = ""
    st.session_state.dt_release_product = None
    st.session_state.nr_user_squads = None
    st.session_state.ds_name_user_squads = ""


# =============================================================================
#  UI
# =============================================================================

st.subheader("📝 Indicação de Produto para Reúso")
st.markdown("Preencha os campos abaixo para enviar uma indicação de produto para reúso.")

# Campo ds_email_sender
st.text_input(
    label="e-mail do solicitante:",
    placeholder="Digite o e-mail do solicitante que está recomendando o produto para reúso.",
    help="Digite o e-mail do solicitante que está recomendando o produto para reúso.",
    key="ds_email_sender"
)

# Campo nm_product
st.text_input(
    label="Nome do produto:",
    placeholder="Exemplo: Rules Manager",
    help="Digite o nome do produto indicado para reúso.",
    key="nm_product"
)

# Campo nm_product_use_method
product_use_method_options = get_product_use_method_options()
st.multiselect(
    label="Métodos de Uso do Produto:",
    options=product_use_method_options,
    placeholder="Selecione TODOS os métodos de uso que o produto permite.",
    help="Selecione TODOS os métodos de uso que o produto permite. Caso não encontre a opção desejada na lista, selecione `Opção não localizada - Incluir novas opções no campo abaixo` e descreva o método de uso no campo abaixo.",
    key="selected_use_method"
)

# Campo ds_other_product_use_method
st.text_input(
    label="Adicionar novos métodos de uso do produto, não localizados na lista acima:",
    placeholder="Descreva os métodos de uso do produto não disponíveis na lista acima, separando-os com ponto e vírgula.",
    help="Descreva os métodos de uso do produto não disponíveis na lista acima, separando-os com ponto e vírgula.",
    key="ds_other_product_use_method"
)

# Campo nm_product_scope
product_scope_options = get_product_scope_options()
st.multiselect(
    label="Escopos do Produto:",
    options=product_scope_options,
    placeholder="Selecione TODOS os escopos que o produto atende.",
    help="Selecione TODOS os escopos que o produto atende. Caso não encontre a opção desejada na lista, selecione `Opção não localizada - Incluir novas opções no campo abaixo` e descreva o escopo do produto no campo abaixo.",
    key="selected_scope"
)

# Campo ds_other_product_scope
st.text_input(
    label="Adicionar novos escopos do produto, não localizados na lista acima:",
    placeholder="Descreva os escopos do produto não disponíveis na lista acima, separando-os com ponto e vírgula.",
    help="Descreva os escopos do produto não disponíveis na lista acima, separando-os com ponto e vírgula.",
    key="ds_other_product_scope"
)

# Campo nm_squad_owner
st.text_input(
    label="Nome da Squad Owner do produto indicado para reúso:",
    placeholder="Informe a squad responsável pelo produto.",
    help="Informe a squad responsável pelo produto.",
    key="nm_squad_owner"
)


# Campo fl_squad_owner_financas
st.radio(
    label="A squad owner do produto pertence a Finanças?",    
    options=['Y', 'N'],
    horizontal=True,
    index=None,
    help="Selecione (Y) Yes ou (N) No",
    key="fl_squad_owner_financas"
)

# Campo ds_email_product_manager
st.text_input(
    label="e-mail do PM (Product Manager):",
    placeholder="Digite o e-mail do PM responsável pelo produto.",
    help="Digite o e-mail do PM responsável pelo produto.",
    key="ds_email_product_manager"
)

# Campo ds_email_tech_lead
st.text_input(
    label="e-mail do Tech Lead:",
    placeholder="Digite o e-mail do Tech Lead responsável pelo produto.",
    help="Digite o e-mail do Tech Lead responsável pelo produto.",
    key="ds_email_tech_lead"
)

# Campo ds_sn_st_product
st.text_input(
    label="Nome do SN (Serviço de Negócio) ou ST (Serviço de Tecnlogia) do produto:",
    placeholder="Digite o nome do SN ou ST do produto.",
    help="Digite o nome do SN ou ST do produto.",
    key="ds_sn_st_product"
)

# Campo fl_support
st.radio(
    label="O produto possui processo e equipe para suporte?",    
    options=['Y', 'N'],
    horizontal=True,
    index=None,
    help="Selecione (Y) Yes ou (N) No",
    key="fl_support"
)

# Campo ds_support_tier
support_tier_options = get_support_tier_options()
st.selectbox(
    label="Tier de suporte do produto",
    options=[""] + support_tier_options,  # Adiciona uma opção vazia para estado inicial
    help="Selecione o tier de suporte do produto.",
    key="selected_support_tier"
)

# Campo fl_allow_inner_source
st.radio(
    label="O produto permite Inner Source?",    
    options=['Y', 'N'],
    horizontal=True,
    index=None,
    help="Selecione (Y) Yes ou (N) No",
    key="fl_allow_inner_source"
)

# Campo url_git_repository
st.text_input(
    label="URL do repositório Git com código do produto:",
    placeholder="Digite a URL do repositório Git.",
    help="Digite a URL do repositório Git com código do produto.",
    key="url_git_repository"
)

# Campo fl_user_documentation
st.radio(
    label="O produto possui documentação de uso?",    
    options=['Y', 'N'],
    horizontal=True,
    index=None,
    help="Selecione (Y) Yes ou (N) No",
    key="fl_user_documentation"
)

# Campo url_user_documentation
st.text_input(
    label="URL da documentação de uso do produto:",
    placeholder="Digite a URL da documentação de uso do produto.",
    help="Digite a URL da documentação de uso do produto.",
    key="url_user_documentation"
)

# Campo fl_inner_source_documentation
st.radio(
    label="O produto possui documentação para desenvolvedor e processo de Inner Source?",    
    options=['Y', 'N'],
    horizontal=True,
    index=None,
    help="Selecione (Y) Yes ou (N) No",
    key="fl_inner_source_documentation"
)

# Campo url_inner_source_documentation
st.text_input(
    label="URL da documentação para o desenvolvedor e processo de Inner Source:",
    placeholder="Digite a URL da documentação para o desenvolvedor e processo de Inner Source.",
    help="Digite a URL da documentação para o desenvolvedor e processo de Inner Source.",
    key="url_inner_source_documentation"
)

# Campo fl_iu_digital_store
st.radio(
    label="O produto está publicado na IU Digital Store?",    
    options=['Y', 'N'],
    horizontal=True,
    index=None,
    help="Selecione (Y) Yes ou (N) No",
    key="fl_iu_digital_store"
)

# Campo url_iu_digital_store
st.text_input(
    label="URL da página do IU Digital Store do produto:",
    placeholder="Digite a URL da página do IU Digital Store do produto.",
    help="Digite a URL da página do IU Digital Store do produto.",
    key="url_iu_digital_store"
)

# Campo fl_video_user_product
st.radio(
    label="O produto possui vídeo com guia de uso e apresentação das funcionalidades?",
    options=['Y', 'N'],
    horizontal=True,
    index=None,
    help="Selecione (Y) Yes ou (N) No",
    key="fl_video_user_product"
)

# Campo url_video_user_product
st.text_input(
    label="URL do vídeo de guia de uso e apresentação das funcionalidades do produto:",
    placeholder="Digite a URL do vídeo de guia de uso e apresentação das funcionalidades do produto.",
    help="Digite a URL do vídeo de guia de uso e apresentação das funcionalidades do produto.",
    key="url_video_user_product"
)

# Campo fl_video_inner_source
st.radio(
    label="O produto possui vídeo com direcionamentos para desenvolvedor e processo de Inner Source?",
    options=['Y', 'N'],
    horizontal=True,
    index=None,
    help="Selecione (Y) Yes ou (N) No",
    key="fl_video_inner_source"
)

# Campo url_video_inner_source
st.text_input(
    label="URL do vídeo com direcionamentos para desenvolvedor e processo de Inner Source:",
    placeholder="Digite a URL com direcionamentos para desenvolvedor e processo de Inner Source.",
    help="Digite a URL com direcionamentos para desenvolvedor e processo de Inner Source.",
    key="url_video_inner_source"
)

st.date_input(
    label="Data de lançamento do produto:",
    value=None,
    format="DD/MM/YYYY",
    help="Selecione a data aproximada em que produto ficou disponível para uso pela primeira vez na empresa.",
    key="dt_release_product"
)

# Campo nr_user_squads
st.number_input(
    label="Número de squads que já estão utilizando o produto:",
    min_value=0, # Garante que o número não seja negativo
    step=1,      # Define o incremento como um número inteiro
    value=None,  # Define o valor inicial como nulo para que o campo comece vazio
    placeholder="Digite a quantidade de squads que já estão utilizando o produto.",
    help="Digite a quantidade de squads que já estão utilizando o produto.",
    key="nr_user_squads",
)

# Campo ds_name_user_squads
st.text_input(
    label="Nome das squads que já estão utilizando o produto:",
    placeholder="Digite o nome das squads que já estão utilizando o produto, separando-os por ponto e vírgula.",
    help="Digite o nome das squads que já estão utilizando o produto, separando-os por ponto e vírgula.",
    key="ds_name_user_squads"
)


st.divider()

# Botão de submissão
submitted = st.button("🚀 Enviar Indicação de Produto para Reúso")

# --- Lógica de Submissão ---

if submitted:

    # Validação dos campos
    ds_email_sender = st.session_state.ds_email_sender
    nm_product = st.session_state.nm_product
    nm_product_use_method_list = st.session_state.selected_use_method
    ds_other_product_use_method = st.session_state.ds_other_product_use_method
    nm_product_scope_list = st.session_state.selected_scope
    ds_other_product_scope = st.session_state.ds_other_product_scope
    nm_squad_owner = st.session_state.nm_squad_owner
    fl_squad_owner_financas = st.session_state.fl_squad_owner_financas
    ds_email_product_manager = st.session_state.ds_email_product_manager
    ds_email_tech_lead = st.session_state.ds_email_tech_lead
    ds_sn_st_product = st.session_state.ds_sn_st_product
    fl_support = st.session_state.fl_support
    ds_support_tier = st.session_state.selected_support_tier
    fl_allow_inner_source = st.session_state.fl_allow_inner_source
    url_git_repository = st.session_state.url_git_repository
    fl_user_documentation = st.session_state.fl_user_documentation
    url_user_documentation = st.session_state.url_user_documentation
    fl_inner_source_documentation = st.session_state.fl_inner_source_documentation
    url_inner_source_documentation = st.session_state.url_inner_source_documentation
    fl_iu_digital_store = st.session_state.fl_iu_digital_store
    url_iu_digital_store = st.session_state.url_iu_digital_store
    fl_video_user_product = st.session_state.fl_video_user_product
    url_video_user_product = st.session_state.url_video_user_product
    fl_video_inner_source = st.session_state.fl_video_inner_source
    url_video_inner_source = st.session_state.url_video_inner_source
    dt_release_product = st.session_state.dt_release_product
    nr_user_squads = st.session_state.nr_user_squads
    ds_name_user_squads = st.session_state.ds_name_user_squads


    # Verifica se os campos obrigatórios estão preenchidos
    if (not ds_email_sender 
        or not nm_product 
        or not nm_product_use_method_list
        or not nm_product_scope_list
        or not nm_squad_owner
        or not fl_support
        or not ds_support_tier
        or not fl_allow_inner_source
        or not url_git_repository
        or not fl_user_documentation
        or not fl_inner_source_documentation
        or not fl_iu_digital_store
        or not fl_video_user_product
        or not fl_video_inner_source
        or not dt_release_product
        or not nr_user_squads
        or not ds_name_user_squads
        ):
        st.warning("Por favor, preencha todos os campos obrigatórios.")

    # Verifica se o e-mail tem um formato válido
    elif not is_valid_email(ds_email_sender):
        st.warning("O e-mail inserido não é válido. Por favor, corrija.")
    else:

        # Gera cd_product a partir do nm_product
        cd_product = transform_snake_case(nm_product)

        # Converte as listas dos multiselects em strings separadas por "; "
        nm_product_use_method_str = "; ".join(nm_product_use_method_list)
        nm_product_scope_str = "; ".join(nm_product_scope_list)

        # Chama a função para inserir os dados no banco
        success, error_message = insert_form_data(
            ds_email_sender=ds_email_sender,
            cd_product=cd_product,
            nm_product=nm_product,
            # Passa as strings convertidas para a função de inserção
            nm_product_use_method=nm_product_use_method_str,
            ds_other_product_use_method=ds_other_product_use_method,
            nm_product_scope=nm_product_scope_str,
            ds_other_product_scope=ds_other_product_scope,
            nm_squad_owner=nm_squad_owner,
            fl_squad_owner_financas=fl_squad_owner_financas,
            ds_email_product_manager=ds_email_product_manager,
            ds_email_tech_lead=ds_email_tech_lead,
            ds_sn_st_product=ds_sn_st_product,
            fl_support=fl_support,
            ds_support_tier=ds_support_tier,
            fl_allow_inner_source=fl_allow_inner_source,
            url_git_repository=url_git_repository,
            fl_user_documentation=fl_user_documentation,
            url_user_documentation=url_user_documentation,
            fl_inner_source_documentation=fl_inner_source_documentation,
            url_inner_source_documentation=url_inner_source_documentation,
            fl_iu_digital_store=fl_iu_digital_store,
            url_iu_digital_store=url_iu_digital_store,
            fl_video_user_product=fl_video_user_product,
            url_video_user_product=url_video_user_product,
            fl_video_inner_source=fl_video_inner_source,
            url_video_inner_source=url_video_inner_source,
            dt_release_product=dt_release_product,
            nr_user_squads=nr_user_squads,
            ds_name_user_squads=ds_name_user_squads
        )
        
        # Mensagem de sucesso/erro é exibida temporariamente antes do sleep e do diálogo
        temp_message_placeholder = st.empty()
        if success: temp_message_placeholder.success(f"Produto indicado para reúso com sucesso! Produto: '{nm_product}'.")
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
        message = f"Produto indicado para reúso com sucesso! Produto: '{nm_product}'." if success else f"Ocorreu um erro ao inserir o registro: {error_message}"
        show_result_dialog(success, message)
