#IMPORTS 
from PIL import Image
from math import sqrt

#Function definition
def get_pixel_value(x, y):
   width, height = image.size
   pixel = data[y * width + x]
   return pixel

def compare_column(x1,x2):
   
  dist = rd = gd = bd = 0
  for y in range(0,height):
    data1 = get_pixel_value(x1,y)
    data2 = get_pixel_value(x2,y)
    
    rd = abs(data1[0] - data2[0])
    gd = abs(data1[1] - data2[1])
    bd = abs(data1[2] - data2[2])
    dist += sqrt( ( rd*rd + gd*gd + bd*bd) )
  return dist/height

def show_result(list):
  unshredded = Image.new("RGBA", image.size)
  for i in range(0, len(list)):
    x1, y1 = (shredwidth * list[i]), 0
    x2, y2 = x1 + shredwidth, height
    source_region = image.crop((x1, y1, x2, y2))
    destination_point = (i * shredwidth, 0)
    unshredded.paste(source_region, destination_point)
  # Output the new image
  unshredded.save("unshredded.jpg", "JPEG")  
    
def compare_shred(shred1, shred2):
  col1 = (shred1 * shredwidth) + shredwidth - 1
  col2 = (shred2 * shredwidth) 
  return compare_column(col1, col2)

def grow_sorted_list(sense):   # sense = True ->       sense = Left <-
  inserted = True
  while(inserted == True):
    inserted = False
    bestfit_result = 0
    bestfit = 0
    for i in range (0, len(unsorted)):
      if (sense):
        comparison = compare_shred(sorted[-1],unsorted[i])
      else:
        comparison = compare_shred(unsorted[i], sorted[0])
      if(( comparison < bestfit_result) or (bestfit_result == 0)):
        bestfit_result = comparison
        bestfit = unsorted[i]
            
    if(bestfit_result < threshold):
      if(sense):
        sorted.append(bestfit)
      else:
        sorted.insert(0, bestfit)
      if (len(unsorted)==1):
        return
      unsorted.remove(bestfit)
      inserted=True
    else:
      return
  
  bestfit = 0
  bestfit_result = 0

  
def main():
  
  #global variables
  global filename
  global shredwidth
  global width
  global height
  global totalshreds
  global image
  global data
  global unsorted
  global sorted
  global threshold
  
  
  #defines
  filename="TokyoPanoramaShredded.png"
  shredwidth=32
  threshold=70
  unsorted = range (1 , 20)
  
  #Image Reading
  image = Image.open(filename)
  width, height = image.size
  totalshreds=width/shredwidth
  #print totalshreds
  data = image.getdata() # This gets pixel data
  
  #first shred first and then...
  sorted = [0]
  grow_sorted_list(True)  #to the right
  
  grow_sorted_list(False)  #to the left
  ##Tricky threshold increase because of black and white skyscrapper
  if (len(unsorted)>1):
    threshold = 85
    grow_sorted_list(False)
  show_result(sorted)

if __name__ == "__main__": 
  main()