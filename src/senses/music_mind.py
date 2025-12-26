import logging
import queue
import threading
import time

import librosa
import numpy as np
import pyaudio

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("MusicMind")

class MusicMind:
    def __init__(self, rate=22050, chunk=2048):
        self.rate = rate
        self.chunk = chunk
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.running = False
        self.audio_queue = queue.Queue()
        self.analysis_thread = None

    def start_listening(self):
        """Starts the audio stream and analysis thread."""
        self.running = True
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunk,
                                  stream_callback=self._audio_callback)

        self.stream.start_stream()
        logger.info("👂 MusicMind is listening... (Play some music!)")

        self.analysis_thread = threading.Thread(target=self._analyze_loop)
        self.analysis_thread.start()

    def stop_listening(self):
        """Stops the listening process."""
        self.running = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        if self.analysis_thread:
            self.analysis_thread.join()
        logger.info("🛑 MusicMind stopped.")

    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Callback to capture audio chunks."""
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        self.audio_queue.put(audio_data)
        return (in_data, pyaudio.paContinue)

    def _analyze_loop(self):
        """Continuous analysis loop."""
        buffer = np.array([], dtype=np.float32)
        buffer_duration = 5.0 # Analyze 5-second windows
        buffer_size = int(self.rate * buffer_duration)

        while self.running:
            try:
                # Get new data
                new_data = self.audio_queue.get(timeout=1)
                buffer = np.concatenate((buffer, new_data))

                # Keep buffer at fixed size
                if len(buffer) > buffer_size:
                    buffer = buffer[-buffer_size:]

                    # Analyze only when we have enough data
                    self._process_music(buffer)

            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in analysis loop: {e}")

    def _process_music(self, y):
        """Extracts musical features and maps to affect."""
        try:
            # 1. Tempo (BPM)
            tempo, _ = librosa.beat.beat_track(y=y, sr=self.rate)

            # 2. Spectral Centroid (Brightness)
            cent = librosa.feature.spectral_centroid(y=y, sr=self.rate)
            avg_brightness = np.mean(cent)

            # 3. RMS Energy (Loudness/Intensity)
            rms = librosa.feature.rms(y=y)
            avg_loudness = np.mean(rms)

            # 4. Chroma (Harmony)
            chroma = librosa.feature.chroma_stft(y=y, sr=self.rate)
            avg_chroma = np.mean(chroma, axis=1)

            # --- Affective Mapping (Heuristic) ---
            mood = "Neutral"

            # Energy/Arousal
            if avg_loudness > 0.05:
                if tempo > 120:
                    mood = "Energetic/Intense"
                elif tempo < 90:
                    mood = "Powerful/Solemn"
                else:
                    mood = "Active"
            else:
                if tempo > 120:
                    mood = "Nervous/Fluttering"
                elif tempo < 90:
                    mood = "Calm/Melancholic"
                else:
                    mood = "Quiet"

            # Brightness modifier
            if avg_brightness > 3000:
                mood += " (Bright)"
            elif avg_brightness < 1000:
                mood += " (Dark)"

            # Log the experience
            logger.info(f"🎵 Music Analysis:")
            logger.info(f"   Tempo: {tempo:.1f} BPM")
            logger.info(f"   Intensity: {avg_loudness:.4f}")
            logger.info(f"   Brightness: {avg_brightness:.1f} Hz")
            logger.info(f"   Affective State: {mood}")
            logger.info("-" * 30)

        except Exception as e:
            logger.error(f"Feature extraction error: {e}")

if __name__ == "__main__":
    mind = MusicMind()
    try:
        mind.start_listening()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mind.stop_listening()
