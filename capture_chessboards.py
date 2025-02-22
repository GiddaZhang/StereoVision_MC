#!/bin/python
# Copyright (C) 2014 Daniel Lee <lee.daniel.1986@gmail.com>
#
# This file is part of StereoVision.
#
# StereoVision is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# StereoVision is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with StereoVision.  If not, see <http://www.gnu.org/licenses/>.

"""
Take pictures of a chessboard visible to both cameras in a stereo pair.
"""

from progressbar import ProgressBar, Bar, Percentage
from stereovision.stereo_cameras import ChessboardFinder
import time
import os
import cv2


def main():
    lcam, rcam = 1, 2
    num_pictures = 50
    output_folder = 'chessboards/3'
    rows, columns = 9, 6

    progress = ProgressBar(maxval=num_pictures,
                           widgets=[Bar("=", "[", "]"),
                                    " ", Percentage()])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    progress.start()
    
    with ChessboardFinder((lcam, rcam)) as pair:

        # Sets initial position of windows, based on image size
        set_window_position(pair)

        for i in range(num_pictures):

            # Introduces a 5 second delay before the camera pair is scanned for new images
            enforce_delay(pair, 5)

            frames, corners = pair.get_chessboard(columns, rows, True)
            for side, frame in zip(("left", "right"), frames):
                number_string = str(i + 1).zfill(len(str(num_pictures)))
                filename = "{}_{}.ppm".format(side, number_string)
                output_path = os.path.join(output_folder, filename)
                cv2.imwrite(output_path, frame)

            progress.update(progress.maxval - (num_pictures - i))

            # Displays the recent accepted image pair. Helps in generating diverse calibration images.
            show_selected_frames(frames, corners, pair, columns, rows, True)

        progress.finish()
        cv2.destroyAllWindows()


def show_selected_frames(frames, corners, pair, columns, rows, draw_corners=False):
    """
    Display the most recently captured (left as well as right) images.
    If draw_corners is set to true, the identified corners are marked on the images.
    """

    if draw_corners:
        for frame, corner in zip(frames, corners):
            cv2.drawChessboardCorners(frame, (columns, rows), corner, True)

    cv2.imshow("{} selected".format(pair.windows[0]), frames[0])
    cv2.imshow("{} selected".format(pair.windows[1]), frames[1])


def enforce_delay(pair, delay):
    """
    Enforces a delay of 5 seconds. This helps the user to change the chessboard perspective.
    A timer is displayed indicating the time remaining before the next sample is captured.
    """

    font = cv2.FONT_HERSHEY_SIMPLEX
    line_type = cv2.LINE_4
    line_thickness = 4

    start_time = time.time()
    now = start_time

    while now - start_time < delay:

        frames = pair.get_frames()

        # Calculates the time remaining before the next sample is captured
        time_remaining = "{:.2f}".format(delay - now + start_time)

        # Estimating the scale factor.
        font_scale = get_approx_font_scale(frames[0], time_remaining, font, line_thickness)

        text_size = cv2.getTextSize(time_remaining, font, font_scale, line_thickness)[0]

        # Calculates the position of the text
        ### Gidda: text_x & text_y must be integer
        text_x = (int)((frames[0].shape[1] - text_size[0]) / 2)
        text_y = (int)((frames[0].shape[0] + text_size[1]) / 2)

        for frame, window in zip(frames, pair.windows):
            cv2.putText(frame, time_remaining, (text_x, text_y), font, font_scale, (255, 50, 50),
                        line_thickness, line_type)
            cv2.imshow(window, frame)

        cv2.waitKey(1)
        now = time.time()


def get_approx_font_scale(frame, text, font, line_thickness):
    """
    Approximate the font scale for the timer display.
    """

    _, width = frame.shape[:2]
    target_width = width / 2

    base_text_size = cv2.getTextSize(text, font, 1.0, line_thickness)[0]
    scale_factor = float(target_width) / base_text_size[0]

    return scale_factor


def set_window_position(pair):

    """
    Set initial the positions of windows.
    The top left and right windows display the live cam stream with timer overlay.
    The bottom left and right windows display recently selected frame.
    """

    frames = pair.get_frames()
    pair.show_frames(1)

    # Setting initial position of cameras
    cv2.moveWindow(pair.windows[0], 0, 0)
    cv2.moveWindow(pair.windows[1], frames[1].shape[1], 0)

    # Setting initial position of selected frames
    cv2.namedWindow("{} selected".format(pair.windows[0]), cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("{} selected".format(pair.windows[0]), 0, frames[0].shape[0] + 30)

    cv2.namedWindow("{} selected".format(pair.windows[1]), cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("{} selected".format(pair.windows[1]), frames[1].shape[1], frames[1].shape[0] + 30)


if __name__ == "__main__":
    main()
