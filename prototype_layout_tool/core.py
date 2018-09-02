import math
import csv
import textwrap
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

# anchors are center of of each card
# 3x3 poker cards on 8.5"x11" paper
POKER_9 = {'card_dim' : (2.5*inch, 3.5*inch),
           'anchors' : [(1.75, 9)  , (4.25, 9)  , (6.75, 9),
                        (1.75, 5.5), (4.25, 5.5), (6.75, 5.5),
                        (1.75, 2)  , (4.25, 2)  , (6.75, 2)],
           'card_rots' : [0,0,0,0,0,0,0,0,0]}
POKER_9['anchors'] = [(inch*a[0], inch*a[1]) for a in POKER_9['anchors']]

POKER_L = {'card_dim' : (3.5*inch, 2.5*inch),
           'anchors' : [(1.75, 9)  , (4.25, 9)  , (6.75, 9),
                        (1.75, 5.5), (4.25, 5.5), (6.75, 5.5),
                        (1.75, 2)  , (4.25, 2)  , (6.75, 2)],
           'card_rots' : [90,90,90,90,90,90,90,90,90]}
POKER_L['anchors'] = [(inch*a[0], inch*a[1]) for a in POKER_L['anchors']]

# 4x2 poker cards on 8.5"x11" paper
POKER_8 = {'card_dim' : (2.5*inch, 3.5*inch),
           'anchors' : [(2.5, 9.25), (6, 9.25),
                        (2.5, 6.75), (6, 6.75),
                        (2.5, 4.25), (6, 4.25),
                        (2.5, 1.75), (6, 1.75)],
           'card_rots' : [-90, 90, -90, 90, -90, 90, -90, 90]}
POKER_8['anchors'] = [(inch*a[0], inch*a[1]) for a in POKER_8['anchors']]

BRIDGE = {'card_dim' : (2.25*inch, 3.5*inch),
          'anchors' : [(2, 9)  , (4.25, 9)  , (6.5, 9),
                       (2, 5.5), (4.25, 5.5), (6.5, 5.5),
                       (2, 2)  , (4.25, 2)  , (6.5, 2)],
          'card_rots' : [0,0,0,0,0,0,0,0,0]}
BRIDGE['anchors'] = [(inch*a[0], inch*a[1]) for a in BRIDGE['anchors']]

TAROT = {'card_dim' : (2.75*inch, 4.75*inch),
         'anchors' : [(1.875, 7.875), (1.875, 3.125),
                      (5.625, 8.25), (5.625, 5.5), (5.625, 2.75)],
         'card_rots' : [0, 0, 90, 90, 90]}
TAROT['anchors'] = [(inch*a[0], inch*a[1]) for a in TAROT['anchors']]

JUMBO = {'card_dim' : (3.34090909*inch, 5.25*inch),
         'anchors' : [(2.5795455, 8.125), (5.9204546, 8.125),
                      (2.5795455, 2.875), (5.9204546, 2.875)],
         'card_rots' : [0, 0, 0, 0]}
JUMBO['anchors'] = [(inch*a[0], inch*a[1]) for a in JUMBO['anchors']]

JUMBO_L = {'card_dim' : (3.34090909*inch, 5.25*inch),
           'anchors' : [(2.5795455, 8.125), (5.9204546, 8.125),
                        (2.5795455, 2.875), (5.9204546, 2.875)],
           'card_rots' : [90, 90, 90, 90]}
JUMBO_L['anchors'] = [(inch*a[0], inch*a[1]) for a in JUMBO_L['anchors']]

SQUARE_4_INCH = {'card_dim' : (4*inch, 4*inch),
                'anchors' : [(2.25, 7.5), (6.25, 7.5),
                             (2.25, 3.5), (6.25, 3.5)],
                'card_rots' : [0,0,0,0]}
SQUARE_4_INCH['anchors'] = [(inch*a[0], inch*a[1]) for a in SQUARE_4_INCH['anchors']]

SQUARE_2_INCH = {
    'card_dim' : (2*inch, 2*inch),
    'anchors' : [(1.25,9.5), (3.25,9.5), (5.25,9.5), (7.25,9.5),
                 (1.25,7.5), (3.25,7.5), (5.25,7.5), (7.25,7.5),
                 (1.25,5.5), (3.25,5.5), (5.25,5.5), (7.25,5.5),
                 (1.25,3.5), (3.25,3.5), (5.25,3.5), (7.25,3.5),
                 (1.25,1.5), (3.25,1.5), (5.25,1.5), (7.25,1.5)],
    'card_rots' : [0]*20}
SQUARE_2_INCH['anchors'] = [(inch*a[0], inch*a[1]) for a in SQUARE_2_INCH['anchors']]

def read_specs(spec_filename):
    with open(spec_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        specs = [row for row in reader]

    card_list = []
    line_list = []
    rect_list = []
    section_specs = []
    bg_image = None
    for spec in specs:
        print(spec)
        if spec[0] == '' or spec[0][0] == '#': continue
        elif spec[0] == 'layout':
            layout = eval(spec[1].upper())
        elif spec[0] == 'bg_image':
            bg_image = spec[1]
        elif spec[0] == 'no_bg_image':
            bg_image = None
        elif spec[0] == 'lines':
            for l in spec[1:]:
                if not l: continue
                line_list.append(eval(l))
        elif spec[0] == 'rects':
            for r in spec[1:]:
                if not r: continue
                rect_list.append(eval(r))
        elif spec[0] == 'text':
            section_specs = []
            for i in range(1,len(spec)):
                if not spec[i]: continue
                section_specs.append(eval(spec[i]))
        else:
            num_copies = eval(spec[0])
            section_list = []
            for i in range(1, len(section_specs)+1):
                if not spec[i]: continue
                section_list.append(Section(
                    spec[i],
                    section_specs[i-1])
                )
            for i in range(num_copies):
                card_list.append(
                    Card(layout['card_dim'],
                         bg_image,
                         section_list,
                         line_list,
                         rect_list)
                )
    return (card_list, layout)
                

def draw_cards(card_list, filename, layout):
    num_cards = len(card_list)
    cards_per_sheet = len(layout['anchors'])
    num_pages = math.ceil(num_cards / cards_per_sheet)

    c = canvas.Canvas(filename, pagesize=letter)
    c.setStrokeColorRGB(0,0,0)
    for i in range(num_pages):
        for j in range(cards_per_sheet):
            if i*cards_per_sheet + j > num_cards - 1:
                break
            card = card_list[i*cards_per_sheet + j]
            card.draw(c, layout['anchors'][j], layout['card_rots'][j])
        c.showPage()
    c.save()


class Card(object):
    def __init__(self, dim, bg_image=None,
                 section_list=(), line_list=(), rect_list=()):
        self.dim = dim
        self.bg_image = bg_image
        self.section_list = section_list
        self.line_list = line_list
        self.rect_list = rect_list

    def draw(self, c, anchor, rot):
        c.saveState()

        # translate and rotate
        c.translate(*anchor)
        #c.translate(*[x/2 for x in self.dim])
        c.rotate(rot)
        c.translate(*[-x/2 for x in self.dim])

        # draw background image
        if self.bg_image:
            c.drawImage(self.bg_image, 0, 0, *self.dim)
            
        # draw lines
        for line in self.line_list:
            line_abs = [d*l for d,l in zip(self.dim*2, line)]
            c.line(*line_abs)

        # draw rectangles
        for rect in self.rect_list:
            rect_abs = [d*r for d,r in zip(self.dim*2, rect)]
            print(rect_abs)
            c.rect(*rect_abs)

        for section in self.section_list:
            font_size = section.font_size
            font_name = section.font_name
            textobject = c.beginText()
            textobject.setFont(font_name, font_size)
            textobject.setFillColorRGB(0.35, 0.35, 0.45) # cool dark grey
            text_posn_abs = [d*t for d,t in zip(self.dim, section.posn)]
            textobject.setTextOrigin(*text_posn_abs)
            for text in section.text_list:
                text_width = c.stringWidth(text, font_name, font_size)
                if section.alignment == 'left':
                    x_offset = 0
                elif section.alignment == 'right':
                    x_offset = -text_width
                elif section.alignment == 'center':
                    x_offset = -text_width/2

                textobject.moveCursor(x_offset, 0)
                textobject.textOut(text)
                textobject.moveCursor(-x_offset, font_size)

            c.drawText(textobject)

        c.restoreState()


class Section(object):
    def __init__(self, text, spec):
        self.alignment = 'left'
        self.font_size = 10
        self.font_name = 'Helvetica'
        self.posn = spec[:2]
        self.wrap_width = spec[2]

        self.text_list = text.split('\n')
        self.text_list = [textwrap.wrap(t, self.wrap_width)
                          for t in self.text_list]
        self.text_list = [[''] if len(l) == 0 else l
                          for l in self.text_list]
        self.text_list = [item for sublist in self.text_list
                          for item in sublist]

        if len(spec) > 3:
            self.alignment = spec[3]
        if len(spec) > 4:
            self.font_size = spec[4]
        if len(spec) > 5:
            self.font_name = spec[5]
