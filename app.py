import streamlit as st
import pandas as pd
from faker import Faker
import base64
from validate_docbr import CPF, CNPJ

st.title('Gerador de CSV Personalizado')

st.markdown('''
Adicione colunas, escolha o tipo de dado e gere dados sintéticos válidos para importar no seu sistema.
''')

fake = Faker('pt_BR')
cpf_gen = CPF()
cnpj_gen = CNPJ()

def generate_data(tipo, n):
    if tipo == 'Nome':
        return [fake.name() for _ in range(n)]
    elif tipo == 'Nome Social':
        return [fake.name() for _ in range(n)]
    elif tipo == 'Email':
        return [fake.email() for _ in range(n)]
    elif tipo == 'CPF':
        # Gera CPF no formato 99999999999
        return [cpf_gen.generate() for _ in range(n)]
    elif tipo == 'CNPJ':
        # Gera CNPJ no formato 99999999999999
        return [cnpj_gen.generate() for _ in range(n)]
    elif tipo == 'Telefone':
        return [fake.phone_number() for _ in range(n)]
    elif tipo == 'Endereço':
        return [fake.address().replace('\n', ', ') for _ in range(n)]
    elif tipo == 'Texto':
        return [fake.text(max_nb_chars=20) for _ in range(n)]
    elif tipo == 'Número':
        return [str(fake.random_number(digits=5)) for _ in range(n)]
    elif tipo == 'Matrícula':
        return [str(fake.random_int(100000, 999999)) for _ in range(n)]
    elif tipo == 'Cargo':
        cargos = ['Analista', 'Gerente', 'Diretor', 'Assistente', 'Coordenador', 'Supervisor']
        return [fake.random_element(cargos) for _ in range(n)]
    elif tipo == 'Departamento':
        departamentos = ['RH', 'Financeiro', 'TI', 'Marketing', 'Operações', 'Vendas']
        return [fake.random_element(departamentos) for _ in range(n)]
    elif tipo == 'Valor Salário Base':
        # Formato 2.350,00
        return [f"{fake.random_int(1200, 15000):,.2f}".replace(",", "@").replace(".", ",").replace("@", ".") for _ in range(n)]
    elif tipo == 'Data admissão':
        # Formato DD/MM/AAAA
        return [fake.date_between(start_date='-10y', end_date='today').strftime('%d/%m/%Y') for _ in range(n)]
    else:
        return ['' for _ in range(n)]

col_types = [
    'Nome',
    'Nome Social',
    'CPF',
    'Matrícula',
    'Cargo',
    'Email',
    'CNPJ',
    'Departamento',
    'Valor Salário Base',
    'Data admissão',
    'Texto',
    'Número',
    'Telefone',
    'Endereço'
]




st.sidebar.header('Configuração das Colunas')
default_columns = [
    'Nome completo',
    'CPF',
    'Matrícula',
    'Cargo',
    'Email',
    'CNPJ',
    'Departamento',
    'Valor Salário Base',
    'Data admissão',
    'Nome Social'
]
default_types = [
    'Nome',
    'CPF',
    'Matrícula',
    'Cargo',
    'Email',
    'CNPJ',
    'Departamento',
    'Valor Salário Base',
    'Data admissão',
    'Nome Social'
]

# Estado das colunas dinâmicas
if 'columns' not in st.session_state:
    st.session_state['columns'] = default_columns.copy()
    st.session_state['types'] = default_types.copy()

# Adicionar coluna
new_col = st.sidebar.text_input('Nova coluna')
new_type = st.sidebar.selectbox('Tipo da nova coluna', col_types, key='new_type')
if st.sidebar.button('Adicionar coluna') and new_col:
    st.session_state['columns'].append(new_col)
    st.session_state['types'].append(new_type)

# Remover coluna específica
if st.session_state['columns']:
    col_to_remove = st.sidebar.selectbox('Remover coluna', st.session_state['columns'], key='remove_col')
    if st.sidebar.button('Remover coluna selecionada'):
        idx = st.session_state['columns'].index(col_to_remove)
        st.session_state['columns'].pop(idx)
        st.session_state['types'].pop(idx)

# Editar colunas existentes
columns = []
types = []
for i, col in enumerate(st.session_state['columns']):
    col_name = st.sidebar.text_input(f'Nome da coluna {i+1}', value=col, key=f'col_{i}')
    tipo_sel = st.sidebar.selectbox(f'Tipo da coluna {i+1}', col_types, index=col_types.index(st.session_state['types'][i]) if st.session_state['types'][i] in col_types else 0, key=f'tipo_{i}')
    columns.append(col_name)
    types.append(tipo_sel)

num_rows = st.sidebar.number_input('Quantidade de linhas', min_value=1, max_value=10000, value=10)

generate = st.button('Gerar CSV')

if generate:
    data = {}
    for col, tipo in zip(columns, types):
        data[col] = generate_data(tipo, num_rows)
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False).encode('utf-8')
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="dados.csv">Baixar CSV</a>'
    st.success('Dados gerados com sucesso!')
    st.markdown(href, unsafe_allow_html=True)
    st.dataframe(df)
