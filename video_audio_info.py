import ffmpeg

def get_video_audio_info(file_path):
    # Use ffmpeg.probe to get metadata of the media file
    probe = ffmpeg.probe(file_path)
    
    # Extract overall bitrate
    format_info = probe.get('format', {})
    overall_bitrate = int(format_info.get('bit_rate', 0))  # Overall bitrate (bps)

    # Extract stream-specific bitrates and audio FPS
    video_bitrate = None
    audio_bitrate = None
    audio_fps = None

    for stream in probe['streams']:
        if stream['codec_type'] == 'video' and 'bit_rate' in stream:
            video_bitrate = int(stream['bit_rate'])  # Video stream bitrate (bps)
        if stream['codec_type'] == 'audio':
            audio_bitrate = int(stream.get('bit_rate', 0))  # Audio stream bitrate (bps)
            audio_fps = int(stream.get('sample_rate', 0))  # Audio sampling rate (Hz)
            audio_codec = stream['codec_name']

    return {
        "overall_bitrate": int(overall_bitrate / 1000) if overall_bitrate else None,
        "video_bitrate": int(video_bitrate / 1000) if video_bitrate else None,
        "audio_bitrate": int(audio_bitrate / 1000) if audio_bitrate else None,
        "audio_fps": audio_fps,  # Audio sampling rate in Hz
        "audio_codec": audio_codec
    }

# Example usage
# file_path = "1.mp4"
# info = get_video_audio_info(file_path)

# print("Overall Bitrate: ", info['overall_bitrate'], "kbps")
# print("Video Bitrate: ", info['video_bitrate'], "kbps")
# print("Audio Bitrate: ", info['audio_bitrate'], "kbps")
# print("Audio FPS (Sampling Rate): ", info['audio_fps'], "Hz")
