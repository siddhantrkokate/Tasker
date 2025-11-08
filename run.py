import os
import sys
import subprocess
from datetime import datetime

def check_and_install_dependencies():
	"""Check if required packages are installed, if not install them automatically."""
	required_packages = {
		'sounddevice': 'sounddevice',
		'numpy': 'numpy',
		'speech_recognition': 'SpeechRecognition',
		'pyttsx3': 'pyttsx3',
		'win32com': 'pywin32',
		'requests': 'requests'
	}
	
	missing_packages = []
	
	# Check which packages are missing
	for import_name, package_name in required_packages.items():
		try:
			__import__(import_name)
		except ImportError:
			missing_packages.append(package_name)
	
	# Install missing packages
	if missing_packages:
		print("=" * 60)
		print("First-time setup: Installing required dependencies...")
		print("=" * 60)
		print(f"Missing packages: {', '.join(missing_packages)}")
		print("\nThis may take a few minutes. Please wait...\n")
		
		for package in missing_packages:
			try:
				print(f"Installing {package}...")
				subprocess.check_call([sys.executable, "-m", "pip", "install", package])
				print(f"✓ {package} installed successfully\n")
			except subprocess.CalledProcessError as e:
				print(f"✗ Failed to install {package}: {e}")
				print("Please install it manually using: pip install " + package)
				sys.exit(1)
		
		print("=" * 60)
		print("All dependencies installed successfully!")
		print("=" * 60)
		print("\n")

# Check and install dependencies before importing them
check_and_install_dependencies()

import wave
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import main as tasker_one
from modules import gemini as ai

def record_voice_to_file(filename="output.wav", duration=None):
	"""
	Records voice from microphone and saves to a WAV file. Press Enter or Space to stop early.
	If duration is set, records for that many seconds.
	"""
	import threading
	import msvcrt
	import time
	stop_flag = threading.Event()

	def wait_for_key():
		while True:
			if msvcrt.kbhit():
				key = msvcrt.getch()
				if key in [b'\r', b' ']:
					stop_flag.set()
					break
	key_thread = threading.Thread(target=wait_for_key)
	key_thread.daemon = True
	key_thread.start()

	CHANNELS = 1
	RATE = 16000
	print(f"Recording... Press Enter or Space to stop.")
	
	# Record audio data
	audio_data = []
	start_time = time.time()
	
	def audio_callback(indata, frames, time, status):
		if status:
			print(f"Audio status: {status}")
		audio_data.extend(indata[:, 0])
	
	with sd.InputStream(samplerate=RATE, channels=CHANNELS, callback=audio_callback, dtype='int16'):
		while True:
			if stop_flag.is_set():
				break
			if duration and (time.time() - start_time) > duration:
				break
			sd.sleep(100)  # Sleep for 100ms
	
	# Convert to numpy array and save as WAV
	audio_array = np.array(audio_data, dtype=np.int16)
	
	wf = wave.open(filename, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(2)  # 16-bit = 2 bytes
	wf.setframerate(RATE)
	wf.writeframes(audio_array.tobytes())
	wf.close()
	print(f"Saved recording to {filename}")
	return filename

def speech_to_text_from_file(filename):
	"""
	Converts speech in a WAV file to text using multiple recognition methods.
	"""
	recognizer = sr.Recognizer()
	
	try:
		with sr.AudioFile(filename) as source:
			# Adjust for ambient noise
			recognizer.adjust_for_ambient_noise(source, duration=0.5)
			audio = recognizer.record(source)
		
		# Try Google Speech Recognition first (requires internet)
		try:
			text = recognizer.recognize_google(audio)
			if text.strip():
				return text.strip()
		except (sr.UnknownValueError, sr.RequestError):
			pass
		
		# Fallback to Windows Speech Recognition (offline)
		try:
			import win32com.client
			sapi = win32com.client.Dispatch("SAPI.SpVoice")
			file_stream = win32com.client.Dispatch("SAPI.SpFileStream")
			file_stream.Open(filename)
			
			recognizer_sapi = win32com.client.Dispatch("SAPI.SpInProcRecoContext")
			text = recognizer_sapi.CreateResultFromObject(file_stream).PhraseInfo.GetText()
			if text and text.strip():
				return text.strip()
		except:
			pass
		
		# Final fallback - return empty if all methods fail
		print("Could not understand audio")
		return ""
		
	except Exception as e:
		print(f"Error in speech recognition: {e}")
		return ""


import pyttsx3

def speak(text):
	engine = pyttsx3.init()
	# Set properties for more natural speech
	rate = engine.getProperty('rate')
	engine.setProperty('rate', int(rate * 0.85))  # slower, more natural
	volume = engine.getProperty('volume')
	engine.setProperty('volume', 1.0)  # max volume
	voices = engine.getProperty('voices')
	# Try to select a more expressive voice if available
	for v in voices:
		if 'female' in v.name.lower():
			engine.setProperty('voice', v.id)
			break
		elif 'zira' in v.name.lower():
			engine.setProperty('voice', v.id)
			break
	# Optionally, adjust pitch (not all engines support this)
	try:
		engine.setProperty('pitch', 70)  # lower pitch for warmth
	except Exception:
		pass
	engine.say(text)
	engine.runAndWait()

# Setup API keys on first run
print("Initializing Tasker One...")
ai.setup_api_keys()

# Example usage:

while True:
	record_voice_to_file()
	response = speech_to_text_from_file("output.wav")
	# response = "whenever my battery is 100% that time in loud voice speak battery is changed!"
	if response.strip().lower() == "stop":
		break
	print("\nYou:", response)
	response_ai = tasker_one.automate_task(response)
	print("\nTasker One:", response_ai)
	speak(response_ai)
