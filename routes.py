import os
import json
import logging
from urllib.parse import urlparse
from flask import render_template, request, redirect, url_for, session, flash, jsonify, send_file
from app import app
from downloader import TikTokDownloader
from languages import get_supported_languages, detect_browser_language, get_translation

# Initialize downloader
downloader = TikTokDownloader()

@app.route('/')
def index():
    # Get user's preferred language
    lang = session.get('language')
    if not lang:
        lang = detect_browser_language(request.headers.get('Accept-Language', ''))
        session['language'] = lang
    
    translation = get_translation(lang)
    return render_template('index.html', t=translation, current_lang=lang)

@app.route('/set_language/<language>')
def set_language(language):
    if language in get_supported_languages():
        session['language'] = language
    
    # Always redirect to home page to avoid method issues
    return redirect(url_for('index'))

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url', '').strip()
    lang = session.get('language', 'en')
    translation = get_translation(lang)
    
    if not url:
        flash(translation['error_no_url'], 'error')
        return redirect(url_for('index'))
    
    # Validate TikTok URL
    if not downloader.is_valid_tiktok_url(url):
        flash(translation['error_invalid_url'], 'error')
        return redirect(url_for('index'))
    
    try:
        # Get video info
        video_info = downloader.get_video_info(url)
        if not video_info:
            flash(translation['error_fetch_failed'], 'error')
            return redirect(url_for('index'))
        
        return render_template('download.html', 
                             video_info=video_info, 
                             url=url, 
                             t=translation, 
                             current_lang=lang)
    
    except Exception as e:
        logging.error(f"Error processing video: {e}")
        flash(translation['error_processing'], 'error')
        return redirect(url_for('index'))

@app.route('/download_file')
def download_file():
    url = request.args.get('url')
    quality = request.args.get('quality', 'best')
    lang = session.get('language', 'en')
    translation = get_translation(lang)
    
    if not url:
        flash(translation['error_no_url'], 'error')
        return redirect(url_for('index'))
    
    try:
        # Download the video
        file_path = downloader.download_video(url, quality)
        if file_path and os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=os.path.basename(file_path))
        else:
            flash(translation['error_download_failed'], 'error')
            return redirect(url_for('index'))
    
    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        flash(translation['error_download_failed'], 'error')
        return redirect(url_for('index'))

@app.route('/faq')
def faq():
    lang = session.get('language', 'en')
    translation = get_translation(lang)
    return render_template('faq.html', t=translation, current_lang=lang)

@app.route('/terms')
def terms():
    lang = session.get('language', 'en')
    translation = get_translation(lang)
    return render_template('terms.html', t=translation, current_lang=lang)

@app.route('/privacy')
def privacy():
    lang = session.get('language', 'en')
    translation = get_translation(lang)
    return render_template('privacy.html', t=translation, current_lang=lang)

@app.errorhandler(404)
def not_found(error):
    lang = session.get('language', 'en')
    translation = get_translation(lang)
    return render_template('index.html', t=translation, current_lang=lang), 404

@app.errorhandler(500)
def internal_error(error):
    lang = session.get('language', 'en')
    translation = get_translation(lang)
    flash(translation['error_server'], 'error')
    return render_template('index.html', t=translation, current_lang=lang), 500
