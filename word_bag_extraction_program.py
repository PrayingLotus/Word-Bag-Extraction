import os
import PyPDF2
import pandas
import webbrowser
import tkinter as tk
from tkinter import StringVar
from tkinter import ttk
from tkinter import filedialog
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

#----Functions----#

#Method that a PDF that is read into the program goes through to eliminate any unwanted words or symbols#
def preprocess_token(text):
    #Filters out punctuation from paragraph which becomes tokenized to words and punctuation#
    result1 = RegexpTokenizer(r'\w+').tokenize(text)
    
    #Makes all words lowercase#
    result2 = [item.lower() for item in result1]
    
    #Removes all remaining tokens that are not alphabetic#
    result3 = [word for word in result2 if word.isalpha()]
    
    #Imports and removes the stop words from the paragraph#
    filtered_result = []
    for w in result3:
        if w not in stopwords.words("english"):
            filtered_result.append(w)

    #Lemmatization, which reduces word to their base word, which is linguistically correct lemmas#
    lem = WordNetLemmatizer()
    lemmatized_result = ' '.join([lem.lemmatize(w,'n') and lem.lemmatize(w,'v') for w in filtered_result])
    
    #Re-tokenize lemmatized words string#
    tokenized_result = word_tokenize(lemmatized_result)
    return tokenized_result

#Wraps two functions inside an object which allows both functions to use filename#
class PDFSelector:
    #Allows user to select PDF to use in program#
    def select_PDF(self):
        #Opens file directory to select a file, and shows both folders and PDF files only#
        self.filename = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("pdf files", "*.pdf"), ("all files", "*.*")))
        file_name.set(self.filename)
        window.update_idletasks()
        window.update()
        
    #Method for PDF to run through to convert it into text, then print it out in a browser#
    def run_program(self):    
        #Loads in PDF into program#
        read_pdf = PyPDF2.PdfFileReader(open(self.filename, 'rb'))
    
        #Sets the document content to 'null'#
        doc_content = ""
    
        #Extract text from the PDF file#
        for i in range(read_pdf.getNumPages()):
            doc_content += read_pdf.getPage(i).extractText()
        
        #Turns text drawn from the PDF file into data the remaining code can understand#
        tokenized_words = preprocess_token(doc_content)
        
        #Determine frequency of words tokenized#
        fdist_token = FreqDist(tokenized_words)
        final_list_token = fdist_token.most_common(int(user_input.get()))
                
        #Organize data into two columns and export the data to an html that automatically opens is run#
        df_token = pandas.DataFrame(final_list_token, columns = ["Word", "Frequency"])
        df_token.to_html('word_frequency.html')
        webbrowser.open('file://' + os.path.realpath('word_frequency.html'))      
        
#----Main----#

#Creates an instance of the wrapped functions to use the GUI#        
selector = PDFSelector()

#Creats the GUI that will be used to select inputs#
window = tk.Tk()
window.geometry("600x130")
window.title("Word Frequency Program")
window.resizable(0, 0)

#Code literally just to make the GUI look better#
for x in range(0, 4)
    lblfilla = tk.Label(window, text = "   ").grid(row = 0, column = x)
for x in range(1, 4)
    lblfillf = tk.Label(window, text = "   ").grid(row = x, column = 0)

#A label on the GUI that will update with the name of the file selected after it is selected#
lbl1 = tk.Label(window, text = "File Selected: ")
lbl1.grid(row = 1, column = 1)
file_name = StringVar()
lbl1a = tk.Label(window, textvariable = file_name)
lbl1a.grid(row = 1, column = 2)

#Label asking for input to determine number of words to be displayed in the data table#
lbl2 = tk.Label(window, text = "Number of Words: ")
lbl2.grid(row = 2, column = 1)
user_input = tk.Entry(window)
user_input.grid(row = 2, column = 2)

#Shows a warning at all times that if a number is not present in entry portion, the program will not execute#
lbl3 = tk.Label(window, text = "*PROGRAM WILL ONLY RUN WHEN NUMBER IS ENTERED*")
lbl3.grid(row = 3, column = 2)
lbl3.configure(font = ('None', '10', 'bold'), fg = 'red')

#Calls the select_PDF method to choose a PDF for the program to read#
button1 = ttk.Button(window, text = "Select File", command = selector.select_PDF)
button1.grid(row = 1, column = 4)

#Button to make the program execute#
button2 = ttk.Button(window, text = "Run", command = selector.run_program)
button2.grid(row = 2, column = 4)

#Quits out of the program when certain button clicked#
button3 = ttk.Button(window, text = "Quit", command = window.quit).grid(row = 4, column = 2)

window.mainloop()
window.destroy()
