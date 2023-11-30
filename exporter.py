import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk



ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

saldo_inicial, saldo_atual, gastos = 0, 0, []

def moedaformat(valor):
    """
        Formata o valor para o padrão brasileiro.

        Parâmetros:
        - valor (float or str): Valor a ser formatado.

        Retorno:
        - str: Valor formatado.

        Exemplo:
        >>> moedaformat(1250.50)
        1.250,50

        >>> moedaformat(1,000.50)
        1.000,50
    """
    return '{:_.2f}'.format(float(valor)).replace('.', ',').replace('_', '.')

def moedaraw(valor):
    """
        Converte o valor para o formato padrão de float do python

        Parâmetros:
        - valor (str): Valor a ser convertido.

        Retorno:
        - float: Valor convertido.

        Exemplo:
        >>> moedaraw('1.250,50')
        1250.5
        
        >>> moedaraw('1.000,50')
        1000.5
    """
    return float(valor.replace('.', '_').replace(',', '.'))

def export_values(saldo_ini, saldo_at, gast):
    """
        Salva os valores para exportação (transporte entre arquivos)

        Parâmetros:
        - saldo_ini (float): Saldo inicial
        - saldo_atua (float): Saldo atual
        - gasts (list): Lista de gastos 
    """
    global saldo_inicial, saldo_atual, gastos
    saldo_inicial, saldo_atual, gastos = saldo_ini, saldo_at, gast


def export_screen():
    """
        Cria a tela de exportação de arquivos

        Retorno:
        - Tela (CTk): Tela de exportação de arquivos.

        Exemplo:
        >>> export_screen()
        - Exibe a tela de exportação de arquivos
        - Fecha a tela de exportação de arquivos
        - Retorna para a tela principal
    """
    global exp_app
    exp_app = ctk.CTk()
    exp_app.geometry("480x260")
    exp_app.title("Exportar")

    export_frame = ctk.CTkFrame(exp_app)
    export_frame.pack(pady=55, anchor='center')

    archivename_label = ctk.CTkLabel(export_frame, text="Nome para o arquivo (opcional)") # Label do nome do arquivo
    archivename_label.pack(pady=5)

    global archivename_entry
    archivename_entry = ctk.CTkEntry(export_frame)
    archivename_entry.pack(pady=5)

    text_label = ctk.CTkLabel(export_frame, text="Escolha uma opção para exportação")
    text_label.pack(pady=5)

    excel_button = ctk.CTkButton(export_frame, text="Excel", command=lambda: export_excel(saldo_inicial, saldo_atual, gastos)) # Exportar para Excel
    excel_button.pack(pady=5, padx=5, side='left')

    nsei_button = ctk.CTkButton(export_frame, text="None", command=lambda: export_none(saldo_inicial, saldo_atual, gastos)) # Nada
    nsei_button.pack(pady=5, padx=5, side='right')

    pdf_button = ctk.CTkButton(export_frame, text="PDF", command=lambda: export_pdf(saldo_inicial, saldo_atual, gastos)) # Exportar para PDF
    pdf_button.pack(pady=5, padx=5, side='right')

    empty_label2 = ctk.CTkLabel(export_frame, text="")
    empty_label2.pack(pady=5)


    exp_app.mainloop()


# PDF
def export_pdf(saldo_inicial, saldo_atual, gastos):
    """
        Cria um arquivo em PDF com os dados de saldos e gastos

        Parâmetros:
        - saldo_inicial (float): Saldo inicial
        - saldo_atual (float): Saldo atual
        - gastos (list): Lista de gastos 
        - nome_arquivo (str): Nome do arquivo tirado da entry
        - caminho_diretorio (str): Caminho do diretório selecionado pelo usuário para salvar o arquivo

        Retorno:
        - Arquivo PDF com todas as informações de exportação

        Exemplo:
        >>> export_pdf(1000.0, 850.0, [('Gasto 1', 100.0), ('Gasto 2', 50.0)])
        Exporta os dados para um PDF formatado.
    """
    nome_arquivo = archivename_entry.get()
    
    if nome_arquivo == '':
        nome_arquivo = 'Controle de Gastos'

    exp_app.withdraw()

    caminho_diretorio = filedialog.askdirectory(title='Escolha uma pasta')

    exp_app.deiconify()

    # Garante que não ocorra erros caso o usuário cancele a seleção
    try:
        caminho_pdf = os.path.join(caminho_diretorio, f'{nome_arquivo}.pdf')
    except TypeError:
        return None

    pdf = SimpleDocTemplate(caminho_pdf, pagesize=letter, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)

    elements = []
    styles = getSampleStyleSheet()

    caixa_style = TableStyle(
        [
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('LINEABOVE', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black),
            ('LINELEFT', (0, 0), (-1, -1), 1, colors.black),
            ('LINERIGHT', (0, 0), (-1, -1), 1, colors.black),
        ]
    )

    valor_inicial = moedaformat(saldo_inicial)
    valor_final = moedaformat(saldo_atual)
    diferenca = moedaformat(saldo_inicial - saldo_atual)

    caixa_data = [
        [Paragraph(f'Saldo inicial - R$ {valor_inicial}', styles['Normal']),
        Paragraph(f'Total de Gastos - R$ -{diferenca}', styles['Normal']),
        Paragraph(f'Saldo Final - R$ {valor_final}', styles['Normal'])]
    ]

    caixa_table = Table(caixa_data, colWidths=[pdf.width / 3] * 3)
    caixa_table.setStyle(caixa_style)
    elements.append(caixa_table)

    elements.append(Spacer(1, 12))

    data = [['Gasto', 'Valor do gasto']]
    data.extend([[gasto, f'R$ {valor}'] for gasto, valor in gastos])

    table_style = TableStyle(
        [
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]
    )

    table = Table(data, colWidths=[pdf.width / len(data[0])] * len(data[0]))
    table.setStyle(table_style)
    elements.append(table)

    pdf.build(elements)

# Excel
def export_excel(saldo_inicial, saldo_atual, gastos):
    """
        Cria um arquivo em Excel com os dados de saldos e gastos

        Parâmetros:
        - saldo_inicial (float): Saldo inicial
        - saldo_atual (float): Saldo atual
        - gastos (list): Lista de gastos 
        - nome_arquivo (str): Nome do arquivo tirado da entry
        - caminho_diretorio (str): Caminho do diretório selecionado pelo usuário para salvar o arquivo

        Retorno:
        - Arquivo Excel com todas as informações de exportação

        Exemplo:
        >>> export_excel(1000.0, 850.0, [('Gasto 1', 100.0), ('Gasto 2', 50.0)])
        Exporta os dados para um Excel.
    """

    nome_arquivo = archivename_entry.get()

    if nome_arquivo == '':
        nome_arquivo = 'Controle de Gastos'

    exp_app.withdraw()

    caminho_diretorio = filedialog.askdirectory(title='Escolha uma pasta')

    exp_app.deiconify()

    # Garante que não ocorra erros caso o usuário cancele a seleção
    try:
        caminho_excel = os.path.join(caminho_diretorio, f'{nome_arquivo}.xlsx')
    except TypeError:
        return None

    df = pd.DataFrame(columns=['Saldo', 'Gasto', 'Valor do Gasto', f'Saldo final: R$ {moedaformat(saldo_atual)}'])

    dados = []

    # Adicionar colunas
    df['Saldo'] = ['']
    df['Gasto'] = ['']
    df['Valor do Gasto'] = ['']
    df[f'Saldo final: R$ {moedaformat(saldo_atual)}'] = ['']

    saldo = saldo_inicial
    # Adicionar mais linhas
    for nome, valor in gastos:
        nova_linha = {'Saldo': f'R$ {moedaformat(saldo)}', 
                    'Gasto': nome, 
                    'Valor do Gasto': f'R$ {moedaformat(moedaraw(valor))}', 
                    f'Saldo final: R$ {moedaformat(saldo_atual)}': f'R$ {moedaformat(saldo - moedaraw(valor))}'}
        dados.append(nova_linha)
        saldo = saldo - moedaraw(valor)

        
    df_novo = pd.DataFrame(dados)

    # Concatenar o DataFrame novo com o DataFrame existente
    df = pd.concat([df, df_novo], ignore_index=True)

    # Salvar o DataFrame em um arquivo xlsx
    df.to_excel(caminho_excel, index=False, engine='openpyxl')

def export_none(saldo_inicial, saldo_atual, gastos):
    """
        Não faz nada até o momento (WIP)
    """
    print("None")


def import_values():
    """
        Importa os dados de um arquivo Excel exportado anteriormente e retorna os valores de saldo e gastos

        Parâmetros:
        - None

        Retorno:
        - primeiro_saldo (float): Saldo inicial
        - lista_gastos (list): Lista de gastos

        Exemplo:
        >>> import_values():
        Abre uma janela para selecionar um arquivo xlsx compatível
        Lê o arquivo, formata seus valores novamente e devolve ao arquivo main para ser editado
    """

    # Garante que não ocorra erros caso o usuário cancele a seleção
    try:
        caminho_arquivo = filedialog.askopenfilename(
            title='Escolha um arquivo',
            filetypes=[('Arquivos Excel', '*.xlsx')]
        )
    except TypeError:
        return None

    try:
        imported_df = pd.read_excel(caminho_arquivo, engine='openpyxl')
        primeiro_saldo = imported_df.loc[1, 'Saldo']

        dados_gastos = imported_df.loc[1:, ['Gasto', 'Valor do Gasto']]

        lista_gastos = [(row['Gasto'], moedaraw(row['Valor do Gasto'][3:])) for index, row in dados_gastos.iterrows()]

        return primeiro_saldo, lista_gastos

    except Exception as e:
        print(f"Erro ao importar o arquivo Excel: {e}")
        return None