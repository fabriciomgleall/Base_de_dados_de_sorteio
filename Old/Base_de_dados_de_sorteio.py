import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
from tkinter.ttk import Combobox

# Configurar o banco de dados
conn = sqlite3.connect('Base_de_dados_de_sorteio/sorteios.db')
cursor = conn.cursor()

# Criar tabela (se ainda não existir)
cursor.execute('''
CREATE TABLE IF NOT EXISTS sorteios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto TEXT NOT NULL,
    dias_sorteio TEXT NOT NULL,
    mes_sorteio TEXT NOT NULL,
    multiplo REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    modalidade INTEGER NOT NULL,
    frequencia TEXT NOT NULL
)
''')
conn.commit()

# Função para inserir os dados no banco de dados
def inserir_sorteio():
    produto = produto_var.get()
    dias_sorteio = dias_var.get()
    mes_sorteio = mes_var.get()
    multiplo = multiplo_var.get()
    quantidade = quantidade_var.get()
    modalidade = modalidade_var.get()
    frequencia = frequencia_var.get()

    if produto and dias_sorteio and mes_sorteio and multiplo and quantidade and modalidade and frequencia:
        try:
            cursor.execute('''
            INSERT INTO sorteios (produto, dias_sorteio, mes_sorteio, multiplo, quantidade, modalidade, frequencia)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (produto, dias_sorteio, mes_sorteio, float(multiplo), int(quantidade), int(modalidade), frequencia))
            conn.commit()
            messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")
            limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir os dados: {e}")
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")

# Função para limpar os campos de entrada
def limpar_campos():
    produto_var.set("")
    dias_var.set("")
    mes_var.set("")
    multiplo_var.set("")
    quantidade_var.set("")
    modalidade_var.set("")
    frequencia_var.set("")

# Configuração da interface gráfica
root = Tk()
root.title("Cadastro de Sorteios")

# Variáveis para armazenar os valores dos campos
produto_var = StringVar()
dias_var = StringVar()
mes_var = StringVar()
multiplo_var = StringVar()
quantidade_var = StringVar()
modalidade_var = StringVar()
frequencia_var = StringVar()

# Lista de meses abreviados
meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

# Lista de dias da semana
dias_semana = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]

# Lista de opções de frequência
frequencias = ["Primeira semana", "Última semana", "Todas as semanas"]

# Rótulos e campos de entrada
Label(root, text="Produto:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
Entry(root, textvariable=produto_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Dias do Sorteio:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
dias_combobox = Combobox(root, textvariable=dias_var, values=dias_semana, state="readonly")
dias_combobox.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Frequência:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
frequencia_combobox = Combobox(root, textvariable=frequencia_var, values=frequencias, state="readonly")
frequencia_combobox.grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Mês do Sorteio:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
mes_combobox = Combobox(root, textvariable=mes_var, values=meses, state="readonly")
mes_combobox.grid(row=3, column=1, padx=10, pady=5)

Label(root, text="Múltiplo:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
Entry(root, textvariable=multiplo_var).grid(row=4, column=1, padx=10, pady=5)

Label(root, text="Quantidade:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
Entry(root, textvariable=quantidade_var).grid(row=5, column=1, padx=10, pady=5)

Label(root, text="Modalidade:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
Entry(root, textvariable=modalidade_var).grid(row=6, column=1, padx=10, pady=5)

# Botão para salvar os dados
Button(root, text="Salvar", command=inserir_sorteio).grid(row=7, column=0, columnspan=2, pady=10)

# Iniciar a interface gráfica
root.mainloop()

# Fechar conexão com o banco de dados
conn.close()
