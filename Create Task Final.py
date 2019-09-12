from Tkinter import *
import ttk
import random
import time
import os.path


class gameHome:
    def __init__(self, master):

        # Hides the master window
        master.withdraw()

        # initialize variables
        self.gameName = 'Memory Challenge'
        self.defaultSleepTime = 3
        self.defaultLives = 5
        self.tileLimit = 4
        self.sleepTime = self.defaultSleepTime
        self.livesRemaining = self.defaultLives
        self.roundNumber = 0
        self.score = 0
        self.colorChoices = ('Blue', 'Green', 'Orange', 'Purple', 'Red')
        self.colorName = []
        self.shapeChoices = ('Circle', 'Diamond', 'Square', 'Star', 'Triangle')
        self.shapeName = []
        self.tileNumberPrefixes = ('first', 'second', 'third', 'fourth', 'fifth')
        self.questionType = ('color', 'shape')
        self.userName = ""
        self.scoreList = []
        self.countLesserScores = 0
        self.countTotalScores = 0
        self.countTotalScoreSum = 0
        self.highScorePlayerLabels = []  # list of the widgets containing the high score player names
        self.highScoreRoundLabels = []  # list of canvas labels containing the Round values
        self.highScoreScoreLabels = []  # list of canvas labels containing the High Score values
        self.finishPlace = 6  # initialize out of top 5 list to start

        # Default Geometry Points are based on 50pixel canvas with default 8 pixel padding
        # padding can be removed by subtracting 8 from all numbers and then canvas will be 34 pixels
        # scale accordingly
        self.base50ptCircleGeometry = (8, 8, 42, 42)  # defines bounding square
        self.base50ptDiamondGeometry = (25, 8, 36, 25, 25, 42, 14, 25)
        self.base50ptSquareGeometry = (8, 8, 42, 42)
        self.base50ptStarGeometry = (
        25, 8, 29.2, 20.71, 42, 20.99, 31.8, 29.12, 35.51, 42, 25, 34.31, 14.49, 42, 18.2, 29.12, 8, 20.99, 20.8, 20.71)
        self.base50ptTriangleGeometry = (25, 8, 42, 42, 8, 42)
        self.gameTileScale = 6.0
        self.gameTileCircleGeometry = [self.gameTileScale * x for x in self.base50ptCircleGeometry]
        self.gameTileDiamondGeometry = [self.gameTileScale * x for x in self.base50ptDiamondGeometry]
        self.gameTileSquareGeometry = [self.gameTileScale * x for x in self.base50ptSquareGeometry]
        self.gameTileStarGeometry = [self.gameTileScale * x for x in self.base50ptStarGeometry]
        self.gameTileTriangleGeometry = [self.gameTileScale * x for x in self.base50ptTriangleGeometry]

        # Define ttk styles
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 12), foreground="black", background="gray")
        self.style.configure('Correct.TButton', font=('Arial', 14, 'bold'), foreground="green", background="green")
        self.style.configure('Incorrect.TButton', font=('Arial', 10, 'bold'), foreground="red", background="red")
        self.style.configure('MainButtons.TButton', font=('Arial', 18, 'bold'), foreground="black", background="black")
        self.style.configure('SmallButtons.TButton', font=('Arial', 8), foreground="black", background="black")
        self.style.configure('TFrame', background='#CCFFFF')
        self.style.configure('TLabel', background='#CCFFFF', font=('Arial', 11))

        # Create Home Window, Frame, and Widgets
        self.windowHome = Toplevel(master)
        self.middleScreen = str(int((self.windowHome.winfo_screenwidth() - 640) / 2)) + "+" + str(
            int((self.windowHome.winfo_screenheight() - 440) / 2))
        self.windowHome.geometry("640x480+" + self.middleScreen)
        self.windowHome.title('Create Task - ' + self.gameName + ' - Home Screen')
        self.windowHome.resizable(False, False)

        self.frameHome = ttk.Frame(self.windowHome)
        self.frameHome.place(x=2, y=2)
        self.frameHome.config(height=476, width=636)

        self.playButton = ttk.Button(self.frameHome, text='Play', command=self.play)
        self.playButton.place(relx=.3, rely=.7, anchor='center')
        self.playButton.config(style='MainButtons.TButton', state='disabled')

        self.howToPlayButton = ttk.Button(self.frameHome, text='How To Play', style='gameButtons.TButton',
                                          command=self.howToPlay)
        self.howToPlayButton.place(relx=.7, rely=.7, anchor='center')
        self.howToPlayButton.config(style='MainButtons.TButton')

        self.saveNameButton = ttk.Button(self.frameHome, text='Save', style='SmallButtons.TButton', width=4,
                                         command=self.saveName)
        self.saveNameButton.place(relx=.38, rely=.95, anchor='sw')

        self.exitHomeButton = ttk.Button(self.frameHome, text='Exit', command=master.destroy)
        self.exitHomeButton.place(relx=.95, rely=.95, anchor='se')

        self.homeTitle = ttk.Label(self.frameHome, text=self.gameName, font=('Arial', 40, 'bold'))
        self.homeTitle.place(relx=.5, rely=.3, anchor='center')

        self.homeUserNameInstruction = ttk.Label(self.frameHome, text='Enter your name below in order to begin',
                                                 font=('Arial', 10))
        self.homeUserNameInstruction.place(relx=.3, rely=.8, anchor='sw')

        self.homeUserNamePrompt = ttk.Label(self.frameHome, text='Type your name in the box below', font=('Arial', 10))
        self.homeUserNamePrompt.place(relx=.05, rely=.9, anchor='sw')

        self.userNameEntryHome = ttk.Entry(self.frameHome, width=33)
        self.userNameEntryHome.place(relx=.05, rely=.95, anchor='sw')
        self.userNameEntryHome.focus()
        # Bind the enter key for the user name entry field so that it will trigger the save button event if they hit enter
        self.userNameEntryHome.bind("<Return>", self.enterKeyPressed)
        
        '''
        Alternate code to load logo from file - replaced with dynamic construction of logo
        which makes the program self sufficient and with a better quality logo
        '''
        
        """
        self.logo = PhotoImage(file = 'Images\LogoSmall.gif')
        self.logoLabel = ttk.Label(self.frameHome, image = self.logo)
        self.logoLabel.place (relx = .02, rely = .02, anchor = 'nw')
        self.logoLabel2 = ttk.Label(self.frameHome, image = self.logo)
        self.logoLabel2.place (relx = .98, rely = .02, anchor = 'ne')
        """

        self.logoCanvas1 = Canvas(self.frameHome)
        self.logoCanvas1.config(width=50, height=50, bd=0, highlightthickness=0, relief='flat', bg='#CCFFFF')
        self.logoCanvas1.place(x=10, y=10)
        self.constructLogo(self.logoCanvas1, 50)

        self.logoCanvas2 = Canvas(self.frameHome)
        self.logoCanvas2.config(width=50, height=50, bd=0, highlightthickness=0, relief='flat', bg='#CCFFFF')
        self.logoCanvas2.place(x=625, y=10, anchor='ne')
        self.constructLogo(self.logoCanvas2, 50)

        # Create HowToPlay Window, Frame, and Widgets
        self.windowHowToPlay = Toplevel(master)
        self.windowHowToPlay.state('withdrawn')
        self.windowHowToPlay.geometry("640x480+" + self.middleScreen)
        self.windowHowToPlay.title('Create Task - ' + self.gameName + ' - How To Play')
        self.windowHowToPlay.resizable(False, False)

        self.frameHowToPlay = ttk.Frame(self.windowHowToPlay)
        self.frameHowToPlay.place(x=2, y=2)
        self.frameHowToPlay.config(height=476, width=636, borderwidth=2)

        self.returnHomeButton = ttk.Button(self.frameHowToPlay, text='Return Home', style='gameButtons.TButton',
                                           command=self.returnHome)
        self.returnHomeButton.place(relx=.05, rely=.95, anchor='sw')
        self.returnHomeButton.config(style='MainButtons.TButton')

        self.exitHowToPlayButton = ttk.Button(self.frameHowToPlay, text='Exit', style='gameButtons.TButton',
                                              command=master.destroy)
        self.exitHowToPlayButton.place(relx=.95, rely=.95, anchor='se')

        self.howToPlayTitle = ttk.Label(self.frameHowToPlay, text='How to Play ' + self.gameName,
                                        font=('Arial', 24, 'bold'))
        self.howToPlayTitle.place(relx=.5, rely=.1, anchor='center')

        self.logoCanvas3 = Canvas(self.frameHowToPlay)
        self.logoCanvas3.config(width=50, height=50, bd=0, highlightthickness=0, relief='flat', bg='#CCFFFF')
        self.logoCanvas3.place(x=10, y=10)
        self.constructLogo(self.logoCanvas3, 50)

        self.logoCanvas4 = Canvas(self.frameHowToPlay)
        self.logoCanvas4.config(width=50, height=50, bd=0, highlightthickness=0, relief='flat', bg='#CCFFFF')
        self.logoCanvas4.place(x=625, y=10, anchor='ne')
        self.constructLogo(self.logoCanvas4, 50)

        # help text construction moved to a method to save space here
        self.constructHelpText()

        # Create the Play Window, Frame and Widgets
        self.windowPlay = Toplevel(master)
        self.windowPlay.state('withdrawn')
        self.windowPlay.geometry("640x480+" + self.middleScreen)
        self.windowPlay.title('Create Task - ' + self.gameName + ' - Let\'s Play!')
        self.windowPlay.resizable(False, False)

        self.framePlay = ttk.Frame(self.windowPlay)
        self.framePlay.place(x=2, y=2)
        self.framePlay.config(height=476, width=636, borderwidth=2)

        self.returnHomeFromPlayButton = ttk.Button(self.framePlay, text='Return Home', style='gameButtons.TButton',
                                                   command=self.returnHome)
        self.returnHomeFromPlayButton.place(relx=.05, rely=.95, anchor='sw')

        self.exitPlayButton = ttk.Button(self.framePlay, text='Exit', style='gameButtons.TButton',
                                         command=master.destroy)
        self.exitPlayButton.place(relx=.95, rely=.95, anchor='se')

        self.readyButton = ttk.Button(self.framePlay, text='Ready!', style='gameButtons.TButton', command=self.ready)
        self.readyButton.place(relx=.5, rely=.95, anchor='s')
        self.readyButton.config(style='MainButtons.TButton')

        self.startLabel = ttk.Label(self.framePlay, text='Press the Ready button to start!', font=('Arial', 12))
        self.startLabel.place(relx=.5, rely=.5, anchor='center')

        self.helloPlay = ttk.Label(self.framePlay, text=('Hello ' + self.userName), foreground='blue',
                                   font=('Arial', 11))
        self.helloPlay.place(relx=.5, rely=.2, anchor='center')

        self.scoreLabel = ttk.Label(self.framePlay, text='Score: ' + str(self.score), font=('Arial', 24, 'bold'))
        self.scoreLabel.place(relx=.98, rely=.07, anchor='ne')

        self.scoreCanvas = Canvas(self.framePlay)
        self.scoreCanvas.config(width=152, height=92, bd=0, highlightthickness=0, relief='flat', bg='#CCFFFF')
        self.scoreCanvas.place(x=8, y=8)

        self.scoreCanvas.create_rectangle(0, 0, 150, 90, outline='black', fill='white')
        self.scoreCanvas.create_line(0, 30, 150, 30, fill='black')
        self.scoreCanvas.create_line(0, 60, 150, 60, fill='black')
        self.scoreCanvas.create_line(110, 0, 110, 90, fill='black')

        self.scoreCanvas.create_text(5, 15, anchor='w', text='Round', font=('Arial', 10))
        self.roundsLabel = self.scoreCanvas.create_text(130, 15, anchor='center', text=str(self.roundNumber),
                                                        fill='black', font=('Arial', 10))
        self.scoreCanvas.create_text(5, 45, anchor='w', text='Display Time (s)', font=('Arial', 10))
        self.timeLabel = self.scoreCanvas.create_text(130, 45, anchor='center', text=str(round(self.sleepTime, 3)),
                                                      fill='black', font=('Arial', 10))
        self.scoreCanvas.create_text(5, 75, anchor='w', text='Lives Remaining', font=('Arial', 10))
        self.livesLabel = self.scoreCanvas.create_text(130, 75, anchor='center', text=str(self.livesRemaining),
                                                       fill='red', font=('Arial', 10, 'bold'))

        # Create the Game Over Window, Frame and Widgets
        self.windowGameOver = Toplevel(master)
        self.windowGameOver.state('withdrawn')
        self.windowGameOver.geometry("640x480+" + self.middleScreen)
        self.windowGameOver.title('Create Task - ' + self.gameName + ' - Game Over')
        self.windowGameOver.resizable(False, False)

        self.frameGameOver = ttk.Frame(self.windowGameOver)
        self.frameGameOver.place(x=2, y=2)
        self.frameGameOver.config(height=476, width=636, borderwidth=2)

        self.gameOverTitle = ttk.Label(self.frameGameOver, text='Game Over', font=('Arial', 48, 'bold', 'italic'))
        self.gameOverTitle.place(relx=.5, rely=.1, anchor='center')

        self.exitGameOverButton = ttk.Button(self.frameGameOver, text='Exit', style='gameButtons.TButton',
                                             command=master.destroy)
        self.exitGameOverButton.place(relx=.95, rely=.95, anchor='se')

        self.playAgainGameOverButton = ttk.Button(self.frameGameOver, text='Play Again', style='gameButtons.TButton',
                                                  command=self.playAgain)
        self.playAgainGameOverButton.place(relx=.95, rely=.85, anchor='se')

        self.logoCanvas5 = Canvas(self.frameGameOver)
        self.logoCanvas5.config(width=50, height=50, bd=0, highlightthickness=0, relief='flat', bg='#CCFFFF')
        self.logoCanvas5.place(x=10, y=10)
        self.constructLogo(self.logoCanvas5, 50)

        self.logoCanvas6 = Canvas(self.frameGameOver)
        self.logoCanvas6.config(width=50, height=50, bd=0, highlightthickness=0, relief='flat', bg='#CCFFFF')
        self.logoCanvas6.place(x=625, y=10, anchor='ne')
        self.constructLogo(self.logoCanvas6, 50)

        # On the Game Over Screen, create a canvas and widgets to create a table of top 5 scores
        self.topFiveScoreHeader = ttk.Label(self.frameGameOver, text=('Memory Challenge Leaderboard'),
                                            font=('Arial', 16))
        self.topFiveScoreHeader.place(relx=.5, rely=.29, anchor='s')

        self.highScoreHeight = 200
        self.highScoreRowHeight = 30  # make sure this is less than the total height/5!
        self.highScoreTitleHeight = (self.highScoreHeight - self.highScoreRowHeight * 5)
        self.highScoreWidth = 300
        self.highScoreCol1Width = 150
        self.highScoreCol2Width = 75  # again, make sure col 1 + col2 widths total less than the total width of the canvas
        self.highScoreCol3Width = self.highScoreWidth - self.highScoreCol1Width - self.highScoreCol2Width

        self.highScoreCanvas = Canvas(self.frameGameOver)
        self.highScoreCanvas.config(width=self.highScoreWidth + 2, height=self.highScoreWidth + 2, bd=0,
                                    highlightthickness=0, relief='flat',
                                    bg='#CCFFFF')  # 5 rows of 30, plus 50 for header and 2 for border
        self.highScoreCanvas.place(relx=.5, rely=.3, anchor='n')
        self.highScoreCanvas.create_rectangle(0, 0, self.highScoreWidth, self.highScoreHeight, outline='black',
                                              fill='white')
        self.highScoreCanvas.create_line(0, self.highScoreTitleHeight, self.highScoreWidth, self.highScoreTitleHeight,
                                         fill='black')
        for rownum in range(1, 5):
            rownumy = self.highScoreTitleHeight + 30 * rownum
            self.highScoreCanvas.create_line(0, rownumy, self.highScoreWidth, rownumy, fill='black')

        self.highScoreCanvas.create_line(self.highScoreCol1Width, 0, self.highScoreCol1Width, self.highScoreHeight,
                                         fill='black')
        self.highScoreCanvas.create_line(self.highScoreCol1Width + self.highScoreCol2Width, 0,
                                         self.highScoreCol1Width + self.highScoreCol2Width, self.highScoreHeight,
                                         fill='black')

        # Create High Score Column Labels
        self.gameOverPlayerName = self.highScoreCanvas.create_text(self.highScoreCol1Width / 2,
                                                                   self.highScoreTitleHeight / 2, anchor='center',
                                                                   text="Player Name", fill='black',
                                                                   font=('Arial', 12, 'bold'))
        self.gameOverRounds = self.highScoreCanvas.create_text(self.highScoreCol1Width + self.highScoreCol2Width / 2,
                                                               self.highScoreTitleHeight / 2, anchor='center',
                                                               text="Rounds", fill='black', font=('Arial', 12, 'bold'))
        self.gameOverRounds = self.highScoreCanvas.create_text(
            self.highScoreCol1Width + self.highScoreCol2Width + self.highScoreCol3Width / 2,
            self.highScoreTitleHeight / 2, anchor='center', text="Score", fill='black', font=('Arial', 12, 'bold'))

        # Create placeholder objects for later update with actual high scores
        for scoreRank in range(0, 5):
            self.highScorePlayerLabels.append(self.highScoreCanvas.create_text(5,
                                                                               self.highScoreTitleHeight + self.highScoreRowHeight * (
                                                                               scoreRank + .5), anchor='w',
                                                                               text="Player" + str(scoreRank + 1)))
            self.highScoreRoundLabels.append(
                self.highScoreCanvas.create_text(self.highScoreCol1Width + self.highScoreCol2Width / 2,
                                                 self.highScoreTitleHeight + self.highScoreRowHeight * (scoreRank + .5),
                                                 anchor='center', text="Rounds" + str(scoreRank + 1)))
            self.highScoreScoreLabels.append(
                self.highScoreCanvas.create_text(self.highScoreWidth - self.highScoreCol3Width / 2,
                                                 self.highScoreTitleHeight + self.highScoreRowHeight * (scoreRank + .5),
                                                 anchor='center', text="Score" + str(scoreRank + 1)))
        # print(self.highScorePlayerLabels)

        self.finishMessageLine1 = ttk.Label(self.frameGameOver, text=('Congratulations Line'), font=('Arial', 11))
        self.finishMessageLine1.place(relx=.05, rely=.8, anchor='sw')
        self.finishMessageLine2 = ttk.Label(self.frameGameOver, text=('Score Summary Line'), font=('Arial', 11))
        self.finishMessageLine2.place(relx=.05, rely=.85, anchor='sw')
        self.finishMessageLine3 = ttk.Label(self.frameGameOver, text=('Percentile Compare'), font=('Arial', 11))
        self.finishMessageLine3.place(relx=.05, rely=.9, anchor='sw')
        self.finishMessageLine4 = ttk.Label(self.frameGameOver, text=('Percentile Compare'), font=('Arial', 11))
        self.finishMessageLine4.place(relx=.05, rely=.95, anchor='sw')

    # Defines the different button commands
    
    def play(self):
        # print('Play Clicked!')
        self.windowHowToPlay.state('withdrawn')
        self.windowPlay.state('normal')
        self.windowHome.state('withdrawn')
        self.windowGameOver.state('withdrawn')
        self.windowPlay.attributes("-topmost", True)

    def howToPlay(self):
        # print('howToPlay Clicked!')
        self.windowHowToPlay.state('normal')
        self.windowPlay.state('withdrawn')
        self.windowHome.state('withdrawn')
        self.windowGameOver.state('withdrawn')
        self.windowHowToPlay.attributes("-topmost", True)

    def saveName(self):
        # print('saveName Clicked')
        self.userName = self.userNameEntryHome.get().capitalize()
        # print(self.userName)
        self.playButton.config(state='enabled')
        self.homeUserNameInstruction.place_forget()
        self.helloPlay.config(text='Hello ' + self.userName)

    def returnHome(self):
        # print('returnHome Clicked!')
        self.windowHowToPlay.state('withdrawn')
        self.windowPlay.state('withdrawn')
        self.windowHome.state('normal')
        self.windowGameOver.state('withdrawn')
        self.windowHome.attributes("-topmost", True)

    def ready(self):
        # print('Ready! Clicked!')
        self.windowHowToPlay.state('withdrawn')
        self.windowPlay.state('normal')
        self.windowHome.state('withdrawn')
        self.windowGameOver.state('withdrawn')
        self.windowPlay.attributes("-topmost", True)
        self.readyButton.place_forget()
        self.startLabel.place_forget()
        self.returnHomeFromPlayButton.place_forget()
        self.initiateRound()

    # Reinitializes the game variables in order to allow the user to play again
    def playAgain(self):
        # print('Play Again Clicked!')
        self.readyButton.place(relx=.5, rely=.95, anchor='s')
        self.readyButton.config(text='Ready!')
        self.startLabel.place(relx=.5, rely=.5, anchor='center')
        self.answerButton0.place_forget()
        self.answerButton1.place_forget()
        self.answerButton2.place_forget()
        self.answerButton3.place_forget()
        self.answerButton4.place_forget()
        self.scoreLabel.focus()
        self.questionLabel.place_forget()
        self.sleepTime = self.defaultSleepTime
        self.livesRemaining = self.defaultLives
        self.roundNumber = 0
        self.score = 0
        self.play()
        self.scoreList = []
        self.countLesserScores = 0
        self.countTotalScores = 0
        self.countTotalScoreSum = 0
        self.finishPlace = 6
        self.scoreCanvas.itemconfigure(self.livesLabel, text=str(self.livesRemaining))
        self.scoreCanvas.itemconfigure(self.roundsLabel, text=str(self.roundNumber))
        self.scoreCanvas.itemconfigure(self.timeLabel, text=str(round(self.sleepTime, 3)))
        self.scoreLabel.config(text='Score: ' + str(self.score))

    def enterKeyPressed(self, event):
        # print('Enter Key Pressed in User Name entry field')
        self.saveName()

    # Used to show configure the How to Play window
    def constructHelpText(self):
        self.helpTextList = ('1. Save your name on the Home screen and click Play.', '',
                             '2. Click Ready once you are ready to play the game.', '',
                             '3. Attempt to memorize the series of shapes with various colors',
                             '   that will flash in front of you.', '',
                             '4. You will be asked 3 questions after each series of shapes',
                             '   to test how well you remember what you saw.', '',
                             '5. Questions may ask about either the shape or the color',
                             '   of an object.', '',
                             'Note: After each round your time shown per shape will be shortened',
                             '      so make sure you\'re ready')

        helpX = 20
        helpTopY = 100
        helpBotY = 380
        helpDeltaY = (helpBotY - helpTopY) / (len(self.helpTextList) - 1)
        helpLineCounter = 0
        for helpLines in self.helpTextList:
            lineYCoord = helpTopY + helpLineCounter * helpDeltaY
            myLabel = ttk.Label(self.frameHowToPlay, text=helpLines, font=('Consolas', 11))
            myLabel.place(x=helpX, y=lineYCoord, anchor='sw')
            helpLineCounter += 1

    # Keeps track of the lives and when they run out of lives switch to game over window
    def livesController(self):
        self.scoreCanvas.itemconfigure(self.livesLabel, text=str(self.livesRemaining))
        if self.livesRemaining == 0:
            time.sleep(.2)
            self.gameOver()

    # Checks to see if they got the answer correct by checking their answer with an index containing the correct answer
    def checkAnswer(self, ordinal):
        if self.activeQuestionType == 'color':
            self.correctOrdinal = self.colorChoices.index(self.colorName[self.activeTileNumber])
            # print('The answer is ' + self.colorName[self.activeTileNumber])
        else:
            self.correctOrdinal = self.shapeChoices.index(self.shapeName[self.activeTileNumber])
            # print('The answer is ' + self.shapeName[self.activeTileNumber])

        # print('The correct ordinal is ' + str(self.correctOrdinal))

        if ordinal == self.correctOrdinal:
            self.activeAnswerCorrect = True
        else:
            self.activeAnswerCorrect = False
            self.livesRemaining -= 1
            self.livesController()

        # print('The answer is correct?: ' + str(self.activeAnswerCorrect))
        # Makes the correct answer highlight green and if they got it wrong highlight the wrong button red
        if self.activeAnswerCorrect == True:
            self.score += self.roundNumber
            self.scoreLabel.config(text='Score: ' + str(self.score))
        else:
            if ordinal == 0:
                self.answerButton0.config(style='Incorrect.TButton')
                self.answerButton0.update()
            elif ordinal == 1:
                self.answerButton1.config(style='Incorrect.TButton')
                self.answerButton1.update()
            elif ordinal == 2:
                self.answerButton2.config(style='Incorrect.TButton')
                self.answerButton2.update()
            elif ordinal == 3:
                self.answerButton3.config(style='Incorrect.TButton')
                self.answerButton3.update()
            elif ordinal == 4:
                self.answerButton4.config(style='Incorrect.TButton')
                self.answerButton4.update()
        # Turns the correct button green no matter their choice
        if self.correctOrdinal == 0:
            self.answerButton0.config(style='Correct.TButton')
            self.answerButton0.update()
        elif self.correctOrdinal == 1:
            self.answerButton1.config(style='Correct.TButton')
            self.answerButton1.update()
        elif self.correctOrdinal == 2:
            self.answerButton2.config(style='Correct.TButton')
            self.answerButton2.update()
        elif self.correctOrdinal == 3:
            self.answerButton3.config(style='Correct.TButton')
            self.answerButton3.update()
        elif self.correctOrdinal == 4:
            self.answerButton4.config(style='Correct.TButton')
            self.answerButton4.update()
            
        # Makes sure they can't press any buttons multiple times after answering
        self.answerButton0.config(state='disabled')
        self.answerButton1.config(state='disabled')
        self.answerButton2.config(state='disabled')
        self.answerButton3.config(state='disabled')
        self.answerButton4.config(state='disabled')

        self.scoreLabel.focus()
        self.questionNumber += 1
        time.sleep(1)
        self.questionLabel.place_forget()
        
        # Calls the round controller function to run next round
        self.roundController()

    # Run to initilize variables only the first time playing the game
    def initiateRound(self):
        self.roundNumber += 1
        self.scoreCanvas.itemconfigure(self.roundsLabel, text=str(self.roundNumber))
        self.colorName = []
        self.shapeName = []
        self.questionRoundHistory = []
        if self.roundNumber == 1:
            self.gameCanvas = Canvas(self.framePlay)
            self.gameCanvas.config(width=300, height=300, bg='white')
        self.gameCanvas.place(x=168, y=104)
        self.defineRandomObjects()
        self.drawRandomObjects()
        if self.roundNumber == 1:
            self.constructAnswerButtons()
        self.placeAnswerButtons()
        self.questionNumber = 1
        self.roundController()

    # Keeps track of round functions and makes sure the round keeps running
    def roundController(self):
        if self.questionNumber < 4:
            self.askQuestions()
            self.configAnswerButtons()
        else:
            self.answerButton0.place_forget()
            self.answerButton1.place_forget()
            self.answerButton2.place_forget()
            self.answerButton3.place_forget()
            self.answerButton4.place_forget()
            self.readyButton.place(relx=.5, rely=.5, anchor='center')
            self.readyButton.config(text='Continue to Next Round')

    # Creates the random tiles and appends their characteristics into a list to be checked later
    def defineRandomObjects(self):
        for self.tileNumber in range(0, self.tileLimit):
            self.colorName.append(random.choice(self.colorChoices))
            self.shapeName.append(random.choice(self.shapeChoices))
            # print('Tile ' + str(self.tileNumber+1) + ': ' + self.colorName[self.tileNumber] + ' ' + self.shapeName[self.tileNumber])

    # Graphically creates the previously chosen random shapes and colors
    def drawRandomObjects(self):
        for self.tileNumber in range(0, self.tileLimit):
            self.activeShape = self.shapeName[self.tileNumber]
            self.activeColor = self.colorName[self.tileNumber]
            # print('Tile ' + str(self.tileNumber+1) + ': Starting If Statements')
            if self.activeShape == 'Circle':
                # print('Tile ' + str(self.tileNumber+1) + ': Circle was True')
                self.gameTile = self.gameCanvas.create_oval(self.gameTileCircleGeometry, outline='black',
                                                            fill=self.activeColor)
            elif self.activeShape == 'Square':
                # print('Tile ' + str(self.tileNumber+1) + ': Square was True')
                self.gameTile = self.gameCanvas.create_rectangle(self.gameTileSquareGeometry, outline='black',
                                                                 fill=self.activeColor)
            elif self.activeShape == 'Triangle':
                # print('Tile ' + str(self.tileNumber+1) + ': Triangle was True')
                self.gameTile = self.gameCanvas.create_polygon(self.gameTileTriangleGeometry, outline='black',
                                                               fill=self.activeColor)
            elif self.activeShape == 'Star':
                # print('Tile ' + str(self.tileNumber+1) + ': Star was True')
                self.gameTile = self.gameCanvas.create_polygon(self.gameTileStarGeometry, outline='black',
                                                               fill=self.activeColor)
            elif self.activeShape == 'Diamond':
                # print('Tile ' + str(self.tileNumber+1) + ': Diamond was True')
                self.gameTile = self.gameCanvas.create_polygon(self.gameTileDiamondGeometry, outline='black',
                                                               fill=self.activeColor)
            self.gameCanvas.update()
            time.sleep(self.sleepTime)
            self.gameCanvas.delete(self.gameTile)
            self.gameCanvas.update()
            time.sleep(0.2)

        #Sets a minimum value for sleep time
        if self.sleepTime > 0.5:
            self.sleepTime *= 0.95
            self.scoreCanvas.itemconfigure(self.timeLabel, text=str(round(self.sleepTime, 3)))
            # roundNumber
        self.gameCanvas.place_forget()

    # Generates the random questions based on the characteristics of the previous randomly generated shapes
    def askQuestions(self):
        while True:
            self.activeQuestionType = random.choice(self.questionType)
            self.activeTileNumber = random.randint(0, self.tileLimit - 1)
            self.QuestionIndex = str(self.activeTileNumber) + self.activeQuestionType
            if self.QuestionIndex not in self.questionRoundHistory:
                self.questionRoundHistory.append(str(self.activeTileNumber) + self.activeQuestionType)
                break
        self.activeQuestionPrefix = self.tileNumberPrefixes[self.activeTileNumber]
        self.questionText = 'What was the ' + self.activeQuestionType + ' of the ' + self.activeQuestionPrefix + ' object?'
        self.questionLabel = ttk.Label(self.framePlay, text=self.questionText, font=('Arial', 14))
        self.questionLabel.place(relx=.5, rely=.3, anchor='center')
        '''
        if self.activeQuestionType == 'color':
            print('The answer is ' + self.colorName[self.activeTileNumber])
        else:
            print('The answer is ' + self.shapeName[self.activeTileNumber])
        '''

    # Creates the button frames
    def constructAnswerButtons(self):
        self.answerButtonLabels = ['Answer0', 'Answer1', 'Answer2', 'Answer3', 'Answer4']
        self.answerButton0 = ttk.Button(self.framePlay, text=self.answerButtonLabels[0], style='gameButtons.TButton',
                                        command=lambda: self.checkAnswer(0))
        self.answerButton1 = ttk.Button(self.framePlay, text=self.answerButtonLabels[1], style='gameButtons.TButton',
                                        command=lambda: self.checkAnswer(1))
        self.answerButton2 = ttk.Button(self.framePlay, text=self.answerButtonLabels[2], style='gameButtons.TButton',
                                        command=lambda: self.checkAnswer(2))
        self.answerButton3 = ttk.Button(self.framePlay, text=self.answerButtonLabels[3], style='gameButtons.TButton',
                                        command=lambda: self.checkAnswer(3))
        self.answerButton4 = ttk.Button(self.framePlay, text=self.answerButtonLabels[4], style='gameButtons.TButton',
                                        command=lambda: self.checkAnswer(4))
        
    # Places the answer buttons when they are needed
    def placeAnswerButtons(self):
        self.gameCanvas.place_forget()
        self.answerButton0.place(relx=.35, rely=.5, anchor='center')
        self.answerButton1.place(relx=.65, rely=.5, anchor='center')
        self.answerButton2.place(relx=.2, rely=.7, anchor='center')
        self.answerButton3.place(relx=.5, rely=.7, anchor='center')
        self.answerButton4.place(relx=.8, rely=.7, anchor='center')

    # Chooses what text to put on each button depending on the question
    def configAnswerButtons(self):
        if self.activeQuestionType == 'color':
            self.answerButtonLabels = self.colorChoices
        else:
            self.answerButtonLabels = self.shapeChoices
        self.answerButton0.config(text=self.answerButtonLabels[0], style='TButton', state='enabled')
        self.answerButton1.config(text=self.answerButtonLabels[1], style='TButton', state='enabled')
        self.answerButton2.config(text=self.answerButtonLabels[2], style='TButton', state='enabled')
        self.answerButton3.config(text=self.answerButtonLabels[3], style='TButton', state='enabled')
        self.answerButton4.config(text=self.answerButtonLabels[4], style='TButton', state='enabled')

    # A function that can graphically and dynamically create the game logo based on a given height value and what canvas to put it on
    def constructLogo(self, logoCanvasName, canvasHeight):
        logoScale = canvasHeight / 50.0 / 2
        # create outline square
        logoCanvasName.create_rectangle(0, 0, canvasHeight - 1, canvasHeight - 1, outline='black', fill='#EEEEEE')
        logoCanvasName.create_line(0, canvasHeight / 2, canvasHeight - 1, canvasHeight / 2, fill='black')
        logoCanvasName.create_line(canvasHeight / 2, 0, canvasHeight / 2, canvasHeight - 1, fill='black')
        logoStarGeometry = [logoScale * x for x in self.base50ptStarGeometry]
        logoCanvasName.create_polygon(logoStarGeometry, outline='black', fill='blue')
        logoSquareGeometry = [logoScale * x for x in self.base50ptSquareGeometry]
        # shift square down by canvasHeight/2
        logoSquareGeometry = self.shiftCoords(False, True, canvasHeight / 2, logoSquareGeometry)
        logoCanvasName.create_rectangle(logoSquareGeometry, outline='black', fill='red')
        # shift triangle right by canvasHeight/2
        logoTriangleGeometry = [logoScale * x for x in self.base50ptTriangleGeometry]
        logoTriangleGeometry = self.shiftCoords(True, False, canvasHeight / 2, logoTriangleGeometry)
        logoCanvasName.create_polygon(logoTriangleGeometry, outline='black', fill='purple')
        # shift circle down and right by canvasHeight/2
        logoCircleGeometry = [logoScale * x for x in self.base50ptCircleGeometry]
        logoCircleGeometry = self.shiftCoords(True, True, canvasHeight / 2, logoCircleGeometry)
        logoCanvasName.create_oval(logoCircleGeometry, outline='black', fill='green')

    # A function that adjusts the x or y or both coordinates in coordList by shiftval amount
    #x and y will be shifted if the shiftxTF and/or shiftyTF parameters are set to true
    def shiftCoords(self, shiftxTF, shiftyTF, shiftval, coordList):
        if shiftxTF == True and shiftyTF == True:
            stepval = 1
        else:
            stepval = 2

        if shiftxTF == True:
            listStart = 0
        else:
            listStart = 1

        for i in range(listStart, len(coordList), stepval):
            coordList[i] += shiftval

        # print("coordList: " + str(coordList))

        return (coordList)

    # Runs when they run out of lives
    def gameOver(self):
        self.windowHowToPlay.state('withdrawn')
        self.windowPlay.state('withdrawn')
        self.windowHome.state('withdrawn')
        self.windowGameOver.state('normal')
        self.windowGameOver.attributes("-topmost", True)
        if not os.path.isfile("gamestats.txt"):
            # print("file does not exist")
            self.initializeStatisticsFile()
        fw = open("gamestats.txt", "a")
        fw.write(str(self.score) + "," + str(self.roundNumber) + "," + self.userName.strip() + "\n")
        fw.close()

        fr = open("gamestats.txt", "r")
        for line in fr:
            if len(line) > 3:
                lineList = []
                lineScore, lineRound, lineName = line.split(",")
                lineList.append(int(lineScore))
                lineList.append(int(lineRound))
                lineList.append(lineName[0:len(lineName) - 1])
                self.scoreList.append(lineList)
                self.countTotalScores += 1
                self.countTotalScoreSum += int(lineScore)
                if int(lineScore) < self.score:
                    self.countLesserScores += 1
        fr.close
        # print(self.scoreList)
        # print (str(self.countTotalScores))
        # print (str(self.countLesserScores))
        self.scorePercentile = 1 - (self.countLesserScores + 1) / self.countTotalScores
        self.averageScore = self.countTotalScoreSum / self.countTotalScores
        # print ('You beat ' + str(round((self.scorePercentile*100),2)) + '% of previous scores')
        # print ('The average score is ' + str(round(self.averageScore,2)))
        # print ('Your score was ' + str(self.score))
        self.scoreListSorted = sorted(self.scoreList, reverse=True)[0:5]
        # print(self.scoreListSorted)
        self.configureTopScores(self.scoreListSorted)

    # Runs if the user doesn't have a text file
    def initializeStatisticsFile(self):
        self.InitialStatistics = (
        (10, 3, 'Albert Einstein'), (8, 3, 'Monty Python'), (7, 3, 'Wolverine'), (4, 2, 'Spongebob Squarepants'),
        (1, 2, 'Rodney Dangerfield'))
        fwi = open("gamestats.txt", "w+")
        for initScore, initRound, initName in self.InitialStatistics:
            fwi.write(str(initScore) + "," + str(initRound) + "," + initName + "\n")
        fwi.close()

    # Highlights the users current score if they made it onto th leaderboard
    def configureTopScores(self, scoreList):
        # print(scoreList)
        # print(self.highScorePlayerLabels)
        # sample code to revise canvas items
        highlightcounter = 0
        #Grabs the top 5 scores out of the list of scores
        for lineNumber in range(0, 5):
            self.highScoreCanvas.itemconfigure(self.highScorePlayerLabels[lineNumber],
                                               text=str(scoreList[lineNumber][2]), font=('Arial', 10),
                                                   fill='black')
            self.highScoreCanvas.itemconfigure(self.highScoreRoundLabels[lineNumber],
                                               text=str(scoreList[lineNumber][1]), font=('Arial', 10),
                                                   fill='black')
            self.highScoreCanvas.itemconfigure(self.highScoreScoreLabels[lineNumber],
                                               text=str(scoreList[lineNumber][0]), font=('Arial', 10),
                                                   fill='black')

            if int(scoreList[lineNumber][0]) == int(self.score) and int(scoreList[lineNumber][1]) == int(
                    self.roundNumber) and str(scoreList[lineNumber][2]).strip() == str(
                    self.userName).strip() and highlightcounter == 0:
                # print('score line matches!')
                highlightcounter = 1
                self.finishPlace = lineNumber
                self.highScoreCanvas.itemconfigure(self.highScorePlayerLabels[lineNumber], font=('Arial', 14),
                                                   fill='blue')
                self.highScoreCanvas.itemconfigure(self.highScoreRoundLabels[lineNumber], font=('Arial', 14),
                                                   fill='blue')
                self.highScoreCanvas.itemconfigure(self.highScoreScoreLabels[lineNumber], font=('Arial', 14),
                                                   fill='blue')

        self.finishMessage = ''  # single message for the console
        if self.finishPlace >= 0 and self.finishPlace < 6:
            self.finishMessage = 'Congratulations you finished in ' + self.tileNumberPrefixes[
                self.finishPlace] + ' place!'
            self.finishMessageLine1.config(
                text='Congratulations you finished in ' + self.tileNumberPrefixes[self.finishPlace] + ' place!')
            
        # Performs some calculations on their score in order to show the user the statistics of their score
        else:
            self.finishMessageLine1.config(text='You did not make the leaderboard, better luck next time!')
        self.finishMessage += 'You scored ' + str(self.score) + '\n'
        self.finishMessage += 'You finished in the top ' + str(
            round((self.scorePercentile * 100), 2)) + ' percent of all users \n'
        self.finishMessageLine2.config(text='You scored ' + str(self.score) + '.')
        self.finishMessageLine3.config(
            text='You finished in the top ' + str(round((self.scorePercentile * 100), 2)) + '% of all users')

        # Runs this if the code is higher than average
        if self.score > self.averageScore:
            self.finishMessage += 'You beat the average score of ' + str(self.averageScore) + ' by ' + str(
                round(self.score - self.averageScore, 1)) + ' points!'
            self.finishMessageLine4.config(
                text='You beat the average score of ' + str(round(self.averageScore, 1)) + ' by ' + str(
                    round(self.score - self.averageScore, 1)) + ' points!')
        # Runs this if the code is not higher than average
        else:
            self.finishMessage += 'You did not quite reach the average score of ' + str(round(self.averageScore, 1))
            self.finishMessageLine4.config(
                text='You did not quite reach the average score of ' + str(round(self.averageScore)))

            # print(self.finishMessage)


# Main
def main():
    root = Tk()
    mainScreen = gameHome(root)
    root.mainloop()


if __name__ == "__main__": main()

