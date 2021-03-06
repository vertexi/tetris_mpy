from PIL import Image
import pathlib
import os


def gif2jpg(file_name: str, num_key_frames: int = None,
            trans_color: tuple = (0, 0, 0),
            resize: tuple = None, output_dir: str = None, crop: tuple = None):
    """
    convert gif to `num_key_frames` images with jpg format
    :param file_name: gif file name
    :param num_key_frames: result images number
    :param trans_color: set converted transparent color in jpg image
    :param resize: resize image to maximum (width, height) dimension
    :param output_dir: set output images dir
    :param crop: image crop box dimension
    :return:
    """
    path = pathlib.PurePath(file_name)
    file_pure_name = path.name
    dot_pos = file_pure_name.rfind('.')
    directory_name = path.parents[0]
    if dot_pos != -1:
        file_pure_name = file_pure_name[:dot_pos]

    if output_dir:
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

    im = Image.open(file_name)
    if num_key_frames is None:
        num_key_frames = im.n_frames

    elif num_key_frames > im.n_frames:
        print("warning: the number of key frames is out of maximum frams in given gif image.")
        num_key_frames = im.n_frames
    im.close()

    with Image.open(file_name) as im:
        for i in range(num_key_frames):
            im.seek(im.n_frames // num_key_frames * i)
            image = im.convert("RGBA")
            if crop:
                image = image.crop(crop)
            datas = image.getdata()
            new_data = []
            for item in datas:
                if item[3] == 0:  # if transparent
                    new_data.append(trans_color)  # set transparent color in jpg
                else:
                    new_data.append(tuple(item[:3]))
            image = Image.new("RGB", image.size)
            image.getdata()
            image.putdata(new_data)
            if resize:
                image.thumbnail(resize, Image.ANTIALIAS)
            if output_dir:
                image.save('{}/{}{}.jpg'.format(output_dir, file_pure_name, i))
            else:
                image.save(
                    '{}/{}{}.jpg'.format(directory_name, file_pure_name, i))


def png2jpg(file_name: str, trans_color: tuple):
    """
    convert png file to jpg file
    :param file_name: png file name
    :param trans_color: set transparent color in jpg image
    :return:
    """
    with Image.open(file_name) as im:
        image = im.convert("RGBA")
        datas = image.getdata()
        new_data = []
        for item in datas:
            if item[3] == 0:  # if transparent
                new_data.append(trans_color)  # set transparent color in jpg
            else:
                new_data.append(tuple(item[:3]))
        image = Image.new("RGB", im.size)
        image.getdata()
        image.putdata(new_data)
        image.save('{}.jpg'.format(file_name))


def create_thumbnail(infile: str, size: tuple):
    im = Image.open(infile)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(infile)


left = 72
top = 0
right = 498-72
bottom = 249

# convert image.gif to 8 jpg images with white background
gif2jpg("utils/pikachu-love.gif", num_key_frames=17, trans_color=(0, 0, 0),
        resize=(100, 100), output_dir="img")
gif2jpg("utils/pikachu-pokemon.gif", num_key_frames=14, trans_color=(0, 0, 0),
        resize=(100, 100), output_dir="img", crop=(left, top, right, bottom))


def image_color_filter(filename, color_threshold_to_black, color):
    with Image.open(filename) as im:
        image = im.convert("RGB")
        datas = image.getdata()
        new_data = []
        for item in datas:
            if item[0] > color_threshold_to_black[0] \
                    and item[1] > color_threshold_to_black[1] \
                    and item[2] > color_threshold_to_black[2]:
                new_data.append(color)
            else:
                new_data.append(tuple(item[:3]))
        image.putdata(new_data)
        image.save(filename)

