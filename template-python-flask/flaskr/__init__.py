import os

from flask import Flask, session
from flask import Flask, render_template, request
from flask_session import Session



def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )
    Session(app)
    app.config['SESSION_TYPE'] = 'filesystem'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        to_do_list = ['Clean Bathrooms', 'Laundry', 'Vacuum', 'Swiffer', 'Check Emails', 'Lesson Plan for next week', 'Update Infinite Campus', 'Send HW Emails']
        session['to_do_list'] = to_do_list
        session['action'] = '/home'


        return render_template('index.html', to_do_list = to_do_list)


    def get_what_button_pushed():
        if request.method == "POST":
            print("posts")
            entry_orig = request.form
            entry_dict = entry_orig.to_dict()
            entry_list = list(entry_dict.values())
            entry = entry_list[0]

            for list_entry in session['to_do_list']:
                if list_entry == entry:
                    session['entry'] = entry
                    print(session['entry'])
                
         
        elif request.method == "GET":
            print("Get")  
        else:
            print("MAJOR ERROR IN GET WHAT BUTTON PUSHED!!!")     

    def cross_off_or_go_back(to_do_list):
        if request.method == "POST":
            print("post cross off")
            print(request.form)
            if request.form.get("cross_off"):
                entry = session['entry']
                to_do_list.remove(entry)
                session['to_do_list'] = to_do_list
                session['action'] = '/home'
                print(session['to_do_list'])

            elif request.form.get('back_to_home'):
                print('Go back to list without any changes')
                session['action'] = '/'

            else:
                pass

    def add_new_item(to_do_list):
        print(request.method)
        if request.method == "POST":
            items = request.form
            items_dict = items.to_dict()
            items_list = list(items_dict.values())
            
            if request.form.get("add_item"):
                new_item = request.form['new_item']
                to_do_list.append(new_item)
                session['to_do_list'] = to_do_list
                session['action'] = '/home'

            elif request.form.get('back_to_home'):
                print('Go back to list without any changes')
                session['action'] = '/'

            else:
                print("MAJOR ERROR")
                pass


    @app.route("/do_something_to_item", methods=['GET','POST'])
    def do_something_to_item():
        get_what_button_pushed()

        return render_template('do_something_to_item.html', entry = session['entry'],action = session['action']) 
        
    
    @app.route('/home', methods=['GET','POST'])
    def home():
        cross_off_or_go_back(session['to_do_list'])
        to_do_list = session['to_do_list']
        return render_template('index.html', to_do_list = to_do_list, action = session['action'])



    @app.route("/add_new_item", methods=['GET','POST'])
    def add_new():
        session['action'] = ''
        to_do_list = session['to_do_list']
        add_new_item(to_do_list)


        return render_template('add_new_item.html', action = session['action']) 

    


    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
   # app.add_url_rule("/", endpoint="index")


    sess = Session()
    sess.init_app(app)

    return app








#helpful websites
#https://stackoverflow.com/questions/15557392/how-do-i-display-images-from-google-drive-on-a-website
#https://unsplash.com/images/stock/blogging
#https://getbootstrap.com/docs/3.3/components/#btn-groups
#https://www.w3schools.com/bootstrap/bootstrap_theme_me.asp
#https://stackoverflow.com/questions/42601478/flask-calling-python-function-on-button-onclick-event