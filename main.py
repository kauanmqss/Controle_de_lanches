import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import font
from PIL import Image, ImageTk

def abrir_controle_pedidos():
    janela_principal = tk.Tk()
    janela_principal.geometry("900x600")
    janela_principal.title("controle_de_pedidos")
    janela_principal.configure(bg="#F2F2F2")
    janela_principal.resizable(False, False)

    def criar_banco_pedidos():
        conn = sqlite3.connect("lanchonete.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            item TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            observacao TEXT
        )""")
        conn.commit()
        conn.close()

    criar_banco_pedidos()

    #funcao para cadastrar pedido
    def cadastrar_pedido():
        cliente = entry_cliente.get().strip()
        item = combobox_item.get().strip()
        quantidade = spinbox_quantidade.get().strip()
        observacao = entry_observacao.get("1.0", tk.END).strip()
        
        if not cliente or not item or not quantidade.isdigit():
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        conn = sqlite3.connect("lanchonete.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pedidos (cliente, item, quantidade, observacao) VALUES (?, ?, ?, ?)", (cliente, item, quantidade, observacao))

        conn.commit()
        conn.close()

        listar_pedidos()
        limpar_campos()

    #função para listar os pedidos na tela
    def listar_pedidos():
        conn = sqlite3.connect("lanchonete.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM pedidos")
        pedidos = cursor.fetchall()
        conn.close()

        tree_lista.delete(*tree_lista.get_children())

        for pedido in pedidos:
            tree_lista.insert("", tk.END, values=pedido)



    #funcao para editar pedido
    def editar_pedido():
        selecionado = tree_lista.selection()
        if not selecionado:
            messagebox.showwarning("Atenção!","Selecione um item para editar!")
            return
        
        valores = tree_lista.item(selecionado)["values"]
        pedido_id = valores[0]


        janela_edicao = tk.Toplevel()
        janela_edicao.title("Editar itens")
        janela_edicao.geometry("400x300")
        janela_edicao.configure(bg="#F2F2F2")
        janela_edicao.resizable(False, False)
        janela_edicao.grab_set()

        edicao_cliente = tk.Label(janela_edicao, text="Editar cliente")
        edicao_cliente.pack()

        edicao_cliente_entry = tk.Entry(janela_edicao, width=20)
        edicao_cliente_entry.pack(pady=5)
        edicao_cliente_entry.insert(0, valores[1])

        label_edicao_item = tk.Label(janela_edicao, text="Editar os itens")
        label_edicao_item.pack()
        edicao_item = ttk.Combobox(janela_edicao, values=opcoes_itens, width=20)
        edicao_item.pack(pady=5)
        edicao_item.set(valores[2])


        label_edicao_quantidade = tk.Label(janela_edicao, text="Editar quantidade")
        label_edicao_quantidade.pack()
        edicao_quantidade = tk.Spinbox(janela_edicao, from_= 1, to= 100, width= 20)
        edicao_quantidade.pack(pady=5)
        edicao_quantidade.delete(0, tk.END)
        edicao_quantidade.insert(0, valores[3])

        label_edicao_observacao = tk.Label(janela_edicao, text="Editar observação")
        label_edicao_observacao.pack()
        edicao_observacao = tk.Text(janela_edicao, width=20, height=5)
        edicao_observacao.pack(pady=5)
        edicao_observacao.insert("1.0", valores[4])


        #funcao para abrir janela de edicao
        def salvar_edicao():
            novo_cliente = edicao_cliente_entry.get().strip()
            novo_item = edicao_item.get().strip()
            nova_quantidade = edicao_quantidade.get().strip()
            nova_observacao = edicao_observacao.get("1.0", tk.END).strip()
            
            if not novo_cliente or novo_item == "Escolha um item" or not nova_quantidade.isdigit():
                messagebox.showerror("Erro!", "Preencha todos os campos corretamente")
                return

            conn = sqlite3.connect("lanchonete.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pedidos
                SET cliente = ?, item = ?, quantidade = ?, observacao = ?
                WHERE id = ?
            """, (novo_cliente, novo_item, int(nova_quantidade), nova_observacao, pedido_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Confirmação", "Editado com sucesso!")
            janela_edicao.destroy()
            listar_pedidos()

        btn_salvar_edicao = tk.Button(janela_edicao, text="Salvar alterações", command=salvar_edicao)
        btn_salvar_edicao.pack()




    #função para excluir pedido
    def excluir_pedido():
        selecionado = tree_lista.selection()
        if not selecionado:
            messagebox.showwarning("Atenção!", "Selecione um item para apagar!")
            return
        
        confirmado = messagebox.askyesno("Atenção!", "Deseja realmente excluir?")
        if not confirmado:
            return
        
        item = tree_lista.item(selecionado)
        pedido_id = item["values"][0]

        conn = sqlite3.connect("lanchonete.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pedidos WHERE id = ?", (pedido_id,))

        conn.commit()
        conn.close()

        listar_pedidos()


    #função para limpar campos do pedido
    def limpar_campos():
        entry_cliente.delete(0, tk.END)
        combobox_item.set("Escolha um item")
        spinbox_quantidade.delete(0, tk.END)
        spinbox_quantidade.insert(0, "1")
        entry_observacao.delete("1.0", tk.END)

    def exibir_relatorios():
        relatorios_janela = tk.Toplevel()
        relatorios_janela.title("relatório")
        relatorios_janela.geometry("800x700")
        relatorios_janela.resizable(True, False)
        relatorios_janela.configure(bg="#F2F2F2")
        relatorios_janela.grab_set()

        tree_relatorio = ttk.Treeview(relatorios_janela, columns=("ID", "Cliente", "Item", "Quantidade", "Observação"), show="headings")

        tree_relatorio.heading("ID", text="ID")
        tree_relatorio.heading("Cliente", text="Cliente")
        tree_relatorio.heading("Item", text="Item")
        tree_relatorio.heading("Quantidade", text="Quantidade")
        tree_relatorio.heading("Observação", text="Observação")

        tree_relatorio.column("ID", width=20)
        tree_relatorio.column("Cliente", width=150)
        tree_relatorio.column("Item", width=250)
        tree_relatorio.column("Quantidade", width=80)
        tree_relatorio.column("Observação", width=250)

        tree_relatorio.pack(expand=True, fill="both", pady=20, padx=10)

        conn = sqlite3.connect("lanchonete.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pedidos")
        pedidos = cursor.fetchall()
        conn.close()

        for pedido in pedidos:
            tree_relatorio.insert("", tk.END, values=pedido)


    #validando apenas números para Quantidade
    def validar_numeros(texto):
        return texto.isdigit()


    #registrando a função
    vcmd = janela_principal.register(validar_numeros)

    #carregando imagem
    img = Image.open("images/kfc.png")
    img = img.resize((100, 50))
    img_tk = ImageTk.PhotoImage(img)

    #exibindo a imagem
    label_img = tk.Label(janela_principal, image=img_tk)
    label_img.pack(pady=8)
    label_img.image = img_tk


    #criando label e entry do cliente
    label_cliente = tk.Label(janela_principal, text="Cliente", bg="#F2F2F2", font=("Century Gothic", 12))
    label_cliente.pack()

    entry_cliente = tk.Entry(janela_principal, width=30, font=("Century Gothic", 10))
    entry_cliente.pack(pady=5)


    #criando label e combobox dos itens
    label_item = tk.Label(janela_principal, text="Item", bg ="#F2F2F2", font=("Century Gothic", 12))
    label_item.pack()

    #criando a lista de opções dos itens
    opcoes_itens = [
        "Hambúrguer com queijo e maionese",
        "Hambúrguer com queijo e BBQ",
        "Hambúrguer com salada e maionese",
        "Batata frita com cheddar e bacon",
        "Sorvete de chocolate",
        "Sorvete de baunilha",
        "Guaraná Coca-Cola",
        "Guaraná Antártica",
    ]

    combobox_item = ttk.Combobox(janela_principal, values=opcoes_itens, width=35, font=("Century Gothic", 10), state="readonly")
    combobox_item.pack(pady=5)
    combobox_item.set("Escolha um item")



    #criando label e spinbox da quantidade
    label_quantidade = tk.Label(janela_principal, text="Quantidade", bg="#F2F2F2", font=("Century Gothic", 12))
    label_quantidade.pack()

    spinbox_quantidade = tk.Spinbox(janela_principal, from_=1, to=100, width=28, font=("Century Gothic", 10), validate="key", validatecommand=(vcmd, "%P"))
    spinbox_quantidade.pack(pady=5)


    #criando label e entry para observacoes no pedido
    label_observacao = tk.Label(janela_principal, text="Observações", bg="#F2F2F2", font=("Century Gothic", 12))
    label_observacao.pack()

    entry_observacao = tk.Text(janela_principal, height=2, width=35, font=("Century Gothic", 10))
    entry_observacao.pack(pady=(0,20))



    #criando um frame para os botões
    frame_botoes = tk.Frame(janela_principal)
    frame_botoes.pack()



    #criando botoes
    btn_cadastrar = tk.Button(frame_botoes, text="Cadastrar pedido", bg="#D41C00", fg= "white", font=("Verdana", 12, "bold"), command=cadastrar_pedido)
    btn_cadastrar.pack(side="left", padx=5)

    btn_editar = tk.Button(frame_botoes, text="Editar pedidos", bg="#D41C00", fg="white", font=("Verdana", 12, "bold"), command=editar_pedido)
    btn_editar.pack(side="left", padx=5)

    btn_excluir = tk.Button(frame_botoes, text="Excluir pedido", bg="red", fg="white", font=("Verdana", 12, "bold"), command=excluir_pedido)
    btn_excluir.pack(side="left", padx=5)

    btn_relatorios = tk.Button(frame_botoes, text="Relatórios", bg="#D41C00", fg="white", font=("Verdana", 12, "bold"), command=exibir_relatorios)
    btn_relatorios.pack(side="left", padx=5)



    #criando a lista de pedidos
    tree_lista = ttk.Treeview(janela_principal, columns=("ID", "Cliente", "Item", "Quantidade", "Observação"), show="headings")

    #configurando os cabeçalhos
    tree_lista.heading("ID", text="ID")
    tree_lista.heading("Cliente", text="Cliente")
    tree_lista.heading("Item", text="Item")
    tree_lista.heading("Quantidade", text="Quantidade")
    tree_lista.heading("Observação", text="Observação")

    #configurando as colunas
    tree_lista.column("ID", width=50, stretch=False)
    tree_lista.column("Cliente", width=150)
    tree_lista.column("Item", width=250)
    tree_lista.column("Quantidade", width=50)
    tree_lista.column("Observação", width=250)

    #adicionando o widget à interface
    tree_lista.pack(expand=True, fill="both", pady=15)











    janela_principal.mainloop()