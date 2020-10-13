import logging

from datetime import datetime
# import utils.html_markup as markup
# from config.config_rw import ConfigRW
from dashboards.nlp_dashboard import NlpDashboard
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_cors import CORS
from inMemoryData.InMemoryManager import InMemoryManager
from inMemoryData.InMemoryManager import ActivityNote

import definitions
# from definitions import Settings
from utils.print_enh import print_begin
from utils.print_enh import print_end

import pandas as pdb


# think of using connexion for swagger implementation
app = Flask(__name__,
            template_folder=f'{definitions.get_project_root()}/web',
            static_folder=f'{definitions.get_project_root()}/web')
CORS(app)
my_ip_address = definitions.get_ip_address()
imm = InMemoryManager()

# def start_app() -> None:
current_logger = definitions.setup_logger(__name__, level=logging.DEBUG)

@app.route('/status')
def hello_world():
    """
    See if the application is up and running.
    :return: nothing
    ---
    tag:
        - status
    """
    return f'<b>Hello World!</b> I\'m alive. prior_auth<p>'

@app.route('/', methods=['GET', 'POST'])
def login():
    """
    Login
    :return: redirects to the page
    ---
    tag:
        - login
    """

    error = None
    try:
        user_name = request.form['userName']
    except Exception:
        user_name = ''

    print_begin()
    if request.method == 'POST' and user_name:
        return redirect(url_for('main_page', display_name=user_name))

    return render_template('login.html', error=error, user_name=user_name)


@app.route('/main_page/<display_name>')
def main_page(display_name):
    """
    :param display_name:hwo to get requirements.
    :return:
    ---
    tags:
        - main page
    """
    # config_rw = ConfigRW(Settings.PRIOR_AUTH_SETTINGS.value)
    print_begin()
    ip_address = definitions.get_ip_address()
    # server_options = markup.server_options(ip_address)
    return render_template('DashboardPriorAuth.html', error=None,
                           def_server_option=ip_address,
                           display_name=display_name,
                           )


dashboard = NlpDashboard()


@app.route('/basic/<method_call>', methods=['POST'])
def main_dashboard(method_call):
    """
    Main application call
    :param method_call:
    :return:
    ---
    tags:
        - main dashboard
    """
    return dashboard.post(method_call)

@app.route('/search', methods=['GET', 'POST'])
def search_data():
    """
    search for data with in pandas
    :param speech_text:
    :return:
    ---
    tags:
        - search text
    """
    if request.method == "POST":
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        # {"author":"Roland","speech_text":"sister-in-law, Jill"}​​​​
        author = request.json.get("author", None)
        speech_text = request.json.get("speech_text", None)
    else:
        author = request.args.get('author')
        speech_text = request.args.get('speech_text')

    if not author:
        return jsonify({"msg": "Missing author parameter"}), 400
    if not speech_text:
        return jsonify({"msg": "Missing search parameter"}), 400

    InMemoryManager.dataframes_load(str(author))

    return jsonify({"speech_text": f'{imm.dataframes_search(str(speech_text))}'}), 200

@app.route('/post', methods=['GET', 'POST'])
def post_data():
    """
    search for data with in pandas
    :param speech_text:
    :return:
    ---
    tags:
        - search text
    """
    if request.method == "POST":
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        author = request.json.get("author", None)
        mbr_id = request.json.get("mbr_id", None)
        case_id = request.json.get("case_id", None)
        activity_type = request.json.get("activity_type", None)
        note = request.json.get("note", None)
    else:
        author = request.args.get('author')
        mbr_id = request.args.get('mbr_id')
        case_id = request.args.get('case_id')
        activity_type = request.args.get('activity_type')
        note = request.args.get('note')

    if not author:
        return jsonify({"msg": "Missing author parameter"}), 400
    if not activity_type:
        return jsonify({"msg": "Missing activity parameter"}), 400
    if not note:
        return jsonify({"msg": "Missing note parameter"}), 400
    my_activity = ActivityNote(Author=author, Mbr_Id=mbr_id, Case_Id=case_id, Activity_Type=activity_type, Note=note,
                               Date_Time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    return jsonify({"note added = ": f'{imm.workbook_add(my_activity)}'}), 200
