import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime

r = sr.Recognizer()

# Função para detectar idioma falado
def detectar_idioma():
    with sr.Microphone() as source:
        print("Diga 'english' ou 'português' para escolher o idioma:")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            # Primeiro tenta reconhecer em inglês
            texto_en = r.recognize_google(audio, language="en-US").lower()
            print("Você disse (en-US):", texto_en)
            if "english" in texto_en:
                return "en"
        except:
            pass

        try:
            # Depois tenta reconhecer em português
            texto_pt = r.recognize_google(audio, language="pt-BR").lower()
            print("Você disse (pt-BR):", texto_pt)
            if "português" in texto_pt or "portugues" in texto_pt:
                return "pt"
        except:
            pass

        print("Idioma não reconhecido, usando padrão: português")
        return "pt"

idioma = detectar_idioma()

# Configura idioma do Wikipedia
wikipedia.set_lang("en" if idioma == "en" else "pt")

# Função para falar com a voz correta
def speak(command):
    mecanismo = pyttsx3.init()
    voices = mecanismo.getProperty("voices")

    for voice in voices:
        if idioma == "en" and "english" in voice.name.lower():
            mecanismo.setProperty("voice", voice.id)
            break
        elif idioma == "pt" and ("brazil" in voice.name.lower() or "português" in voice.name.lower()):
            mecanismo.setProperty("voice", voice.id)
            break

    mecanismo.say(command)
    mecanismo.runAndWait()

# Função principal
def commands():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening..." if idioma == "en" else "Escutando... pode perguntar...")
            audio = r.listen(source)

            texto = r.recognize_google(audio, language="en-US" if idioma == "en" else "pt-BR")
            texto = texto.lower()
            print("You said:" if idioma == "en" else "Você disse:", texto)

            # Comandos em inglês
            if idioma == "en":
                if "thank you" in texto:
                    print("Closing...")
                    speak("Closing...")
                    exit()
                elif "send" in texto:
                    msg = texto.replace("send", "", 1)
                    speak("Sending " + msg)
                    pywhatkit.sendwhatmsg_instantly("+5511977779334", msg)
                elif "play" in texto:
                    music = texto.replace("play", "")
                    speak("Playing " + music)
                    pywhatkit.playonyt(music)
                elif "date" in texto:
                    today = datetime.date.today()
                    speak("Today is " + str(today))
                elif "time" in texto:
                    now = datetime.datetime.now().strftime("%H:%M")
                    speak("It is " + now)
                elif "info" in texto:
                    person = texto.replace("info", "")
                    info = wikipedia.summary(person, 1)
                    speak(info)
                elif "search" in texto:
                    search_term = texto.replace("search", "")
                    pywhatkit.search(search_term)
                    speak("Searching " + search_term)

            # Comandos em português
            else:
                if "obrigado" in texto:
                    print("Por nada, qualquer dúvida ou ajuda é só chamar!")
                    speak("Por nada, qualquer dúvida ou ajuda é só chamar!")
                    exit()
                elif "enviar" in texto:
                    msg = texto.replace("enviar", "", 1)
                    speak("Enviando " + msg)
                    pywhatkit.sendwhatmsg_instantly("+5511977779334", msg)
                elif "tocar" in texto:
                    musica = texto.replace("tocar", "")
                    speak("Tocando " + musica)
                    pywhatkit.playonyt(musica)
                elif "data" in texto:
                    hoje = datetime.date.today()
                    meses = [
                        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
                        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
                    ]
                    dia = hoje.day
                    mes = meses[hoje.month - 1]
                    ano = hoje.year
                    data_formatada = f"{dia} de {mes} de {ano}"
                    speak("Hoje é " + data_formatada)
                elif "hora" in texto or "horas" in texto:
                    horario = datetime.datetime.now().strftime("%H:%M")
                    speak("Agora são " + horario)
                elif "procure" in texto:
                    pessoa = texto.replace("procure", "")
                    info = wikipedia.summary(pessoa, 1)
                    speak(info)
                elif "pesquisar" in texto:
                    pesquisa = texto.replace("pesquisar", "")
                    pywhatkit.search(pesquisa)
                    speak("Pesquisando " + pesquisa)

    except Exception as e:
        print("Erro ao capturar o áudio:" if idioma == "pt" else "Error capturing audio:", e)

# Loop
while True:
    commands()
