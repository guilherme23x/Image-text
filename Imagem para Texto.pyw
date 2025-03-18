import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract

# Especifique o caminho do executável do Tesseract, se necessário.
# Altere o caminho para o local correspondente no seu sistema.
pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'

# Defina a variável de ambiente TESSDATA_PREFIX para apontar para a pasta tessdata.
os.environ['TESSDATA_PREFIX'] = r'Tesseract-OCR\tessdata'

class OCRApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Texto da Imagem")
        self.geometry("600xauto")

        # Frame para exibição da imagem
        self.image_frame = ctk.CTkFrame(self, width=400, height=400)
        self.image_frame.grid(row=0, column=0, padx=10, pady=10)

        # Label para exibir a imagem
        self.image_label = ctk.CTkLabel(self.image_frame, text="Nenhuma imagem carregada")
        self.image_label.pack(expand=True, fill="both")

        # Frame para os controles (botões e exibição do texto extraído)
        self.controls_frame = ctk.CTkFrame(self, width=400, height=400)
        self.controls_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Botão para selecionar a imagem
        self.select_button = ctk.CTkButton(self.controls_frame, text="Selecionar Imagem", command=self.select_image)
        self.select_button.pack(pady=10)

        # Botão para extrair o texto
        self.extract_button = ctk.CTkButton(self.controls_frame, text="Extrair Texto", command=self.extract_text, state="disabled")
        self.extract_button.pack(pady=10)

        # Text box para exibir o texto extraído
        self.text_box = ctk.CTkTextbox(self.controls_frame, width=350, height=250)
        self.text_box.pack(pady=10)

        # Variável para armazenar a imagem selecionada (PIL Image)
        self.loaded_image = None

    def select_image(self):
        filepath = filedialog.askopenfilename(
            title="Selecione uma Imagem",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp"), ("Todos arquivos", "*.*")]
        )
        if not filepath:
            return

        try:
            self.loaded_image = Image.open(filepath)
            # Redimensiona a imagem mantendo a proporção para caber no frame.
            img_resized = self.loaded_image.copy()
            img_resized.thumbnail((400, 400))

            # Converter a imagem para ImageTk
            self.imgtk = ImageTk.PhotoImage(img_resized)
            self.image_label.configure(image=self.imgtk, text="")

            # Habilita o botão de extrair texto
            self.extract_button.configure(state="normal")

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a imagem.\n{e}")
            self.loaded_image = None
            self.extract_button.configure(state="disabled")

    def extract_text(self):
        if self.loaded_image is None:
            messagebox.showwarning("Aviso", "Por favor, selecione uma imagem primeiro.")
            return

        try:
            # Garantir que a imagem está no modo RGB
            if self.loaded_image.mode != "RGB":
                img = self.loaded_image.convert("RGB")
            else:
                img = self.loaded_image

            # Realiza a extração do texto utilizando pytesseract com o idioma português ('por')
            extracted_text = pytesseract.image_to_string(img, lang='por')

            # Limpa o text box e insere o texto extraído
            self.text_box.delete("1.0", "end")
            self.text_box.insert("1.0", extracted_text)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao extrair texto.\n{e}")

if __name__ == "__main__":
    app = OCRApp()
    app.mainloop()
