import asyncio
import json
import os
from datetime import datetime
from playwright.async_api import async_playwright

TIMEOUT_PAGINA = 90000

# ==========================================
# FUNÇÃO PARA LER AS URLs DO ARQUIVO JSON
# ==========================================
def carregar_urls():
    # Pega o caminho exato onde este script está rodando
    diretorio_atual = os.path.dirname(__file__)
    caminho_arquivo = os.path.join(diretorio_atual, "urls.json")
    
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        return json.load(f)

# Esta função cuida de UMA única página
async def processar_pagina(nome_pagina, url, contexto, pasta_evidencias, semaforo, registrar_log):
    async with semaforo:
        pagina = None
        try:
            registrar_log(f"⏳ [INICIANDO] {nome_pagina}")
            pagina = await contexto.new_page()
            await pagina.goto(url, timeout=TIMEOUT_PAGINA)
            
            # Scroll humanizado assíncrono
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

    # Carrega as URLs diretamente do arquivo JSON!
    urls_teste = carregar_urls()

    registrar_log(f"🚀 Iniciando Suíte Visual TURBO ({len(urls_teste)} páginas | 5 abas simultâneas)...")

    async with async_playwright() as p:
        # Modo invisível para voar baixo
        navegador = await p.chromium.launch(headless=True)
        contexto = await navegador.new_context(viewport={'width': 1920, 'height': 1080})
        
        # O semáforo limita para 5 abas abertas ao mesmo tempo
        semaforo = asyncio.Semaphore(5)
        tarefas = []

        # Prepara a fila de trabalho
        for nome_pagina, url in urls_teste.items():
            tarefa = asyncio.create_task(
                processar_pagina(nome_pagina, url, contexto, pasta_evidencias, semaforo, registrar_log)
            )
            tarefas.append(tarefa)

        # Dispara todas as tarefas
        await asyncio.gather(*tarefas)

        await navegador.close()
        registrar_log("\n🎉 Regressão Visual TURBO Finalizada!")

if __name__ == "__main__":
    asyncio.run(rodar_regressao_turbo())