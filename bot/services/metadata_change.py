import base64

from mutagen.oggopus import OggOpus
from mutagen.flac import Picture


def write_metadata(
    audio_path: str,
    title: str,
    artist: str,
    album: str,
    thumbnail_path: str | None = None
):
    audio = OggOpus(audio_path)

    audio["TITLE"] = [title]
    audio["ARTIST"] = [artist]
    audio["ALBUM"] = [album]

    if thumbnail_path:
        picture = Picture()

        with open(thumbnail_path, "rb") as image:
            picture.data = image.read()

        picture.type = 3
        picture.mime = "image/jpeg"

        encoded = base64.b64encode(
            picture.write()
        ).decode("ascii")

        audio["metadata_block_picture"] = [encoded]

    audio.save()

    return audio_path