import yt_dlp
from django.shortcuts import render, redirect
import os
from django.http import FileResponse
import tempfile
import threading

def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    
    else:
        url = request.POST.get('url')
        tipo = request.POST.get('tipo')
        plataforma = request.POST.get('plataforma')

        return redirect(f"/{plataforma}?url={url}&tipo={tipo}")


def youtube(request):
    url = request.GET.get('url')
    tipo = request.GET.get('tipo')

    if request.method == 'POST':
        format_id = request.POST.get('format_id')

        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, '%(title)s.%(ext)s')

        # DEFINE FORMATO
        if tipo == 'audio':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }]
            }

        elif tipo == 'video':
            ydl_opts = {
                'format': format_id,
                'outtmpl': output_path
            }

        else:  # ambos
            ydl_opts = {
                'format': f'{format_id}+bestaudio/best',
                'outtmpl': output_path,
                'merge_output_format': 'mp4'
            }

        # DOWNLOAD
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            # Ajusta extensão final
            if tipo == 'audio':
                filename = os.path.splitext(filename)[0] + '.mp3'
            elif tipo == 'ambos' and not filename.endswith('.mp4'):
                filename = os.path.splitext(filename)[0] + '.mp4'

            file = open(filename, 'rb')
            response = FileResponse(file, as_attachment=True)
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'

            # =========================
            # LIMPEZA AUTOMÁTICA
            # =========================
            def cleanup():
                try:
                    file.close()
                    if os.path.exists(filename):
                        os.remove(filename)
                    if os.path.exists(temp_dir):
                        os.rmdir(temp_dir)
                except Exception as e:
                    print("Erro ao limpar arquivo:", e)

            threading.Timer(5, cleanup).start()

            return response

        except Exception as e:
            return render(request, 'home.html', {
                'erro': str(e),
                'url': url,
                'tipo': tipo
            })

    # =========================
    # GET = LISTAR QUALIDADES
    # =========================
    opcoes_unicas = []
    titulo = None

    if url:
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)

            titulo = info.get('title')
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

        except Exception as e:
            print("Erro ao buscar info:", e)

    # =========================
    # SEMPRE RETORNA
    # =========================
    return render(request, 'home.html', {
        'url': url,
        'tipo': tipo,
        'opcoes': opcoes_unicas,
        'titulo': titulo
    })

    
def instagram(request):
    url = request.GET.get('url')
    tipo = request.GET.get('tipo')

    if request.method == 'POST':
        format_id = request.POST.get('format_id')

        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, '%(title)s.%(ext)s')

        # =========================
        # DEFINE FORMATO
        # =========================
        if tipo == 'audio':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                }]
            }

        elif tipo == 'video':
            ydl_opts = {
                'format': format_id or 'bestvideo/best',
                'outtmpl': output_path
            }

        else:  # ambos
            ydl_opts = {
                'format': f'{format_id}+bestaudio/best' if format_id else 'bestvideo+bestaudio/best',
                'outtmpl': output_path,
                'merge_output_format': 'mp4'
            }

        # =========================
        # DOWNLOAD
        # =========================
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            # Corrige extensão final
            if tipo == 'audio':
                filename = os.path.splitext(filename)[0] + '.mp3'

            elif tipo == 'ambos':
                filename = os.path.splitext(filename)[0] + '.mp4'

            file = open(filename, 'rb')

            response = FileResponse(
                file,
                as_attachment=True
            )

            response['Content-Disposition'] = (
                f'attachment; filename="{os.path.basename(filename)}"'
            )

            # =========================
            # LIMPEZA AUTOMÁTICA
            # =========================
            def cleanup():
                try:
                    file.close()

                    if os.path.exists(filename):
                        os.remove(filename)

                    if os.path.exists(temp_dir):
                        os.rmdir(temp_dir)

                except Exception as e:
                    print("Erro ao limpar:", e)

            threading.Timer(5, cleanup).start()

            return response

        except Exception as e:
            return render(request, 'home.html', {
                'erro': str(e),
                'url': url,
                'tipo': tipo
            })

    # =========================
    # GET = LISTAR QUALIDADES
    # =========================
    opcoes_unicas = []
    titulo = None

    if url:
        try:
            with yt_dlp.YoutubeDL({
                'quiet': True
            }) as ydl:

                info = ydl.extract_info(
                    url,
                    download=False
                )

            titulo = info.get('title')
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

            for op in sorted(
                opcoes,
                key=lambda x: x['altura']
            ):

                if op['altura'] not in vistos:
                    vistos.add(op['altura'])
                    opcoes_unicas.append(op)

        except Exception as e:
            print("Erro ao buscar info Instagram:", e)

    return render(request, 'home.html', {
        'url': url,
        'tipo': tipo,
        'opcoes': opcoes_unicas,
        'titulo': titulo
    })

def facebook(request):
    pass

def twitter(request):
    pass