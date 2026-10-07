#!/usr/bin/env python3
"""Genera public/media/ a partir del material fuente.

    python3 resources/build-media.py

Fuentes (rutas locales del autor; se pueden sobrescribir con variables de entorno):
  AVATAR    foto de perfil (resources/portrait-source.png por defecto)
  HOTPLATE  landing-page/public/media del repositorio smd-soldering-hotplate
  KLOG      landing/public/media del workspace de kLog
  CHROME    binario de Chrome/Chromium para renderizar og-cover.html

Requiere Pillow con soporte WebP.
"""
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
MEDIA = ROOT / 'public' / 'media'
HOME = Path.home()
AVATAR = Path(os.environ.get('AVATAR', ROOT / 'resources' / 'portrait-source.png'))
HOTPLATE = Path(os.environ.get('HOTPLATE', HOME / 'Projects/electronica/smi-soldering-hot-plate/landing-page/public/media'))
KLOG = Path(os.environ.get('KLOG', HOME / 'Projects/krisskira/klog/landing/public/media'))
CHROME = os.environ.get('CHROME', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')

BLUE, YELLOW, RED, DARK = '#2a74c0', '#f0df41', '#eb5151', '#1b1b1b'


def webp(source, target, width=None, quality=82):
    image = Image.open(source)
    image = image.convert('RGBA' if image.mode in ('RGBA', 'LA', 'P') else 'RGB')
    if width and image.width > width:
        image = image.resize((width, round(image.height * width / image.width)), Image.LANCZOS)
    image.save(MEDIA / target, 'WEBP', quality=quality, method=6)
    print(f'{target}: {image.width}x{image.height}')


def portrait(source):
    """Avatar ya editado (fondo transparente y anillo blanco): solo se reduce y pasa a WebP."""
    image = Image.open(source).convert('RGBA')
    image.thumbnail((720, 800), Image.LANCZOS)
    image.save(MEDIA / 'portrait.webp', 'WEBP', quality=82, method=6, exact=True)
    print(f'portrait.webp: {image.width}x{image.height}')


def icon(size, target):
    """Mismo dibujo que logo.svg: tres escalones con los colores de la marca."""
    scale = size / 64
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=14 * scale, fill=DARK)
    for x, y, color in ((12, 38, BLUE), (25, 25, YELLOW), (38, 12, RED)):
        draw.rounded_rectangle((x * scale, y * scale, (x + 14) * scale, (y + 14) * scale), radius=3 * scale, fill=color)
    image.save(MEDIA / target)
    print(f'{target}: {size}x{size}')


def og_cover():
    with tempfile.TemporaryDirectory() as tmp:
        shot = Path(tmp) / 'og.png'
        subprocess.run(
            [
                CHROME,
                '--headless=new',
                '--hide-scrollbars',
                '--force-device-scale-factor=1',
                '--allow-file-access-from-files',
                '--window-size=1200,630',
                f'--screenshot={shot}',
                (ROOT / 'resources' / 'og-cover.html').as_uri(),
            ],
            check=True,
            capture_output=True,
        )
        Image.open(shot).convert('RGB').save(MEDIA / 'og-cover.jpg', 'JPEG', quality=86, optimize=True, progressive=True)
    print('og-cover.jpg: 1200x630')


def main():
    MEDIA.mkdir(parents=True, exist_ok=True)
    portrait(AVATAR)
    webp(HOTPLATE / 'hotplate-demo-poster.jpg', 'hotplate-cycle.webp')
    webp(HOTPLATE / 'studio-heat.webp', 'hotplate-studio.webp', width=1440)
    webp(KLOG / 'screen-explorer.webp', 'klog-explorer.webp', width=1200)
    shutil.copyfile(HOTPLATE / 'hotplate-demo.mp4', MEDIA / 'hotplate-demo.mp4')
    print('hotplate-demo.mp4: copiado')
    icon(180, 'apple-touch-icon.png')
    icon(192, 'icon-192.png')
    icon(512, 'icon-512.png')
    og_cover()
    for leftover in ('placeholder.svg', 'og-cover.png'):
        (MEDIA / leftover).unlink(missing_ok=True)


if __name__ == '__main__':
    main()
