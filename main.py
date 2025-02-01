import customtkinter as ctk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from datetime import date, timedelta
from holidays.countries import Brazil  # <-- Importação direta do submódulo

# -----------------------------------------
# 1) Gerar a lista de dias úteis dinamicamente
# -----------------------------------------
def obter_dias_uteis(ano, mes):
    # Cria objeto de feriados para o Brasil (estado de SP)
    br_holidays = Brazil(state='SP')

    # Se quiser adicionar manualmente feriados municipais de São Paulo
    # (exemplo: Aniversário da cidade em 25/01)
    br_holidays[date(ano, 1, 25)] = "Aniversário de SP (Feriado Municipal)"

    data_inicial = date(ano, mes, 1)
    if mes == 12:
        # Se for dezembro, termina dia 31
        data_final = date(ano, 12, 31)
    else:
        # Caso contrário, define o último dia do mês de forma simples:
        data_final = date(ano, mes + 1, 1) - timedelta(days=1)

    dias_uteis = []
    data_atual = data_inicial

    while data_atual <= data_final:
        # weekday() retorna 0 para segunda, 6 para domingo
        # Verifica também se não é feriado
        if data_atual.weekday() < 5 and data_atual not in br_holidays:
            dias_uteis.append(data_atual.strftime('%d/%m/%Y'))
        data_atual += timedelta(days=1)

    return dias_uteis

# -----------------------------------------
# Criação da lista de dias úteis com base na data atual
# -----------------------------------------
hoje = date.today()
dias_uteis = obter_dias_uteis(hoje.year, hoje.month)

def iniciar_processo():
    username = entry_usuario.get()
    password = entry_senha.get()

    # Verificar se o nome de usuário e senha foram inseridos
    if not username or not password:
        messagebox.showerror("Erro", "Por favor, insira o nome de usuário e senha.")
        return

    # Configurações do WebDriver
    driver_path = "./msedgedriver.exe"  # Ajuste se necessário
    login_url = 'https://discovery.leega.com.br/account/login?ReturnUrl=%2fApontamento.aspx'
    apontamento_url = 'https://discovery.leega.com.br/Apontamento.aspx'

    # Inicializar o WebDriver
    service = Service(driver_path)
    
    # Se estiver marcado para headless, passamos a opção ao Edge
    if headless_var.get():
        edge_options = Options()
        edge_options.add_argument("--headless")
        edge_options.add_argument("--disable-gpu")
        
        driver = webdriver.Edge(service=service, options=edge_options)
    else:
        driver = webdriver.Edge(service=service)

    try:
        # Acessar a página de login
        driver.get(login_url)
        time.sleep(2)

        # Preencher o campo de login
        driver.find_element(By.ID, 'Login').send_keys(username)
        # Preencher a senha
        driver.find_element(By.ID, 'Password').send_keys(password)

        # Clicar no botão de login
        driver.find_element(By.XPATH, '//input[@type="submit" and @value="Login"]').click()
        time.sleep(2)

        # Navegar até a página de apontamento
        driver.get(apontamento_url)
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, 'icon-edit').click()
        
        # Esperar até que o popup esteja visível
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'ctl00_MainContent_ControleApontamento_txtDataApontamento'))
        )
        
        # Preencher os apontamentos para cada dia útil
        for i, data in enumerate(dias_uteis):
            # Verificar se o dia está bloqueado
            if bloqueios[i].get():
                print(f"Dia {data} bloqueado. Pulando...")
                continue

            # Preencher a data
            data_field = driver.find_element(By.ID, 'ctl00_MainContent_ControleApontamento_txtDataApontamento')
            data_field.clear()
            data_field.send_keys(data)

            # Preencher o esforço (horas)
            esforco_field = driver.find_element(By.ID, 'ctl00_MainContent_ControleApontamento_CaixaEsforço')
            esforco_field.clear()
            esforco_field.send_keys(horas[i].get())

            # Preencher o %Atividade (porcentagem inteira)
            atividade_field = driver.find_element(By.ID, 'ctl00_MainContent_ControleApontamento_CaixaStatus')
            atividade_field.clear()
            atividade_field.send_keys(str(int(porcentagens[i].get())))  # Garantir que seja um número inteiro

            # Clicar no botão "Salvar"
            driver.find_element(By.ID, 'ctl00_MainContent_ControleApontamento_BotaoSalvar').click()
            
            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element_located((By.ID, "PainelAguarde"))
            )

            # Atualiza a label com o dia que foi salvo
            label_status.configure(text=f"Apontamento para {data} salvo com sucesso!")
            root.update_idletasks()

            print(f"Apontamento para {data} salvo com sucesso!")
            time.sleep(1)

        # Alerta de sucesso
        messagebox.showinfo("Sucesso", "Processo concluído com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        # Fechar o navegador
        driver.quit()

def editar_celula(event):
    item = tree.selection()[0]  # Item selecionado
    coluna = tree.identify_column(event.x)  # Coluna clicada

    # Verificar se a célula é editável (Horas, % do Mês ou Bloquear)
    if coluna == "#2" or coluna == "#3":
        valor_atual = tree.item(item, "values")[int(coluna[1]) - 1]
        entry_editar = ctk.CTkEntry(tree, width=100)
        entry_editar.insert(0, valor_atual)
        entry_editar.bind("<Return>", lambda e: salvar_edicao(item, coluna, entry_editar))
        entry_editar.bind("<FocusOut>", lambda e: salvar_edicao(item, coluna, entry_editar))

        tree.update()
        x, y, largura, altura = tree.bbox(item, coluna)
        entry_editar.grid(row=tree.index(item), column=int(coluna[1]) - 1, padx=x, pady=y)

    elif coluna == "#4":  # Coluna de Bloquear
        indice = tree.index(item)
        bloqueios[indice].set(not bloqueios[indice].get())
        tree.set(item, coluna, "Sim" if bloqueios[indice].get() else "Não")

def salvar_edicao(item, coluna, entry_editar):
    novo_valor = entry_editar.get()
    valores = list(tree.item(item, "values"))
    valores[int(coluna[1]) - 1] = novo_valor
    tree.item(item, values=valores)

    indice = tree.index(item)
    if coluna == "#2":  # Coluna de Horas
        horas[indice].set(novo_valor)
    elif coluna == "#3":  # Coluna de % do Mês
        novo_valor_sem_porcentagem = novo_valor.replace('%', '')
        porcentagens[indice].set(int(novo_valor_sem_porcentagem))

    entry_editar.destroy()

# --------------------------
# Criação da interface GUI
# --------------------------
root = ctk.CTk()
root.title("Automação de Apontamento")
root.geometry("800x600")

# Frame de Login
frame_login = ctk.CTkFrame(root)
frame_login.pack(pady=10)

ctk.CTkLabel(frame_login, text="Usuário:").grid(row=0, column=0, padx=10, pady=10)
entry_usuario = ctk.CTkEntry(frame_login)
entry_usuario.grid(row=0, column=1, padx=10, pady=10)

ctk.CTkLabel(frame_login, text="Senha:").grid(row=1, column=0, padx=10, pady=10)
entry_senha = ctk.CTkEntry(frame_login, show="*")
entry_senha.grid(row=1, column=1, padx=10, pady=10)

# Checkbox para modo headless
headless_var = ctk.BooleanVar(value=False)
headless_check = ctk.CTkCheckBox(frame_login, text="Executar em modo Headless", variable=headless_var)
headless_check.grid(row=2, column=0, columnspan=2, pady=10)

# Frame da Tabela
frame_tabela = ctk.CTkFrame(root)
frame_tabela.pack(pady=10)

ctk.CTkLabel(frame_tabela, text="Dias Úteis do Mês", font=("Arial", 12, "bold")).pack()

tree = ttk.Treeview(frame_tabela, columns=("Data", "Horas", "% do Mês", "Bloquear"), show="headings", height=10)
tree.heading("Data", text="Data")
tree.heading("Horas", text="Horas")
tree.heading("% do Mês", text="% do Mês")
tree.heading("Bloquear", text="Bloquear")
tree.pack(padx=10, pady=10)

tree.bind("<Double-1>", editar_celula)

# Variáveis para edição
horas = []
porcentagens = []
bloqueios = []

# Preencher a tabela dinamicamente a partir de dias_uteis
for i, data in enumerate(dias_uteis):
    porcentagem = round((i + 1) * (100 / len(dias_uteis)))
    if i == len(dias_uteis) - 1:
        porcentagem = 100

    horas_var = ctk.StringVar(value="08:00")
    porcentagem_var = ctk.IntVar(value=porcentagem)
    bloqueio_var = ctk.BooleanVar(value=False)

    horas.append(horas_var)
    porcentagens.append(porcentagem_var)
    bloqueios.append(bloqueio_var)

    tree.insert("", "end", values=(data, horas_var.get(), f"{porcentagem_var.get()}%", "Não"))

# Label para status das mensagens
label_status = ctk.CTkLabel(root, text="", text_color="green")
label_status.pack(pady=5)

start_button = ctk.CTkButton(root, text="Start", command=iniciar_processo)
start_button.pack(pady=10)

root.mainloop()
