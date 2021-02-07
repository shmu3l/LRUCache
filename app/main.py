from flask import Blueprint, render_template
from app import settings
from app.data_model import UrlsAnalyzer

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index.html')
def index():
    print(settings.global_cache.cache)
    return render_template('index.html', url_list=settings.global_cache.cache)


@main.route('/load')
@main.route('/index.html')
def load_from_txt():
    UrlsAnalyzer().load_url_list()
    return render_template('index.html', url_list=settings.global_cache.cache)


@main.route('/scan')
@main.route('/index.html')
def scan():
    q_status = settings.background_processing()
    print(q_status)
    return render_template('index.html', url_list=settings.global_cache.cache, message=q_status)


@main.route('/refresh')
@main.route('/index.html')
def refresh_view():
    print(settings.global_cache.cache)
    return render_template('index.html', url_list=settings.global_cache.cache)





