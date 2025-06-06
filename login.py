import tkinter as tk
from tkinter import messagebox
import sqlite3
from main import abrir_controle_pedidos
from tkinter import font
from PIL import Image, ImageTk

#CRIANDO PAGINA DE LOGIN
#CRIANDO O BANCO DE DADOS
def criar_banco():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   usuario TEXT UNIQUE NOT NULL,
                   senha TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

criar_banco()

#CRIANDO A FUNÇÃO DE VERIFICAR O LOGIN
def verificar_login():
    usuario = entry_usuario.get().strip()
    senha = entry_senha.get().strip()

    if not usuario or not senha:
        messagebox.showwarning("Erro ao logar!", "Todos os campos são obrigatórios!")
        return
    
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?",(usuario,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado and resultado[0] == senha:
        messagebox.showinfo("Logado!", "Logado com sucesso!")
        janela.destroy()
        abrir_controle_pedidos()
    else:
        messagebox.showerror("Erro ao logar!", "Usuário ou senha incorretos!")

#CRIANDO FUNÇÃO PRA ABRIR A TABELA DE REGISTRO
def abrir_tela_registro():
    janela.withdraw() #PARA ESCONDER A JANELA DE LOGIN
    janela_registro = tk.Toplevel()#CRIA UMA JANELA INDEPENDENTE NO PROGRAMA
    janela_registro.title("Registro")
    janela_registro.geometry("800x600")
    janela_registro.configure(bg="#D3D3D3")

    entrada_usuario = tk.StringVar()
    entrada_senha = tk.StringVar()
    entrada_confirmar_senha = tk.StringVar()

    def registrar_usuario():
        usuario = entrada_usuario.get().strip()
        senha = entrada_senha.get().strip()
        confirmar_senha = entrada_confirmar_senha.get().strip()

        if not usuario or not senha or not confirmar_senha:
            messagebox.showwarning("Erro ao registrar!", "Todos os campos são obrigatórios")
            return
        
        if senha != confirmar_senha:
            messagebox.showerror("Erro ao registrar!", "As senhas não coincidem!")
            return
        
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
            conn.commit()
            messagebox.showinfo("Registrado!", "Registrado com sucesso!")
            janela_registro.destroy()
            janela.deiconify()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro ao registrar!", "Usuário já existe!")
        finally:
            conn.close()

    
    #CRIANDO O FRAME PRINCIPAL DA PAGINA DE REGISTRO
    frame_principal = tk.Frame(janela_registro, bg="#D3D3D3")
    frame_principal.pack(expand=True)


    #TITULO DA PAGINA REGISTRO
    lbl_titulo = tk.Label(frame_principal, text="Cadastro", bg="#D3D3D3", fg="black", font=("Century Gothic", 30))
    lbl_titulo.pack(pady=40)


    #CRIANDO LABEL E ENTRY DO USUARIO DA PAGINA REGISTRO
    lbl_usuario_registro = tk.Label(frame_principal, text="Usuário", bg="#D3D3D3", fg="black", font=("Century Gothic", 15))
    lbl_usuario_registro.pack(pady=20)


    entry_usuario_registro = tk.Entry(frame_principal, width=28, textvariable=entrada_usuario, fg="black", font=("Century Gothic", 13))
    entry_usuario_registro.pack(pady=5)


    #CRIANDO LABEL E ENTRY DA SENHA E DA CONFIRMAÇÃO DE SENHA DA PAGINA REGISTRO
    lbl_senha_registro = tk.Label(frame_principal, text="Senha", bg="#D3D3D3", fg="black", font=("Century Gothic", 15))
    lbl_senha_registro.pack(pady=20)


    entry_senha_registro = tk.Entry(frame_principal, width=50, show="•", textvariable=entrada_senha, fg="black")
    entry_senha_registro.pack(pady=5)


    lbl_confirmar_senha_registro = tk.Label(frame_principal, text="Confirmar Senha", bg="#D3D3D3", fg="red", font=("Century Gothic", 15))
    lbl_confirmar_senha_registro.pack(pady=20)

    entry_confirmar_senha_registro = tk.Entry(frame_principal, width=50, show="*", textvariable=entrada_confirmar_senha, fg="red")
    entry_confirmar_senha_registro.pack(pady=5)


    #CRIANDO O BOTAO DE REGISTRAR DA PAGINA REGISTRO
    btn_registrar_registro = tk.Button(frame_principal, text="Registrar", command=registrar_usuario, bg="white", fg="red", font=("Century Gothic", 15, "bold"))
    btn_registrar_registro.pack(pady=20)


    btn_registrar_registro.bind("<Enter>", em_cima_botao)
    btn_registrar_registro.bind("<Leave>", sair_cima_botao)



#CRIANDO FUNCAO PRA ALTERAR O HOVER DO BOTAO
def em_cima_botao(event):
    event.widget["background"] = "#4169E1"

def sair_cima_botao(event):
    event.widget["background"] = "white"


    
#CRIANDO A JANELA
janela = tk.Tk()
janela.title("Minha Window")
janela.geometry("800x600")
janela.configure(bg="#F2F2F2")
janela.resizable(True, True)


#CRIANDO O FRAME PRINCIPAL
frame_principal = tk.Frame(janela, bg="#F2F2F2")
frame_principal.pack(expand=True)


#CRIANDO TITUTLO DA PAGINA
titulo_login = tk.Label(frame_principal, text="Login", font=("Century Gothic", 30), bg="#F2F2F2")
titulo_login.pack(pady=40)


#CRIANDO O LABEL E O ENTRY 1
#CAMPO USUARIO
label1 = tk.Label(frame_principal, text="Usuario", font=("Century Gothic", 15), bg="#F2F2F2", fg="red")
label1.pack(pady=5)


entry_usuario = tk.Entry(frame_principal, width=30, fg="black", font=("Century Gothic", 12))
entry_usuario.pack(pady=10)


#CRIANDO O LABEL E O ENTRY 2    
#CAMPO DO USUARIO
label2 = tk.Label(frame_principal, text="Senha", font=("Century Gothic", 15), bg="#F2F2F2", fg="black")
label2.pack(pady=5)

entry_senha = tk.Entry(frame_principal, width=50, show="•", fg="black")
entry_senha.pack(pady=10)


#CRIANDO FUNCAO PRA ALTERAR O HOVER DO BOTAO
def em_cima_botao(event):
    event.widget["background"] = "#B22222"
    event.widget["foreground"] = "white"

def sair_cima_botao(event):
    event.widget["background"] = "white"
    event.widget["foreground"] = "black"


#CRIANDO O BOTÃO PRA LOGAR
btn = tk.Button(frame_principal, text="LOGAR", command=verificar_login, fg="black", bg="white", font=("Century Gothic", 15, "bold"), activebackground="red")
btn.pack(pady=15)
btn.bind("<Enter>", em_cima_botao)
btn.bind("<Leave>", sair_cima_botao)


#CRIANDO BOTAO PRA REGISTRAR-SE
btn_registrar = tk.Button(frame_principal, text="REGISTRAR-SE", command=abrir_tela_registro, bg="white", fg="red", font=("Century Gothic", 15, "bold"))
btn_registrar.pack(pady=5)
btn_registrar.bind("<Enter>", em_cima_botao)
btn_registrar.bind("<Leave>", sair_cima_botao)



janela.mainloop()

