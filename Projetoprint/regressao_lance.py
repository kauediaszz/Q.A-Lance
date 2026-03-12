from playwright.sync_api import sync_playwright
import os
from datetime import datetime
import time

# --- FUNÇÃO ÚTIL PARA SCROLL HUMANIZADO ---
def fazer_scroll_suave(pagina, tempo_segundos):
    print(f"   ⬇️ Fazendo scroll suave de {tempo_segundos}s para carregar imagens...")
    tempo_ms = tempo_segundos * 1000 
    passos = 20  
    
    # Executa o JavaScript na página para descer aos poucos
    pagina.evaluate("""([tempoTotal, qtdPassos]) => {
        return new Promise((resolve) => {
            const intervalo = tempoTotal / qtdPassos;
            const distancia = document.body.scrollHeight / qtdPassos;
            let passoAtual = 0;
            
            const timer = setInterval(() => {
                window.scrollBy(0, distancia);
                passoAtual++;
                
                if (passoAtual >= qtdPassos) {
                    clearInterval(timer);
                    resolve();
                }
            }, intervalo);
        });
    }""", [tempo_ms, passos])


def realizar_regressao_visual():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pasta_output = f"regressao_lance_{timestamp}"
    os.makedirs(pasta_output, exist_ok=True)
    
    print(f"📁 Pasta criada: {pasta_output}")

    # Lista completa de URLs para a regressão do Lance!
    urls_mapeadas = {
        "1Home_Principal": "https://www.lance.com.br/",
        "2Tabelas_Brasileirao": "https://www.lance.com.br/tabela/brasileirao",
        "3Tabelas_Champions_League": "https://www.lance.com.br/tabela/champions-league",
        "4Tempo_Real_Agenda": "https://www.lance.com.br/temporeal/agenda",
        "5Time_Flamengo": "https://www.lance.com.br/flamengo",
        "6Time_Palmeiras": "https://www.lance.com.br/palmeiras",
        "7Time_Atletico_MG": "https://www.lance.com.br/atletico-mineiro",
        "8Time_Corinthians": "https://www.lance.com.br/corinthians",
        "9Time_Fortaleza": "https://www.lance.com.br/fortaleza",
        "10Time_Santos": "https://www.lance.com.br/santos",
        "11Time_Bahia": "https://www.lance.com.br/bahia",
        "12Time_Cruzeiro": "https://www.lance.com.br/cruzeiro",
        "13Time_Gremio": "https://www.lance.com.br/gremio",
        "14Time_Sao_Paulo": "https://www.lance.com.br/sao-paulo",
        "15Time_Botafogo": "https://www.lance.com.br/botafogo",
        "16Time_Internacional": "https://www.lance.com.br/internacional",
        "17Time_Vasco": "https://www.lance.com.br/vasco",
        "18Time_Ceara": "https://www.lance.com.br/ceara",
        "19Time_Fluminense": "https://www.lance.com.br/fluminense",
        "20Time_Vitoria": "https://www.lance.com.br/vitoria",
        "21Ultimas_Noticias": "https://www.lance.com.br/mais-noticias",
        "22futebol_internacional": "https://www.lance.com.br/futebol-internacional",
        "23futebol_feminino": "https://www.lance.com.br/futebol-feminino",
        "24mercado_da_bola": "https://www.lance.com.br/mercado-da-bola",
        "25galerias": "https://www.lance.com.br/galerias",
        "26nba": "https://www.lance.com.br/nba",
        "27tenismo": "https://www.lance.com.br/tenis",
        "28volei": "https://www.lance.com.br/volei",
        "29formula 1": "https://www.lance.com.br/formula-1",
        "30lutas": "https://www.lance.com.br/lutas",
        "31onde_assistir": "https://www.lance.com.br/onde-assistir"
    }

    with sync_playwright() as p:
        print("🚀 Abrindo o seu Google Chrome...")
        navegador = p.chromium.launch(channel="chrome", headless=False) 
        contexto = navegador.new_context(viewport={'width': 1920, 'height': 1080})
        pagina = contexto.new_page()

        for nome_pagina, url in urls_mapeadas.items():
            print(f"🌐 Acessando: {nome_pagina}")
            
            try:
                
                pagina.goto(url, timeout=100000)
                
                
                fazer_scroll_suave(pagina, tempo_segundos=5)
                
               
                time.sleep(1) 
                
                
                pagina.evaluate("window.scrollTo(0, 0)")
                
                
                if nome_pagina == "Tempo_Real_Agenda":
                    print("   ⏳ Aguardando 15s extras (Tempo_Real_Agenda)...")
                    time.sleep(15) 
                else:
                    time.sleep(5) 
                
               
                caminho_arquivo = os.path.join(pasta_output, f"{nome_pagina}.png")
                pagina.screenshot(path=caminho_arquivo, full_page=True)
                print(f"  Print salvo: {caminho_arquivo}")
                
            except Exception as e:
                print(f"  Erro na página {nome_pagina}: {e}")

        navegador.close()
        print("\n🎉 Automação finalizada! Verifique a pasta criada com os prints.")

if __name__ == "__main__":
    realizar_regressao_visual()