import yt_dlp

url = input("Cole a URL do vídeo do Instagram: ")

ydl_opts = {
    'outtmpl': '%(title)s.%(ext)s',  # nome do arquivo
    'format': 'best',  # melhor qualidade disponível
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])