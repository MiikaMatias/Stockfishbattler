from cgitb import text
from importlib.resources import path
from logging import root
from random import seed
from textwrap import wrap
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
import tkinter
from turtle import back, bgcolor, color, heading, width
from webbrowser import BackgroundBrowser
import numpy as np
import os
import Engine_Sim
from stockfish.models import Stockfish
import stockfish
import chess
import PGN_Processor as pgn


class App():

    def __init__(self):
        self.start = False
        self.copy = False

        self.root = Tk()
        self.root.withdraw() #should hide the console in exe
        self.root.title("MagaChess 2.0")
        self.root.rowconfigure(0,weight=1)
        self.root.columnconfigure(0,weight=1)

        self.player_one = "stockfish 8"
        self.player_two = "stockfish 15"

        self.create_styles() # creates styles
        self.build() # frames -> creates widgets -> places

    def create_styles(self):
        self.sGrey = ttk.Style()
        self.sGrey.configure('Frame0.TFrame',background='#000814')

        self.sRed = ttk.Style()
        self.sRed.configure('Frame1.TFrame', background = '#540b0e')

        self.sWhite = ttk.Style()
        self.sWhite.configure('Frame2.TFrame', background = '#d39461')

        self.sGreyFore = ttk.Style()
        self.sGreyFore.configure('Frame3.TFrame',background = '#edf2f4')

    def startfunc(self):
        first = None
        last = None
        if "15" in self.player_one:
            first = Engine_Sim.EngineSim(15,self.inputbox.get("1.0","end-1c").split(" "),int(self.depth.get()))
        if "8" in self.player_one:
            first = Engine_Sim.EngineSim(8,self.inputbox.get("1.0","end-1c").split(" "),int(self.depth.get()))
        if "15" in self.player_two:
            last = Engine_Sim.EngineSim(15,self.inputbox.get("1.0","end-1c").split(" "),int(self.depth.get()))
        if "8" in self.player_two:
            last = Engine_Sim.EngineSim(8,self.inputbox.get("1.0","end-1c").split(" "),int(self.depth.get()))
        
        self.log.insert("end", f"First to move -> {self.player_one} \nSecond to move -> {self.player_two}\n")
        self.outputbox.delete("1.0","end-1c")
        self.outputbox.insert("end", "".join([str(move) + " " for move in last.boardstate]) + " ")     
        self.root.update()
        
        for i in range(1,int(self.howmanymoves.get())+1):
            try:
                self.log.insert("end",f"Turn {i}\n\n")
                self.log.yview_moveto(1)
                self.outputbox.yview_moveto(1)
                self.root.update()

                move = first.calculate_move()
                if move == None:
                    raise ValueError
                first.addmoves([move])
                self.outputbox.insert("end",move + " ")  
                self.log.insert("end",f"Player 1 ({self.player_one}) moves {move}\n")   
                self.log.yview_moveto(1)

                self.root.update()

                last.setboard(first.boardstate)
                move = last.calculate_move()
                if move == None:
                    raise ValueError
                last.addmoves([move])
                self.outputbox.insert("end",move + " ")     
                first.setboard(last.boardstate)
                self.log.insert("end",f"Player 2 ({self.player_two}) moves {move}\n\n")   
                self.log.yview_moveto(1)

                self.root.update()
                i += 1
            except ValueError:
                break

        read = pgn.Reader(last.boardstate,str(f'{self.player_one} (depth {self.depth.get()})'),
        str(f'{self.player_two} (depth {self.depth.get()})'))

        self.log.insert("end", "\n\nGame over! PGN: \n")
        self.log.insert("end",str(read.get_pgn()))

        self.log.yview_moveto(1)
        self.outputbox.yview_moveto(1)

        self.root.update()


    def copyfunc(self):
        self.inputbox.delete("1.0","end-1c")
        self.inputbox.insert("end", self.outputbox.get("1.0","end-1c"))     

    def player_one_set(self, value:str): #options menu
        print(value)
        self.player_one = value
    def player_two_set(self,value:str): #options menu
        print(value)
        self.player_two = value


    def build(self):
        """Builds the main grid with coloured
            squares."""

        def maingrid():
            """Creates frame L,TR,BR"""
            self.topframe = ttk.Frame(self.root,width=1400,height=700,style='Frame0.TFrame')
            self.topframe.columnconfigure(0,weight=3)
            self.topframe.columnconfigure(1,weight=1)
            self.topframe.rowconfigure(0, weight=1)
            self.topframe.rowconfigure(1, weight=1)
            self.topframe.grid(row=0,column=0,sticky='news')

            self.frameL = ttk.Frame(self.topframe,width=800,height=700,style='Frame3.TFrame')

            self.frameTR = ttk.Frame(self.topframe,width=600,height=450,style='Frame2.TFrame')

            self.frameBR = ttk.Frame(self.topframe,width=600,height=250,style='Frame1.TFrame')

            self.frameL.grid(row=0,column=0,sticky = 'news',rowspan=2,padx=5,pady=5)

            self.frameTR.grid(row=1,column=1,sticky='news',padx=5,pady=5)

            self.frameBR.grid(row=0,column=1,sticky='news',pady=5,padx=5)

        def build_board():
            """Builds the board; pieces, tiles to the 
            beige section"""
            pass 

        def build_input_output():
            """Builds the input output á la original magachess 
            to the white section. Configures frame."""

            self.inputbox_title = tkinter.Label(self.frameL,text='Input game')
            self.inputbox_title.grid(row=0,column=0,sticky='NW')
            self.inputbox = scrolledtext.ScrolledText(self.frameL,wrap=WORD,width = 40, height=8)
            self.inputbox.grid(row=1,column=0,sticky="news")
            self.frameL.rowconfigure(0,weight=0)
            self.frameL.rowconfigure(1,weight=1)
            self.frameL.columnconfigure(0,weight=1)
            input = ["e2e4", "e7e6"]
            self.inputbox.insert("end",input)

            self.outputbox_title = tkinter.Label(self.frameL,text='Output')
            self.outputbox_title.grid(row=2,column=0,sticky='W')
            self.outputbox = scrolledtext.ScrolledText(self.frameL,wrap=WORD,width=40, height=8)
            self.outputbox.grid(row=3,column=0,sticky="news")
            self.frameL.rowconfigure(2,weight=0)
            self.frameL.rowconfigure(3,weight=1)

            self.log_title = tkinter.Label(self.frameL,text='Log')
            self.log_title.grid(row=2,column=1,sticky='W')
            self.log = scrolledtext.ScrolledText(self.frameL,wrap=WORD,width=20, height=8)
            self.log.grid(row=3,column=1,sticky="news")
            self.frameL.columnconfigure(1,weight=0)

            #buttons
            self.buttons = tkinter.Frame(self.frameL)
            self.buttons.grid(row=1,column=1,sticky='news')

            self.startbutton = tkinter.Button(self.buttons,text='   Start   ',width=13,command = lambda: self.startfunc())
            self.startbutton.grid(row=0,column=1,sticky='E')
            self.startbutton_title = tkinter.Label(self.buttons,text='Simulate moves: ')
            self.startbutton_title.grid(row=0,column=0,sticky='W')

            self.startbutton_title = tkinter.Label(self.buttons,text='')
            self.startbutton_title.grid(row=1,column=0,sticky='W')

            self.howmanymoves_title = tkinter.Label(self.buttons,text='Turns (2 moves): ')
            self.howmanymoves_title.grid(row=2,column=0,sticky='W')
            self.howmanymoves = tkinter.Entry(self.buttons, width=2)
            self.howmanymoves.insert("end","5")
            self.howmanymoves.grid(row=2,column=1)

            self.depth_title = tkinter.Label(self.buttons,text='Depth: ')
            self.depth_title.grid(row=3,column=0,sticky='W')
            self.depth = tkinter.Entry(self.buttons, width=2)
            self.depth.insert("end","20")
            self.depth.grid(row=3,column=1)
            
            self.startbutton_title = tkinter.Label(self.buttons,text='')
            self.startbutton_title.grid(row=4,column=0,sticky='W')

                #options menu

            options = ['stockfish 8','stockfish 15']

                #White
            self.White_title = tkinter.Label(self.buttons,text='First: ')
            self.White_title.grid(row=5,column=0,sticky='W')
            tkvargW = StringVar(self.root)
            tkvargW.set(options[0])
            self.White = tkinter.OptionMenu(self.buttons,tkvargW,*options,command=lambda sfversion = tkvargW:self.player_one_set(sfversion))
            self.White.grid(row=5, column=1,sticky='E')        
            self.White.config(width=10)

                #Black
            self.Black_title = tkinter.Label(self.buttons,text='Second: ')
            self.Black_title.grid(row=6,column=0,sticky='W')
            tkvargB = StringVar(self.root)
            tkvargB.set(options[1])
            self.Black = tkinter.OptionMenu(self.buttons,tkvargB,*options,command = lambda sfversion = tkvargB:self.player_two_set(sfversion))
            self.Black.grid(row=6, column=1,sticky='E') 
            self.Black.config(width=10)

            self.copybutton = tkinter.Button(self.buttons,text='   Copy!   ',width=13,command = lambda: self.copyfunc())
            self.copybutton.grid(row=7,column=1,sticky='E')
            self.copybutton_title = tkinter.Label(self.buttons,text='Copy the game: ')
            self.copybutton_title.grid(row=7,column=0,sticky='W')

            self.buttons.rowconfigure(0,weight=1)
            self.buttons.rowconfigure(1,weight=1)
            self.buttons.rowconfigure(2,weight=0)
            self.buttons.rowconfigure(3,weight=1)
            self.buttons.rowconfigure(4,weight=0)
            self.buttons.rowconfigure(5,weight=1)
            self.buttons.rowconfigure(6,weight=1)
            self.buttons.rowconfigure(7,weight=1)
            self.buttons.columnconfigure(0,weight=1)
            self.buttons.columnconfigure(1,weight=1)

        def build_settings():
            """Builds the settings menu to the 
            red corner"""
            pass

        maingrid()
        build_input_output()

def run():
    app = App()
    app.root.mainloop()

run()
