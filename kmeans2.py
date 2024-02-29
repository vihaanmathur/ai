# Name: Vihaan Mathur
# Date: 3/9/22
#Implements k-means algorithm on any image. 


''' Test cases:
6 https://cf.geekdo-images.com/imagepage/img/5lvEWGGTqWDFmJq_MaZvVD3sPuM=/fit-in/900x600/filters:no_upscale()/pic260745.jpg
10 cute_dog.jpg
6 turtle.jpg
'''

from http.client import NETWORK_AUTHENTICATION_REQUIRED
import PIL
from PIL import Image
import urllib.request
import io, sys, os, random
import tkinter as tk
from PIL import Image, ImageTk  # Place this at the end (to avoid any conflicts/errors)

def choose_random_means(k, img, pix):
   means = [(1,2,3) for x in range(k)]
   for x in range(len(means)):
       a = round(random.uniform(0, img.size[0]), 5)
       b = round(random.uniform(0, img.size[1]), 5)
       means[x] = pix[a,b]
   return means

# goal test: no hopping
def check_move_count(mc):
   return([0 for x in range(len(mc))] == mc)

# calculate distance with the current color with each mean
# return the index of means
def dist(col, means):
   minIndex, dist_sum = 0, 255**2+255**2+255**2
   for x in range(len(means)): 
       dist = (means[x][0] - col[0])**2 + (means[x][1] - col[1])**2 + (means[x][2] - col[2])**2
       if(dist_sum) > dist:
           dist_sum = dist
           minIndex = x
   return minIndex  

def clustering(img, pix, cb, mc, means, count):
   #cb = count buckets 
   #mc = move count 
   #m = means 
   temp_mc =  []
   temp_pb =  [[] for x in means]
   temp_cb = [0 for x in means]
   for x in range(img.size[0]):
    for y in range(img.size[1]):
        r, g, b = pix[x, y]
        minIndex = dist((r, g, b), means)
        temp_cb[minIndex] += 1
        temp_pb[minIndex].append((r, g, b))
   #print('counts', temp_cb)
   for x in range(len(temp_pb)):
      new_r = 0 
      new_g = 0
      new_b = 0
      for y in temp_pb[x]:
         new_r += y[0]
         new_g += y[1]
         new_b += y[2]
      length = len(temp_pb[x])
      new_r = new_r/length
      new_g = new_g/length
      new_b = new_b/length
      means[x] = (new_r, new_g, new_b)
   #print('meanlas', means)
   temp_mc = [(a-b) for a, b in zip(temp_cb, cb)]
   print ('diff', count, ':', temp_mc)
   return temp_cb, temp_mc, means

def update_picture(img, pix, means):
   region_dict = {}
   for x in range(img.size[0]):
    for y in range(img.size[1]):
       r, g, b = pix[x,y]
       dist1 = dist((r, g, b), means)
       new_color = (int(means[dist1][0]), int(means[dist1][1]), int(means[dist1][2]))
       pix[x,y] = new_color
   return pix, region_dict
   


def distinct_pix_count(img, pix):
   distincts = {}
   max_col, max_count = pix[0, 0], 0
   for x in range(img.size[0]):
    for y in range(img.size[1]):
       r, g, b = pix[x,y]
       color = (r, g, b)
       if color not in distincts:
         distincts[color] = 1 
       else:
         distincts[color] += 1
       if(distincts[color]) > max_count:
          max_col = color
          max_count = distincts[color]
   print(max(distincts))
   return len(distincts), max_col, max_count


'''
def count_regions(img, region_dict, pix, means):
   region_count = [0 for x in means]
   return region_count
'''
 
def main():
   k = int(sys.argv[1])
   file = sys.argv[2]
   if not os.path.isfile(file):
      file = io.BytesIO(urllib.request.urlopen(file).read())
   
   window = tk.Tk() #create an window object
   
   img = Image.open(file)
   
   img_tk = ImageTk.PhotoImage(img)
   lbl = tk.Label(window, image = img_tk).pack()  # display the image at window
   
   pix = img.load()   # pix[0, 0] : (r, g, b) 
   print ('Size:', img.size[0], 'x', img.size[1])
   print ('Pixels:', img.size[0]*img.size[1])
   d_count, m_col, m_count = distinct_pix_count(img, pix)
   print ('Distinct pixel count:', d_count)
   print ('Most common pixel:', m_col, '=>', m_count)

   count_buckets = [0 for x in range(k)]
   move_count = [10 for x in range(k)]
   means = choose_random_means(k, img, pix)
   print ('random means:', means)
   count = 1
   while not check_move_count(move_count):
      count += 1
      count_buckets, move_count, means = clustering(img, pix, count_buckets, move_count, means, count)
      if count == 2:
         print ('first means:', means)
         print ('starting sizes:', count_buckets)
   pix, region_dict = update_picture(img, pix, means)  # region_dict can be an empty dictionary
   print ('Final sizes:', count_buckets)
   print ('Final means:')
   for i in range(len(means)):
      print (i+1, ':', means[i], '=>', count_buckets[i])
      
   img1_tk = ImageTk.PhotoImage(img)
   lbl = tk.Label(window, image = img1_tk).pack()  # display the image at window
   
   #img.save("kmeans/{}.png".format(1524344), "PNG")  # change to your own filename
   window.mainloop()
   #img.show()
   
if __name__ == '__main__': 
   main()

'''
def BFS(initial_state):
   Q = [initial_state]
   explored = {initial_state: "s"}
   while(len(Q) > 0):
      s = Q.pop(0)
      if (s == '_12345678'):
         return (display_path(s, explored))
      for a in generate_children(s):
         if a not in explored:
            Q.append(a)
            explored[a] = s
   return "No Solution"

def DFS(initial):
   Q = [initial]
   explored = {initial: "s"}
   while(len(Q) >= 0):
      if len(Q) == 0:
         return ("No solution")
      s = Q.pop()
      if (s == '_12345678'):
         return (display_path(s, explored))
      for a in generate_children(s):
         if a not in explored:
            Q.append(a)
            explored[a] = s
 '''
