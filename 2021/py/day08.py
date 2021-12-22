from collections import Counter
from operator import itemgetter
from string import ascii_lowercase
import string
from PIL import Image, ImageColor
import PIL
import itertools


def parse(str_):
    lst = [x.split(" | ") for x in str_]
    signal, output = map(list, zip(*lst))
    signal = [x.split() for x in signal]
    output = [x.split() for x in output]
    return signal, output


def day08a(inputs):
    signals, outputs = parse(inputs)
    out = [len(item) for sublist in outputs for item in sublist]
    return sum(itemgetter(2, 3, 4, 7)(Counter(out)))


#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....

#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg

# Just working out below some facts about the digit/pos combo
# figuring out how to logically determine the decoding sequence.

# 2: 1
# 3: 7
# 4: 4
# 5: 2 3 5 {a:3,b:1,c:2,d:3,e:1,f:2,g:3}
# 6: 0 6 9 {a:3,b:3,c:3,d:2,e:2,f:3,g:3}
# 7: 8
# all: {a:8,b:6,c:8,d:7,e:4,f:9,g:7}

# Ended up with:
# (assuming inputs are a scrambled mix of only 0-9 not repeated)
# pos a: check 1/7, the extra signal in 7 must be a (as 1+7 use pos c&f)
# pos e: count all total signals grouped, the signal with 4 must be e
#      - as above in 'all' counting all signals, e will be the signal with
#      - a 4 count.  Prob could have figured out b with this too (cnt 6)
# pos f: as above but it is only 9 counts
# pos b: comparing 4, to the sub of 2,3,5 (the sig that has only 1 in total of 235, also in common with 4 is b)
# pos c: 1 only has c or f, and we know f from above, so we can determine c from what isnt allocated in 1
# pos d: only d remains not allocated from 4
# pos g: only one left not allocated


def get_keys(dict_, val):
    res = []
    for key, value in dict_.items():
        if val == value:
            res.append(key)
    return res


def get_tabula_rasa(str_):
    str_ = ["".join(sorted(x)) for x in str_]
    res = []
    [res.append(x) for x in str_ if x not in res]
    signal_len_map = {}
    tabula_rasa = dict.fromkeys(ascii_lowercase[0:7], 0)
    for i in range(2, 8):
        signal_len_map[i] = []
    for entry in str_:
        signal_len_map[len(entry)].append(entry)
    # Determine sig 'e' by counting all signals and returning 4 counts
    sig_all = Counter("".join(str_))
    tabula_rasa["e"] = get_keys(sig_all, 4)[0]
    # Determine sig 'f' by counting all signals and returning 9 counts
    tabula_rasa["f"] = get_keys(sig_all, 9)[0]
    # get signal b and e by comparing 4 and 2,3 and 5
    sig_5 = Counter("".join(signal_len_map[5]))
    tabula_rasa["b"] = [x for x in signal_len_map[4][0] if x in get_keys(sig_5, 1)][0]

    # Deterimine sig 'a' by comparing 1 and 7
    tabula_rasa["a"] = [
        x for x in signal_len_map[3][0] if x not in signal_len_map[2][0]
    ][0]
    # Determine sig c from what isn't allocated from 1
    tabula_rasa["c"] = [
        x for x in signal_len_map[2][0] if x not in tabula_rasa.values()
    ][0]
    # Determine sig d from what isn't allocated from 4
    tabula_rasa["d"] = [
        x for x in signal_len_map[4][0] if x not in tabula_rasa.values()
    ][0]
    # Determine sig g from what isn't allocated at all
    tabula_rasa["g"] = [
        x for x in ascii_lowercase[0:7] if x not in tabula_rasa.values()
    ][0]

    return tabula_rasa


def ssd_to_int(str_):
    lst = str_.split()
    key = {
        "abcefg": "0",
        "cf": "1",
        "acdeg": "2",
        "acdfg": "3",
        "bcdf": "4",
        "abdfg": "5",
        "abdefg": "6",
        "acf": "7",
        "abcdefg": "8",
        "abcdfg": "9",
    }
    return [key["".join(sorted(x))] for x in lst]


def decode_string(str_, tabula_rasa):
    decoded_str = []
    for item in str_:
        s = ""
        for char in item:
            s += get_keys(tabula_rasa, char)[0]
        decoded_str.append(s)
    return " ".join(decoded_str)


def int_to_ssd(str_):
    key = {
        "0": "abcefg",
        "1": "cf",
        "2": "acdeg",
        "3": "acdfg",
        "4": "bcdf",
        "5": "abdfg",
        "6": "abdefg",
        "7": "acf",
        "8": "abcdefg",
        "9": "abcdfg",
    }
    return key[str_]


def create_ssd_image(encoded_inputs, decoded_inputs):

    border_pixels_top = 10
    border_pixels_left = 10
    digit_spacing_x = 8
    digit_spacing_y = 10

    colours = [(238, 75, 43), (0, 150, 255)]

    img_ssd = create_seven_segment(int_to_ssd("8"))
    ssd_height = img_ssd.height + digit_spacing_y
    ssd_width = img_ssd.width + digit_spacing_x
    width = (ssd_width * 15) + (border_pixels_left * 2)
    height = (border_pixels_top * 2) + (len(encoded_inputs) * ssd_height * 2)
    img = Image.new("RGBA", (width, height), color=(75, 75, 75, 255))
    alternating_lists = [
        x
        for x in itertools.chain.from_iterable(
            itertools.zip_longest(encoded_inputs, decoded_inputs)
        )
    ]
    for xidx, line in enumerate(alternating_lists):
        str_ = line.split()
        for yidx, digit in enumerate(str_):
            if digit != "|":
                img_ssd = create_seven_segment(digit, colours[xidx % 2])
                img.paste(
                    img_ssd,
                    (
                        border_pixels_top + (ssd_width * yidx),
                        border_pixels_left + (ssd_height * xidx),
                    ),
                    img_ssd,
                )

    img.save(f"day08.png")
    return True


def day08b(inputs, output_ssd=False):
    signals, outputs = parse(inputs)
    results = []
    decoded_inputs = []
    for signal, output in zip(signals, outputs):
        # Decode output
        tabula_rasa = get_tabula_rasa(signal)
        decoded_signal_ssd = decode_string(signal, tabula_rasa)
        decoded_output_ssd = decode_string(output, tabula_rasa)
        decoded_output_int = ssd_to_int(decoded_output_ssd)
        results.append(int("".join(decoded_output_int)))
        decoded_inputs.append(" | ".join([decoded_signal_ssd, decoded_output_ssd]))

    if output_ssd:
        create_ssd_image(inputs, decoded_inputs)

    return sum(results)


def rotate_image(img):
    return img.rotate(90, PIL.Image.NEAREST, expand=1)


def change_ssd_colour(img, colour):
    new_img = []
    if type(colour) == str:
        r, g, b = ImageColor.getrgb(colour)
    elif type(colour) == tuple:
        r, g, b = colour
    pixel_data = img.getdata()
    for pixel in pixel_data:
        if pixel[0:3] == (255, 255, 255):
            new_img.append((r, g, b, pixel[3]))
        else:
            new_img.append(pixel)
    img.putdata(new_img)
    return img


def create_seven_segment(str_, colour="White"):

    str_ = str_.lower()
    ssd = Image.open("../graphics/SevenSegmentDisplay.png")

    if type(colour) == tuple:
        ssd = change_ssd_colour(ssd, colour)
    elif colour != "White":
        ssd = change_ssd_colour(ssd, colour)

    ssd_outside = ssd.crop((0, 0, ssd.width, ssd.height / 2))
    ssd_inside = ssd.crop((0, ssd.height / 2, ssd.width, ssd.height))

    width = ssd.width + 20
    height = ssd.width * 2 + 20

    img = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))
    if "a" in str_:
        img.paste(
            ssd_outside,
            (int((img.width / 2) - (ssd_outside.width / 2)), 0),
            ssd_outside,
        )
    ssd_outside = rotate_image(ssd_outside)
    if "b" in str_:
        img.paste(
            ssd_outside,
            (0, 10),
            ssd_outside,
        )
    if "e" in str_:
        img.paste(
            ssd_outside,
            (0, ssd_outside.height + 10),
            ssd_outside,
        )
    ssd_outside = rotate_image(ssd_outside)
    if "g" in str_:
        img.paste(
            ssd_outside,
            (
                int((img.width / 2) - (ssd_outside.width / 2)),
                img.height - ssd_outside.height,
            ),
            ssd_outside,
        )
    ssd_outside = rotate_image(ssd_outside)
    if "c" in str_:
        img.paste(
            ssd_outside,
            (img.width - ssd_outside.width, 10),
            ssd_outside,
        )
    if "f" in str_:
        img.paste(
            ssd_outside,
            (img.width - ssd_outside.width, ssd_outside.height + 10),
            ssd_outside,
        )
    if "d" in str_:
        img.paste(
            ssd_inside,
            (
                10,
                int((img.height / 2) - (ssd_inside.height / 2)),
            ),
            ssd_inside,
        )

    basewidth = 20
    wpercent = basewidth / float(img.size[0])
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)

    return img


ex = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""".split(
    "\n"
)

# print(
#     day08b(
#         ["acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab".split()],
#         ["cdfeb fcadb cdfeb cdbaf".split()],
#     )
# )

day08b(ex, True)


def test_08_ex1a():
    assert day08a(ex) == 26


def test_08_ex1b():
    assert day08b(ex) == 61229


def test_08a(day08_lines):
    assert day08a(day08_lines) == 274


def test_08b(day08_lines):
    assert day08b(day08_lines) == 1012089


# if __name__ == "__main__":
