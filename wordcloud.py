import re, string, operator
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import random
from tools import Counter, Box


STOPWORDS = set([x.strip() for x in open('stopwords').read().split('\n')])
PASSWORDS = set([x.strip() for x in open('passwords').read().split('\n')])


        
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


def pre_process(words):
    '''
    words pre-processing

    R text process refs: https://cran.r-project.org/web/packages/tm/tm.pdf
    Python package: NLTK (but a heavy package)
    '''

    words = [tokenize(word) for word in words] # to lower case
    # words = [word for word in words if word not in STOPWORDS] # remove STOPWORDS
    words = [word for word in words if word in PASSWORDS] # only allow PASSWORDS
    
    return words




from PIL import Image, ImageFont, ImageDraw, ImageEnhance
def plot_from_freq(freq):
    freq = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
    freq = freq[:100]
    max_freq = float(freq[0][1])
    
    max_size = 100
    min_size = 10
    
    width = 1000
    height = 1000
    
    img_color = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img_color)
    
    draw.rectangle(((0, 0), (width, height)), fill="white")
    a = Canvas(width,height)
    rank = 1
    for word, f in freq:
        f_normalize = f/max_freq # normalize frequency
        size = (max_size - min_size) * f_normalize + min_size
        
        # f_normalize = rank -1 # draw by rank
        # size = max_size - (max_size - min_size)/100 * f_normalize
        rank = rank + 1
        # get (lx,ly) from (word, size, [font])
        # print(lx,ly)
        font = ImageFont.truetype("DroidSansMono.ttf", int(size))
        lx,ly = draw.textsize(word, font = font)

        # find (x,y,rotation) from (lx,ly)
        x,y,rotation = a.find_position(lx,ly)
        print(x,y,lx,ly,rotation)

        if x<0:
            continue
        # plot word on x,y with rotation    
        if (not rotation):
            draw.text((x,y), word, font = font, fill = (random.randint(0,255),random.randint(0,255),random.randint(0,255),0))
            a.add(Box(x,y,lx,ly))
        else:
            font = ImageFont.TransposedFont(font, orientation=Image.ROTATE_90)
            draw.text((x,y), word, font = font, fill = (random.randint(0,255),random.randint(0,255),random.randint(0,255),0))
            a.add(Box(x,y,ly,lx))
            
    img_color.save("tres_leches.jpg","JPEG")



class WordCloud(object):
    def __init__(self):
        return

    
    def plot(freq):
        '''
        
        R world cloud refs: https://cran.r-project.org/web/packages/wordcloud/wordcloud.pdf
        
        '''


def read_file(filename):
    return open(filename).read()

def text_to_words(text):
    return text.split()

def words_to_freq(words):
    freq = Counter()
    for word in words:
        freq[word] += 1
    return freq
