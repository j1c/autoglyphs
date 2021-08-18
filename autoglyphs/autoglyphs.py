from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from web3 import Web3

SIZE = 64
HALF_SIZE = 32
ONE = int("100000000", base=16)

SCHEME = {
    1: bytes.fromhex("2E582F5C2e"),  # X/\
    2: bytes.fromhex("2E2B2D7C2e"),  # +-|
    3: bytes.fromhex("2E2F5C2E2e"),  # /\
    4: bytes.fromhex("2E5C7C2D2F"),  # \|-/
    5: bytes.fromhex("2E4F7C2D2e"),  # O|-
    6: bytes.fromhex("2E5C5C2E2e"),  # \
    7: bytes.fromhex("2E237C2D2B"),  # |-+
    8: bytes.fromhex("2E4F4F2E2e"),  # OO
    9: bytes.fromhex("2E232E2E2e"),  # #
    10: bytes.fromhex("2E234F2E2e"),  # #O
}


def get_scheme(a):
    index = a % 83
    if index < 20:
        scheme = 1
    elif index < 35:
        scheme = 2
    elif index < 48:
        scheme = 3
    elif index < 59:
        scheme = 4
    elif index < 68:
        scheme = 5
    elif index < 73:
        scheme = 6
    elif index < 77:
        scheme = 7
    elif index < 80:
        scheme = 8
    elif index < 82:
        scheme = 9
    else:
        scheme = 10

    return SCHEME[scheme]


def generate_glyph(seed):
    a = Web3.toInt(Web3.solidityKeccak(["uint256"], [seed])[-20:])
    mod = (a % 11) + 5
    symbols = get_scheme(a)
    output = []

    for i in range(SIZE):
        y = 2 * (i - HALF_SIZE) + 1

        if a % 3 == 1:
            y = -y
        elif a % 3 == 2:
            y = abs(y)

        y = y * a

        for j in range(SIZE):
            x = 2 * (j - HALF_SIZE) + 1

            if a % 2 == 1:
                x = abs(x)

            x = x * a
            v = int((x * y / ONE) % mod)

            if v < 5:
                value = chr(symbols[v])
            else:
                value = "."

            output.append(value)
        output.append("\n")  # newline

    art = "".join(output)
    return art


def plot_glyph(art):
    fig, ax = plt.subplots(dpi=300, figsize=(5, 5))

    ax.xaxis.set_visible(False)  # same for y axis.
    ax.yaxis.set_visible(False)  # same for y axis.
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    plotting_str = art.replace("\n", "")
    plotting_str = [plotting_str[i : i + 64] for i in range(0, len(plotting_str), 64)]

    ax.set_ylim(65, -1)
    ax.set_xlim(-1, 65)

    c = "k"
    lw = 0.9

    for x, chars in enumerate(plotting_str):
        for y, char in enumerate(chars):
            if char == ".":
                continue
            elif char == "O":
                circ = Circle((x + 0.5, y + 0.5), 0.5, color=c, fill=False)
                ax.add_patch(circ)
            elif char == "-":
                ax.plot([x, x + 1], [y + 0.5, y + 0.5], c=c, lw=lw)
            elif char == "|":
                ax.plot([x + 0.5, x + 0.5], [y, y + 1], c=c, lw=lw)
            elif char == "X":
                ax.plot([x, x + 1], [y, y + 1], c=c, lw=lw)
                ax.plot([x + 1, x], [y, y + 1], c=c, lw=lw)
            elif char == "/":
                ax.plot([x, x + 1], [y, y + 1], c=c, lw=lw)
            elif char == "\\":
                ax.plot([x + 1, x], [y, y + 1], c=c, lw=lw)
            elif char == "#":
                rect = Rectangle((x, y), 1, 1, color=c, lw=0)
                ax.add_patch(rect)
            elif char == "+":
                ax.plot([x + 0.5, x + 0.5], [y, y + 1], c=c, lw=lw)
                ax.plot([x, x + 1], [y + 0.5, y + 0.5], c=c, lw=lw)
    return fig


def mint(seed, out_path):
    p = Path(out_path)
    art = generate_glyph(seed)

    plotting_str = art.replace("\n", "")
    if len(set(plotting_str)) == 1:  # Degenerate cases
        raise ValueError("Degenerate seed")

    fig = plot_glyph(plotting_str)

    fig.savefig(p / f"autoglyph_{seed}.png", pad_inches=1)

    plt.close("all")
