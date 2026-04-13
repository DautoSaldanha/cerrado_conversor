import yt_dlp

url = input("Cole a URL do vídeo: ")

# Pega info
with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
    info = ydl.extract_info(url, download=False)
    formats = info.get('formats', [])

print("\n📺 Qualidades disponíveis:\n")

opcoes = []
for f in formats:
    # Só vídeo (mesmo sem áudio)
    if f.get('vcodec') != 'none':
        altura = f.get('height')
        ext = f.get('ext')
        tamanho = f.get('filesize')

        if altura:
            opcoes.append((f['format_id'], altura, ext, tamanho))

# Remove duplicadas por resolução
vistos = set()
opcoes_unicas = []
for op in sorted(opcoes, key=lambda x: x[1]):
    if op[1] not in vistos:
        vistos.add(op[1])
        opcoes_unicas.append(op)

for i, op in enumerate(opcoes_unicas):
    size_mb = (op[3] / 1024 / 1024) if op[3] else 0
    print(f"{i} - {op[1]}p ({op[2]}) - {round(size_mb, 2)} MB")

escolha = int(input("\nEscolha o número da qualidade: "))
format_id = opcoes_unicas[escolha][0]

print("\n⬇️ Baixando...\n")

ydl_opts = {
    'format': f'{format_id}+bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'merge_output_format': 'mp4'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("\n✅ Download concluído!")