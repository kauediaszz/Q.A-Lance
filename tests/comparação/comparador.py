import os
from datetime import datetime
from selenium import webdriver
from PIL import Image

def juntar_imagens_lado_a_lado(img_a_path, img_b_path, output_path):
    img_a = Image.open(img_a_path).convert('RGB')
    img_b = Image.open(img_b_path).convert('RGB')

    largura_a, altura_a = img_a.size
    largura_b, altura_b = img_b.size

    nova_largura = largura_a + largura_b
    nova_altura = max(altura_a, altura_b)
    nova_imagem = Image.new('RGB', (nova_largura, nova_altura))

    nova_imagem.paste(img_a, (0, 0))
    nova_imagem.paste(img_b, (largura_a, 0))

    nova_imagem.save(output_path)

def iniciar_qa_comparador():
    print("===================================================")
    print(" 🕵️‍♂️  COMPARADOR DE Q.A. (VISUAL LADO A LADO)  🕵️‍♂️")
    print("===================================================\n")

    link1 = input("🔗 Digite a URL do Link 1 (ex: hml): ").strip()
    link2 = input("🔗 Digite a URL do Link 2 (ex: prod): ").strip()

    print("\n🚀 Abrindo o navegador...")
    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get(link1)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(link2)

    print("\n⏸️  NAVEGADOR ABERTO!")
    input("➡️  Ajuste as telas e PRESSIONE ENTER no terminal para capturar tudo... ")

    print("\n📸 Coletando evidências...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pasta_teste = f"evidencias_lado_a_lado/teste_{timestamp}"
    os.makedirs(pasta_teste, exist_ok=True)

    tmp_a = "temp_a.png"
    tmp_b = "temp_b.png"
    imagem_final_path = f"{pasta_teste}/comparacao_visual.png"

    driver.switch_to.window(driver.window_handles[0])
    driver.save_screenshot(tmp_a)

    driver.switch_to.window(driver.window_handles[1])
    driver.save_screenshot(tmp_b)

    juntar_imagens_lado_a_lado(tmp_a, tmp_b, imagem_final_path)
    os.remove(tmp_a)
    os.remove(tmp_b)

    driver.quit()

    print(f"\n✅ SUCESSO! Evidência gerada na pasta:")
    print(f"📂 {pasta_teste}")
    print(f"   -> comparacao_visual.png")

if __name__ == "__main__":
    iniciar_qa_comparador()