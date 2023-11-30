import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from funcs import moedaformat, moedaraw, export, importer
from PIL import Image, ImageTk


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

gastos = []
saldo_inicial = 0
saldo_atual = saldo_inicial
_saldo_inicial_error = None
_value_error = None


def _value_test(value):
    """
        Verifica se o valor inserido é válido.
        
        Parâmetros:
        - value (str or float): Valor a ser checado.

        Retorna:
        - None para um valor compatível com float
        - 'string' se o valor não for válido.

        Exemplos:
        >>> _value_test('123.45')
        None

        >>> _value_test('abc')
        'string'
    """

    try: 
        moedaraw(value)
        return None
    except:
        return 'string'

def verify_value(valor):
    """
        Verifica se há caractéres inválidos no valor inserido e os remove.

        Parâmetros:
        - valor (str): Valor a ser verificado.

        Retorna:
        - valor (str): Valor sem caractéres inválidos.

        Exemplos:
        >>> verify_value('R$ 123,45')
        '123,45'

        >>> verify_value('123.45$')
        '123.45'

        >>> verify_value('USD$ 123.45')
        '123.45'
    """

    BAN_CHARS = '$BRLUSDusdbrl '
    if any(char in valor for char in BAN_CHARS):
        for char in BAN_CHARS:
            valor = valor.replace(char, '')
        return valor
    else:
        return valor

def adicionar_gasto():
    """
        Adiciona um novo item na lista de gastos

        Parâmetros:
        - Recebe diretamente do campo de Entry

        Retorna:
        - Insere um novo valor na Treeview
        - Adiciona um novo item na lista de gastos
        - Atualiza o saldo atual
        - Verifica se há erros de entrada de dados e os trata
    """

    global _value_error
    nome = nome_entry.get()
    valor = valor_entry.get()

    if nome == '':
        nome = 'Não definido'

    valor = verify_value(valor)

    try:
        _test = _value_test(valor)
        if _test is None:
            if _value_error is not None:
                _value_error.destroy()
            pass
        else:
            int(_test)
    except:
        if _value_error is not None:
            _value_error.destroy()
        _value_error = ctk.CTkLabel(frame, text='Insira um valor válido!', text_color='#d45b50')
        _value_error.grid(row=1, column=3, padx=5, pady=5)
        return

    gastos.append((nome, valor))

    # Adiciona espaçamento nos itens com base em seu tamanho em caractéres
    _spacing_v = 70 - len(f'{valor}')
    if len(f'{nome}') <= 3:
        _spacing_n = 66 - len(f'{nome}')
    elif nome == 'Não definido':
        _spacing_n = 58
    else:
        _spacing_n = 69 - len(f'{nome}')
    valor_rs = 'R$ ' + valor
    tabela.insert("", tk.END, values=(f"{nome:^{_spacing_n}}", f"{valor_rs:^{_spacing_v}}")) # Insere os itens na tabela
    # Reseta as entry para receberem novos valores
    nome_entry.delete(0, tk.END)
    valor_entry.delete(0, tk.END)
    
    atualizar_saldo()

def remover_gasto():
    """
        Remove um item da lista de gastos

        Parâmetros:
        - Seleção do campo atráves do Treeview

        Retorna:
        - Remoção dos itens selecionados
        - Atualiza o saldo atual
    """
    item_selecionado = tabela.selection()
    if item_selecionado:
        for item in item_selecionado:
            indice = tabela.index(item)
            nome, valor = gastos[indice]
            tabela.delete(item)
            del gastos[indice]
            atualizar_saldo()

def atualizar_saldo():
    """
        Atualiza a variável do saldo atual

        Parâmetros:
        - Lista de valores dos gastos

        Retorna:
        - Valor atualizado do saldo baseado em todos os itens
    """
    global saldo_atual
    saldo_v = 0
    for nome, gasto in gastos:
        try:
            val = moedaraw(gasto)
        except AttributeError:
            val = gasto
        saldo_v += float(val)
    saldo_atual = saldo_inicial - saldo_v
    saldo_label.configure(text=f"Saldo Atual: R$ {moedaformat(saldo_atual)}")

def update_variables(saldo, _gastos):
    """
        Atualiza as variáveis de saldo_inicial e gastos após importar um arquivo

        Parâmetros:
        - saldo (float): Valor inicial do saldo
        - _gastos (list): Lista de tuplas com os nomes e valores dos gastos

        Retorna:
        - Atualiza as variáveis de saldo_inicial e gastos com os valores importados
        - Atualiza a tabela com os novos valores de gastos
        - Atualiza o saldo atual com os novos valores de saldo_inicial e gastos
        - Exibe a tabela de gastos
        - Exibe o saldo atualizado

        Exemplos:
        >>> update_variables(100.0, [('Gasto 1', 50.0), ('Gasto 2', 25.0)])
        >>> print(saldo_inicial)
        100.0
        >>> print(gastos)
        [('Gasto 1', 25.0), ('Gasto 2', 25.0)]
        >>> print(saldo_atual)
        50.0
    """
    global saldo_inicial
    global gastos
    saldo_inicial = moedaraw(verify_value(saldo))
    gastos = _gastos
    tabela.delete(*tabela.get_children())

    for nome, valor in gastos:
        _spacing_v = 70 - len(f'{valor}')
        if len(f'{nome}') <= 3:
            _spacing_n = 66 - len(f'{nome}')
        elif nome == 'Não definido':
            _spacing_n = 58
        else:
            _spacing_n = 69 - len(f'{nome}')
        valor_rs = 'R$ ' + f'{valor}'
        tabela.insert("", tk.END, values=(f"{nome:^{_spacing_n}}", f"{valor_rs:^{_spacing_v}}"))
    atualizar_saldo()


def iniciar_programa():
    """
        Pega um valor inicial para o saldo e inicia o programa.

        Parâmetros:
        - Recebe diretamente do campo de Entry

        Retorna:
        - Inicia o programa com o valor inicial
        - Atualiza o saldo atual
        - Exibe a tabela de gastos
    """
    global saldo_inicial
    global _saldo_inicial_error
    try:
        saldo_get_entry = saldo_inicial_entry.get()
        saldo_get_entry = verify_value(saldo_get_entry)
        saldo_inicial = float(moedaraw(saldo_get_entry))
    except:
        if _saldo_inicial_error is not None:
            _saldo_inicial_error.destroy()
        _saldo_inicial_error = ctk.CTkLabel(saldo_frame, text='Insira um valor válido', text_color='#d45b50')
        _saldo_inicial_error.pack()
        return
    saldo_atual = saldo_inicial
    saldo_label.configure(text=f"Saldo Atual: R$ {moedaformat(saldo_atual)}")
    saldo_frame.pack_forget()
    tabela.pack(pady=10)
    button_frame.pack()


app = ctk.CTk()
app.geometry("600x520")
app.title("Controle de Gastos")

icon = ImageTk.PhotoImage(Image.open('assets/app_icon.ico'))
app.wm_iconphoto(True, icon)

saldo_frame = ctk.CTkFrame(app)
saldo_frame.pack(pady=200, fill='both')

saldo_label = ctk.CTkLabel(saldo_frame, text="Informe o Saldo Inicial:")
saldo_label.pack()

saldo_inicial_entry = ctk.CTkEntry(saldo_frame) # Entry de saldo inicial
saldo_inicial_entry.pack(pady=5)

iniciar_button = ctk.CTkButton(saldo_frame, text="Iniciar", command=iniciar_programa) # Botão que inicia a aplicação após receber o valor
iniciar_button.pack(pady=5)


style = ttk.Style()
    
style.theme_use("default")
    
style.configure("Treeview",
    background="#2a2d2e",
    foreground="white",
    rowheight=25,
    fieldbackground="#343638",
    bordercolor="#343638",
    borderwidth=0)
style.map('Treeview', background=[('selected', '#2fa572')])

style.configure("Treeview.Heading",
    background="#3c4042",
    foreground="white",
    relief="flat")
style.map("Treeview.Heading",
    background=[('active', '#2fa572')])

tabela = ttk.Treeview(app, columns=("Nome", "Valor"))
tabela.heading("Nome", text="Nome do Gasto")
tabela.heading("Valor", text="Valor do Gasto")
tabela.column("#0", width=0, stretch=tk.NO)

frame = ctk.CTkFrame(app)
frame.pack(pady=10)

nome_label = ctk.CTkLabel(frame, text="Nome do Gasto:")
nome_label.grid(row=0, column=0, padx=5, pady=5)
nome_entry = ctk.CTkEntry(frame, placeholder_text='Nome') # Entry de nome do gasto
nome_entry.grid(row=0, column=1, padx=5, pady=5)

valor_label = ctk.CTkLabel(frame, text="Valor do Gasto:")
valor_label.grid(row=1, column=0, padx=5, pady=5)
valor_entry = ctk.CTkEntry(frame, placeholder_text='Valor numérico') # Entry de valor do gasto
valor_entry.grid(row=1, column=1, padx=5, pady=5)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

adicionar_button = ctk.CTkButton(button_frame, text="Adicionar Gasto", command=adicionar_gasto) # Botão para adicionar gasto à tabela
adicionar_button.pack(side=tk.LEFT, padx=5)

remover_button = ctk.CTkButton(button_frame, text="Remover Gasto", command=remover_gasto) # Botão para remover gasto selecionado na tabela
remover_button.pack(side=tk.LEFT, padx=5)

saldo_label = ctk.CTkLabel(button_frame, text=f"Saldo Atual: R$ {moedaformat(saldo_atual)}") # Campo que mostra o saldo atual
saldo_label.pack(side=tk.RIGHT, padx=5)

tabela.pack(pady=5, padx=5, fill=tk.BOTH)

export_frame = ctk.CTkFrame(app)
export_frame.pack(pady=10)

# Botão para exportar os gastos para um arquivo
export_button = ctk.CTkButton(export_frame, text="Exportar", command=lambda: export(saldo_inicial, saldo_atual, gastos))
export_button.pack(side=tk.RIGHT, pady=5, padx=5)

# Botão para importar os gastos de um arquivo feito previamente
import_button = ctk.CTkButton(export_frame, text="Importar", command=lambda: update_variables(*importer()))
import_button.pack(side=tk.LEFT, pady=5, padx=5)

app.mainloop()