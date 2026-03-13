import asyncio
from playwright.async_api import async_playwright
import os
from datetime import datetime

# ==========================================
# MASSA DE DADOS: URLs PARA REGRESSÃO VISUAL
# ==========================================
URLS_TESTE = {
    "1_Home_Principal": "https://www.lance.com.br/",
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
    "29_Tempo_Real_Agenda": "https://www.lance.com.br/temporeal/agenda",
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

# Esta função cuida de UMA única página (agora usando await)
async def processar_pagina(nome_pagina, url, contexto, pasta_evidencias, semaforo, registrar_log):
    # O semáforo segura a emoção do código para não abrir 40 abas de uma vez e explodir a memória do PC
    async with semaforo:
        pagina = None
        try:
            registrar_log(f"⏳ [INICIANDO] {nome_pagina}")
            pagina = await contexto.new_page()
            await pagina.goto(url, timeout=TIMEOUT_PAGINA)
            
            # Scroll humanizado assíncrono (muito mais rápido)
            for _ in range(8):
                await pagina.mouse.wheel(0, 800)
                await asyncio.sleep(0.2)
            await pagina.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
            await asyncio.sleep(1)
            
            caminho_foto = os.path.join(pasta_evidencias, f"{nome_pagina}.png")
            await pagina.screenshot(path=caminho_foto, full_page=True)
            registrar_log(f"✅ [PASSOU] {nome_pagina}")
            
        except Exception as e:
            registrar_log(f"❌ [FALHOU] {nome_pagina}: {e}")
        finally:
            if pagina:
                await pagina.close()

# O Maestro que coordena as abas
async def rodar_regressao_turbo():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pasta_evidencias = f"evidencias_visuais_{timestamp}"
    os.makedirs(pasta_evidencias, exist_ok=True)
    arquivo_log = os.path.join(pasta_evidencias, "relatorio_visual.txt")

    def registrar_log(mensagem):
        print(mensagem)
        with open(arquivo_log, "a", encoding="utf-8") as f:
            f.write(mensagem + "\n")

    registrar_log("🚀 Iniciando Suíte Visual TURBO (5 abas simultâneas)...")

    async with async_playwright() as p:
        # Modo invisível ligado para máxima performance
        navegador = await p.chromium.launch(headless=True)
        contexto = await navegador.new_context(viewport={'width': 1920, 'height': 1080})
        
        # Define que o robô pode abrir até 5 abas ao mesmo tempo
        semaforo = asyncio.Semaphore(5)
        tarefas = []

        # Prepara todas as tarefas
        for nome_pagina, url in URLS_TESTE.items():
            tarefa = asyncio.create_task(
                processar_pagina(nome_pagina, url, contexto, pasta_evidencias, semaforo, registrar_log)
            )
            tarefas.append(tarefa)

        # Dispara todas as 5 abas e vai puxando as próximas da fila conforme forem terminando
        await asyncio.gather(*tarefas)

        await navegador.close()
        registrar_log("\n🎉 Regressão Visual TURBO Finalizada!")

if __name__ == "__main__":
    # O Python precisa desse comando para rodar coisas assíncronas
    asyncio.run(rodar_regressao_turbo())