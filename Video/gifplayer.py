    for ind, file in enumerate(gif_files):
        print(str(ind)+": "+file)
    print("Select gif to display (type number)")
    gif_number = int(input("Select gif to display (type number):"))
    return(gif_files[gif_number])

def retrieve_gif_frame(img, ind):
    img.seek(ind)
    palette = img.getpalette()
    img.putpalette(palette)
    new_im = Image.new("RGBA", img.size)
    new_im.paste(img)
    new_im = new_im.resize((w,h), Image.ANTIALIAS)
