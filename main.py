import argparse
import ffmpeg
import os
import sys

def main():
    parser = argparse.ArgumentParser(description='FFmpeg subtitle burner')
    parser.add_argument('-v', '--video', required=True, help='Video file path')
    parser.add_argument('-sub', '--subtitle', required=True, help='Subtitle file path')
    parser.add_argument('-o', '--output', default='output.mp4', help='Output video path')
    
    parser.add_argument('-t', '--text', help='Text to overlay on video')
    parser.add_argument('-topleft', action='store_true', help='Position text at top left')
    parser.add_argument('-topright', action='store_true', help='Position text at top right')
    parser.add_argument('-bottomleft', action='store_true', help='Position text at bottom left')
    parser.add_argument('-bottomright', action='store_true', help='Position text at bottom right')
    parser.add_argument('-left', type=int, default=10, help='Left margin in pixels')
    parser.add_argument('-right', type=int, default=10, help='Right margin in pixels')
    parser.add_argument('-top', type=int, default=10, help='Top margin in pixels')
    parser.add_argument('-bottom', type=int, default=10, help='Bottom margin in pixels')
    parser.add_argument('-fontsize', type=int, default=24, help='Font size')
    parser.add_argument('-fontcolor', default='white', help='Font color (e.g., white, yellow, red)')
    parser.add_argument('-bgcolor', help='Background color (e.g., black@0.5 for semi-transparent)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.video):
        print(f"[ERROR] Video not found: {args.video}")
        sys.exit(1)
    
    if not os.path.exists(args.subtitle):
        print(f"[ERROR] Subtitle not found: {args.subtitle}")
        sys.exit(1)
    
    filters = []
    
    subtitle_filter = f'subtitles={args.subtitle.replace("\\", "/")}'
    filters.append(subtitle_filter)
    
    if args.text:
        if args.topleft:
            x = str(args.left)
            y = str(args.top)
        elif args.topright:
            x = f'w-tw-{args.right}'
            y = str(args.top)
        elif args.bottomleft:
            x = str(args.left)
            y = f'h-th-{args.bottom}'
        elif args.bottomright:
            x = f'w-tw-{args.right}'
            y = f'h-th-{args.bottom}'
        else:  # default to topleft
            x = str(args.left)
            y = str(args.top)
        
        drawtext = f"drawtext=text='{args.text}':fontsize={args.fontsize}:fontcolor={args.fontcolor}:x={x}:y={y}"
        
        if args.bgcolor:
            drawtext += f":box=1:boxcolor={args.bgcolor}:boxborderw=5"
        
        filters.append(drawtext)
    
    vf_filter = ','.join(filters)
    
    print(f"[INFO] Using filter: {vf_filter}")
    
    (
        ffmpeg
        .input(args.video)
        .output(args.output,
                vf=vf_filter)
        .run(overwrite_output=True)
    )
    
    print(f"[SUCCESS] Output saved to: {args.output}")

if __name__ == "__main__":
    main()