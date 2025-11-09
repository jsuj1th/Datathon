import os
import io
from PIL import Image
import PyPDF2
from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np
from config import Config

# Import video processor for video handling
try:
    from video_processor import VideoProcessor
    VIDEO_PROCESSING_AVAILABLE = True
except ImportError:
    VIDEO_PROCESSING_AVAILABLE = False

# Import video processor for video handling
try:
    from video_processor import VideoProcessor
    VIDEO_PROCESSING_AVAILABLE = True
except ImportError:
    VIDEO_PROCESSING_AVAILABLE = False

class DocumentPreprocessor:
    
    @staticmethod
    def check_file_validity(file_path):
        """
        Perform pre-processing checks on the document
        """
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'metadata': {}
        }
        
        # Check file exists
        if not os.path.exists(file_path):
            results['valid'] = False
            results['errors'].append('File does not exist')
            return results
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > Config.MAX_FILE_SIZE:
            results['valid'] = False
            results['errors'].append(f'File size exceeds maximum ({Config.MAX_FILE_SIZE} bytes)')
            return results
        
        results['metadata']['file_size'] = file_size
        
        # Determine file type and process accordingly
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            pdf_results = DocumentPreprocessor._check_pdf(file_path)
            results['metadata'].update(pdf_results)
        elif file_ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            image_results = DocumentPreprocessor._check_image(file_path)
            results['metadata'].update(image_results)
        elif file_ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']:
            video_results = DocumentPreprocessor._check_video(file_path)
            results['metadata'].update(video_results)
        else:
            results['valid'] = False
            results['errors'].append('Unsupported file type')
        
        return results
    
    @staticmethod
    def _check_pdf(file_path):
        """Check PDF-specific properties"""
        metadata = {
            'type': 'pdf',
            'page_count': 0,
            'image_count': 0,
            'has_text': False,
            'is_legible': True,
            'text_content': ''
        }
        
        try:
            # Read PDF
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata['page_count'] = len(pdf_reader.pages)
                
                # Check page count limit
                if metadata['page_count'] > Config.MAX_PAGES:
                    metadata['is_legible'] = False
                    return metadata
                
                # Extract text from all pages
                text_content = []
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
                
                metadata['text_content'] = '\n'.join(text_content)
                metadata['has_text'] = len(metadata['text_content'].strip()) > 0
                
            # Convert PDF to images to count embedded images
            try:
                images = convert_from_path(file_path, dpi=150)
                metadata['image_count'] = len(images)
            except Exception as e:
                metadata['image_count'] = 0
                
        except Exception as e:
            metadata['is_legible'] = False
            metadata['error'] = str(e)
        
        return metadata
    
    @staticmethod
    def _check_image(file_path):
        """Check image-specific properties"""
        metadata = {
            'type': 'image',
            'page_count': 1,
            'image_count': 1,
            'has_text': False,
            'is_legible': True,
            'width': 0,
            'height': 0,
            'text_content': ''
        }
        
        try:
            # Open image
            img = Image.open(file_path)
            metadata['width'] = img.width
            metadata['height'] = img.height
            
            # Check image quality/legibility
            img_array = np.array(img.convert('L'))
            quality_score = DocumentPreprocessor._assess_image_quality(img_array)
            
            if quality_score < Config.MIN_IMAGE_QUALITY:
                metadata['is_legible'] = False
            
            # Perform OCR to extract text
            try:
                text = pytesseract.image_to_string(img)
                metadata['text_content'] = text
                metadata['has_text'] = len(text.strip()) > 0
            except Exception:
                pass
                
        except Exception as e:
            metadata['is_legible'] = False
            metadata['error'] = str(e)
        
        return metadata
    
    @staticmethod
    def _check_video(file_path):
        """Check video-specific properties using video processor"""
        metadata = {
            'type': 'video',
            'page_count': 1,  # Videos are treated as single "page" documents
            'image_count': 0,
            'has_text': False,
            'is_legible': True,
            'duration': 0,
            'has_audio': False,
            'text_content': '',
            'fps': 0,
            'resolution': (0, 0)
        }
        
        if not VIDEO_PROCESSING_AVAILABLE:
            metadata['is_legible'] = False
            metadata['error'] = 'Video processing not available - install video dependencies'
            return metadata
        
        try:
            # Use video processor for detailed analysis
            video_processor = VideoProcessor()
            validation_result = video_processor.check_video_validity(file_path)
            
            if validation_result['valid']:
                video_metadata = validation_result['metadata']
                metadata.update({
                    'duration': video_metadata.get('duration', 0),
                    'has_audio': video_metadata.get('has_audio', False),
                    'fps': video_metadata.get('fps', 0),
                    'resolution': video_metadata.get('resolution', (0, 0)),
                    'video_codec': video_metadata.get('video_codec', 'unknown'),
                    'audio_codec': video_metadata.get('audio_codec', 'unknown')
                })
                
                # If video has audio, we consider it as having potential text content
                metadata['has_text'] = video_metadata.get('has_audio', False)
            else:
                metadata['is_legible'] = False
                metadata['error'] = '; '.join(validation_result.get('errors', []))
                
        except Exception as e:
            metadata['is_legible'] = False
            metadata['error'] = str(e)
        
        return metadata
    
    @staticmethod
    def _assess_image_quality(img_array):
        """Assess image quality using variance of Laplacian"""
        try:
            laplacian_var = cv2.Laplacian(img_array, cv2.CV_64F).var()
            # Normalize to 0-1 range (typical values: 0-1000+)
            quality_score = min(laplacian_var / 100.0, 1.0)
            return quality_score
        except Exception:
            return 0.5  # Default medium quality
    
    @staticmethod
    def extract_content_for_analysis(file_path, metadata):
        """
        Extract content in a format suitable for LLM analysis
        """
        content = {
            'text': metadata.get('text_content', ''),
            'images': [],
            'metadata': metadata
        }
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            # Convert PDF pages to images for visual analysis
            try:
                images = convert_from_path(file_path, dpi=200)
                for idx, img in enumerate(images[:10]):  # Limit to first 10 pages
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='PNG')
                    content['images'].append({
                        'page': idx + 1,
                        'data': img_byte_arr.getvalue()
                    })
            except Exception:
                pass
        elif file_ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            # Read image file
            with open(file_path, 'rb') as f:
                content['images'].append({
                    'page': 1,
                    'data': f.read()
                })
        elif file_ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']:
            # Extract text content from video using video processor
            if VIDEO_PROCESSING_AVAILABLE and metadata.get('has_audio', False):
                try:
                    video_processor = VideoProcessor()
                    video_content = video_processor.extract_content_for_analysis(file_path, metadata)
                    
                    # Update text content with transcript
                    content['text'] = video_content.get('transcript', '')
                    content['video_transcript'] = video_content.get('transcript', '')
                    content['audio_segments'] = video_content.get('audio_segments', [])
                    content['processing_method'] = video_content.get('processing_method', 'none')
                    content['confidence_score'] = video_content.get('confidence_score', 0.0)
                    content['language_detected'] = video_content.get('language_detected', 'unknown')
                    
                    if video_content.get('error'):
                        content['processing_error'] = video_content['error']
                        
                except Exception as e:
                    content['processing_error'] = f'Video processing failed: {str(e)}'
        
        return content
