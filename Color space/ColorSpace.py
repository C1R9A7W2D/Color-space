from PIL import Image
import matplotlib.pyplot as plt

image = Image.open('Осетинские пироги.png')
image = Image.open('Жаба_крылова_.png')

r, g, b = image.split()

r.save('red_channel.png')
g.save('green_channel.png')
b.save('blue_channel.png')

r_colored = Image.merge("RGB", (r, Image.new('L', image.size), Image.new('L', image.size)))
g_colored = Image.merge("RGB", (Image.new('L', image.size), g, Image.new('L', image.size)))
b_colored = Image.merge("RGB", (Image.new('L', image.size), Image.new('L', image.size), b))

r_colored.save('red_colored.jpg')
g_colored.save('green_colored.jpg')
b_colored.save('blue_colored.jpg')

r_hist = r.histogram()
g_hist = g.histogram()
b_hist = b.histogram()

plt.figure(figsize=(10, 5))
plt.title('Гистограммы цветовых каналов')
plt.xlabel('Интенсивность')
plt.ylabel('Частота')
plt.xlim(0, 255)

plt.plot(r_hist, color='red')
plt.plot(g_hist, color='green')
plt.plot(b_hist, color='blue')

plt.show()
