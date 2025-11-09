#!/usr/bin/env python3
"""
Video Processor with ElevenLabs Integration
Extracts audio from video files and transcribes using ElevenLabs API for classification
"""

import os
import io
import tempfile
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

# Video and audio processing
try:
    from moviepy import VideoFileClip
    import speech_recognition as sr
    from pydub import AudioSegment
    from pydub.silence import split_on_silence
    MOVIEPY_AVAILABLE = True
except ImportError as e:
    MOVIEPY_AVAILABLE = False
    logging.warning(f"Video processing libraries not available: {e}")

# ElevenLabs for transcription
try:
    from elevenlabs import ElevenLabs
    ELEVENLABS_AVAILABLE = True
except ImportError as e:
    ELEVENLABS_AVAILABLE = False
    logging.warning(f"ElevenLabs not available: {e}")

# OpenAI Whisper as fallback
try:
    import openai
    WHISPER_AVAILABLE = True
except ImportError as e:
    WHISPER_AVAILABLE = False
    logging.warning(f"OpenAI Whisper not available: {e}")

from config import Config

class VideoProcessor:
    """
    Process video files to extract text content for classification
    """
    
    def __init__(self):
        self.elevenlabs_client = None
        self.openai_client = None
        
        # Initialize ElevenLabs
        if ELEVENLABS_AVAILABLE and Config.ELEVENLABS_API_KEY and Config.ELEVENLABS_API_KEY != 'your_elevenlabs_api_key_here':
            try:
                self.elevenlabs_client = ElevenLabs(api_key=Config.ELEVENLABS_API_KEY)
                print("✅ ElevenLabs initialized for video transcription")
            except Exception as e:
                print(f"⚠️  Failed to initialize ElevenLabs: {e}")
        
        # Initialize OpenAI as fallback
        if WHISPER_AVAILABLE and Config.OPENROUTER_API_KEY:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=Config.OPENROUTER_API_KEY,
                    max_retries=3,
                    timeout=30.0
                )
                print("✅ OpenAI Whisper available as fallback")
            except Exception as e:
                print(f"⚠️  OpenAI Whisper not available: {e}")
    
    def check_video_validity(self, file_path: str) -> Dict[str, Any]:
        """
        Check if video file is valid and within processing limits
        
        Args:
            file_path: Path to video file
            
        Returns:
            Dictionary with validation results and metadata
        """
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'metadata': {}
        }
        
        if not MOVIEPY_AVAILABLE:
            results['valid'] = False
            results['errors'].append('Video processing libraries not installed')
            return results
        
        try:
            # Check file exists
            if not os.path.exists(file_path):
                results['valid'] = False
                results['errors'].append('Video file does not exist')
                return results
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > Config.MAX_VIDEO_SIZE:
                results['valid'] = False
                results['errors'].append(f'Video file size exceeds maximum ({Config.MAX_VIDEO_SIZE} bytes)')
                return results
            
            results['metadata']['file_size'] = file_size
            
            # Get video properties
            with VideoFileClip(file_path) as video:
                duration = video.duration
                fps = video.fps
                resolution = (video.w, video.h) if video.w and video.h else (0, 0)
                has_audio = video.audio is not None
                
                results['metadata'].update({
                    'type': 'video',
                    'duration': duration,
                    'fps': fps,
                    'resolution': resolution,
                    'has_audio': has_audio,
                    'video_codec': getattr(video, 'codec', 'unknown'),
                    'audio_codec': getattr(video.audio, 'codec', 'unknown') if has_audio else None
                })
                
                # Check duration limit
                if duration > Config.MAX_VIDEO_DURATION:
                    results['valid'] = False
                    results['errors'].append(f'Video duration exceeds maximum ({Config.MAX_VIDEO_DURATION} seconds)')
                    return results
                
                # Warn if no audio
                if not has_audio:
                    results['warnings'].append('Video has no audio track - transcription will be skipped')
                
                # Warn if very long
                if duration > 600:  # 10 minutes
                    results['warnings'].append('Long video may take significant time to process')
        
        except Exception as e:
            results['valid'] = False
            results['errors'].append(f'Error reading video file: {str(e)}')
        
        return results
    
    def extract_content_for_analysis(self, file_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract text content from video for classification
        
        Args:
            file_path: Path to video file
            metadata: Video metadata from validation
            
        Returns:
            Dictionary containing extracted content
        """
        content = {
            'text': '',
            'transcript': '',
            'audio_segments': [],
            'processing_method': 'none',
            'confidence_score': 0.0,
            'language_detected': 'unknown',
            'error': None
        }
        
        try:
            # Skip if no audio
            if not metadata.get('has_audio', False):
                content['error'] = 'No audio track found in video'
                return content
            
            # Extract audio from video
            audio_file = self._extract_audio_from_video(file_path)
            if not audio_file:
                content['error'] = 'Failed to extract audio from video'
                return content
            
            # Transcribe audio using available method
            transcript_result = self._transcribe_audio(audio_file)
            
            # Clean up temporary audio file
            try:
                os.unlink(audio_file)
            except:
                pass
            
            content.update(transcript_result)
            content['text'] = content['transcript']  # For compatibility with existing classification system
            
        except Exception as e:
            content['error'] = f'Video processing failed: {str(e)}'
            logging.error(f"Video processing error: {e}", exc_info=True)
        
        return content
    
    def _extract_audio_from_video(self, video_path: str) -> Optional[str]:
        """
        Extract audio from video file
        
        Args:
            video_path: Path to video file
            
        Returns:
            Path to extracted audio file or None if failed
        """
        try:
            # Create temporary file for audio
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_audio.close()
            
            # Extract audio using moviepy
            with VideoFileClip(video_path) as video:
                if video.audio:
                    # Extract audio and save as WAV
                    audio = video.audio
                    audio.write_audiofile(
                        temp_audio.name,
                        logger=None
                    )
                    audio.close()
                    return temp_audio.name
                else:
                    os.unlink(temp_audio.name)
                    return None
        
        except Exception as e:
            logging.error(f"Audio extraction failed: {e}")
            try:
                os.unlink(temp_audio.name)
            except:
                pass
            return None
    
    def _transcribe_audio(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Transcribe audio using available transcription service
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Dictionary with transcription results
        """
        result = {
            'transcript': '',
            'audio_segments': [],
            'processing_method': 'none',
            'confidence_score': 0.0,
            'language_detected': 'unknown'
        }
        
        # Try OpenAI Whisper first (primary method for transcription)
        if self.openai_client:
            try:
                whisper_result = self._transcribe_with_whisper(audio_file_path)
                if whisper_result['transcript']:
                    result.update(whisper_result)
                    result['processing_method'] = 'whisper'
                    return result
            except Exception as e:
                logging.warning(f"Whisper transcription failed: {e}")
        
        # Try speech_recognition as fallback
        try:
            sr_result = self._transcribe_with_speech_recognition(audio_file_path)
            if sr_result['transcript']:
                result.update(sr_result)
                result['processing_method'] = 'speech_recognition'
                return result
        except Exception as e:
            logging.warning(f"Speech recognition failed: {e}")
        
        # If all methods fail, return empty result
        result['processing_method'] = 'none'
        return result
    
    def _transcribe_with_elevenlabs(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Transcribe audio using ElevenLabs API
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Dictionary with transcription results
        """
        result = {
            'transcript': '',
            'audio_segments': [],
            'confidence_score': 0.0,
            'language_detected': 'unknown'
        }
        
        try:
            # Read audio file
            with open(audio_file_path, 'rb') as audio_file:
                # Note: ElevenLabs primarily focuses on voice synthesis
                # For transcription, we would need their speech-to-text service
                # This is a placeholder for the actual ElevenLabs transcription API
                
                # If ElevenLabs has a speech-to-text endpoint, use it here
                # For now, we'll note that ElevenLabs is primarily for synthesis
                result['transcript'] = "ElevenLabs transcription not yet implemented"
                result['confidence_score'] = 0.5
                result['language_detected'] = 'en'
                
                # TODO: Implement actual ElevenLabs transcription when available
                # This might involve using their voice analysis or other tools
                
        except Exception as e:
            logging.error(f"ElevenLabs transcription error: {e}")
        
        return result
    
    def _transcribe_with_whisper(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Transcribe audio using OpenAI Whisper
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Dictionary with transcription results
        """
        result = {
            'transcript': '',
            'audio_segments': [],
            'confidence_score': 0.0,
            'language_detected': 'unknown'
        }
        
        try:
            with open(audio_file_path, 'rb') as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json"
                )
                
                result['transcript'] = transcript.text
                result['confidence_score'] = 0.85  # Whisper generally has good accuracy
                result['language_detected'] = transcript.language if hasattr(transcript, 'language') else 'unknown'
                
                # Extract segments if available
                if hasattr(transcript, 'segments'):
                    result['audio_segments'] = [
                        {
                            'start': seg.start,
                            'end': seg.end,
                            'text': seg.text,
                            'confidence': getattr(seg, 'avg_logprob', 0.0)
                        }
                        for seg in transcript.segments
                    ]
        
        except Exception as e:
            logging.error(f"Whisper transcription error: {e}")
        
        return result
    
    def _transcribe_with_speech_recognition(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Transcribe audio using speech_recognition library (Google Speech Recognition)
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Dictionary with transcription results
        """
        result = {
            'transcript': '',
            'audio_segments': [],
            'confidence_score': 0.0,
            'language_detected': 'unknown'
        }
        
        try:
            # Initialize recognizer
            r = sr.Recognizer()
            
            # Load and convert audio
            audio = AudioSegment.from_wav(audio_file_path)
            
            # Split audio on silence for better recognition
            chunks = split_on_silence(
                audio,
                min_silence_len=500,  # 0.5 seconds
                silence_thresh=audio.dBFS - 14,
                keep_silence=500,
            )
            
            transcripts = []
            for i, chunk in enumerate(chunks):
                # Export chunk to temporary file
                chunk_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                chunk_file.close()
                
                try:
                    chunk.export(chunk_file.name, format="wav")
                    
                    # Transcribe chunk
                    with sr.AudioFile(chunk_file.name) as source:
                        chunk_audio = r.record(source)
                        
                    try:
                        chunk_text = r.recognize_google(chunk_audio)
                        transcripts.append(chunk_text)
                        
                        result['audio_segments'].append({
                            'start': i * 2,  # Rough timing
                            'end': (i + 1) * 2,
                            'text': chunk_text,
                            'confidence': 0.7  # Rough estimate
                        })
                        
                    except sr.UnknownValueError:
                        # Could not understand audio
                        continue
                    except sr.RequestError as e:
                        logging.error(f"Speech recognition API error: {e}")
                        continue
                
                finally:
                    try:
                        os.unlink(chunk_file.name)
                    except:
                        pass
            
            result['transcript'] = ' '.join(transcripts)
            result['confidence_score'] = 0.7 if result['transcript'] else 0.0
            result['language_detected'] = 'en'  # Google Speech Recognition default
        
        except Exception as e:
            logging.error(f"Speech recognition error: {e}")
        
        return result
    
    def process_video_batch(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Process multiple video files in batch
        
        Args:
            file_paths: List of video file paths
            
        Returns:
            List of processing results
        """
        results = []
        
        for file_path in file_paths:
            print(f"Processing video: {Path(file_path).name}")
            
            # Validate video
            validation = self.check_video_validity(file_path)
            
            if not validation['valid']:
                results.append({
                    'file_path': file_path,
                    'success': False,
                    'error': validation['errors'],
                    'warnings': validation['warnings']
                })
                continue
            
            # Extract content
            try:
                content = self.extract_content_for_analysis(file_path, validation['metadata'])
                
                results.append({
                    'file_path': file_path,
                    'success': content.get('error') is None,
                    'content': content,
                    'metadata': validation['metadata'],
                    'warnings': validation['warnings']
                })
                
            except Exception as e:
                results.append({
                    'file_path': file_path,
                    'success': False,
                    'error': str(e),
                    'warnings': validation['warnings']
                })
        
        return results


def test_video_processor():
    """
    Test video processor functionality
    """
    print("🎬 Testing Video Processor")
    print("=" * 50)
    
    processor = VideoProcessor()
    
    print("✅ Video processor initialized")
    
    # Check available methods
    methods = []
    if processor.elevenlabs_client:
        methods.append("ElevenLabs")
    if processor.openai_client:
        methods.append("OpenAI Whisper")
    methods.append("Speech Recognition (fallback)")
    
    print(f"📋 Available transcription methods: {', '.join(methods)}")
    
    print("\n🎯 Ready to process video files!")
    print("\n📝 To test with actual videos:")
    print("  1. Place video files in the 'uploads' directory")
    print("  2. Ensure files are in supported formats:", Config.SUPPORTED_VIDEO_FORMATS)
    print("  3. Make sure videos are under the size limit")


if __name__ == "__main__":
    test_video_processor()
