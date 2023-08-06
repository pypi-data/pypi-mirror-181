import numpy as np
import cv2


def draw_centered_line(img_size, angle, line_width):
    # draw a line that goes through the center of the image
    img = np.zeros(img_size)
    center = np.array(img_size) / 2
    x1 = 0
    y1 = int(center[1] - np.tan(angle) * center[0])
    x2 = img.shape[1]
    y2 = int(center[1] + np.tan(angle) * (img.shape[1] - center[0]))
    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 5)
    return img

def weighted_mean_row_index(img, threshold=20, verbose=0):
    assert img.ndim == 2
    img = np.where(img > threshold, img, 0)
    if verbose:
        cv2.imshow('img', img)
        cv2.waitKey(0)
    # find index weighted mean
    indeces = np.arange(img.shape[1])
    mean = np.sum(indeces * img, axis=1) / np.sum(img, axis=1)
    return mean

def row_list_to_points(row_list):
    ys = np.arange(len(row_list))
    xs = row_list
    return np.vstack([xs, ys, np.ones(len(xs))]).T

def draw_homg_line(img, l):
    assert l.shape[0] == 3
    out = img.copy()
    x1 = 0
    y1 = int(-l[2] / l[1])
    x2 = img.shape[1]
    y2 = int(-(l[2] + l[0] * x2) / l[1])
    cv2.line(out, (x1, y1), (x2, y2), (255, 0, 0), 1)
    return out

def fit_homogenous_line(points):
   assert points.shape[1] == 3
   # find m,c using least squares
   points = np.asarray(points)
   n, _ = points.shape
   mean_x = np.mean(points[:,0])
   mean_y = np.mean(points[:,1])
   sum_xy = sum([points[i,0]*points[i,1] for i in range(n)])
   sum_x = sum([points[i,0] for i in range(n)])
   sum_y = sum([points[i,1] for i in range(n)])
   sum_x2 = sum([points[i,0]**2 for i in range(n)])
   slope = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x**2)
   intercept = mean_y - slope*mean_x
   return np.array([-slope, 1, -intercept])

def overlap_gray_imgs_rgb(img1, img2):
    assert img1.shape == img2.shape
    rgb_overlap = np.dstack([img1, np.zeros(img1.shape), img2])
    return rgb_overlap

def get_laser_line_as_homg(img, threshold, verbose=0):
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    mean = weighted_mean_row_index(img, threshold, verbose)
    points = row_list_to_points(mean)
    l = fit_homogenous_line(points)
    if verbose:
        zero_img = np.zeros(img.shape)
        cv2.imshow('img', overlap_gray_imgs_rgb(img, draw_homg_line(zero_img, l)))
        cv2.waitKey(0)
    return l



if __name__ == '__main__':
    img = draw_centered_line((500, 500), np.pi / 2.1, 5)
    # blur img
    img = cv2.GaussianBlur(img, (5, 5), 0)

    l = get_laser_line_as_homg(img, 20, verbose=1)

