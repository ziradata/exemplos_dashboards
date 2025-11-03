import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc # Importando a nova biblioteca de layout

# --- Paleta de Cores (para os gráficos) ---
colors = {
    'background': '#17171C',
    'panel': '#1F1F25',
    'text': '#E6E6E6',
    'primary_blue': '#3B82F6',
    'primary_green': '#10B981',
    'red': '#EF4444',
    'yellow': '#F59E0B',
}

# ==============================================================================
# INICIALIZAÇÃO DO APP (Agora com o tema DARKLY do Bootstrap)
# ==============================================================================
# Usar um tema Bootstrap torna o layout muito mais profissional
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# ==============================================================================
# DADOS FALSOS (MOCK DATA)
# ==============================================================================

# --- Dados para o Gráfico 1: Financeiro (Cobrança - Gráfico de Gauge) ---
# (Este gráfico será criado com Plotly Graph Objects, não precisa de DataFrame)

# --- Dados para o Gráfico 2: Financeiro (Faturas Vencidas - Bar Chart) ---
df_faturas_vencidas = pd.DataFrame({
    'Data': ['02/10', '03/10', '04/10', '05/10', '06/10', '07/10', '08/10'],
    'Valor': [9100.10, 17698.26, 14871.20, 24195.21, 1200.00, 1345.80, 4337.45]
})

# --- Dados para o Gráfico 3: Financeiro (Recebidos x Pendentes - H-Bar Chart) ---
df_recebidos_pendentes = pd.DataFrame({
    'Semana': ['27/10/2025', '13/10/2025', '18/10/2025', '24/10/2025', '31/10/2025', '07/11/2025', '14/11/2025', 'Outros (6)'],
    'Recebido': [23094.49, 44152.84, 41936.08, 22104.33, 58706.12, 41120.10, 42128.82, 40177.57],
    'A-Receber': [15090.40, 12000.10, 5009.10, 18001.90, 14000.10, 23000.10, 17000.56, 34193.84] # Exemplo de 'Outros' com pendente
})

# --- Dados para o Gráfico 4: Logística (Performance de Entregas) ---
df_logistica = pd.DataFrame({
    "Mes": ["Jan", "Fev", "Mar", "Abr"],
    "Entregas no Prazo": [120, 140, 130, 150],
    "Entregas Atrasadas": [10, 8, 15, 5]
})

# ==============================================================================
# FIGURAS (Gráficos Plotly)
# ==============================================================================

# --- Figura 1: Gauge Chart (Financeiro) ---
fig_gauge_cobranca = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 73.72,
    number = {'suffix': "%", 'font': {'size': 50}},
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Índice de Recebimento dos Títulos", 'font': {'size': 20, 'color': colors['text']}},
    gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': colors['primary_blue'], 'thickness': 0.3},
        'bgcolor': "rgba(0,0,0,0)",
        'borderwidth': 2,
        'bordercolor': colors['panel'],
        'steps': [
            {'range': [0, 30], 'color': colors['red']},
            {'range': [30, 70], 'color': colors['yellow']},
            {'range': [70, 100], 'color': colors['primary_green']}
        ],
    }
))
fig_gauge_cobranca.update_layout(
    paper_bgcolor=colors['panel'], 
    font_color=colors['text'],
    height=350
)

# --- Figura 2: Bar Chart (Faturas Vencidas) ---
fig_bar_vencidas = px.bar(
    df_faturas_vencidas, x='Data', y='Valor',
    title='Faturas vencidas nos últimos 20 dias'
)
fig_bar_vencidas.update_traces(marker_color=colors['primary_blue'])

# --- Figura 3: Horizontal Bar Chart (Recebidos x Pendentes) ---
fig_bar_pendentes = go.Figure()
fig_bar_pendentes.add_trace(go.Bar(
    y=df_recebidos_pendentes['Semana'],
    x=df_recebidos_pendentes['Recebido'],
    name='Recebido',
    orientation='h',
    marker_color=colors['primary_green']
))
fig_bar_pendentes.add_trace(go.Bar(
    y=df_recebidos_pendentes['Semana'],
    x=df_recebidos_pendentes['A-Receber'],
    name='A-Receber',
    orientation='h',
    marker_color=colors['red']
))
fig_bar_pendentes.update_layout(
    barmode='stack', 
    title='Recebidos x Pendentes - Por Semana',
    yaxis={'categoryorder':'total ascending'} # Ordena as barras
)

# --- Figura 4: Bar Chart (Logística) ---
fig_logistica = px.bar(
    df_logistica, x="Mes", y=["Entregas no Prazo", "Entregas Atrasadas"], 
    title="Performance de Entregas", barmode='group'
)

# --- Figura 5: Gauge Chart (Compliance) ---
fig_compliance = go.Figure(go.Indicator(
    mode="gauge+number",
    value=85,
    title={'text': "Licenças de Frota Ativas (%)"},
    gauge={'axis': {'range': [None, 100]},
           'bar': {'color': colors['primary_blue']},
           'steps': [
               {'range': [0, 50], 'color': colors['red']},
               {'range': [50, 80], 'color': colors['yellow']}],
           }
))

# --- Aplica o Tema Dark em todos os gráficos de barra/linha ---
for fig in [fig_bar_vencidas, fig_bar_pendentes, fig_logistica, fig_compliance]:
    fig.update_layout(
        plot_bgcolor=colors['panel'],
        paper_bgcolor=colors['panel'],
        font_color=colors['text']
    )

# ==============================================================================
# FUNÇÕES DE COMPONENTES REUTILIZÁVEIS (KPI Cards)
# ==============================================================================

# Esta função cria um "Card" de KPI (os retângulos com números grandes)
def create_kpi_card(title, value, id, color=colors['text']):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H6(title, className="card-title", style={'color': colors['text']}),
                html.H4(value, className="card-text", style={'color': color, 'fontSize': '2rem', 'fontWeight': 'bold'}),
            ]
        ),
        className="mb-3",
        style={'backgroundColor': colors['panel']}
    )

# ==============================================================================
# LAYOUT DO APP DASH
# ==============================================================================
app.layout = html.Div(style={'backgroundColor': colors['background'], 'minHeight': '100vh'}, children=[
    dbc.Container(fluid=True, children=[
        html.H1(
            children='Principais KPI`s e Dashboards Corporativos',
            style={'textAlign': 'center', 'color': colors['text'], 'padding': '20px'}
        ),

        dcc.Tabs(id="tabs-dashboards", value='tab-cobranca', children=[
            dcc.Tab(label='Financeiro (Cobrança)', value='tab-cobranca', style={'backgroundColor': colors['panel'], 'color': colors['text']}, selected_style={'backgroundColor': colors['primary_blue'], 'color': colors['panel'], 'fontWeight': 'bold'}),
            dcc.Tab(label='Logística', value='tab-logistica', style={'backgroundColor': colors['panel'], 'color': colors['text']}, selected_style={'backgroundColor': colors['primary_blue'], 'color': colors['panel'], 'fontWeight': 'bold'}),
            dcc.Tab(label='Compliance', value='tab-compliance', style={'backgroundColor': colors['panel'], 'color': colors['text']}, selected_style={'backgroundColor': colors['primary_blue'], 'color': colors['panel'], 'fontWeight': 'bold'}),
        ]),
        
        # Conteúdo que será trocado pela Callback
        html.Div(id='tabs-content-output', style={'paddingTop': '20px'})
    ])
])

# ==============================================================================
# CALLBACKS (Interatividade)
# ==============================================================================

@app.callback(Output('tabs-content-output', 'children'),
              Input('tabs-dashboards', 'value'))
def render_content(tab):
    
    # --- ABA 1: FINANCEIRO (COBRANÇA) ---
    if tab == 'tab-cobranca':
        return dbc.Container(fluid=True, children=[
            # --- Primeira Linha ---
            dbc.Row([
                # Coluna 1: Gauge Chart
                dbc.Col(
                    dcc.Graph(id='gauge-cobranca', figure=fig_gauge_cobranca),
                    md=4, # 4 de 12 colunas = 33%
                    style={'height': '100%'}
                ),
                # Coluna 2: KPIs Principais
                dbc.Col([
                    create_kpi_card("Valor Total de títulos com Vencimento até ontem", "R$1.269.773,23", "kpi-total", colors['primary_blue']),
                    create_kpi_card("Valor Total de títulos pago no mês até ontem", "R$2.269.773,23", "kpi-total", colors['primary_blue']),
                                
                    
                    dbc.Row([
                        dbc.Col(create_kpi_card("Qtd. com vencimento até ontem", "936", "kpi-qtd"), md=6),
                        dbc.Col(create_kpi_card("Qtd. pagos no mês, vencimentos até ontem", "690", "kpi-pagos"), md=6),
                        
                    ])
                ], md=8), # 8 de 12 colunas = 66%
            ]),
            
            # --- Segunda Linha ---
            dbc.Row([
                # Coluna 1: Bar Chart Vertical
                dbc.Col(
                    dcc.Graph(id='bar-vencidas', figure=fig_bar_vencidas),
                    md=6 # 6 de 12 colunas = 50%
                ),
                # Coluna 2: Bar Chart Horizontal
                dbc.Col(
                    dcc.Graph(id='bar-pendentes', figure=fig_bar_pendentes),
                    md=6 # 6 de 12 colunas = 50%
                ),
            ]),
            
            # --- Terceira Linha (KPIs Inferiores) ---
            dbc.Row([
                dbc.Col(create_kpi_card("Faturas vencidas nos últimos 20 dias", "R$259.002,18", "kpi-vencidas", colors['red']), md=3),
                dbc.Col(create_kpi_card("Faturas a Receber nos próximos 20 dias", "R$804.862,72", "kpi-receber", colors['primary_green']), md=3),
                dbc.Col(create_kpi_card("Total de Títulos com Vencimentos no Mês", "936", "kpi-total-mes"), md=3),
                dbc.Col(create_kpi_card("Vencimentos do Mês", "R$1.269.773,23", "kpi-venc-mes"), md=3),
            ])
        ])
    
    # --- ABA 2: LOGÍSTICA ---
    elif tab == 'tab-logistica':
        return dbc.Container(fluid=True, children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id='logistica-graph', figure=fig_logistica), md=12)
            ]),
            dbc.Row([
                dbc.Col(create_kpi_card("Total de Entregas", "448", "kpi-log-1"), md=4),
                dbc.Col(create_kpi_card("Taxa de Atraso Média", "6.2%", "kpi-log-2", colors['red']), md=4),
                dbc.Col(create_kpi_card("Custo Médio por Entrega", "R$12,45", "kpi-log-3"), md=4),
            ])
        ])
        
    # --- ABA 3: COMPLIANCE ---
    elif tab == 'tab-compliance':
        return dbc.Container(fluid=True, children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id='compliance-graph', figure=fig_compliance), md=6),
                dbc.Col([
                    create_kpi_card("Total de Licenças", "120", "kpi-comp-1"),
                    create_kpi_card("Licenças a Vencer (30 dias)", "18", "kpi-comp-2", colors['yellow']),
                    create_kpi_card("Licenças Vencidas", "5", "kpi-comp-3", colors['red']),
                ], md=6)
            ])
        ])

# ==============================================================================
# EXECUTAR O SERVIDOR
# =Corrigindo a linha conforme sua solicitação
# ==============================================================================
if __name__ == '__main__':
    app.run(debug=True, port=8050)
