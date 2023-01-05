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


from stereovision.stereo_cameras import StereoPair
import os
import time
import cv2

def main():
    """
    Show the video from two webcams successively.
    """

    # 修改此处指定摄像头序号
    lcam = 1
    rcam = 2
    capture_pic = True

    with StereoPair(devices=(lcam, rcam)) as pair:

        if not capture_pic:
            pair.show_videos()

        else:
            interval = 10       # 时间间隔
            output_folder = 'pics'
            i = 1
            while True:
                start = time.time()
                while time.time() < start + interval:
                    pair.show_frames(1)
                images = pair.get_frames()
                for side, image in zip(("left", "right"), images):
                    filename = "{}_{}.png".format(side, i)
                    output_path = os.path.join(output_folder, filename)
                    cv2.imwrite(output_path, image)
                i += 1

if __name__ == "__main__":
    main()
