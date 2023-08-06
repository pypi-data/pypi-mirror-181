#!/usr/bin/python3

from datetime import timedelta
from enum import IntEnum
from operator import floordiv, truediv
from os import getcwd, remove
from os.path import basename, dirname, isfile, join, realpath, splitext
from random import randrange
from subprocess import call, check_output

from iso639 import Language

from tnmake import __project__, __version__
from tnmake.logging import get_basic_logger
logger = get_basic_logger() # stdout only
from rapidjson import loads  # python wrapper around rapidjson


def hrunits(value: int) -> str: # human-readable units

    for unit in ['bytes', 'KiB', 'MiB', 'GiB', 'TiB']:

        if value < 1024:
            return f'{value:0.1f} {unit}'
        value = truediv(value, 1024)

    return f'{value:0.1f} PiB' # pebibyte = 1024^5 bytes

StreamType = IntEnum('StreamType', 'Video Audio SubTitle', start = 0)

def gcd(a: int, b: int) -> int:
    '''
    computes the greatest common divisor of the integers a and b
    '''
    return a if b == 0 else not a % b and b or gcd(b, a % b)

def unify(title: str) -> str:
    '''
    '''
    if title is None:
        return ''
    return ' '.join(map(lambda x: x[0].upper() + x[1:], ''.join(filter(lambda x: x.isalnum() or x == ' ', title.replace(chr(45), chr(32)))).split()))


class Thumbnail:

    def __init__(self, options: dict):

        logger.info(f'{__project__} v{__version__}')
        self.fpath = dirname(realpath(__file__))
        self.options = {
            'comment': options.get('comment').strip(),
            'extension': options.get('ext', 'jpg'),
            'font': options.get('font') or '', # default system font
            'fontsize': options.get('size') or 13,
            'grid': options.get('layout', f'3x8'),
            'quality': options.get('quality', 100),
            # 'tfont': join(self.fpath, 'ColabLig.otf'), # Personal Use Only
            'width': options.get('width', 1150)
            }
# DBG # -----------------------------------------------------------------------
        for k, v in self.options.items(): # dump options
            logger.debug(f'"{k}": {v}') # for debug purposes
# --- # -----------------------------------------------------------------------

    def perform(self, video: str, output = None):

        filename, ext = (lambda t: (t[0], t[1][1:]))(splitext(basename(video)))
        metadata = loads(
            check_output(['ffprobe',
                '-v', 'error',
                '-show_entries',
                'format=duration,size,bit_rate:stream=codec_name,codec_long_name,profile,codec_type,bit_rate,sample_rate,width,height,pix_fmt,field_order,display_aspect_ratio,r_frame_rate,level,channel_layout,sample_fmt,channels:stream_tags=language,title,BPS',
                '-of', 'json', video]))
        duration = int(float(metadata['format']['duration'])) # seconds
        streams = [[],[],[]] # codec_type -> [0]video, [1]audio, [2]subtitle
        filesize = int(metadata['format']['size']) # bytes
        # go through all streams and fetch required metadata
        for stream in metadata['streams']:
            avg = False # calculated bitrate is probably average
            # try to get codec short name
            codec_name = stream.get('codec_name', 'unknown')
            if codec_name in ['png']: # ignore list
                continue
            m = Language.match(stream.get('tags', {}).get('language'))
            language = m.name if m else 'Unknown'
            if stream['codec_type'] == 'subtitle':
                title = unify(stream['tags'].get('title')) # .replace(language, '')
                streams[StreamType.SubTitle].append(
                    f'{language}{" (" + title + ")" if title else ""}')
                continue # enough information for subtitles
            # try to get bitrate of a stream
            bitrate = stream.get('bit_rate') # or "None" by default
            if not bitrate or bitrate in ['0', '1', 'N/A']:
                bitrate = stream.get('tags', {}).get('BPS')
            if not bitrate:
                avg = True
                bitrate = metadata.get('format').get('bit_rate')
            if bitrate is not None:
                bitrate = str(floordiv(int(bitrate), 1000))
            # handle video codec type specific tags
            if stream['codec_type'] == 'video':
                self.options['pointsize'] = truediv(stream['height'], 4.4)
            # try to get video resolution
                resolution = f'{stream["width"]}x{stream["height"]}'
            # try to get display aspect ratio, e.g. 16:9
                ratio = stream.get(
                    'display_aspect_ratio',
                    (lambda w, h: f'{floordiv(w, gcd(w, h))}:{floordiv(h, gcd(w, h))}')(stream['width'], stream['height']))
            # try to get fps, frames per second
                fps = (lambda x: truediv(x[0], x[1]))(list(map(int, stream['r_frame_rate'].split(chr(47)))))
            # try to get encode profile
                profile = stream.get('profile') # could be empty
                level = (lambda x: f'{x[:1]}.{x[1:]}' if len(x)>1 else f'L{x}')(str(stream['level']))
                # pix_fmt = stream.get('pix_fmt', 'Unknown')
                # field_order = stream.get('field_order', 'Unknown').title()
            # append a stream desc string to the corresponding stream list
                streams[StreamType.Video].append(
                    f'Video: {codec_name.title()} ({profile}@{level}) {bitrate} kbps{" (avg)" if avg else ""}, {resolution} ({ratio}) at {fps:0.3f} fps')
            else:
            # try to get sample rate in Hz
                sample_rate = stream.get('sample_rate')
            # try to get channel_layout
                channel_layout = stream.get('channel_layout').title().replace('(', ' (')
                sample_fmt = stream.get('sample_fmt', 'Unknown')
            # save parsed stream as a string
                streams[StreamType.Audio].append(
                    f'Audio: {codec_name.upper()} ({language}), {floordiv(float(sample_rate), 1000):0.1f} kHz, {channel_layout}, {sample_fmt}, {bitrate} kbps')
# DBG # -----------------------------------------------------------------------
        for s in streams[:-1]:
            for x in s:
                logger.debug(f'"{x}"')
        logger.debug(f'"Subtitles: {", ".join(streams[2]) or "Not Present"}"')
# --- # -----------------------------------------------------------------------
    # PART 2: Snapshot Taking
        shots = (lambda x: x[0]*x[1])(list(map(int, self.options['grid'].split('x'))))
        framelist = []
        if not output or output.endswith(chr(47)):
            output = f'{output or ""}{filename}'
        thumbnail = join(getcwd(), f'{output or filename}.bmp')
        for i in range(shots):
            step = floordiv(duration, shots)
            if step <= 0:
                raise Exception('The delay between screenshots is zero or less!')
            frame = step * i + randrange(step)
            # append a frame id to the frame list
            framelist.append(join(getcwd(), f'frame{frame:06d}.bmp'))
            call(['ffmpeg', '-ss', str(frame), '-v', 'error', '-i', video, '-vframes', '1', framelist[-1], '-y'])
            call(['convert', framelist[-1],
                # '-undercolor', 'white',
                '-pointsize', f'{self.options["pointsize"]:.0f}',
                '-gravity', 'South',
                '-stroke', 'rgba(0,0,0,0.750)',
                # '-strokewidth', '1',
                '-fill', 'rgba(255,255,255,0.20)',
                '-annotate', '+0+30', f'{str(timedelta(seconds=frame)).zfill(8)}',
                framelist[-1]])
        # concate screenshots to a pre-defined grid layout
        call(['montage', '-tile', self.options.get('grid'), '-geometry', '+3+3', *framelist, thumbnail])
        # adjust the thumbnail width to a value you prefere
        call(['mogrify', '-resize', str(self.options.get('width')), thumbnail])
        # create an annotation containing tech information
        n, st_string = len(streams[StreamType.SubTitle]), 'Not Present'
        if n:
            st_string = ', '.join(streams[2][:3]) + (f' and {n - 3} more' if n > 3 else '')
        annotation = (
            f'Filename: {filename}.{ext}\n'
            f'{chr(10).join([i for j in streams[:2] for i in j])}\n' # video & audio streams
            f'Duration: {str(timedelta(seconds=duration)).zfill(8)}, ' # hh:mm:ss
            f'Size: {filesize:,} Bytes ({hrunits(filesize)})'
            f'{chr(10) if len(streams[StreamType.SubTitle]) > 2 else ", "}'
            f'Subtitles: {st_string}'
            f'{chr(10) + "Comment: " + self.options.get("comment") if self.options.get("comment") else ""}')
        # render annotation string ('annotation.bmp')
        convert = ['convert']
        if self.options.get('font'):
            convert.extend(['-font', self.options.get('font')])
        call([*convert,
            '-density', '300', # 288
            '-resize', '25%',
            '-pointsize', str(self.options.get('fontsize')),
            f'label:{annotation}',
            'annotation.bmp']) # create annotation
        # calculate height of annotation.bmp plus padding
        height = int(check_output(['identify',
            '-ping',
            '-format', '%h',
            'annotation.bmp'])) + 10
        # concatenate annotation and thumbnail to one image file
        call(['convert',
            thumbnail,
            '-quality', str(self.options.get('quality')),
            '-splice', f'0x{height}',
            '-draw', 'image over 5,5 0,0 annotation.bmp',
            f'{thumbnail[:-3]}{self.options.get("extension")}'])
# CLR # -----------------------------------------------------------------------
        remove(join(getcwd(), 'annotation.bmp'))
        for i in framelist:
            remove(i)
        if self.options.get('extension') != 'bmp': remove(thumbnail)
# --- # -----------------------------------------------------------------------

# Thumbnail!MAKER creates customisable thumbnails and adds some tech details in the picture's header
