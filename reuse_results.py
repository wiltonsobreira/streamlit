# app.py
from configparser import NoSectionError
import streamlit as st
import time
from mysql.connector import Error
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import re
from unicodedata import normalize
import altair as alt

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
    page_title="Resultados de Reúso em Finanças", 
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
#  get data
# =============================================================================

@st.cache_data(ttl=3600)
def get_reuse_results_data():
    """Busca todos os dados da tabela tm_reuse_results."""
    try:
        df = conn.query("SELECT * FROM tm_reuse_results;")
        return df
    except Exception as e:
        st.error(f"Erro ao buscar dados dos resultados de reúso: {e}")
        return None

# =============================================================================
#  UI
# =============================================================================

st.subheader("📊 Resultados de Reúso em Finanças")

df_results = get_reuse_results_data()

if df_results is not None and not df_results.empty:

    # Criação de dois DataFrames separados para maior clareza
    df_tables = df_results[df_results['nm_product'] != 'Todos Produtos'].copy()
    df_charts = df_results.copy()
    # st.divider()
    st.markdown("")

    # Configuração de formatação para as colunas das tabelas
    column_config = {
        "qt_save_days_product": st.column_config.NumberColumn("Dias Econ. (Produto)", format="%d"),
        "qt_squads_aws_accounts_use": st.column_config.NumberColumn("Qt. Squads", format="%d"),
        "qt_save_days_release": st.column_config.NumberColumn("Dias Econ. (Release)", format="%d"),
        "vl_avg_save_day_tech": st.column_config.NumberColumn("Custo Médio/Dia (R$)", format="R$ %.2f"),
        "vl_save_release": st.column_config.NumberColumn("Valor Econ. (Release) (R$)", format="R$ %.2f"),
    }

    # 1) Tabela com todos os dados dentro de um st.expander
    with st.expander("Clique aqui para visualizar ou fechar todos os dados brutos", expanded=False):
        st.dataframe(df_tables, column_config=column_config)

    # st.divider()

    # 2) Tabela filtrada com seu próprio filtro
    st.subheader("Detalhes de Uso por Produto e Release")
    product_options_table = sorted(list(df_tables['nm_product'].str.strip().unique()))
    selected_products_table = st.multiselect(
        label="Filtre a tabela por Produto:",
        options=product_options_table,
        default=product_options_table,
        help="Selecione os produtos para visualizar na tabela abaixo.",
        key="table_filter"
    )

    if selected_products_table:
        table_df_filtered = df_tables[df_tables['nm_product'].isin(selected_products_table)]
        st.dataframe(table_df_filtered[[
            'ds_year_release',
            'nm_product',
            'qt_squads_aws_accounts_use',
            'ds_squads_aws_accounts_use'
        ]])
    else:
        st.warning("Selecione ao menos um produto para visualizar a tabela de detalhes.")

    st.divider()

    # Filtro compartilhado para os gráficos
    st.subheader("Análise Gráfica da Economia Gerada")
    # As opções para o gráfico devem vir do dataframe original e completo
    product_options_charts = sorted(list(df_charts['nm_product'].str.strip().unique()))

    # Define 'Todos Produtos' como padrão, se existir na lista de opções.
    charts_default_selection = ['Todos Produtos'] if 'Todos Produtos' in product_options_charts else []

    selected_products_charts = st.multiselect(
        label="Filtre os gráficos por Produto:",
        options=product_options_charts,
        default=charts_default_selection,
        help="Selecione os produtos para comparar nos gráficos de evolução. Por padrão, é exibido o resultado consolidado.",
        key="charts_filter"
    )

    if selected_products_charts:
        charts_df = df_charts[df_charts['nm_product'].isin(selected_products_charts)]

        # 3) Gráfico de linhas: qt_save_days_release
        st.markdown("##### Evolução de Dias Economizados por Release")
        
        # Gráfico base
        base = alt.Chart(charts_df).encode(
            x=alt.X('ds_year_release:N', title='Release'),
            y=alt.Y('qt_save_days_release:Q', title='Dias Economizados'),
            color=alt.Color('nm_product:N', title='Produto')
        ).properties(
            width=700
        )
        
        # Camada de linha
        line = base.mark_line(point=True)
        
        # Camada de texto (rótulos)
        text = base.mark_text(
            align='left',
            baseline='middle',
            dy=-10  # Desloca o texto um pouco para cima da linha
        ).encode(
            text=alt.Text('qt_save_days_release:Q', format=',')
        )
        
        st.altair_chart(line + text, use_container_width=True)

        # 4) Gráfico de linhas: vl_save_release
        st.markdown("##### Evolução do Valor Economizado por Release (em R$)")

        # Gráfico base
        base_vl = alt.Chart(charts_df).encode(
            x=alt.X('ds_year_release:N', title='Release'),
            y=alt.Y('vl_save_release:Q', title='Valor Economizado (R$)'),
            color=alt.Color('nm_product:N', title='Produto')
        ).properties(
            width=700
        ).transform_calculate(
            # Cria um novo campo com o valor formatado como string para o rótulo
            formatted_value="'R$ ' + format(datum.vl_save_release, ',.2f')"
        ) 

        # Camada de linha
        line_vl = base_vl.mark_line(point=True)

        # Camada de texto (rótulos)
        text_vl = base_vl.mark_text(
            align='left',
            baseline='middle',
            dy=-10  # Desloca o texto um pouco para cima da linha
        ).encode(
            text='formatted_value:N' # Usa o campo calculado para o texto do rótulo
        )

        st.altair_chart(line_vl + text_vl, use_container_width=True)
    else:
        st.warning("Por favor, selecione ao menos um produto para visualizar os gráficos.")

else:
    st.warning("Não foram encontrados dados de resultados de reúso para exibir.")
