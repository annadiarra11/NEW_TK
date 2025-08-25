import os
import re
import tempfile
import logging
from urllib.parse import urlparse
import yt_dlp

class TikTokDownloader:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def is_valid_tiktok_url(self, url):
        """Validate if the URL is a valid TikTok URL"""
        tiktok_patterns = [
            r'https?://(?:www\.)?tiktok\.com/@[^/]+/video/\d+',
            r'https?://(?:www\.)?tiktok\.com/t/[A-Za-z0-9]+',
            r'https?://vm\.tiktok\.com/[A-Za-z0-9]+',
            r'https?://(?:www\.)?tiktok\.com/@[^/]+/video/\d+\?.*',
        ]
        
        for pattern in tiktok_patterns:
            if re.match(pattern, url):
                return True
        return False
    
    def get_video_info(self, url):
        """Get video information without downloading"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extractaudio': False,
                'outtmpl': os.path.join(self.temp_dir, '%(title)s.%(ext)s'),
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Extract relevant information
                video_info = {
                    'title': info.get('title', 'TikTok Video'),
                    'thumbnail': info.get('thumbnail', ''),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'formats': []
                }
                
                # Extract available formats
                if 'formats' in info:
                    seen_qualities = set()
                    for fmt in info['formats']:
                        if fmt.get('vcodec') != 'none':  # Skip audio-only formats
                            height = fmt.get('height', 0)
                            if height and height not in seen_qualities:
                                video_info['formats'].append({
                                    'format_id': fmt['format_id'],
                                    'quality': f"{height}p",
                                    'height': height,
                                    'ext': fmt.get('ext', 'mp4')
                                })
                                seen_qualities.add(height)
                
                # Sort formats by quality (highest first)
                video_info['formats'].sort(key=lambda x: x['height'], reverse=True)
                
                # Add default "best" option
                if video_info['formats']:
                    video_info['formats'].insert(0, {
                        'format_id': 'best',
                        'quality': 'Best Quality',
                        'height': 999,
                        'ext': 'mp4'
                    })
                
                return video_info
                
        except Exception as e:
            logging.error(f"Error extracting video info: {e}")
            return None
    
    def download_video(self, url, quality='best'):
        """Download video with specified quality"""
        try:
            # Clean up any existing files first
            self.cleanup()
            # Create fresh temp directory
            self.temp_dir = tempfile.mkdtemp()
            
            # Set up download options
            if quality == 'best':
                format_selector = 'best[ext=mp4]/best'
            else:
                # Fix the format selector - quality comes as "720p", "480p", etc.
                height = quality.replace("p", "") if quality != 'Best Quality' else '9999'
                format_selector = f'best[height<={height}][ext=mp4]/best[height<={height}]'
            
            output_path = os.path.join(self.temp_dir, '%(title)s.%(ext)s')
            
            ydl_opts = {
                'format': format_selector,
                'outtmpl': output_path,
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first to know the expected filename
                info = ydl.extract_info(url, download=False)
                
                # Download the video
                ydl.download([url])
                
                # Use the actual title to find the correct file
                expected_title = info.get('title', 'video')
                # Sanitize title for filename matching
                import string
                safe_chars = string.ascii_letters + string.digits + ' .-_'
                safe_title = ''.join(c for c in expected_title if c in safe_chars)
                
                # Find the downloaded file by checking all files
                for file in os.listdir(self.temp_dir):
                    if file.endswith(('.mp4', '.webm', '.mkv')):
                        return os.path.join(self.temp_dir, file)
                
                return None
                
        except Exception as e:
            logging.error(f"Error downloading video: {e}")
            return None
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            import shutil
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except Exception as e:
            logging.error(f"Error cleaning up temp files: {e}")
