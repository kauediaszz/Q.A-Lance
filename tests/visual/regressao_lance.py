from playwright.sync_api import sync_playwright
import time
import os
from datetime import datetime

# ==========================================
# MASSA DE DADOS: URLs PARA REGRESSÃO VISUAL
# ==========================================
URLS_TESTE = {
    # 1. HOME PRINCIPAL
    "1_Home_Principal": "https://www.lance.com.br/",

    # 2. HOMES INTERNAS (TIMES)
    "2_Time_Flamengo": "https://www.lance.com.br/flamengo",
    "3_Time_Palmeiras": "https://www.lance.com.br/palmeiras",
    "4_Time_Atletico_MG": "https://www.lance.com.br/atletico-mineiro",
    "5_Time_Corinthians": "https://www.lance.com.br/corinthians",
    "6_Time_Fortaleza": "https://www.lance.com.br/fortaleza",
    "7_Time_Santos": "https://www.lance.com.br/santos",
    "8_Time_Bahia": "https://www.lance.com.br/bahia",
    "9_Time_Cruzeiro": "https://www.lance.com.br/cruzeiro",
    "10_Time_Gremio": "https://www.lance.com.br/gremio",
    "11_Time_Sao_Paulo": "https://www.lance.com.br/sao-paulo",
    "12_Time_Botafogo": "https://www.lance.com.br/botafogo",
    "13_Time_Internacional": "https://www.lance.com.br/internacional",
    "14_Time_Vasco": "https://www.lance.com.br/vasco",
    "15_Time_Ceara": "https://www.lance.com.br/ceara",
    "16_Time_Fluminense": "https://www.lance.com.br/fluminense",
    "17_Time_Vitoria": "https://www.lance.com.br/vitoria",

    # 3. TABELAS DE CAMPEONATOS
    "18_Tabelas_Brasileirao": "https://www.lance.com.br/tabela/brasileirao",
    "19_Tabelas_Brasileirao_Serie_B": "https://www.lance.com.br/tabela/brasileirao-serie-b",
    "20_Tabelas_Copa_do_Brasil": "https://www.lance.com.br/tabela/copa-do-brasil",
    "21_Tabelas_Libertadores": "https://www.lance.com.br/tabela/libertadores",
    "22_Tabelas_Champions_League": "https://www.lance.com.br/tabela/champions-league",
    "23_Tabelas_Premier_League": "https://www.lance.com.br/tabela/premier-league",
    "24_Tabelas_Campeonato_Espanhol": "https://www.lance.com.br/tabela/campeonato-espanhol",
    "25_Tabelas_Campeonato_Saudita": "https://www.lance.com.br/tabela/campeonato-saudita",
    "26_Tabelas_Campeonato_Italiano": "https://www.lance.com.br/tabela/campeonato-italiano",
    "27_Tabelas_Campeonato_Alemao": "https://www.lance.com.br/tabela/campeonato-alemao",
    "28_Tabelas_Campeonato_Frances": "https://www.lance.com.br/tabela/campeonato-frances",

    # 4. TEMPO REAL E AGENDA
    "29_Tempo_Real_Agenda": "https://www.lance.com.br/temporeal/agenda",

    # 5. DEMAIS PÁGINAS E EDITORIAS
    "30_Ultimas_Noticias": "https://www.lance.com.br/mais-noticias",
    "31_Futebol_Internacional": "https://www.lance.com.br/futebol-internacional",
    "32_Futebol_Feminino": "https://www.lance.com.br/futebol-feminino",
    "33_Mercado_da_Bola": "https://www.lance.com.br/mercado-da-bola",
    "34_Galerias": "https://www.lance.com.br/galerias",
    "35_NBA": "https://www.lance.com.br/nba",
    "36_Tenis": "https://www.lance.com.br/tenis",
    "37_Volei": "https://www.lance.com.br/volei",
    "38_Formula_1": "https://www.lance.com.br/formula-1",
    "39_Lutas": "https://www.lance.com.br/lutas",
    "40_Onde_Assistir": "https://www.lance.com.br/onde-assistir"
}

TIMEOUT_PAGINA = 90000

def realizar_regressao_visual():
    # 1. Configurações de pastas e logs
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pasta_evidencias = f"evidencias_visuais_{timestamp}"
    os.makedirs(pasta_evidencias, exist_ok=True)
    arquivo_log = os.path.join(pasta_evidencias, "relatorio_visual.txt")

    def registrar_log(mensagem):
        print(mensagem)
        with open(arquivo_log, "a", encoding="utf-8") as f:
            f.write(mensagem + "\n")

    # =========================================================
    # FUNÇÃO: Scroll Humanizado (Evita quebra por Lazy Loading)
    # =========================================================
    def scroll_humanizado(pagina_alvo):
        registrar_log("   👉 Executando scroll humanizado...")
        for _ in range(8):
            pagina_alvo.mouse.wheel(0, 800)
            time.sleep(0.5)
        pagina_alvo.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        time.sleep(2)

    registrar_log("🚀 Iniciando Suíte de Regressão Visual em Lote - Lance.com.br")
    registrar_log(f"📁 As 40 evidências serão salvas em: {pasta_evidencias}\n")

    with sync_playwright() as p:
        navegador = p.chromium.launch(channel="chrome", headless=False)
        contexto = navegador.new_context(viewport={'width': 1920, 'height': 1080})
        pagina = contexto.new_page()

        # O laço de repetição (for) vai ler a nossa lista de 40 URLs uma por uma
        for nome_pagina, url in URLS_TESTE.items():
            try:
                registrar_log(f"⏳ Acessando [{nome_pagina}]: {url}")
                pagina.goto(url, timeout=TIMEOUT_PAGINA)
                
                # Roda o scroll em todas as páginas para garantir o visual perfeito
                scroll_humanizado(pagina)
                
                # Define o caminho e o nome da foto
                caminho_foto = os.path.join(pasta_evidencias, f"{nome_pagina}.png")
                
                # Tira a foto pegando a PÁGINA INTEIRA (full_page=True)
                pagina.screenshot(path=caminho_foto, full_page=True)
                registrar_log(f"✅ PASSOU - Print capturado: {nome_pagina}.png\n")
                
            except Exception as e:
                registrar_log(f"❌ FALHOU - Erro ao capturar {nome_pagina}: {e}\n")

        navegador.close()
        registrar_log("\n🎉 Regressão Visual Finalizada! Todas as 40 páginas foram processadas.")

if __name__ == "__main__":
    realizar_regressao_visual()