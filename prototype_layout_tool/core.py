import math
import csv
import textwrap
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# anchors are center of each card

# 3x3 poker cards on 8.5"x11" paper
POKER_9 = {'page' : letter,
           'card_dim' : (2.5*inch, 3.5*inch),
           'anchors' : [(1.75, 9)  , (4.25, 9)  , (6.75, 9),
                        (1.75, 5.5), (4.25, 5.5), (6.75, 5.5),
                        (1.75, 2)  , (4.25, 2)  , (6.75, 2)],
           'card_rots' : [0,0,0,0,0,0,0,0,0]}
POKER_9['anchors'] = [(inch*a[0], inch*a[1]) for a in POKER_9['anchors']]

POKER_L = {'page' : letter,
           'card_dim' : (3.5*inch, 2.5*inch),
           'anchors' : [(1.75, 9)  , (4.25, 9)  , (6.75, 9),
                        (1.75, 5.5), (4.25, 5.5), (6.75, 5.5),
                        (1.75, 2)  , (4.25, 2)  , (6.75, 2)],
           'card_rots' : [90,90,90,90,90,90,90,90,90]}
POKER_L['anchors'] = [(inch*a[0], inch*a[1]) for a in POKER_L['anchors']]

# 4x2 poker cards on 8.5"x11" paper
POKER_8 = {'page' : letter,
           'card_dim' : (2.5*inch, 3.5*inch),
           'anchors' : [(2.5, 9.25), (6, 9.25),
                        (2.5, 6.75), (6, 6.75),
                        (2.5, 4.25), (6, 4.25),
                        (2.5, 1.75), (6, 1.75)],
           'card_rots' : [-90, 90, -90, 90, -90, 90, -90, 90]}
POKER_8['anchors'] = [(inch*a[0], inch*a[1]) for a in POKER_8['anchors']]

BRIDGE = {'page' : letter,
          'card_dim' : (2.25*inch, 3.5*inch),
          'anchors' : [(2, 9)  , (4.25, 9)  , (6.5, 9),
                       (2, 5.5), (4.25, 5.5), (6.5, 5.5),
                       (2, 2)  , (4.25, 2)  , (6.5, 2)],
          'card_rots' : [0,0,0,0,0,0,0,0,0]}
BRIDGE['anchors'] = [(inch*a[0], inch*a[1]) for a in BRIDGE['anchors']]

TAROT = {'page' : letter,
         'card_dim' : (2.75*inch, 4.75*inch),
         'anchors' : [(1.875, 7.875), (1.875, 3.125),
                      (5.625, 8.25), (5.625, 5.5), (5.625, 2.75)],
         'card_rots' : [0, 0, 90, 90, 90]}
TAROT['anchors'] = [(inch*a[0], inch*a[1]) for a in TAROT['anchors']]

JUMBO = {'page' : letter,
         'card_dim' : (3.34090909*inch, 5.25*inch),
         'anchors' : [(2.5795455, 8.125), (5.9204546, 8.125),
                      (2.5795455, 2.875), (5.9204546, 2.875)],
         'card_rots' : [0, 0, 0, 0]}
JUMBO['anchors'] = [(inch*a[0], inch*a[1]) for a in JUMBO['anchors']]

JUMBO_L = {'page' : letter,
           'card_dim' : (3.34090909*inch, 5.25*inch),
           'anchors' : [(2.5795455, 8.125), (5.9204546, 8.125),
                        (2.5795455, 2.875), (5.9204546, 2.875)],
           'card_rots' : [90, 90, 90, 90]}
JUMBO_L['anchors'] = [(inch*a[0], inch*a[1]) for a in JUMBO_L['anchors']]

SQUARE_4_INCH = {'page' : letter,
                'card_dim' : (4*inch, 4*inch),
                'anchors' : [(2.25, 7.5), (6.25, 7.5),
                             (2.25, 3.5), (6.25, 3.5)],
                'card_rots' : [0,0,0,0]}
SQUARE_4_INCH['anchors'] = [(inch*a[0], inch*a[1]) for a in SQUARE_4_INCH['anchors']]

SQUARE_2_INCH = {
    'page' : letter,
    'card_dim' : (2*inch, 2*inch),
    'anchors' : [(1.25,9.5), (3.25,9.5), (5.25,9.5), (7.25,9.5),
                 (1.25,7.5), (3.25,7.5), (5.25,7.5), (7.25,7.5),
                 (1.25,5.5), (3.25,5.5), (5.25,5.5), (7.25,5.5),
                 (1.25,3.5), (3.25,3.5), (5.25,3.5), (7.25,3.5),
                 (1.25,1.5), (3.25,1.5), (5.25,1.5), (7.25,1.5)],
    'card_rots' : [0]*20}
SQUARE_2_INCH['anchors'] = [(inch*a[0], inch*a[1]) for a in SQUARE_2_INCH['anchors']]

SQUARE_2_5_INCH = {'page' : letter,
           'card_dim' : (2.5*inch, 2.5*inch),
           'anchors' : [(1.75, 9)  , (4.25, 9)  , (6.75, 9),
                        (1.75, 5.5), (4.25, 5.5), (6.75, 5.5),
                        (1.75, 2)  , (4.25, 2)  , (6.75, 2)],
           'card_rots' : [0,0,0,0,0,0,0,0,0]}
SQUARE_2_5_INCH['anchors'] = [(inch*a[0], inch*a[1]) for a in SQUARE_2_5_INCH['anchors']]

ICF_OBLIQUE = {'page' : (191.304, 263.304),
        'card_dim' : (2.657*inch, 3.657*inch),
        'anchors' : [(1.3285*inch, 1.8285*inch)],
        'card_rots' : [0]}

def read_specs(spec_filename):
    with open(spec_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        specs = [row for row in reader]

    card_list = []
    line_list = []
    rect_list = []
    section_specs = []
    background = None
    for spec in specs:
        print(spec)
        if spec[0] == '' or spec[0][0] == '#': continue
        elif spec[0] == 'layout':
            layout = eval(spec[1].upper())
        elif spec[0] == 'bg_image':
            bg_filename = spec[1]
            if len(spec) > 2 and spec[2] != '':
                bg_spec = eval(spec[2])
            else:
                bg_spec = None
            background = Background(bg_filename, bg_spec)
        elif spec[0] == 'no_bg_image':
            background = None
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
                         background,
                         section_list,
                         line_list,
                         rect_list)
                )
    return (card_list, layout)
                

def draw_cards(card_list, filename, layout):
    num_cards = len(card_list)
    cards_per_sheet = len(layout['anchors'])
    num_pages = math.ceil(num_cards / cards_per_sheet)

    c = canvas.Canvas(filename, pagesize=layout['page'])
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
    def __init__(self, dim, background=None,
                 section_list=(), line_list=(), rect_list=()):
        self.dim = dim
        self.bg = background
        self.section_list = section_list
        self.line_list = line_list
        self.rect_list = rect_list

    def draw(self, c, anchor, rot):
        # translate and rotate
        c.saveState() # to draw card
        c.translate(*anchor)
        c.rotate(rot)
        c.translate(*[-x/2 for x in self.dim])

        # draw background image
        if self.bg:
            c.saveState() # to draw background image
            p = c.beginPath()
            p.rect(0,0,*self.dim)
            c.clipPath(p, stroke=0)
            c.drawImage(self.bg.image,
                        self.bg.x_offset,
                        self.bg.y_offset,
                        self.dim[0]*self.bg.x_scale,
                        self.dim[1]*self.bg.y_scale,
                        mask='auto')
            c.restoreState() # background image complete
            
        # draw lines
        for line in self.line_list:
            line_abs = [d*l for d,l in zip(self.dim*2, line)]
            c.line(*line_abs)

        # draw rectangles
        for rect in self.rect_list:
            rect_abs = [d*r for d,r in zip(self.dim*2, rect)]
            print(rect_abs)
            c.rect(*rect_abs)

        # draw text sections
        registered_fonts = c.getAvailableFonts()
        needed_fonts = list(set([s.font_name for s in self.section_list]))
        for f in needed_fonts:
            if f not in registered_fonts:
                pdfmetrics.registerFont(TTFont(f, '{0}.ttf'.format(f)))
        for section in self.section_list:
            c.saveState() # to draw section
            c.translate(*anchor)
            c.rotate(section.rot)
            c.translate(*[-x/2 for x in self.dim])

            font_size = section.font_size
            font_name = section.font_name
            textobject = c.beginText()
            textobject.setFont(font_name, font_size)
            textobject.setFillColorRGB(*section.font_color)
            text_posn_abs = [d*t for d,t in zip(self.dim, section.posn)]
            textobject.setTextOrigin(*text_posn_abs)

            if 'bottom' in section.alignment:
                y_offset = len(section.text_list) * -font_size
            elif 'middle' in section.alignment:
                y_offset = len(section.text_list) * -font_size/2
            else: # elif 'top' in section.alignment:
                y_offset = 0

            textobject.moveCursor(0,font_size/1.4)
            textobject.moveCursor(0, y_offset)

            for text in section.text_list:
                text_width = c.stringWidth(text, font_name, font_size)
                if 'right' in section.alignment:
                    x_offset = -text_width
                elif 'center' in section.alignment:
                    x_offset = -text_width/2
                else: # elif 'left' in section.alignment:
                    x_offset = 0

                textobject.moveCursor(x_offset, 0)
                textobject.textOut(text)
                textobject.moveCursor(-x_offset, font_size)

            textobject.moveCursor(0, -y_offset)
            textobject.moveCursor(0, -font_size/1.4)

            c.drawText(textobject)

            c.restoreState() # section complete

        c.restoreState() # card complete


class Section(object):
    def __init__(self, text, spec):
        self.alignment = 'bottomleft'
        self.font_size = 10
        self.font_name = 'Helvetica'
        self.font_color = (0,0,0)
        self.posn = spec[:2]
        self.rot = spec[2]
        self.wrap_width = spec[3]

        self.text_list = text.split('\n')
        self.text_list = [textwrap.wrap(t, self.wrap_width)
                          for t in self.text_list]
        self.text_list = [[''] if len(l) == 0 else l
                          for l in self.text_list]
        self.text_list = [item for sublist in self.text_list
                          for item in sublist]

        if len(spec) > 4:
            self.alignment = spec[4].lower()
        if len(spec) > 5:
            self.font_size = spec[5]
        if len(spec) > 6:
            self.font_name = spec[6]
        if len(spec) > 7:
            self.font_color = spec[7]


class Background(object):
    def __init__(self, filename, spec=None):
        self.image = filename
        if spec:
            (self.x_offset,
             self.y_offset,
             self.x_scale,
             self.y_scale) = spec
        else:
            (self.x_offset,
             self.y_offset,
             self.x_scale,
             self.y_scale) = (0,0,1,1)
