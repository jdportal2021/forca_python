from tkinter import CENTER, Tk, Label, StringVar, messagebox, Entry
from awesometkinter import Frame3d, Button3d
from random import randrange
from PIL import Image, ImageTk

class forca():
    def __init__(self) -> None:
        self.set_var()
        self.dimension()
        self.frames()
        self.widgets()
        self.root.mainloop()

    def set_var(self):
        self.root = Tk()
        self.secret_word_stv = StringVar()
        self.phrase = StringVar()
        self.phrase_lost = StringVar()
        self.wrong_letters = StringVar()
        self.letter = StringVar()
        self.list_wrong_letters = []
        self.lost = False
        self.won = False
        
    def dimension(self):
        self.root.title('Meu Portal')
        self.root.iconbitmap('Imagens/icone python.ico')
        self.root.configure(background='#004FA5')
        self.root.resizable(True, True)
        self.root.maxsize(600, 400)
        self.root.minsize(600, 400)
        # dimensões da janela
        self.width = 600
        self.height = 400
        # resolução do nosso sistema
        self.width_screen = self.root.winfo_screenwidth()
        self.height_screen = self.root.winfo_screenheight()
        # posição da janela
        self.posx = self.width_screen/2 - self.width/2
        self.posy = self.height_screen/2 - self.height/2
        # definir a geometry
        self.root.geometry('%dx%d+%d+%d' %
                           (self.width, self.height, self.posx, self.posy))

    def frames(self):
        self.frame = Frame3d(self.root, width=590, height=390, bg='#004FA5')
        self.frame.place(x=5, y=5)

    def widgets(self):
        #widgets
        #imagem
        self.img_welcome_resized = self.resized_img('Imagens/bem vindo.png', 300, 60)
        self.img_welcome = Label(self.frame, image=self.img_welcome_resized, borderwidth=0)
        self.img_award_resized = self.resized_img('Imagens/transparente.png', 300, 225)
        self.img_award = Label(self.frame, image=self.img_award_resized, borderwidth=0)
        #label
        self.lbl_secret_word = Label(self.frame, textvariable=self.secret_word_stv, bg='#004FA5', fg='white', font='Helvetica 30')
        self.lbl_phrase = Label(self.frame, textvariable=self.phrase, bg='#004FA5', fg='#9FDAEA', font='Helvetica 10')
        self.lbl_phrase_lost = Label(self.frame, textvariable=self.phrase_lost, bg='#004FA5', fg='#9FDAEA', font='Helvetica 10')
        self.lbl_wrong_letters = Label(self.frame, textvariable=self.wrong_letters, bg='#004FA5', fg='#9FDAEA', font='Helvetica 20')
        #entry
        self.func_check = (self.frame.register(self.input_value_test), '%P')
        self.ety_letter = Entry(self.frame, justify=CENTER, validate='key', validatecommand=self.func_check, textvariable=self.letter)
        #button
        self.btn_start = Button3d(self.frame, text='Iniciar', bg='#FFFE00', command=lambda:self.start())
        #layout
        #imagem
        self.img_welcome.place(x=140, y=6)
        self.img_award.place(x=20, y=50)
        #label
        self.lbl_secret_word.place(x=10, y=280)
        self.lbl_phrase.place(x=10, y=10)
        self.lbl_phrase_lost.place(x=10, y=30)
        self.lbl_wrong_letters.place(x=10, y=50)
        #entry
        self.ety_letter.place(x=11, y=350, width=50)
        self.ety_letter.config(state='disabled')
        self.ety_letter.bind('<KeyRelease>', self.logic)
        #button
        self.btn_start.place(x=440, y=340, width=140, height=40)
        
    def start(self):
        self.ety_letter.config(state='normal')
        self.img_welcome.destroy()
        self.img_forca_resized = self.resize_img('Imagens/forca0.png', 160, 240)
        self.img_forca = Label(self.frame, image=self.img_forca_resized, borderwidth=0)
        self.img_forca.place(x=420, y=10)
        self.img_award_resized = self.resize_img('Imagens/transparent.png', 300, 225)
        self.img_award.configure(image=self.img_award_resized)
        self.img_award.image = self.img_award_resized

        self.wrong_letters.set('')
        self.list_wrong_letters = []
        self.phrase_lost.set('')
        self.secret_word = self.get_secret_word()
        self.correct_letters = self.start_correct_letters(self.secret_word)
        self.secret_word_stv.set(self.correct_letters)
        self.lost = False
        self.won = False
        self.error = 0
        self.missing_letters = len(self.correct_letters)
        self.phrase.set(f'Você tem {6-self.error} tentativas')
        self.ety_letter.focus_force()
  
    def get_secret_word(self):
        self.words = []
        with open("words.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                self.words.append(line)

        self.number = randrange(0, len(self.words))
        self.word_secret = self.words[self.number].upper()
        if len(self.word_secret) > 14:
            messagebox.showerror('ERRO', 'Coloque no arquivo de texto somente palavras até 14 letras')
            self.get_secret_word()
        return self.word_secret

    def start_correct_letters(self, word):
        return ["_" for letter in word]

    def set_kick(self):
        self.kick = self.letter.get()
        self.kick = self.kick.strip().upper()
        if (self.kick in self.list_wrong_letters):
            messagebox.showerror('ERRO', 'Você já digitou essa letra')
            return ''
        else:
            self.list_wrong_letters.append(self.kick)
            if (self.list_wrong_letters[-1] == ''):
                    self.list_wrong_letters.pop()
            self.wrong_letters.set(self.list_wrong_letters)
            return self.kick
            
    def set_correct_kick(self, kick, correct_letters, secret_word):
        self.index = 0
        for letter in secret_word:
            if (kick == letter):
                correct_letters[self.index] = letter
            self.index += 1

    def print_msg_won(self):
        self.wrong_letters.set('')
        self.phrase.set('Parabéns, você ganhou!')
        self.img_award_resized = self.resize_img('Imagens/trofeu.png', 300, 225)
        self.img_award.configure(image=self.img_award_resized)
        self.img_award.image = self.img_award_resized

    def print_msg_lost(self, secret_word):
        self.wrong_letters.set('')
        self.phrase.set('Puxa, você foi enforcado!')
        self.phrase_lost.set(f'A palavra era "{secret_word}"')
        self.img_award_resized = self.resize_img('Imagens/skull.png', 300, 225)
        self.img_award.configure(image=self.img_award_resized)
        self.img_award.image = self.img_award_resized

    def draw_forca(self, error):
        if(error == 1):
            self.img_forca_resized = self.resize_img('Imagens/forca1.png', 160, 240)
            self.img_forca.configure(image=self.img_forca_resized)
            self.img_forca.image = self.img_forca_resized
        if(error == 2):
            self.img_forca_resized = self.resize_img('Imagens/forca2.png', 160, 240)
            self.img_forca.configure(image=self.img_forca_resized)
            self.img_forca.image = self.img_forca_resized

        if(error == 3):
            self.img_forca_resized = self.resize_img('Imagens/forca3.png', 160, 240)
            self.img_forca.configure(image=self.img_forca_resized)
            self.img_forca.image = self.img_forca_resized

        if(error == 4):
            self.img_forca_resized = self.resize_img('Imagens/forca4.png', 160, 240)
            self.img_forca.configure(image=self.img_forca_resized)
            self.img_forca.image = self.img_forca_resized

        if(error == 5):
            self.img_forca_resized = self.resize_img('Imagens/forca5.png', 160, 240)
            self.img_forca.configure(image=self.img_forca_resized)
            self.img_forca.image = self.img_forca_resized

        if(error == 6):
            self.img_forca_resized = self.resize_img('Imagens/forca6.png', 160, 240)
            self.img_forca.configure(image=self.img_forca_resized)
            self.img_forca.image = self.img_forca_resized

    def resized_img(self, path, size_x, size_y):
        self.img_original = Image.open(path)
        self.img_resized = self.img_original.resize((size_x, size_y), Image.Resampling.LANCZOS)
        self.img_resized = ImageTk.PhotoImage(self.img_resized)
        return self.img_resized

    def logic(self, event):
        self.kick = self.set_kick()
        if self.kick != '':
            if (self.kick in self.secret_word):
                self.set_correct_kick(self.kick, self.correct_letters, self.secret_word)
                self.missing_letters = str(self.correct_letters.count('_'))
            else:
                self.error += 1
                self.phrase.set(f'Você ainda tem {6-self.error} tentativas')
                self.draw_forca(self.error)
            self.lost = self.error == 6
            self.won = "_" not in self.correct_letters
            self.secret_word_stv.set(self.correct_letters)
        if (self.won):
            self.print_msg_won()
            self.ety_letter.delete(0)
            self.ety_letter.config(state='disabled')
        elif (self.lost):
            self.print_msg_lost(self.secret_word)
            self.ety_letter.delete(0)
            self.ety_letter.config(state='disabled')
        self.ety_letter.delete(0)
            
    def input_value_test(self, valor):
        self.list = "'abcdefghijklmnopqrstuvwxyzçäãáâéêíöõóôüúABCDEFGHIJKLMNOPQRSTUVWXYZÇÄÃÁÂÉÊÍÖÕÓÔÜÚ"
        if valor in self.list:
            return True
        else:
            return False

    
forca()

