* add below lines at the end of conf.py

def setup(app):
    app.add_stylesheet('custom.css')  # remove line numbers
    app.add_javascript('copybutton.js') # show/hide prompt >>>