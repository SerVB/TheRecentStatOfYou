# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html
from PIL import Image, ImageDraw
import xmltodict
from shutil import copyfile


colors = {
    "badge_10": (224,   0,   0, 255),  # "red"
    "badge_11": (224, 160,  64, 255),  # "orange"
    "badge_12": (224, 224,   0, 255),  # "yellow"
    "badge_13": (  0, 224,   0, 255),  # "green"
    "badge_14": (  0, 160, 224, 255),  # "cyan"
    "badge_15": (160,   0, 160, 255),  # "violet"
}

SRC_XML = "src/gui/flash/atlases/battleAtlas.xml"
SRC_IMAGE = "src/gui/flash/atlases/battleAtlas.dds"
TARGET_XML = "target/gui/flash/atlases/battleAtlas.xml"
TARGET_IMAGE = "target/gui/flash/atlases/battleAtlas.png"


def main():
    atlas = xmltodict.parse(open(SRC_XML, "r", encoding="utf-8").read())

    coordinates = dict()
    for subTexture in atlas["root"]["SubTexture"]:
        if subTexture["name"] in colors.keys():
            coordinates[subTexture["name"]] = (
                int(subTexture["x"]),
                int(subTexture["y"]),
                int(subTexture["width"]),
                int(subTexture["height"]),
            )

    assert len(coordinates) == len(colors)

    image = Image.open(SRC_IMAGE)
    draw = ImageDraw.Draw(image)
    for badgeName, metrics in coordinates.items():
        rectangle = [metrics[0], metrics[1], metrics[0] + metrics[2], metrics[1] + metrics[3]]
        draw.rectangle(rectangle, fill=(0, 0, 0, 0))  # clear rect

        dx = metrics[2] / 4
        dy = metrics[3] / 4

        rectangle[0] += dx
        rectangle[2] -= dx
        rectangle[1] += dy
        rectangle[3] -= dy
        draw.ellipse(rectangle, fill=colors[badgeName], outline=(192, 192, 192, 128))

    image.save(TARGET_IMAGE)
    copyfile(SRC_XML, TARGET_XML)


if __name__ == "__main__":
    main()
