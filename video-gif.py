#!/usr/bin/env python3

import subprocess as subp
import sys
import re
import glob


def main():
    if len(sys.argv) < 1:
        usage()
        sys.exit(1)

    generate_image2()
    image_seq = get_image_seq()
    dither = get_dither(image_seq)
    gif_name = input("gif name: ")

    reply = "y"
    while reply == "y":
        generate_gif(image_seq, dither, gif_name)
        reply = input("Generating gif again? (y/n): ")
        image_seq = get_image_seq()

    clear_png()


def usage():
    print("usage: {} video".format(sys.argv[0]))


def generate_image2():
    ss = input("start seek time (hh:mm:ss): ")
    validate(ss, r"\d{,2}:\d{,2}:\d{,2}")
    t = input("duration: ")
    validate(t, r"\d+")

    cmd = ["ffmpeg",
        "-ss", ss,
        "-i", sys.argv[1],
        "-t", t,
        "-s", "480x270",
        "-f", "image2",
        "%03d.png",
    ]
    try:
        subp.call(cmd)
    except:
        print("Error when generating image")
        print(sys.exc_info()[1])
        sys.exit(1)


def validate(s, format):
    if re.search(format, s):
        return
    print("Error in input format,")
    print("Got: {}".format(s))
    print("Expect: {}".format(format))
    sys.exit(1)



def get_dither(img_seq):
    prepare_cmd = [
        "-append",
        "-format", "%k",
        "info:"
    ]

    dither = 6
    for i in range(9,6,-1):
        prefix_cmd = get_prefix_cmd(img_seq,i)
        output = try_call(prefix_cmd, prepare_cmd)
        if output <= 256:
            dither = i
            break

    return dither


def try_call(pref, prep):
    try:
        output = subp.check_output(pref + prep)
    except:
        print("Error in preparing image")
        print(sys.exc_info()[1])
        sys.exit(1)

    return int(output)


def get_image_seq():
    full = input("image sequence (start end [skip]): ")
    fullint = [int(i) for i in full.split(" ")]

    start = fullint[0]
    end = fullint[1]

    if len(fullint) > 2:
        skip = fullint[2]
    else:
        skip = 1

    imger = lambda i: "{:03d}.png".format(i)

    return [imger(i) for i in range(start, end, skip)]


def get_prefix_cmd(img_seq, dither):
    return ["convert",
        "-delay", "1x8",
    ] + img_seq + [
        "-ordered-dither", "o8x8,{}".format(dither),
        "-coalesce",
        "-layers", "OptimizeTransparency",
    ]


def generate_gif(img_seq, dither, gif_name):
    final_cmd = [
       "+map",
        gif_name,
    ]

    prefix_cmd = get_prefix_cmd(img_seq, dither)

    try:
        subp.call(prefix_cmd + final_cmd)
    except:
        print("Generating gif error")
        print(sys.exc_info()[1])
        sys.exit(1)


def clear_png():
    png_files = glob.glob("???.png")
    try:
        subp.call(["rm"] + png_files)
    except:
        print("Clearing PNG Error")
        print(sys.exc_info()[1])
        sys.exit(1)

if __name__ == "__main__":
    main()

