# prototype-layout-tool
A command-line tool to layout card game prototypes

-- Installation --
1. Clone the repo to someplace convenient
2. Change directories to the root of the repo
3. execute "pip install ."
   - note: prototype-layout-tool depends on reportlab, which will be
     installed automatically by pip
4. execute "plt.py --help" for a usage message

-- Example --
1. Change directories to <repo_root>/example/number_1
2. execute "plt.py -s card_spec.csv -o cards.pdf"
3. cards.pdf will contain bridge-sized cards laid out on 8.5x11" paper
