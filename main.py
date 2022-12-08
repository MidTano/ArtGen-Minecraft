from PIL import Image
import json
import glob


def get_blocks():
    with open('baked_blocks.json', 'r') as f:
        return json.load(f)


def get_image_data(img):
    return list(img.getdata())


def get_pixel_rgb(pixel):
    return {
        'red': pixel[0],
        'green': pixel[1],
        'blue': pixel[2],
    }


def get_pixel_id(pixel_rgb, blocks):
    temp = None
    for key, item in blocks.items():
        dev = abs(pixel_rgb["red"] - item[0]) + abs(pixel_rgb["green"] - item[1]) + abs(pixel_rgb["blue"] - item[2])
    if temp is None or dev < temp["dev"]:
        temp = {"id": key, "dev": dev}
    return temp['id']


def get_output(image_data, blocks):
    output = []
    for i in range(0, len(image_data)):
        pixel_rgb = get_pixel_rgb(image_data[i])
        output.append(get_pixel_id(pixel_rgb, blocks))

    return output


def main(image, ART_SIZE):
    img = Image.open(image)
    img = img.convert("RGB")

    img.save(image)

    img = Image.open(image)

    img = img.resize((ART_SIZE, ART_SIZE))
    img.save(image)

    blocks = get_blocks()
    img = Image.open(image)
    image_data = get_image_data(img)
    output = get_output(image_data, blocks)

    with open('blocks_13.json', 'r') as f:
        blocks_13 = json.load(f)

    for i in range(0, len(output)):
        for key in blocks_13:
            if output[i] == key['texture_image']:

                if 'block_id' in key:
                    output[i] = {'block_id': key['block_id'], 'data_id': key['data_id'], 'game_id': key['game_id']}

    return output


def save_output(mode, image, output, x, y, z):
    if mode == 3:
        with open("RAW_" + image + '.txt', 'w') as f:
            for i in range(0, len(output)):
                if type(output[i]) == dict:
                    f.write("/setblock ~{} ~{} ~{} {} {} replace".format(i % ART_SIZE, z, i // ART_SIZE,
                                                                         output[i]['game_id'],
                                                                         output[i]['data_id']) + "\n")
                else:
                    f.write("/setblock ~{} ~{} ~{} {}".format(i % ART_SIZE, z, i // ART_SIZE, output[i]) + "\n")
        return True

    with open(image + ".txt", 'w') as f:
        if mode == 2:
            f.write("mc.setBlocks({},{},{},{},{},{},20)\n".format(-x, y - 1, z, -x + ART_SIZE, y - 1, z + ART_SIZE))
        for i in range(0, len(output)):
            if type(output[i]) == dict:
                if mode == 1:
                    f.write("world.setBlock(" + str((i % ART_SIZE) - x) + "," + str(y) + "," + str(
                        (i // ART_SIZE) - z) + "," + str(
                        output[i]['block_id']) + "," + str(output[i]['data_id']) + ")\n")
                elif mode == 2:
                    f.write("mc.setBlock(" + str((i % ART_SIZE) - x) + "," + str(y) + "," + str(
                        (i // ART_SIZE) + z) + "," + str(
                        output[i]['block_id']) + "," + str(output[i]['data_id']) + ")\n")
                else:
                    print("Error mode")
                    return False
            else:
                if mode == 1:
                    f.write("world.setBlock(" + str((i % ART_SIZE) - x) + "," + str(y) + "," + str(
                        (i // ART_SIZE) - z) + "," + str(
                        output[i]) + ",0)\n")
                elif mode == 2:
                    f.write("mc.setBlock(" + str((i % ART_SIZE) - x) + "," + str(y) + "," + str(
                        (i // ART_SIZE) + z) + "," + str(
                        output[i]) + ",0)\n")
                else:
                    print("Error mode")
                    return False


def get_format_file():
    format_file = input("Select, convert image to:\n[1] - ProgKids\n[2] - ProgMine\n[3] - Raw data\n")
    if format_file == "1":
        x, y, z = 63, 0, 63
        ART_SIZE = 126
        mode = 1
    elif format_file == "2":
        x, y, z = 129, 120, 134
        ART_SIZE = 126
        mode = 2
    elif format_file == "3":
        x, y, z = 0, 0, 0
        ART_SIZE = 200
        mode = 3
    else:
        print("Error")
        exit()
    return x, y, z, ART_SIZE, mode


if __name__ == '__main__':

    x, y, z, ART_SIZE, mode = get_format_file()

    image_list = []
    for file in glob.glob("*.png"):
        image_list.append(file)
    for file in glob.glob("*.jpg"):
        image_list.append(file)

    image = input("Select:\n[1] - to convert all images in the folder\n[2] - to convert one image\n")
    if image == "1":
        for i in range(0, len(image_list)):
            print("Loading: " + str(i + 1) + "/" + str(len(image_list)))
            output = main(image_list[i], ART_SIZE)
            save_output(mode, image, output, x, y, z)
    elif image == "2":
        for i in range(0, len(image_list)):
            print(f"[{str(i + 1)}] - {image_list[i]}")
        image = input("Enter the image to convert\n")
        image = image_list[int(image) - 1]
        output = main(image, ART_SIZE)
        save_output(mode, image, output, x, y, z)
    else:
        print("Error")
        exit()
