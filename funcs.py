from exporter import export_screen, export_values, import_values


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
    return '{:_.2f}'.format(valor).replace('.', ',').replace('_', '.')

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

def export(saldo_inic, saldo_atua, gasts):
    """
        Transfere o usuário para um tela de exportação de arquivos

        Parâmetros:
        saldo_inic (float): Saldo inicial
        saldo_atua (float): Saldo atual
        gasts (list): Lista de gastos
        
        Exemplo:
        >>> export(3000.50, 1500.50, [('Aluguel', 1500)])
        >>> export_screen()
        - Exibe a tela de exportação de arquivos
        - Exporta os valores para o arquivo de exportação
        - Fecha a tela de exportação de arquivos
        - Retorna para a tela principal
    """
    export_values(saldo_inic, saldo_atua, gasts)
    export_screen()

def importer():
    """
        Encaminha para outra função para importar valores de um arquivo exportado anteriormente

        Retorno:
        - saldo_inicial (float): Saldo inicial
        - gastos (list): Lista de gastos
    """
    saldo_inicial, gastos = import_values()
    return saldo_inicial, gastos