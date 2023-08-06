import cv2
import os
import numpy as np

def rvec_to_vec_to_transf(rvec,tvec):
    R = cv2.Rodrigues(rvec)
    T = np.eye(4)
    T[:3,:3] = R[0]
    T[:3,3] = tvec.squeeze()
    return T

def transf_to_rvec_to_vec(T):
    rvec = cv2.Rodrigues(T[:3,:3])[0]
    tvec = T[:3,3]
    return rvec, tvec

def draw_frame_axes(img, K, dist_coeffs, T, size=10):
    img = img.copy()
    rvec, tvec = transf_to_rvec_to_vec(T)
    cv2.drawFrameAxes(img, K, dist_coeffs, rvec, tvec, size)
    return img

def get_charuco_cb_pose(img, board, K, dist_coeffs, req_det_markers=6):
    corners, ids, rejectedImgPoints = aruco.detectMarkers(img, board.dictionary)
    if ids is not None and len(ids) >= req_det_markers:
        ret, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(corners, ids, img, board)
        if charuco_corners is not None:
            retval, rvec, tvec = aruco.estimatePoseCharucoBoard(charuco_corners, charuco_ids, board, K, dist_coeffs, np.array([]), np.array([]))
            if retval:
                # convert to transformation matrix
                T = rvec_to_vec_to_transf(rvec,tvec)
                return T
    return None



def create_board(squares_x, squares_y, cb_sq_width, aruco_sq_width, aruco_dict_str, start_id):
    aruco_dict = aruco.Dictionary_get(getattr(aruco, aruco_dict_str))
    aruco_dict.bytesList=aruco_dict.bytesList[start_id:,:,:]
    board = aruco.CharucoBoard_create(squares_x,squares_y,cb_sq_width,aruco_sq_width,aruco_dict)
    return board

def load_board_from_dict(board_dict):
    squares_x = board_dict['square_x']
    squares_y = board_dict['square_y']
    cb_sq_width = board_dict['cb_sq_width']
    aruco_sq_width = board_dict['aruco_sq_width']
    aruco_dict_str = board_dict['aruco_dict_str']
    start_id = board_dict['start_id']
    return create_board(squares_x, squares_y, cb_sq_width, aruco_sq_width, aruco_dict_str, start_id)
