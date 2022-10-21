#thư viện dùng trong bot
from ast import Not
from platform import python_implementation
from winsound import PlaySound
import speech_recognition
from gtts import gTTS
from datetime import date, datetime
import webbrowser as wb
import os
import requests
import json
from urllib.request import urlopen
import playsound
import urllib.request
import urllib.parse
import re
dem = 0
tam = []
a = 0
j = 0
# hàm chuyển text sang sound
def speak(text):
	tam = gTTS(text = text, lang='vi')
	filename ='voice.mp3'
	tam.save(filename)
	playsound.playsound(filename)
	os.remove(filename)

while True:

	robot_hear = speech_recognition.Recognizer()
	with speech_recognition.Microphone() as mic:
		print("Robot: Tôi đang nghe")
		speak("Tôi đang nghe")
		audio_data = robot_hear.record(mic,duration=6)
		try:
			you = robot_hear.recognize_google(audio_data, language='vi').lower()
		except:
			you = ""
		print("You:" + you)

#các lệnh có thể thực thi
	if you == "":
		if dem <=2:
			dem = dem + 1
		else:
			break
		robot = "Tôi không thể nghe thấy, vui lòng thử lại"

	elif you[0].isalpha() == False:
		num=[]
		for word in you.split():
			if word.isdigit():
				num.append(word)
		tam = list(map(int,num))    
		chuoi_moi = you.replace(" ","")
		print("You:" + you)
		for i in range(len(chuoi_moi)):
			if chuoi_moi[i] == "+":
				a = tam[j]+tam[j+1]
			elif chuoi_moi[i] == "x":
				a = tam[j] * tam[j+1]
			elif chuoi_moi[i] == "/":
				a = tam[j] / tam[j+1]
			elif chuoi_moi[i] == "-":
				a = tam[j] - tam[j]
		robot = "Kết quả của bạn là: " + str(a)
	
	elif "xin chào" in you:
		robot = "Chào bạn"

	elif "ngày" in you:
		today = date.today()
		robot = today.strftime("Hôm nay là ngày %d tháng %m năm %y")
	
	elif "nhạc" in you:
		robot = "Bạn muốn nghe bài hát nào?"
		print("Robot: " + robot)
		speak(robot)
		with speech_recognition.Microphone() as mic:
			audio_data = robot_hear.record(mic,duration=6)
		try:
			you = robot_hear.recognize_google(audio_data, language='vi').lower()
		except:
			you = ""
		print("You:" + you)
		query_string = urllib.parse.urlencode({"search_query" : you})
		html_content = urllib.request.urlopen("https://www.youtube.com.hk/results?"+query_string)
		search_results = re.findall(r'url\"\:\"\/watch\?v\=(.*?(?=\"))', html_content.read().decode())
		if search_results:
			wb.open_new("http://www.youtube.com/watch?v={}".format(search_results[0]))
		robot =you + " đang mở"

	elif "google" in you:
		wb.open('https://www.google.com', new=1)
		robot = "Google đang mở"
	
	elif "vị trí" in you:
		url = 'http://ipinfo.io/json'
		response = urlopen(url)
		data = json.load(response)
		city = data['city']
		robot = "Bạn đang ở"+" "+city
	
	elif "thời tiết" in you:
		api_key = "317c4c433700801ccfc89195aa094a00"
		BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
		print("Robot: Vui lòng cho tôi biết thành phố bạn đang sống")
		speak("Vui lòng cho tôi biết thành phố bạn đang sống")
		with speech_recognition.Microphone() as mic:
			robot_hear = speech_recognition.Recognizer()
			audio_data = robot_hear.record(mic,duration=6)
			try:
				city = robot_hear.recognize_google(audio_data, language='vi')
			except:
				city = ""
				if city == "":
					print("Robot: Tôi không thể nghe thấy, hãy nhập")
					speak("Tôi không thể nghe thấy, hãy nhập")
					print("You:", end=" ")
					city = input()
			print("You:" + city)
		
		URL = BASE_URL + "q=" + city + "&lang=vi"+"&appid=" + api_key
		response = requests.get(URL).json()
		
		def kelvin_to_celcius(kelvin):
			celcius = kelvin - 273.15
			return celcius
		
		temp_kelvin = response['main']['temp']
		temp_celcius = kelvin_to_celcius(temp_kelvin)
		wind_speed = response['wind']['speed']
		humidity = response['main']['humidity']
		description = response['weather'][0]['description']

		print(f"Nhiệt độ: {temp_celcius:.2f} độ C")
		print(f"Độ ẩm: {humidity}% ")
		print(f"Tốc độ gió: {wind_speed}m/s")		
		print(f"Tổng quan thời tiết tại {city}: {description}")

		robot = "Thời tiết của thành phố "+ city
	

	elif "tạm biệt" in you:
		robot = "Tạm biệt"
		print("Robot: "+ robot)
		speak(robot)
		break
	
	else:
		robot = "Tôi đang học tập, tôi sẽ tìm nó giúp bạn"
		wb.open('https://www.google.com/search?q='+you)
	print("Robot:" + robot)
	speak(robot)