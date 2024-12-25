import dbf
import calendar
from tkinter import Tk, Label, Button, Frame, messagebox
from tkinter.ttk import Combobox
from datetime import datetime

# Configuração do arquivo DBF
dbf_file = "Base_de_dados_de_sorteio/sorteios.dbf"

# Função para carregar os sorteios do arquivo DBF
def carregar_sorteios():
    try:
        table = dbf.Table(dbf_file)
        table.open(mode=dbf.READ_ONLY)
        sorteios = []
        for record in table:
            sorteios.append({
                "produto": record.produto.strip(),
                "mod": record.mod,
                "dias": record.dias.strip(),
                "mes": record.mes.strip(),
                "freq": record.freq.strip()
            })
        table.close()
        return sorteios
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar sorteios: {e}")
        return []

# Função para verificar sorteios em um dia específico
def verificar_sorteios(sorteios, dia, mes, ano):
    dia_semana = calendar.day_name[datetime(ano, mes, dia).weekday()][:3]
    mes_abrev = calendar.month_abbr[mes][:3]
    produtos = []
    for sorteio in sorteios:
        if sorteio["mes"] == mes_abrev and dia_semana in sorteio["dias"]:
            if sorteio["freq"] == "Todas as semanas":
                produtos.append(sorteio["produto"])
            elif sorteio["freq"] == "Primeira semana" and dia <= 7:
                produtos.append(sorteio["produto"])
            elif sorteio["freq"] == "Última semana" and dia > calendar.monthrange(ano, mes)[1] - 7:
                produtos.append(sorteio["produto"])
    return produtos

# Função para desenhar o calendário
def desenhar_calendario(ano, mes):
    for widget in calendario_frame.winfo_children():
        widget.destroy()

    # Cabeçalho do calendário
    Label(calendario_frame, text=f"{calendar.month_name[mes]} {ano}", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=7)

    # Dias da semana
    for i, dia in enumerate(calendar.day_abbr):
        Label(calendario_frame, text=dia, font=("Helvetica", 10, "bold")).grid(row=1, column=i)

    # Dias do mês
    dia_inicio, dias_no_mes = calendar.monthrange(ano, mes)
    sorteios = carregar_sorteios()
    linha = 2
    coluna = dia_inicio
    for dia in range(1, dias_no_mes + 1):
        produtos = verificar_sorteios(sorteios, dia, mes, ano)
        texto = f"{dia}\n" + ("\n".join(produtos) if produtos else "")
        Label(calendario_frame, text=texto, font=("Helvetica", 10), relief="groove", width=12, height=4).grid(row=linha, column=coluna, padx=2, pady=2)
        coluna += 1
        if coluna == 7:
            coluna = 0
            linha += 1

# Funções para navegação
def mes_anterior():
    global ano_atual, mes_atual
    mes_atual -= 1
    if mes_atual == 0:
        mes_atual = 12
        ano_atual -= 1
    desenhar_calendario(ano_atual, mes_atual)

def mes_posterior():
    global ano_atual, mes_atual
    mes_atual += 1
    if mes_atual == 13:
        mes_atual = 1
        ano_atual += 1
    desenhar_calendario(ano_atual, mes_atual)

# Configuração da janela principal
root = Tk()
root.title("Calendário de Sorteios")

# Variáveis globais para o ano e mês atuais
ano_atual = datetime.now().year
mes_atual = datetime.now().month

# Frame para o calendário
calendario_frame = Frame(root)
calendario_frame.pack(pady=10)

# Botões de navegação
navegacao_frame = Frame(root)
navegacao_frame.pack()
Button(navegacao_frame, text="<< Mês Anterior", command=mes_anterior).pack(side="left", padx=10)
Button(navegacao_frame, text="Próximo Mês >>", command=mes_posterior).pack(side="left", padx=10)

# Desenhar o calendário inicial
desenhar_calendario(ano_atual, mes_atual)

# Iniciar a interface
root.mainloop()
