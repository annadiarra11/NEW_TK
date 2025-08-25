# TikTok Downloader

## Overview

This is a multilingual TikTok video downloader web application built with Flask. The application allows users to download TikTok videos by simply pasting the video URL. It features a clean, responsive interface with support for 19 languages and provides video information extraction before download.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask
- **CSS Framework**: Bootstrap 5.3.0 for responsive design
- **JavaScript**: Vanilla JS for client-side validation and interactions
- **Styling**: Custom CSS with CSS variables for theming (TikTok-inspired color scheme)
- **Icons**: Font Awesome 6.0.0 for UI icons
- **Fonts**: Google Fonts (Inter and Poppins) for typography

### Backend Architecture
- **Web Framework**: Flask with Python
- **Route Structure**: Modular routing system with separate routes file
- **Session Management**: Flask sessions for language preferences
- **Video Processing**: yt-dlp library for TikTok video extraction and downloading
- **Internationalization**: JSON-based translation system supporting 19 languages
- **Language Detection**: Automatic browser language detection with manual override

### Core Components
- **TikTokDownloader Class**: Handles video URL validation, metadata extraction, and download processing
- **Language System**: Browser language detection with session-based preferences
- **URL Validation**: Regex-based TikTok URL pattern matching
- **Template Inheritance**: Base template with extensible blocks for consistent UI

### File Structure
- **Application Entry**: `app.py` (Flask app configuration) and `main.py` (entry point)
- **Business Logic**: `downloader.py` (video processing), `languages.py` (i18n), `routes.py` (web routes)
- **Frontend**: `templates/` (Jinja2 templates), `static/` (CSS/JS assets)
- **Translations**: `translations/` (JSON files for 19 languages)

### Key Features
- **Multi-language Support**: 19 languages with automatic detection
- **Responsive Design**: Mobile-first approach with Bootstrap
- **Video Quality Options**: Multiple download quality selections
- **URL Validation**: Client and server-side TikTok URL validation
- **Clean UI**: TikTok-inspired design with modern aesthetics

## External Dependencies

### Core Libraries
- **Flask**: Web framework for Python
- **yt-dlp**: YouTube and TikTok video extraction library
- **Jinja2**: Template engine (included with Flask)

### Frontend Dependencies (CDN)
- **Bootstrap 5.3.0**: CSS framework for responsive design
- **Font Awesome 6.0.0**: Icon library
- **Google Fonts**: Web fonts (Inter and Poppins families)

### Python Standard Libraries
- **os**: Environment variable handling
- **json**: Translation file processing
- **logging**: Application logging
- **tempfile**: Temporary file management for downloads
- **urllib.parse**: URL parsing and validation
- **re**: Regular expression pattern matching

### Browser APIs
- **Accept-Language**: Browser language detection
- **Local Storage**: Potential session persistence (client-side)
- **File Download**: Browser download handling