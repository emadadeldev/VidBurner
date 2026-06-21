import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--video", required=True)
    parser.add_argument("-sub", "--subtitle", required=True)
    parser.add_argument("-o", "--output", default="output.mp4")

    parser.add_argument("-t", "--text")

    parser.add_argument("-font", "--fontfile",
                        default=r"C:\Windows\Fonts\arial.ttf")

    parser.add_argument("-fontsize", type=int, default=24)
    parser.add_argument("-fontcolor", default="white")
    parser.add_argument("-bgcolor")

    parser.add_argument("-topleft", action="store_true")
    parser.add_argument("-topright", action="store_true")
    parser.add_argument("-bottomleft", action="store_true")
    parser.add_argument("-bottomright", action="store_true")

    parser.add_argument("-left", type=int, default=10)
    parser.add_argument("-right", type=int, default=10)
    parser.add_argument("-top", type=int, default=10)
    parser.add_argument("-bottom", type=int, default=10)

    parser.add_argument(
        "-q", "--quality",
        choices=["360", "720", "1080"],
        help="Output resolution"
    )

    args = parser.parse_args()

    ffmpeg_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "bin",
        "ffmpeg.exe"
    )

    if not os.path.exists(ffmpeg_path):
        print("[ERROR] FFmpeg not found:")
        print(ffmpeg_path)
        sys.exit(1)

    if not os.path.exists(args.video):
        print("[ERROR] Video not found")
        sys.exit(1)

    if not os.path.exists(args.subtitle):
        print("[ERROR] Subtitle not found")
        sys.exit(1)

    if args.quality == "360":
        vf_filter += ",scale=-2:360"

    elif args.quality == "720":
        vf_filter += ",scale=-2:720"

    elif args.quality == "1080":
        vf_filter += ",scale=-2:1080"

    filters = []

    subtitle_path = os.path.abspath(args.subtitle)
    subtitle_path = subtitle_path.replace("\\", "/")
    subtitle_path = subtitle_path.replace(":", "\\:")

    filters.append(
        f"subtitles='{subtitle_path}'"
    )

    if args.text:

        if args.topright:
            x = f"w-tw-{args.right}"
            y = str(args.top)

        elif args.bottomleft:
            x = str(args.left)
            y = f"h-th-{args.bottom}"

        elif args.bottomright:
            x = f"w-tw-{args.right}"
            y = f"h-th-{args.bottom}"

        else:
            x = str(args.left)
            y = str(args.top)

        font_path = os.path.abspath(args.fontfile)
        font_path = font_path.replace("\\", "/")
        font_path = font_path.replace(":", "\\:")

        text = args.text
        text = text.replace("\\", "\\\\")
        text = text.replace(":", "\\:")
        text = text.replace("'", "\\'")

        drawtext = (
            f"drawtext="
            f"fontfile='{font_path}':"
            f"text='{text}':"
            f"fontsize={args.fontsize}:"
            f"fontcolor={args.fontcolor}:"
            f"x={x}:"
            f"y={y}"
        )

        if args.bgcolor:
            drawtext += (
                f":box=1"
                f":boxcolor={args.bgcolor}"
                f":boxborderw=5"
            )

        filters.append(drawtext)

    vf_filter = ",".join(filters)

    cmd = [
        ffmpeg_path,
        "-i", args.video,
        "-vf", vf_filter,
        "-c:v", "libx265",
        "-preset", "veryslow",
        "-crf", "30",
        "-c:a", "aac",
        "-b:a", "64k",
        "-movflags", "+faststart",
        "-y",
        args.output
    ]

    print()
    print("[INFO] FFmpeg Command:")
    print(" ".join(cmd))
    print()

    try:
        subprocess.run(cmd, check=True)

        print()
        print("[SUCCESS]")
        print(args.output)

    except subprocess.CalledProcessError:
        print()
        print("[ERROR] FFmpeg failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
