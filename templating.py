import cv2
import numpy

img = cv2.imread("./models_training/images/train/1657142454.923115_1.jpg")
img2 = cv2.imread("./img_tst2.jpeg")

template = cv2.imread("./models_training/images/train/1657142454.923115_0.jpg")

w,h = template.shape[:-1]

threshold = .4

# res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
# loc = numpy.where(res >= threshold)
# for pt in zip(*loc[::-1]):
#   cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)

res2 = cv2.matchTemplate(img2, template, cv2.TM_CCOEFF_NORMED)
loc2 = numpy.where(res2 >= threshold)
for pt in zip(*loc2[::-1]):
  cv2.rectangle(img2, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)

# cv2.imwrite('result.png', img)
cv2.imwrite('result2.png', img2)