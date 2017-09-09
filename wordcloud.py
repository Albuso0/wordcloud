import re, string, operator
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import random
from tools import Counter, Box
import os




        
class Canvas():
    def __init__(self, height=1, width=1):
        self.canvas = Box(0,0, width, height)
        self.boxes = []

    def find_position(self, lx, ly, tstep = 0.1, rstep = 5):
        """
        input: box size lx and ly
        output: (position x, y, rotate)
        """
        centerX = 0.5*self.canvas.w
        centerY = 0.5*self.canvas.h
        r = 0
        theta = 0
        # theta = random.uniform(0, 2*math.pi) # or random(start,stop[,step])
        
        while True:
            if r > 0.5*min(self.canvas.w, self.canvas.h):
                print("Warning: no position available!")
                return (-1,-1,False)
            
            X = centerX + r * math.cos(theta)
            Y = centerY + r * math.sin(theta)
            

            b = Box(X-0.5*lx, Y-0.5*ly, lx, ly)
            if b.inside(self.canvas) and (not b.overlap_any(self.boxes)):
                return (b.x, b.y, False)
            
            b = Box(X-0.5*ly, Y-0.5*lx, ly, lx) # b_rotate
            if b.inside(self.canvas) and (not b.overlap_any(self.boxes)):
                return (b.x, b.y, True)

            theta += tstep
            if theta > 2*math.pi:
                theta -= 2*math.pi
                r += rstep

    def add(self,b):
        self.boxes.append(b)
        


def tokenize(word):
    word = word.lower() # to lower case
    word = word.translate({ord(c): None for c in string.punctuation})  # remove punctuations
    word = word.translate({ord(c): None for c in string.digits})  # remove numbers
    # word = word.translate({ord(c): for c in selectwords}) # only take words in word_to_use？
    return word






from PIL import Image, ImageFont, ImageDraw, ImageEnhance
class WordCloud(object):
    def __init__(self,
                 font_path="DroidSansMono.ttf",
                 max_words=100,
                 max_size=100, min_size=10,
                 width=1000, height=1000,
                 save_file="test.jpg",
                 stopwords="stopwords", passwords=None,
                 verbose=False):
        """
        Object to generate word cloud

        Args:
        font_path: string
        path to the font to be used

        max_words: int
        max number of words to shown in word cloud

        max_size, min_size: int
        maximum and minimum font size

        width, height: int
        size of the entire canvas

        save_file: string
        filename of the saved picture

        stopwords: string
        name of file that contains STOPWORDS

        passwords: string
        name of file that contains PASSWORDS (only use those words)

        verbose: bool
        if verbose=True, will print on screen
        
        """
        self.font_path = font_path
        self.max_words = max_words
        self.max_size = max_size
        self.min_size = min_size
        self.width = width
        self.height = height
        self.save_file = save_file


        self.stopwords = stopwords
        self.passwords = passwords
        self.verbose = verbose


        
    def pre_process(self,words):
        '''
        words pre-processing
        
        R text process refs: https://cran.r-project.org/web/packages/tm/tm.pdf
        Python package: NLTK (but a heavy package)
        '''

        words = [tokenize(word) for word in words] 
        if self.stopwords != None:
            STOPWORDS = set([x.strip() for x in open(self.stopwords).read().split('\n')])
            words = [word for word in words if word not in STOPWORDS] # remove STOPWORDS
        if self.passwords != None:
            PASSWORDS = set([x.strip() for x in open(self.passwords).read().split('\n')])
            words = [word for word in words if word in PASSWORDS] # only allow PASSWORDS
    
        return words

    
    def plot(self,filename):
        text = read_file(filename)
        words = text_to_words(text)
        words = self.pre_process(words)
        freq = words_to_freq(words)
        self.plot_from_freq(freq)


        
    def plot_from_freq(self,freq):
        '''
        
        R world cloud refs: https://cran.r-project.org/web/packages/wordcloud/wordcloud.pdf
        
        '''
        if len(freq) <= 0:
            raise ValueError("We need at least 1 word to plot a word cloud, "
                             "got %d." % len(freq))
        
        freq = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
        freq = freq[:self.max_words]
        max_freq = float(freq[0][1])


        canvas = Canvas(self.width,self.height)                           # an empty canvas
        img_color = Image.new("RGB", (self.width, self.height))           # handler to a colored image
        draw = ImageDraw.Draw(img_color)                                  # tool to draw on img_colord
        draw.rectangle(((0, 0), (self.width, self.height)), fill="white") # initial fill with white
        
        for word, f in freq:
            f_normalize = f/max_freq # normalize frequency

            # compute word size. Possibly other ways, for example, using relative_scaling
            size = (self.max_size - self.min_size) * f_normalize + self.min_size
        
            # get (lx,ly) from (word, size, [font])
            font = ImageFont.truetype(self.font_path, int(size))
            lx,ly = draw.textsize(word, font = font)

            # find (x,y,rotation) from (lx,ly). return x=-1 if failed
            x,y,rotation = canvas.find_position(lx,ly)

            if self.verbose:
                print(x,y,lx,ly,rotation)

            if x<0:
                continue
            # plot word on x,y with rotation    
            if (not rotation):
                draw.text((x,y), word, font = font, fill = (random.randint(0,255),random.randint(0,255),random.randint(0,255),0))
                canvas.add(Box(x,y,lx,ly))
            else:
                font = ImageFont.TransposedFont(font, orientation=Image.ROTATE_90)
                draw.text((x,y), word, font = font, fill = (random.randint(0,255),random.randint(0,255),random.randint(0,255),0))
                canvas.add(Box(x,y,ly,lx))
            
        img_color.save(self.save_file)



def read_file(filename):
    return open(filename).read()

def text_to_words(text):
    return text.split()

def words_to_freq(words):
    freq = Counter()
    for word in words:
        freq[word] += 1
    return freq
