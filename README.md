# prototype-layout-tool
A command-line tool to layout card game prototypes

-- Installation --
1. Clone the repo to someplace convenient
2. Change directories to the root of the repo
3. execute "pip install ."
   - note: prototype-layout-tool depends on reportlab, which will be
     installed automatically by pip
4. execute "plt.py --help" for a usage message

-- Input Format --
This program reads a .csv file as input. Each line of the .csv denotes
a different feature
  -- layout --
  If the first cell in a row is the string "layout", that configures
  the output for the overall layout of cards on the sheet. Layout options
  are:
    POKER_9: 3x3 poker-sized cards on 8.5x11" sheet
    POKER_L: 3x3 poker-sized cards landscape on 8.5x11" sheet
    POKER_8: 4x2 poker-sized cards on 8.5x11" sheet
    BRIDGE: 3x3 bridge-sized cards on 8.5x11" sheet

  (to be continued....)

-- Example --
1. Change directories to <repo_root>/example/number_1
2. execute "plt.py -s card_spec.csv -o cards.pdf"
3. cards.pdf will contain bridge-sized cards laid out on 8.5x11" paper
