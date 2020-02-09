import requests
import hashlib
import sys
import tempfile
from urllib.parse import urlencode

ENGINE_ID = 4
LANGUAGE_ID = 1
VOICE_ID = 1


def build_hash(text, engine, voice, language):
    fragments = [
        "<engineID>%s</engineID>" % engine,
        "<voiceID>%s</voiceID>" % voice,
        "<langID>%s</langID>" % language,
        "<ext>mp3</ext>",
        text,
    ]
    return hashlib.md5(''.join(fragments).encode('utf-8')).hexdigest()


def get_tts_url(text, engine, voice, language):
    hash = build_hash(text, engine, voice, language)
    params = [
        ('engine', engine),
        ('language', language),
        ('voice', voice),
        ('text', text),
        ('useUTF8', 1),
    ]
    params = [(key, value) for (key, value) in params if (key and value)]

    return 'http://cache-a.oddcast.com/c_fs/%s.mp3?%s' % (
        hash,
        urlencode(params),
    )


def get_audio(text):
    url = get_tts_url(text, ENGINE_ID, VOICE_ID, LANGUAGE_ID)
    file = open('audio.mp3', 'wb')
    response = requests.get(url)
    response.raise_for_status()
    file.write(response.content)
    file.close()
    return 'audio.mp3'


if __name__ == '__main__':
    get_audio("1917")
