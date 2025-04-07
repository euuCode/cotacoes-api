import requests
import sqlite3
from datetime import datetime
import os
from tkinter import Tk, Button, messagebox, filedialog

def salvar_cotacoes():
    try:
        # Requisição da API
        url = "https://api.hgbrasil.com/finance/quotations?key=296080c2"
        resposta = requests.get(url)
        dados = resposta.json()

        dolar = dados['results']['currencies']['USD']['buy']
        euro = dados['results']['currencies']['EUR']['buy']
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Janela para salvar
        caminho = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("Banco de Dados SQLite", "*.db")],
            title="Escolha onde salvar o banco",
            initialfile="bdcotacoes.db"
        )

        if not caminho:
            return

        # Conexão e criação da tabela
        conexao = sqlite3.connect(caminho)
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS moedas (
                Data TEXT,
                Dolar REAL,
                Euro REAL
            )
        """)
        cursor.execute("INSERT INTO moedas (Data, Dolar, Euro) VALUES (?, ?, ?)", (data_atual, dolar, euro))
        conexao.commit()
        conexao.close()

        messagebox.showinfo("Sucesso", f"Cotações salvas em:\n{caminho}")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def ver_dados_salvos():
    try:
        caminho = filedialog.askopenfilename(
            title="Selecione o banco de dados",
            filetypes=[("Banco de Dados SQLite", "*.db")]
        )

        if not caminho:
            return

        conexao = sqlite3.connect(caminho)
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM moedas")
        dados = cursor.fetchall()
        conexao.close()

        if not dados:
            messagebox.showinfo("Dados", "Nenhuma cotação encontrada.")
            return

        resultado = ""
        for linha in dados:
            resultado += f"Data: {linha[0]} | Dólar: R${linha[1]} | Euro: R${linha[2]}\n"

        messagebox.showinfo("Cotações Salvas", resultado)

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Criando a janela principal
janela = Tk()
janela.title("Cotações de Moedas")
janela.geometry("300x150")

btn_salvar = Button(janela, text="Consultar e Salvar Cotações", command=salvar_cotacoes)
btn_salvar.pack(pady=10)

btn_ver = Button(janela, text="Ver Dados Salvos", command=ver_dados_salvos)
btn_ver.pack(pady=10)

janela.mainloop()
