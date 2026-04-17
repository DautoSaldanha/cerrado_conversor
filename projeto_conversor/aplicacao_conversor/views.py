import yt_dlp
#from .services import instagram, youtube
from django.shortcuts import render, redirect

def home(request):
    if request.method == 'GET':
        return render(request, 'inicial/home.html')
    
    else:
        url = request.POST.get('url')
        tipo = request.POST.get('tipo')
        plataforma = request.POST.get('plataforma')

        return redirect(f"/{plataforma}?url={url}&tipo={tipo}")


import yt_dlp
import os
from django.http import FileResponse
from django.shortcuts import render

def youtube(request):

    # =========================
    # DOWNLOAD DIRETO
    # =========================
    if request.method == 'POST':
        url = request.POST.get('url')
        format_id = request.POST.get('format_id')

        caminho = 'video.mp4'

        ydl_opts = {
            'format': f'{format_id}+bestaudio/best',
            'outtmpl': caminho,
            'merge_output_format': 'mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        response = FileResponse(open(caminho, 'rb'), as_attachment=True)
        response['Content-Disposition'] = 'attachment; filename="video.mp4"'

        return response

    # =========================
    # LISTAR QUALIDADES
    # =========================
    url = request.GET.get('url')
    tipo = request.GET.get('tipo')

    opcoes_unicas = []

    if url:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])

        opcoes = []
        for f in formats:
            if f.get('vcodec') != 'none':
                altura = f.get('height')
                ext = f.get('ext')

                if altura:
                    opcoes.append({
                        'format_id': f['format_id'],
                        'altura': altura,
                        'ext': ext
                    })

        vistos = set()
        for op in sorted(opcoes, key=lambda x: x['altura']):
            if op['altura'] not in vistos:
                vistos.add(op['altura'])
                opcoes_unicas.append(op)

    return render(request, 'plataformas/youtube.html', {
        'url': url,
        'tipo': tipo,
        'opcoes': opcoes_unicas
    })
    
def instagram(request):
    url = request.GET.get('url')
    tipo = request.GET.get('tipo')
    
    print(url, tipo)
    
    return render(request, 'plataformas/instagram.html', {
        'url': url,
        'tipo': tipo
        })

def facebook(request):
    pass

def twitter(request):
    pass