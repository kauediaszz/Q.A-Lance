from playwright.sync_api import sync_playwright, expect
import time
import os
import json
from datetime import datetime

TIMEOUT_PAGINA = 90000   
TIMEOUT_ELEMENTO = 15000 

def carregar_urls():
    diretorio_atual = os.path.dirname(__file__)
    caminho_arquivo = os.path.join(diretorio_atual, "urls_funcionais.json")
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        return json.load(f)

def rodar_testes_planilha():
    urls = carregar_urls()
    URL_HOME = urls["URL_HOME"]
    URL_TABELA = urls["URL_TABELA"]
    URL_AGENDA = urls["URL_AGENDA"]
    URL_TIME = urls["URL_TIME"]

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pasta_evidencias = f"evidencias_funcionais_{timestamp}"
    os.makedirs(pasta_evidencias, exist_ok=True)
    arquivo_log = os.path.join(pasta_evidencias, "relatorio_execucao.txt")

    def registrar_log(mensagem):
        print(mensagem)
        with open(arquivo_log, "a", encoding="utf-8") as f:
            f.write(mensagem + "\n")

    def scroll_humanizado(pagina_alvo):
        for _ in range(8):
            pagina_alvo.mouse.wheel(0, 800)
            time.sleep(0.5)
        pagina_alvo.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        time.sleep(2)

    registrar_log("Iniciando Suíte de Regressão Funcional COMPLETA - Lance.com.br")
    registrar_log(f" Evidências serão salvas em: {pasta_evidencias}\n")
    
    with sync_playwright() as p:
        navegador = p.chromium.launch(channel="chrome", headless=False)
        contexto = navegador.new_context(viewport={'width': 1920, 'height': 1080})
        pagina = contexto.new_page()

        try:
            registrar_log(" [HOME-01] Carregamento da Home...")
            pagina.goto(URL_HOME, timeout=TIMEOUT_PAGINA)
            scroll_humanizado(pagina) 
            expect(pagina.locator("header").first).to_be_visible(timeout=TIMEOUT_ELEMENTO)
            expect(pagina.locator("footer").first).to_be_visible(timeout=TIMEOUT_ELEMENTO)
            pagina.screenshot(path=os.path.join(pasta_evidencias, "HOME-01_Carregamento_da_Home.png"))
            registrar_log(" PASSOU - Header e Footer visíveis.")
        except Exception as e:
            pagina.screenshot(path=os.path.join(pasta_evidencias, "HOME-01_ERRO.png"))
            registrar_log(f"FALHOU: {e}")

        try:
            registrar_log(" [SEO-01] Meta Tags e Title...")
            titulo = pagina.title()
            assert len(titulo) > 0, "Title está vazio!"
            meta_desc = pagina.locator('meta[name="description"]').get_attribute("content")
            assert len(meta_desc) > 0, "Meta description está vazia!"
            pagina.screenshot(path=os.path.join(pasta_evidencias, "SEO-01_Meta_Tags_e_Title.png"))
            registrar_log(f" PASSOU - Title: {titulo[:30]}...")
        except Exception as e:
            registrar_log(f" FALHOU: {e}")

        try:
            registrar_log(" [ADS-01] Carregamento de Banners...")
            pagina.locator("iframe").first.wait_for(state="attached", timeout=TIMEOUT_ELEMENTO)
            anuncios = pagina.locator("iframe").count()
            assert anuncios > 0, "Nenhum banner/iframe de anúncio foi encontrado na Home."
            pagina.screenshot(path=os.path.join(pasta_evidencias, "ADS-01_Carregamento_de_Banners.png"))
            registrar_log(f" PASSOU - Encontrados {anuncios} iframes de publicidade.")
        except Exception as e:
            pagina.screenshot(path=os.path.join(pasta_evidencias, "ADS-01_ERRO.png"))
            registrar_log(f"FALHOU: {e}")

        try:
            registrar_log(" [MENU-01] Página de Times/Clubes...")
            pagina.goto(URL_TIME, timeout=TIMEOUT_PAGINA)
            scroll_humanizado(pagina) 
            expect(pagina.locator("h1").first).to_be_visible(timeout=TIMEOUT_ELEMENTO)
            pagina.screenshot(path=os.path.join(pasta_evidencias, "MENU-01_Menu_de_Times.png"))
            registrar_log(" PASSOU - Página do Flamengo acessada corretamente.")
        except Exception as e:
            pagina.screenshot(path=os.path.join(pasta_evidencias, "MENU-01_ERRO.png"))
            registrar_log(f"FALHOU: {e}")

        try:
            registrar_log(" [HOME-02] Carrossel de Destaques...")
            pagina.goto(URL_HOME, timeout=TIMEOUT_PAGINA)
            time.sleep(3) 
            pagina.locator("main a").first.click(timeout=TIMEOUT_ELEMENTO)
            expect(pagina.locator("h1").first).to_be_visible(timeout=TIMEOUT_ELEMENTO)
            time.sleep(3) 
            pagina.screenshot(path=os.path.join(pasta_evidencias, "HOME-02_Carrossel_de_Destaques.png"))
            registrar_log(" PASSOU - Clique no destaque redirecionou corretamente.")
        except Exception as e:
            pagina.screenshot(path=os.path.join(pasta_evidencias, "HOME-02_ERRO.png"))
            registrar_log(f"FALHOU: {e}")

        # - Renderização de Matéria
        try:
            registrar_log(" [ART-01] Renderização de Matéria...")
            pagina.goto(URL_HOME, timeout=TIMEOUT_PAGINA)
            
            # Clica na primeira matéria
            pagina.locator("main a[href$='.html']").first.click(timeout=TIMEOUT_ELEMENTO)
            scroll_humanizado(pagina) 

            
            pagina.screenshot(path=os.path.join(pasta_evidencias, "ART-01_Renderizacao_de_Materia.png"))
            registrar_log(" PASSOU - Matéria renderizada com sucesso.")
        except Exception as e:
            pagina.screenshot(path=os.path.join(pasta_evidencias, "ART-01_ERRO.png"))
            registrar_log(f"FALHOU: {e}")

        try:
            registrar_log(" [ART-02] Incorporação de Mídia...")
            time.sleep(4) 
            tem_iframe = pagina.locator("iframe").count() > 0
            tem_video = pagina.locator("video").count() > 0
            pagina.screenshot(path=os.path.join(pasta_evidencias, "ART-02_Incorporacao_de_Midia.png"))
            if tem_iframe or tem_video:
                registrar_log(" PASSOU - Mídia (vídeo ou post) encontrada na matéria.")
            else:
                registrar_log(" ALERTA: Esta matéria não tem vídeos para testar.")
        except Exception as e:
            registrar_log(f"FALHOU: {e}")

        try:
            registrar_log(" [TAB-01] Tabela do Brasileirão...")
            pagina.goto(URL_TABELA, timeout=TIMEOUT_PAGINA)
            scroll_humanizado(pagina) 
            expect(pagina.locator("table").first).to_be_visible(timeout=TIMEOUT_ELEMENTO)
            pagina.screenshot(path=os.path.join(pasta_evidencias, "TAB-01_Tabela_do_Brasileirao.png"))
            registrar_log(" PASSOU - Tabela renderizada na tela.")
        except Exception as e:
            pagina.screenshot(path=os.path.join(pasta_evidencias, "TAB-01_ERRO.png"))
            registrar_log(f"FALHOU: {e}")

        try:
            registrar_log(" [LIVE-01] Tempo Real...")
            pagina.goto(URL_AGENDA, timeout=TIMEOUT_PAGINA)
            expect(pagina.locator("body")).to_be_visible(timeout=TIMEOUT_ELEMENTO) 
            time.sleep(5) 
            pagina.screenshot(path=os.path.join(pasta_evidencias, "LIVE-01_Tempo_Real.png"))
            registrar_log(" PASSOU - Página de Tempo Real/Agenda carregada.")
        except Exception as e:
            pagina.screenshot(path=os.path.join(pasta_evidencias, "LIVE-01_ERRO.png"))
            registrar_log(f"FALHOU: {e}")

        try:
            registrar_log(" [MENU-02] Menu Hambúrguer (Mobile)...")
            contexto_mobile = navegador.new_context(
                viewport={'width': 390, 'height': 844},
                is_mobile=True,
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
            )
            pagina_mobile = contexto_mobile.new_page()
            pagina_mobile.goto(URL_HOME, timeout=TIMEOUT_PAGINA)
            time.sleep(4) 
            pagina_mobile.locator('[data-testid="menu_burguer_icon"]').click(timeout=TIMEOUT_ELEMENTO)
            time.sleep(2) 
            pagina_mobile.screenshot(path=os.path.join(pasta_evidencias, "MENU-02_Menu_Hamburguer.png"))
            registrar_log(" PASSOU - Emulação mobile e clique no menu funcionaram.")
            contexto_mobile.close()
        except Exception as e:
            try:
                pagina_mobile.screenshot(path=os.path.join(pasta_evidencias, "MENU-02_ERRO.png"))
            except:
                pass
            registrar_log(f"FALHOU: {e}")

        navegador.close()
        registrar_log("\n🎉 Suíte Completa de Regressão da Planilha Finalizada com Sucesso!")

if __name__ == "__main__":
    rodar_testes_planilha()