import json
import os
import logging

SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Español',
    'fr': 'Français', 
    'de': 'Deutsch',
    'it': 'Italiano',
    'pt': 'Português',
    'ru': 'Русский',
    'ja': '日本語',
    'ko': '한국어',
    'zh': '中文',
    'ar': 'العربية',
    'hi': 'हिन्दी',
    'tr': 'Türkçe',
    'pl': 'Polski',
    'nl': 'Nederlands',
    'sv': 'Svenska',
    'no': 'Norsk',
    'da': 'Dansk',
    'fi': 'Suomi'
}

def get_supported_languages():
    """Get dictionary of supported languages"""
    return SUPPORTED_LANGUAGES

def detect_browser_language(accept_language_header):
    """Detect user's preferred language from browser header"""
    if not accept_language_header:
        return 'en'
    
    # Parse Accept-Language header
    languages = []
    for item in accept_language_header.split(','):
        if ';' in item:
            lang, priority = item.split(';')
            try:
                priority = float(priority.split('=')[1])
            except:
                priority = 1.0
        else:
            lang = item
            priority = 1.0
        
        lang = lang.strip().lower()
        # Get base language code (e.g., 'en' from 'en-US')
        if '-' in lang:
            lang = lang.split('-')[0]
        
        if lang in SUPPORTED_LANGUAGES:
            languages.append((lang, priority))
    
    # Sort by priority and return the highest priority supported language
    if languages:
        languages.sort(key=lambda x: x[1], reverse=True)
        return languages[0][0]
    
    return 'en'

def get_translation(language_code):
    """Get translation dictionary for specified language"""
    if language_code not in SUPPORTED_LANGUAGES:
        language_code = 'en'
    
    try:
        translation_file = os.path.join('translations', f'{language_code}.json')
        with open(translation_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading translation for {language_code}: {e}")
        # Fallback to English
        try:
            with open('translations/en.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            # Ultimate fallback
            return {
                'site_title': 'TikTok Downloader',
                'download_button': 'Download',
                'paste_url': 'Paste TikTok URL here...'
            }
