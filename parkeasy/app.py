from shiny.express import input, ui, render
from shiny import reactive
import pandas as pd
from datetime import datetime

ui.tags.style("""
:root {
  --cinza-claro: #F5F5F5;
  --cinza-medio: #B0B0B0;
  --cinza-escuro: #4A4A4A;
  --texto-primario: #222222;
  --texto-secundario: #555555;
  --fundo-principal: #FFFFFF;
  --fundo-secundario: #E0E0E0;
}

html, body {
  scrollbar-width: none;
  -ms-overflow-style: none;
  overflow-y: scroll;
}

html::-webkit-scrollbar, 
body::-webkit-scrollbar {
  display: none;
}

body {
  background: var(--fundo-principal);
  color: var(--texto-primario);
  font-family: 'Inter', sans-serif;
  line-height: 1.5;
  margin: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.topo {
  background: var(--cinza-escuro);
  padding: 1rem 2rem;
  color: var(--fundo-principal);
  font-weight: 700;
  font-size: 1.8rem;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  user-select: none;
  text-align: center;
  letter-spacing: 1.2px;
  font-family: 'Inter', sans-serif;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.sidebar {
  background: var(--cinza-escuro);
  padding: 1.5rem 2rem;
  color: var(--fundo-principal);
  font-family: 'Inter', sans-serif;
  user-select: none;
  margin-bottom: 2rem;
  transition: background-color 0.3s ease;
  min-width: 280px;
  height: 100vh;
  box-sizing: border-box;
  overflow-y: auto;
}

.sidebar input[type="text"] {
  width: 100%;
  background: var(--fundo-secundario);
  border: 1.5px solid var(--cinza-medio);
  color: var(--texto-primario);
  border-radius: 10px;
  padding: 0.85rem 1.25rem;
  font-weight: 600;
  font-size: 1rem;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.sidebar input[type="text"]:focus {
  border-color: var(--cinza-claro);
  box-shadow: 0 0 8px 3px rgba(150, 150, 150, 0.5);
  outline: none;
}

.sidebar .btn {
  width: 100%;
  padding: 1rem 0;
  font-weight: 700;
  font-size: 1rem;
  margin-bottom: 1rem;
  border-radius: 12px;
  box-shadow: 0 3px 10px rgba(0,0,0,0.1);
  transition: transform 0.2s ease, box-shadow 0.3s ease;
  background: var(--cinza-medio);
  color: var(--texto-primario);
  border: none;
}

.sidebar .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.2);
}

.sidebar label {
  font-weight: 600;
  letter-spacing: 0.6px;
  margin-bottom: 0.7rem;
  color: var(--texto-primario);
  opacity: 0.95;
  display: block;
  font-size: 1.1rem;
}

.sidebar h3 {
  font-size: 1.4rem;
  letter-spacing: 0.5px;
  margin-bottom: 1.5rem;
  border-left: 3px solid var(--cinza-medio);
  padding-left: 0.75rem;
}

.vagas-disponiveis {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--cinza-medio);
  margin: 1rem 0;
  padding: 0.5rem 1rem;
  background: var(--fundo-secundario);
  border-radius: 8px;
  display: inline-block;
}

.vagas-disponiveis-titulo {
  color: var(--texto-primario);
  font-weight: 600;
  margin-bottom: 0.3rem;
}

main {
  flex: 1 1 auto;
  padding: 1rem 2rem;
  overflow-y: auto;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 6px;
  color: var(--texto-primario);
}

th {
  background: var(--cinza-medio);
  color: var(--texto-primario); /* Corrigido aqui */
  border-bottom: 2px solid var(--cinza-escuro);
  padding: 1rem;
  font-weight: 500;
  text-align: center;
}

td {
  background: var(--fundo-secundario);
  border: none;
  padding: 0.9rem 1rem;
  transition: all 0.2s ease;
  text-align: center;
  font-size: 1.1rem;
}

tbody tr:hover td {
  background: var(--cinza-claro);
  transform: scale(1.005);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

input[type="text"] {
  background: var(--fundo-secundario);
  border: 1px solid var(--cinza-medio);
  color: var(--texto-primario);
  border-radius: 8px;
  padding: 0.8rem 1.2rem;
  transition: all 0.2s ease;
}

input[type="text"]:focus {
  border-color: var(--cinza-claro);
  box-shadow: 0 0 0 3px rgba(150, 150, 150, 0.5);
}

h1, h2, h3, h4, h5, h6 {
  color: var(--texto-primario);
  margin: 0.5rem 0;
}

* {
  transition: background-color 0.2s ease, transform 0.2s ease;
}

main {
  flex: 1 1 auto;
  padding: 1rem 2rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.dataframe {
  flex: 1;
  width: 100% !important;
  max-width: 100% !important;
  overflow-x: auto;
}
""")

vagas_totais = 10
vagas = pd.DataFrame({
    "vaga": list(range(1, vagas_totais + 1)),
    "ocupada": [False] * vagas_totais,
    "placa": [None] * vagas_totais,
    "entrada": [None] * vagas_totais,
})

historico = []

gatilho_vagas = reactive.Value(0)
gatilho_historico = reactive.Value(0)

with ui.tags.div(class_="topo"):
    ui.tags.h1("Sistema de Estacionamento ParkEasy")

with ui.sidebar():
    with ui.tags.div(class_="mb-3"):
        ui.input_text("placa", "Placa do veículo", placeholder="EX: ABC1234")

    with ui.tags.div(class_="d-grid gap-2 mb-2"):
        ui.input_action_button("btn_entrar", "Registrar Entrada")
        ui.input_action_button("btn_sair", "Registrar Saída")

    ui.hr()

    with ui.tags.div(class_="mt-3"):
        ui.markdown("**Vagas disponíveis:**")

        @render.text
        def vagas_disponiveis():
            livres = (~vagas["ocupada"]).sum()
            return f"{livres} de {vagas_totais}"

def icone_ocupada(status: bool):
    return "✅" if status else  "❌"

@render.data_frame
def tabela_vagas():
    gatilho_vagas()
    df = vagas.copy()
    df["ocupada"] = df["ocupada"].apply(icone_ocupada)
    return df[["vaga", "ocupada", "placa", "entrada"]]

@render.data_frame
def tabela_historico():
    gatilho_historico()
    return pd.DataFrame(historico)

@reactive.effect
@reactive.event(input.btn_entrar)
def registrar_entrada():
    placa = input.placa().strip().upper()
    if not placa:
        ui.notification_show("Informe a placa do veículo.", type="warning")
        return
    if placa in vagas["placa"].values:
        ui.notification_show("Veículo já está estacionado.", type="warning")
        return
    vagas_livres = vagas[~vagas["ocupada"]]
    if vagas_livres.empty:
        ui.notification_show("Estacionamento cheio.", type="error")
        return
    idx = vagas_livres.index[0]
    vagas.at[idx, "ocupada"] = True
    vagas.at[idx, "placa"] = placa
    vagas.at[idx, "entrada"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    gatilho_vagas.set(gatilho_vagas() + 1)
    ui.notification_show(f"Veículo {placa} entrou na vaga {vagas.at[idx, 'vaga']}.", type="message")

@reactive.effect
@reactive.event(input.btn_sair)
def registrar_saida():
    placa = input.placa().strip().upper()
    if not placa or placa not in vagas["placa"].values:
        ui.notification_show("Veículo não encontrado no estacionamento.", type="warning")
        return
    idx = vagas[vagas["placa"] == placa].index[0]
    saida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historico.append({
        "Placa": placa,
        "Entrada": vagas.at[idx, "entrada"],
        "Saída": saida,
        "Vaga": vagas.at[idx, "vaga"]
    })
    vagas.at[idx, "ocupada"] = False
    vagas.at[idx, "placa"] = None
    vagas.at[idx, "entrada"] = None
    gatilho_vagas.set(gatilho_vagas() + 1)
    gatilho_historico.set(gatilho_historico() + 1)
    ui.notification_show(f"Veículo {placa} saiu da vaga {vagas.at[idx, 'vaga']}.", type="message")
