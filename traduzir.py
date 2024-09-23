import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from googletrans import Translator
import threading
import os

def traduzir_texto_e_salvar(texto, prefixo_arquivo, idioma_destino, progress_bar):
    """
    Função para traduzir e salvar um texto em partes separadas, com contagem de palavras traduzidas em tempo real.

    Args:
        texto (str): O texto a ser traduzido.
        prefixo_arquivo (str): O prefixo a ser usado nos nomes dos arquivos de saída.
        idioma_destino (str): O código do idioma de destino para a tradução.
        progress_bar (ttk.Progressbar): A barra de progresso a ser atualizada.
    """
    # Inicializa o tradutor
    translator = Translator()

    # Divide o texto em linhas
    linhas_texto = texto.split('\n')

    # Lista para armazenar as traduções de todas as partes
    traducoes = []

    # Inicializa variáveis para contagem de palavras
    total_lines = len(linhas_texto)
    translated_words = 0

    # Inicializa variável para armazenar a parte atual do texto
    parte_atual = ''

    # Atualiza o valor máximo da barra de progresso
    progress_bar["maximum"] = total_lines

    # Traduz e salva cada parte em um arquivo separado
    arquivos_numerados = []  # Lista para armazenar os nomes dos arquivos numerados

    for i, linha in enumerate(linhas_texto):
        # Adiciona a linha atual à parte atual
        parte_atual += linha + '\n'

        # Se a parte atual exceder 4000 caracteres ou for a última linha, traduz e salva
        if len(parte_atual) > 4000 or i == len(linhas_texto) - 1:
            # Traduz apenas a parte após os ":" usando uma list comprehension
            traducoes_parte = []
            for linha_parte in parte_atual.split('\n'):
                if ':' in linha_parte:
                    texto_original, texto_traduzido = linha_parte.split(':', 1)
                    texto_traduzido = texto_traduzido.replace('_', ' ')  # Substitui "_" por espaço

                    try:
                        traducao = translator.translate(texto_traduzido.strip(), src='en', dest=idioma_destino).text
                        translated_words += len(traducao.split())  # Conta as palavras traduzidas
                    except Exception as e:
                        print(f"Erro na tradução da linha: {linha_parte.strip()}. Mensagem de erro: {e}")
                        traducao = texto_traduzido.strip()  # Usa o texto original em caso de erro na tradução
                    traducao = traducao.strip()  # Remove espaços em branco extras
                    traducoes_parte.append(f"{texto_original.strip()}: {traducao}")
                else:
                    traducoes_parte.append(linha_parte)  # Mantém a linha original se não tiver ":"

            parte_traduzida = '\n'.join(traducoes_parte)
            traducoes.append(parte_traduzida)

            # Define o nome do arquivo para esta parte
            nome_arquivo = f"{prefixo_arquivo}_{len(traducoes)}.txt"
            arquivos_numerados.append(nome_arquivo)

            # Abre o arquivo de saída e escreve a tradução
            with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
                arquivo.write(parte_traduzida)

            # Calcula a porcentagem de palavras traduzidas
            porcentagem = (translated_words / len(texto.split())) * 100 if len(texto.split()) > 0 else 0

            # Imprime a contagem de palavras e a porcentagem em tempo real
            print(f"Tradução da parte {len(traducoes)} salva em {nome_arquivo}. Palavras traduzidas: {translated_words}/{len(texto.split())} ({porcentagem:.2f}%)")

            # Atualiza a barra de progresso
            progress_bar["value"] = i + 1
            progress_bar.update_idletasks()

            # Limpa a parte atual para a próxima iteração
            parte_atual = ''

    # Junte todas as traduções em um único texto
    texto_junto = '\n'.join(traducoes)

    # Salve o texto conjunto em um arquivo
    nome_arquivo_junto = f"{prefixo_arquivo}_junto.txt"
    with open(nome_arquivo_junto, 'w', encoding='utf-8') as arquivo_junto:
        arquivo_junto.write(texto_junto)

    # Imprime mensagem final
    print(f"Traduções juntadas em {nome_arquivo_junto}.")

    # Exclui os arquivos numerados
    for nome_arquivo in arquivos_numerados:
        os.remove(nome_arquivo)
        print(f"Arquivo {nome_arquivo} excluído.")

    # Atualiza a barra de progresso para indicar conclusão
    progress_bar["value"] = progress_bar["maximum"]
    progress_bar.update_idletasks()

def carregar_e_traduzir():
    """
    Função para carregar o conteúdo de um arquivo de texto e iniciar o processo de tradução.
    """
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    
    if caminho_arquivo:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            texto = arquivo.read()
            prefixo_arquivo = prefixo_input.get()
            idioma_destino = idioma_opcoes[idioma_combobox.get()]

            if not prefixo_arquivo.strip():
                messagebox.showwarning("Aviso", "Por favor, insira o prefixo para os arquivos.")
                return

            if idioma_destino is None:
                messagebox.showwarning("Aviso", "Por favor, selecione um idioma de destino.")
                return
            
            # Configura a barra de progresso
            progress_bar["value"] = 0
            root.update_idletasks()

            # Executa a tradução em um thread separado
            threading.Thread(target=traduzir_texto_e_salvar, args=(texto, prefixo_arquivo, idioma_destino, progress_bar)).start()

            messagebox.showinfo("Sucesso", "Tradução iniciada. Acompanhe o progresso na barra de carregamento.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Tradutor do programador")

# Label e campo de texto para o prefixo do arquivo
prefixo_label = tk.Label(root, text="Prefixo da tradução:")
prefixo_label.pack(padx=10, pady=5)

prefixo_input = tk.Entry(root, width=80)
prefixo_input.pack(padx=10, pady=5)

# Label e menu suspenso para selecionar o idioma de destino
idioma_label = tk.Label(root, text="Idioma de destino:")
idioma_label.pack(padx=10, pady=5)

# Menu suspenso para selecionar o idioma
idioma_opcoes = {
    "Escolha um idioma": None,
    "Chinês Mandarim": "zh-CN",
    "Espanhol": "es",
    "Inglês": "en",
    "Hindi": "hi",
    "Árabe": "ar",
    "Bengali": "bn",
    "Português": "pt",
    "Russo": "ru",
    "Japonês": "ja",
    "Lao": "lo",
    "Vietnamita": "vi",
    "Alemão": "de",
    "Coreano": "ko",
    "Francês": "fr",
    "Turco": "tr",
    "Tamil": "ta",
    "Urdu": "ur",
    "Punjabi": "pa",
    "Javanês": "jv",
    "Malaio": "ms",
    "Polonês": "pl",
    "Italiano": "it",
    "Ucraniano": "uk",
    "Tailandês": "th",
    "Sueco": "sv",
    "Holandês": "nl"
}

idioma_combobox = ttk.Combobox(root, values=list(idioma_opcoes.keys()))
idioma_combobox.set("Escolha um idioma")
idioma_combobox.pack(padx=10, pady=5)

# Barra de progresso
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(padx=10, pady=20)

# Botão para carregar e traduzir arquivo
carregar_button = tk.Button(root, text="Escolha arquivo para traduzir", command=carregar_e_traduzir)
carregar_button.pack(padx=10, pady=20)

# Inicia o loop da interface gráfica
root.mainloop()
