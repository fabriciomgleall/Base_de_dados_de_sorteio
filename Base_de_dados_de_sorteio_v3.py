import os
import dbf
from tkinter import Tk, Label, Entry, Button, messagebox, ttk
from customtkinter import *

# Configuração do arquivo DBF
dbf_file = "Base_de_dados_de_sorteio/base_de_dados_de_sorteio.dbf"

# Função para criar o arquivo DBF apenas se ele não existir
def criar_arquivo_dbf():
    if not os.path.exists(dbf_file):
        try:
            # Criar o diretório se não existir
            os.makedirs(os.path.dirname(dbf_file), exist_ok=True)
            
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
        table = dbf.Table(dbf_file)
        table.open(mode=dbf.READ_WRITE)

        produto = produto_entry.get()
        mod = int(modalidade_entry.get())
        qtd = int(quantidade_entry.get())
        mult = float(multiplo_entry.get())
        dias = dias_sorteio_combobox.get()
        mes = mes_sorteio_combobox.get()
        freq = frequencia_combobox.get()

        if not produto or not mod or not qtd or not mult or not dias or not mes or not freq:
            raise ValueError("Todos os campos são obrigatórios!")

        if mes == "All":
            for m in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]:
                table.append((produto, mod, qtd, mult, dias, m, freq))
        elif mes == "Sem":
            for m in ["May","Nov"]:
                table.append((produto, mod, qtd, mult, dias, m, freq))
        else:
            table.append((produto, mod, qtd, mult, dias, mes, freq))
   
        table.close()

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

# Configuração da interface gráfica
root = CTk()
root.geometry("350x330")
root.title("Cadastro de Sorteios")

set_appearance_mode("dark")

CTkLabel(root, text="Produto:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
produto_entry = CTkEntry(root)
produto_entry.grid(row=0, column=1, padx=10, pady=5)

CTkLabel(root, text="Modalidade:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
modalidade_entry = CTkEntry(root)
modalidade_entry.grid(row=1, column=1, padx=10, pady=5)

CTkLabel(root, text="Quantidade:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
quantidade_entry = CTkEntry(root)
quantidade_entry.grid(row=2, column=1, padx=10, pady=5)

CTkLabel(root, text="Múltiplo:", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
multiplo_entry = CTkEntry(root)
multiplo_entry.grid(row=3, column=1, padx=10, pady=5)

CTkLabel(root, text="Dia(s) do Sorteio:", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
dias_opcoes = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
dias_sorteio_combobox = CTkComboBox(root, values=dias_opcoes, state="readonly")
dias_sorteio_combobox.grid(row=4, column=1, padx=10, pady=5)

CTkLabel(root, text="Mês do Sorteio:", font=("Arial", 14)).grid(row=5, column=0, padx=10, pady=5, sticky="e")
meses_opcoes = ["All","Sem", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
mes_sorteio_combobox = CTkComboBox(root, values=meses_opcoes, state="readonly")
mes_sorteio_combobox.grid(row=5, column=1, padx=10, pady=5)

CTkLabel(root, text="Frequência:", font=("Arial", 14)).grid(row=6, column=0, padx=10, pady=5, sticky="e")
frequencia_opcoes = ["Todas as semanas", "Primeira semana", "Ultima semana"]
frequencia_combobox = CTkComboBox(root, values=frequencia_opcoes, state="readonly")
frequencia_combobox.grid(row=6, column=1, padx=10, pady=5)

btn = CTkButton(master=root, text="Adicionar Sorteio", command=adicionar_dados, corner_radius=32, fg_color="#132ceb", hover_color="#9413eb").place(relx=0.5, rely=0.9, anchor="center")

# Criar o arquivo DBF se não existir
criar_arquivo_dbf()

root.mainloop()