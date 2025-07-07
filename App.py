# streamlit_app.py
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da página ---
st.set_page_config(
    page_title="Uso de Celular em Adolescentes",
    layout="wide",
    page_icon="📱"
)

st.markdown("""
<style>
.alert-box {
    padding: 15px;
    background-color: #fbe9e7;
    border-left: 6px solid #c0392b;
    margin-bottom: 20px;
    border-radius: 5px;
}
.alert-box p {
    color: #2c3e50;
    font-size: 16px;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_dados():
    df = pd.read_csv('teen_phone_addiction_dataset.csv')

    # Correção de tipos e normalização
    df['Gender'] = df['Gender'].str.capitalize().str.strip()
    df['Phone_Usage_Purpose'] = df['Phone_Usage_Purpose'].str.title().str.strip()

    # Tratamento de Parental_Control
    df['Parental_Control'] = df['Parental_Control'].apply(
        lambda x: 1 if str(x).lower() in ['1', 'yes', 'true'] else 0
    )

    # Conversão de colunas numéricas
    numeric_cols = [
        'Age', 'Daily_Usage_Hours', 'Sleep_Hours', 'Academic_Performance',
        'Social_Interactions', 'Exercise_Hours', 'Anxiety_Level',
        'Depression_Level', 'Self_Esteem', 'Screen_Time_Before_Bed',
        'Phone_Checks_Per_Day', 'Apps_Used_Daily', 'Time_on_Social_Media',
        'Time_on_Gaming', 'Time_on_Education', 'Weekend_Usage_Hours',
        'Addiction_Level', 'Family_Communication'
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Tratamento de valores ausentes
    df.fillna({
        'Academic_Performance': df['Academic_Performance'].median(),
        'Sleep_Hours': df['Sleep_Hours'].median(),
        'Anxiety_Level': df['Anxiety_Level'].median(),
        'Depression_Level': df['Depression_Level'].median(),
        'Self_Esteem': df['Self_Esteem'].median()
    }, inplace=True)

    # Criação de faixas etárias mais informativas
    bins = [0, 13, 16, 19, 26]
    labels = ['10-12', '13-15', '16-18', '19+']
    df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

    # Categorização do nível de vício
    df['Addiction_Category'] = pd.cut(
        df['Addiction_Level'],
        bins=[-1, 3, 7, 11],
        labels=['Baixo', 'Moderado', 'Alto'],
        right=True
    )

    return df

df = carregar_dados()

with st.sidebar:
    st.title("🔍 Filtros Avançados")
    st.markdown("Use os filtros abaixo para refinar a análise no dashboard.")

    with st.expander("📌 Filtros Demográficos", expanded=True):
        idade = st.slider("Faixa Etária",
                         int(df['Age'].min()),
                         int(df['Age'].max()),
                         (int(df['Age'].min()), int(df['Age'].max())))

        generos_disponiveis = df['Gender'].unique().tolist()
        genero = st.multiselect("Gênero", generos_disponiveis, default=generos_disponiveis)

        grupos_etarios_disponiveis = df['Age_Group'].dropna().unique().tolist()
        age_group = st.multiselect("Grupo Etário", grupos_etarios_disponiveis, default=grupos_etarios_disponiveis)

    with st.expander("📱 Filtros de Uso", expanded=True):
        propositos_disponiveis = df['Phone_Usage_Purpose'].unique().tolist()
        proposito = st.multiselect("Propósito Principal", propositos_disponiveis, default=propositos_disponiveis)

        addiction_level = st.slider("Nível de Vício",
                                   0.0, 10.0,
                                   (0.0, 10.0))

        parental_control = st.selectbox("Controle Parental",
                                      ["Todos", "Sim", "Não"])

# Aplicação dos filtros
df_filtrado = df[
    (df['Age'] >= idade[0]) & (df['Age'] <= idade[1]) &
    (df['Gender'].isin(genero)) &
    (df['Age_Group'].isin(age_group)) &
    (df['Phone_Usage_Purpose'].isin(proposito)) &
    (df['Addiction_Level'] >= addiction_level[0]) &
    (df['Addiction_Level'] <= addiction_level[1])
].copy()

if parental_control != "Todos":
    pc_value = 1 if parental_control == "Sim" else 0
    df_filtrado = df_filtrado[df_filtrado['Parental_Control'] == pc_value]

st.title("📱 Dashboard Analítico: Uso de Celular entre Adolescentes")
st.markdown("""
    Este dashboard explora visualmente os padrões de uso de smartphones e seus impactos em adolescentes, facilitando a descoberta de tendências e relações.
    Use os filtros na barra lateral para explorar os dados e segmentar a análise.
""")

st.info("Navegue pelas abas abaixo para explorar os diferentes aspectos da análise, desde a visão geral até os impactos na saúde mental.", icon="👆")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visão Geral",
    "📱 Padrões de Uso",
    "🧠 Saúde Mental",
    "📈 Análise de Correlações"
])

# ----------------------------
# TAB 1: Visão Geral
# ----------------------------
with tab1:
    st.subheader("Principais Indicadores do Grupo Selecionado")

    media_geral_horas = df['Daily_Usage_Hours'].mean()
    media_geral_desempenho = df['Academic_Performance'].mean()
    media_geral_vicio = df['Addiction_Level'].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Adolescentes", f"{len(df_filtrado):,}")
    with col2:
        delta_horas = df_filtrado['Daily_Usage_Hours'].mean() - media_geral_horas
        st.metric("Média de Horas/Dia",
                  f"{df_filtrado['Daily_Usage_Hours'].mean():.1f}h",
                  f"{delta_horas:+.1f}h vs Média Geral",
                  delta_color="inverse")
    with col3:
        delta_desempenho = df_filtrado['Academic_Performance'].mean() - media_geral_desempenho
        st.metric("Desempenho Escolar",
                  f"{df_filtrado['Academic_Performance'].mean():.0f}/100",
                  f"{delta_desempenho:+.0f} pts vs Média Geral",
                  delta_color="normal")
    with col4:
        delta_vicio = df_filtrado['Addiction_Level'].mean() - media_geral_vicio
        st.metric("Nível de Vício",
                  f"{df_filtrado['Addiction_Level'].mean():.1f}/10",
                  f"{delta_vicio:+.1f} vs Média Geral",
                  delta_color="inverse")

    st.markdown("---")

    st.subheader("Distribuição Demográfica")


    fig_demo, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Gráfico 1: Distribuição por gênero
    gender_dist = df_filtrado['Gender'].value_counts()
    axes[0].pie(gender_dist, labels=gender_dist.index, autopct='%1.1f%%', startangle=90)
    axes[0].set_title('Distribuição por Gênero')

    # Gráfico 2: Distribuição por faixa etária
    age_dist = df_filtrado['Age_Group'].value_counts().sort_index()
    age_dist.plot(kind='bar', ax=axes[1], color='skyblue')
    axes[1].set_title('Distribuição por Faixa Etária')
    axes[1].set_xlabel('Faixa Etária')
    axes[1].set_ylabel('Contagem')

    # Garante que a imagem não fique cortada
    plt.tight_layout()

    st.pyplot(fig_demo)

    st.subheader("Padrões de Uso por Idade e Gênero")

    usage_by_age_gender = df_filtrado.groupby(['Age', 'Gender'])['Daily_Usage_Hours'].mean().unstack()

    fig_heatmap = px.imshow(
        usage_by_age_gender,
        labels=dict(x="Gênero", y="Idade", color="Horas de Uso"),
        x=usage_by_age_gender.columns,
        y=usage_by_age_gender.index,
        color_continuous_scale='Reds',
        title="Média de Horas de Uso Diário por Idade e Gênero"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

# ----------------------------
# TAB 2: Padrões de Uso
# ----------------------------
with tab2:
    st.subheader("Como os Adolescentes Usam seus Celulares?")

    col1, col2 = st.columns(2)
    with col1:
        purpose_dist = df_filtrado['Phone_Usage_Purpose'].value_counts()
        fig_purpose = px.pie(
            purpose_dist,
            values=purpose_dist.values,
            names=purpose_dist.index,
            title="Distribuição do Propósito Principal de Uso"
        )
        st.plotly_chart(fig_purpose, use_container_width=True)

    with col2:
        fig_usage_purpose = px.box(
            df_filtrado,
            x="Phone_Usage_Purpose",
            y="Daily_Usage_Hours",
            color="Phone_Usage_Purpose",
            labels={ "Phone_Usage_Purpose": "Propósito Principal", "Daily_Usage_Hours": "Horas de Uso Diário" },
            title="Distribuição de Horas de Uso por Propósito"
        )
        st.plotly_chart(fig_usage_purpose, use_container_width=True)

    st.markdown("---")
    st.subheader("Relação entre Horas de Uso e Desempenho Escolar")

    fig_scatter = px.scatter(
        df_filtrado,
        x="Daily_Usage_Hours",
        y="Academic_Performance",
        color="Addiction_Category",
        color_discrete_map={'Baixo': 'green', 'Moderado': 'orange', 'Alto': 'red'},
        trendline="lowess",
        hover_data=["Gender", "Phone_Usage_Purpose"],
        labels={ "Daily_Usage_Hours": "Horas de Uso Diário", "Academic_Performance": "Desempenho Escolar (0-100)", "Addiction_Category": "Nível de Vício" },
        title="Horas de Uso vs Desempenho Escolar"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ----------------------------
# TAB 3: Saúde Mental
# ----------------------------
with tab3:

    st.subheader("O Preço Invisível: Impactos na Saúde Mental e no Sono")

    st.markdown("""
    <div class="alert-box">
        <p><strong>Conclusão Chave:</strong> O aumento do tempo de tela, especialmente antes de dormir, está fortemente associado a menos horas de sono, maiores níveis de ansiedade e menor autoestima entre os adolescentes.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Média de Ansiedade", f"{df_filtrado['Anxiety_Level'].mean():.1f}/10")
    with col2:
        st.metric("Média de Depressão", f"{df_filtrado['Depression_Level'].mean():.1f}/10")
    with col3:
        st.metric("Média de Autoestima", f"{df_filtrado['Self_Esteem'].mean():.1f}/10")

    # Relação entre sono e saúde mental
    st.subheader("Relação entre Sono e Saúde Mental")

    fig_sleep_mental = px.scatter_matrix(
        df_filtrado,
        dimensions=["Sleep_Hours", "Anxiety_Level", "Depression_Level", "Self_Esteem"],
        color="Addiction_Category",
        labels={
            "Sleep_Hours": "Horas de Sono",
            "Anxiety_Level": "Nível de Ansiedade",
            "Depression_Level": "Nível de Depressão",
            "Self_Esteem": "Autoestima",
            "Addiction_Category": "Nível de Vício"
        },
        title="Matriz de Dispersão: Sono vs Saúde Mental"
    )
    st.plotly_chart(fig_sleep_mental, use_container_width=True)

    st.markdown("---")
    st.subheader("Relação entre Tempo de Tela Antes de Dormir e Bem-Estar")

    col1, col2 = st.columns(2)
    with col1:
        fig_screen_sleep = px.scatter(
            df_filtrado, x="Screen_Time_Before_Bed", y="Sleep_Hours",
            color="Addiction_Category", trendline="lowess",
            color_discrete_map={'Baixo': 'green', 'Moderado': 'orange', 'Alto': 'red'},
            labels={ "Screen_Time_Before_Bed": "Tela Antes de Dormir (horas)", "Sleep_Hours": "Horas de Sono", "Addiction_Category": "Nível de Vício" },
            title="Tela Antes de Dormir vs Horas de Sono"
        )
        st.plotly_chart(fig_screen_sleep, use_container_width=True)

    with col2:
        fig_screen_anxiety = px.scatter(
            df_filtrado, x="Screen_Time_Before_Bed", y="Anxiety_Level",
            color="Age_Group", size="Addiction_Level",
            trendline="lowess",
            labels={ "Screen_Time_Before_Bed": "Tela Antes de Dormir (horas)", "Anxiety_Level": "Nível de Ansiedade", "Age_Group": "Faixa Etária", "Addiction_Level": "Nível de Vício" },
            title="Tela Antes de Dormir vs Nível de Ansiedade"
        )
        st.plotly_chart(fig_screen_anxiety, use_container_width=True)

# ----------------------------
# TAB 4: Análise de Correlações
# ----------------------------
with tab4:
    st.subheader("Quais Fatores Estão Mais Conectados?")

    selected_vars = st.multiselect(
        "Selecione variáveis para a análise de correlação:",
        options=df.select_dtypes(include='number').columns.tolist(),
        default=[
            'Daily_Usage_Hours', 'Academic_Performance', 'Sleep_Hours',
            'Anxiety_Level', 'Addiction_Level', 'Time_on_Social_Media'
        ]
    )

    if len(selected_vars) >= 2:
        corr = df_filtrado[selected_vars].corr()
        fig_corr = px.imshow(
            corr, text_auto=True, aspect="auto",
            color_continuous_scale='RdBu_r',
            range_color=[-1, 1],
            title="Matriz de Correlação entre Variáveis Selecionadas"
        )
        st.plotly_chart(fig_corr, use_container_width=True)

        with st.expander("📌 Como interpretar a Matriz de Correlação?"):
            st.markdown("""
            Este gráfico mostra como as variáveis se movem em conjunto:
            - **Valores próximos de +1 (Azul Intenso):** Indicam uma forte correlação positiva. Quando uma variável aumenta, a outra tende a aumentar também. (Ex: `Daily_Usage_Hours` e `Addiction_Level`).
            - **Valores próximos de -1 (Vermelho Intenso):** Indicam uma forte correlação negativa. Quando uma variável aumenta, a outra tende a diminuir. (Ex: `Sleep_Hours` e `Anxiety_Level`).
            - **Valores próximos de 0 (Branco/Cores Claras):** Indicam pouca ou nenhuma correlação linear entre as variáveis.
            """)
    else:
        st.warning("Selecione pelo menos 2 variáveis para visualizar a matriz de correlação.")

st.markdown("---")
st.markdown("""
    <div style="text-align: center;">
        <p>Dashboard desenvolvido como ferramenta de conscientização sobre o uso de tecnologia na adolescência.</p>
        <p><strong>Dados:</strong> Dataset simulado para fins educacionais, contendo 1000 registros.</p>
    </div>
    """, unsafe_allow_html=True)