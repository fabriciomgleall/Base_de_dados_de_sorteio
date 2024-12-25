import os
import dbf
from tkinter import Tk, Label, Entry, Button, messagebox, ttk

# Configuração do arquivo DBF
dbf_file = "Base_de_dados_de_sorteio/base_de_dados_de_sorteio.dbf"

# Função para criar o arquivo DBF apenas se ele não existir
def criar_arquivo_dbf():
    if not os.path.exists(dbf_file):
        try:
            # Criar o arquivo com a estrutura necessária
            table = dbf.Table(
                dbf_file,
                "produto C(100); mod N(5,0); qtd N(10,0); mult N(10,2); dias C(100); mes C(3); freq C(20)"
            )
            table.open(mode=dbf.READ_WRITE)
            table.close()
            print(f"Arquivo {dbf_file} criado com sucesso.")
        except Exception as e:
            print(f"Erro ao criar o arquivo DBF: {e}")
    else:
        print(f"Arquivo {dbf_file} já existe.")

# Função para adicionar dados ao DBF
def adicionar_dados():
    try:
        # Abrir o arquivo DBF
        table = dbf.Table(dbf_file)
        table.open(mode=dbf.READ_WRITE)

        # Obter valores da interface
        produto = produto_entry.get()
        mod = int(modalidade_entry.get())
        qtd = int(quantidade_entry.get())
        mult = float(multiplo_entry.get())
        dias = dias_sorteio_combobox.get()
        mes = mes_sorteio_combobox.get()
        freq = frequencia_combobox.get()

        # Validar dados
        if not produto or not mod or not qtd or not mult or not dias or not mes or not freq:
            raise ValueError("Todos os campos são obrigatórios!")

        # Adicionar registro ao DBF
        table.append((produto, mod, qtd, mult, dias, mes, freq))
        table.close()

        # Limpar os campos e exibir mensagem de sucesso
        produto_entry.delete(0, 'end')
        modalidade_entry.delete(0, 'end')
        quantidade_entry.delete(0, 'end')
        multiplo_entry.delete(0, 'end')
        dias_sorteio_combobox.set("")
        mes_sorteio_combobox.set("")
        frequencia_combobox.set("")
        messagebox.showinfo("Sucesso", "Dados adicionados com sucesso!")
    except ValueError as e:
        messagebox.showerror("Erro", str(e))
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao adicionar dados: {e}")

# Criar arquivo DBF, caso não exista
criar_arquivo_dbf()

# Interface gráfica para adicionar dados
root = Tk()
root.title("Cadastro de Sorteios (DBF)")

# Campos do formulário
Label(root, text="Produto:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
produto_entry = Entry(root)
produto_entry.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Modalidade:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
modalidade_entry = Entry(root)
modalidade_entry.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Quantidade:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
quantidade_entry = Entry(root)
quantidade_entry.grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Múltiplo:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
multiplo_entry = Entry(root)
multiplo_entry.grid(row=3, column=1, padx=10, pady=5)

Label(root, text="Dia(s) do Sorteio:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
dias_opcoes = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
dias_sorteio_combobox = ttk.Combobox(root, values=dias_opcoes, state="readonly")
dias_sorteio_combobox.grid(row=4, column=1, padx=10, pady=5)

Label(root, text="Mês do Sorteio:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
meses_opcoes = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
mes_sorteio_combobox = ttk.Combobox(root, values=meses_opcoes, state="readonly")
mes_sorteio_combobox.grid(row=5, column=1, padx=10, pady=5)

Label(root, text="Frequência:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
frequencia_opcoes = ["Todas as semanas", "Primeira semana", "Última semana"]
frequencia_combobox = ttk.Combobox(root, values=frequencia_opcoes, state="readonly")
frequencia_combobox.grid(row=6, column=1, padx=10, pady=5)

# Botão para adicionar dados
Button(root, text="Adicionar Sorteio", command=adicionar_dados).grid(row=7, column=0, columnspan=2, pady=10)

# Iniciar a interface
root.mainloop()
