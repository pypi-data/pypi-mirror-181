import PIL.Image

ASCII_CHARS = ['@','#','$','%','?','*','+',';',':',',','.']

def resize(image,new_width=100):
    width,height = image.size
    ratio = height/width
    new_height = int(new_width*ratio)
    resized_img = image.resize((new_width,new_height))
    return resized_img

def gray(image):
    grayy = image.convert('L')
    return grayy

def px_ascii(image):
    pxls = image.getdata()
    print(pxls,'====================')
    chars = "".join([ASCII_CHARS[pxl//25] for pxl in pxls])
    return chars




def main(new_width=10):
    path = 'macha-removebg-preview.png'
    image = PIL.Image.open(path)
    img_data = px_ascii(gray(resize(image)))

    pxl_count = len(img_data)
    print(pxl_count,'=============')
    acss_img = "\n".join(img_data[i:(i+new_width)] for i in range(0,pxl_count,new_width))

    print(acss_img)

if __name__ ==  '__main__':
    main(new_width=100)