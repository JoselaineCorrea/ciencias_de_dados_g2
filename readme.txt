# Dashboard: Análise de Vício em Celulares na Adolescência

Este projeto consiste em um dashboard interativo desenvolvido com Streamlit para explorar e visualizar os dados sobre o vício em smartphones entre adolescentes. A aplicação permite a análise de como diferentes padrões de uso se correlacionam com o desempenho acadêmico e indicadores de saúde mental.


---

## 🚀 Principais Funcionalidades

- **Visualização de Dados Agregados:** Métricas gerais sobre a amostra de dados, incluindo horas de uso, desempenho escolar e nível de vício.
- **Análise Demográfica:** Gráficos interativos sobre a distribuição dos dados por gênero e faixa etária.
- **Padrões de Uso:** Análise detalhada de como e para quê os celulares são usados, e a relação entre tempo de tela e performance acadêmica.
- **Impacto na Saúde Mental:** Gráficos que correlacionam o uso do celular com horas de sono, ansiedade, depressão e autoestima.
- **Filtros Interativos:** Permite que o usuário segmente a base de dados por idade, gênero, propósito de uso e nível de vício para análises específicas.

---

## 🛠️ Tecnologias Utilizadas

- **Python**
- **Streamlit** - Para a construção do dashboard interativo.
- **Pandas** - Para manipulação e limpeza dos dados.
- **Plotly** - Para a criação de gráficos interativos.
- **Matplotlib** - Para a criação de gráficos estáticos customizados.

---

## ⚙️ Como Executar o Projeto Localmente

Siga os passos abaixo para rodar o projeto no seu computador.

**1. Pré-requisitos**

- Ter o [Python 3.8+](https://www.python.org/downloads/) instalado.
- Ter o [Git](https://git-scm.com/) instalado.

**2. Clonar o Repositório**

```bash
git clone https://github.com/JoselaineCorrea/ciencias_de_dados_g2.git

cd nome-do-seu-repositorio
```

**3. Criar um Ambiente Virtual (Recomendado)**

Para manter as dependências isoladas, crie um ambiente virtual:

```bash
# Criar o ambiente
python -m venv venv

# Ativar o ambiente
# No Windows:
venv\Scripts\activate

```

**4. Instalar as Dependências**

Com o ambiente virtual ativado, instale as bibliotecas necessárias que estão no arquivo `requirements.txt`:

```bash
pip install streamlit
pip install -r requirements.txt
```

**5. Rodar o Aplicativo Streamlit**

Finalmente, execute o comando abaixo para iniciar o dashboard:

```bash
streamlit run App.py
```

O dashboard abrirá automaticamente no seu navegador padrão.
