import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('rendimentos.csv', sep=',')
years_salaries = df.iloc[:, 0:2]
df = df.iloc[:, 2:].applymap(lambda x: float(x.replace('R$ ', '').replace('.', '').replace(',', '.')))
df = pd.concat([years_salaries, df], axis=1)
df = df[df['Ano Calendário'].isin([2016, 2017, 2018, 2019, 2020])]


def formatar_para_reais(valor):
    return f'R$ {valor:,.2f}' if isinstance(valor, (int, float)) else valor


st.title("Visualização de Dados")

columns_to_display = [
    'Lucros e dividendos recebidos', 
    'Indenizações por rescisão de contrato de trabalho, inclusive a título de PDV, e por acidente de trabalho; e FGTS', 
    'Ganho de capital na alienação do único imóvel por valor igual ou inferior a R$ 440.000,00 e que, nos últimos 5 anos, não tenha efetuado nenhuma outra alienação de imóvel', 
    'Transferências patrimoniais - doações e heranças', 
    'Rendimentos de cadernetas de poupança, letras hipotecárias, letras de crédito do agronegócio e imobiliário (LCA e LCI) e certificados de recebíveis do agronegócio e imobiliários (CRA e CRI)'
]

columns_to_display = [col for col in columns_to_display if col in df.columns]
mandatory_columns = ['Ano Calendário', 'Faixa de Salários-Mínimos']

col1, col2 = st.columns([2, 1])

with col1:
    selected_column = st.selectbox(
        "Selecione a coluna que deseja visualizar:",
        options=columns_to_display
    )
with col2:
    selected_year = st.selectbox(
        "Selecione o Ano Calendário",
        ['Todos os anos'] + list(df['Ano Calendário'].unique()) 
    )

if selected_year == 'Todos os anos':
    df_filtered = df.copy() 
    show_all_years = True
else:
    df_filtered = df[df['Ano Calendário'] == selected_year]
    show_all_years = False

if selected_column:
    df_filtered['Ano Calendário'] = df_filtered['Ano Calendário'].astype(str)
    st.header("DataFrame e Média")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.dataframe(df_filtered[mandatory_columns + [selected_column]].applymap(formatar_para_reais))

    with col2:
        average_value = df_filtered[selected_column].mean()
        total_sum = df_filtered[selected_column].sum()

        st.info(f"A média dos valores é: {formatar_para_reais(average_value)}")
        st.success(f"Somatório Total: {formatar_para_reais(total_sum)}")

    fig = px.line(df_filtered, x='Faixa de Salários-Mínimos', y=selected_column,
                  title=f'Gráfico de {selected_column}',
                  labels={selected_column: 'Reais', 'Faixa de Salários-Mínimos': 'Faixa de Salários-Mínimos'},
                  color='Ano Calendário', 
                  line_group='Ano Calendário', 
                  hover_name='Ano Calendário' 
                  )

    fig.add_hline(y=average_value, line_dash="dot", line_color="red", annotation_text='Média',
                  annotation_position="bottom right")

    st.plotly_chart(fig)
else:
    st.write("Por favor, selecione pelo menos uma coluna para visualizar.")
