# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 13:33:18 2019

@author: Cary Gentry
"""

#To be implemented in later versions:
#1. User input to determine number of words displayed
#2. Name of file displayed when selecting it
#3. Improvement to output in web browser
#4. N-gram word detector
#5. 

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
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

#----Functions----#

#Method that a PDF that is read into the program goes through to eliminate any unwanted words or symbols#
def preprocess(text):
    #Filters out punctuation from paragraph witch becomes tokenized to words and punctuation#
    tokenizer = RegexpTokenizer(r'\w+')
    result = tokenizer.tokenize(text)
    
    #Makes all words lowercase#
    words = [item.lower() for item in result]
    
    #Removes all remaining tokens that are not alphabetic#
    result = [word for word in words if word.isalpha()]
    
    #Imports stopwords to be removed from paragraph#
    stop_words = set(stopwords.words("english"))
    
    #Removes the stop words from the paragraph#
    filtered_sent = []
    for w in result:
        if w not in stop_words:
            filtered_sent.append(w)
    
    #Return word to root word/chop-off derivational affixes#
    ps = PorterStemmer()
    stemmed_words = []
    for w in filtered_sent:
        stemmed_words.append(ps.stem(w))
    
    #Lemmatization, which reduces word to their base word, which is linguistically correct lemmas#
    lem = WordNetLemmatizer()
    lemmatized_words = ' '.join([lem.lemmatize(w,'n') and lem.lemmatize(w,'v') for w in filtered_sent])
    
    #Re-tokenize lemmatized words string#
    tokenized_word = word_tokenize(lemmatized_words)
    return tokenized_word

#Wraps two functions inside an object which allows both functions to use filename#
class PDFSelector:
    #Creates global variable 'filename'#
    def __init(self):
        self.filename = ""

    #Allows user to select PDF to use in program#
    def select_PDF(self):
        #Opens file directory to select a file, and shows both folders and PDF files only#
        self.filename = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("pdf files", "*.pdf"), ("all files", "*.*")))
        file_name.set(self.filename)
        window.update()
        
    #Method for PDF to run through to convert it into text, then print it out in a browser#
    def run_program(self):    
        #Loads in PDF into program#
        PDF_file = open(self.filename, 'rb')
        read_pdf = PyPDF2.PdfFileReader(PDF_file)
    
        #Determines number of pages in PDF file and sets the document content to 'null'#
        number_of_pages = read_pdf.getNumPages()
        doc_content = ""
    
        #Extract text from the PDF file#
        for i in range(number_of_pages):
            page = read_pdf.getPage(0)
            page_content = page.extractText()
            doc_content += page_content
        
        #Turns the text drawn from the PDF file into data the remaining code can understand#
        tokenized_words = preprocess(doc_content)
        
        #Determine frequency of words tokenized + lemmatized text#

        fdist = FreqDist(tokenized_words)
        final_list = fdist.most_common(user_input)
    
        #Organize data into two columns and export the data to an html that automatically opens#
        df = pandas.DataFrame(final_list, columns = ["Word", "Frequency"])
        df.to_html('word_frequency.html')
        webbrowser.open('file://' + os.path.realpath('word_frequency.html'))      

#----Main----#

#Creates an instance of the wrapped functions to use the GUI#        
selector = PDFSelector()

#Creats the GUI that will be used to select inputs#
window = tk.Tk()
window.geometry("375x130")

window.title("Word Frequency Program")

#Code literally just to make the GUI look better#
lblfilla = tk.Label(window, text = "   ").grid(row = 0, column = 0)
lblfillb = tk.Label(window, text = "   ").grid(row = 0, column = 1)
lblfillc = tk.Label(window, text = "   ").grid(row = 0, column = 2)
lblfilld = tk.Label(window, text = "   ").grid(row = 0, column = 3)
lblfille = tk.Label(window, text = "   ").grid(row = 0, column = 4)
lblfillf = tk.Label(window, text = "   ").grid(row = 1, column = 0)
lblfillg = tk.Label(window, text = "   ").grid(row = 2, column = 0)
lblfillh = tk.Label(window, text = "   ").grid(row = 3, column = 0)
lblfilli = tk.Label(window, text = "   ").grid(row = 4, column = 0)

#Just a simple label on the GUI# (FILE NAME IS CURRENTLY NOT ABLE TO BE DISPLAYED)
file_name = StringVar()
lbl1 = tk.Label(window, text = "File Selected: ").grid(row = 1, column = 1)
lbl1a = tk.Label(window, textvariable = file_name).grid(row = 1, column = 2)

#Label asking for input to determine number of words to be displayed in the data table# (NOT IMPLEMENTED YET)
lbl2 = tk.Label(window, text = "Number of Words: ").grid(row = 2, column = 1)
user_input = tk.Entry(window).grid(row = 2, column = 2)

#Calls the select_PDF method to choose a PDF for the program to read#
button1 = ttk.Button(window, text = "Select File", command = selector.select_PDF).grid(row = 1, column = 4)

#Button to make the program execute#
button2 = ttk.Button(window, text = "Run", command = selector.run_program).grid(row = 2, column = 4)

#Quits out of the program when certain button clicked#
button3 = ttk.Button(window, text = "Quit", command = window.quit).grid(row = 3, column = 2)

window.mainloop()
window.destroy()





































