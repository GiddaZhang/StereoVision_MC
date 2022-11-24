Original Author: `Daniel Lee <Lee.Daniel.1986@gmail.com>`_

## TODO
- 坐标系变换
- 物体识别

## Bug list

- 在`capture_chessboards`文件中的 `enforce_delay` 函数, `text_x` 和 `text_y` 必须是整数，修改为
  
    ```
    text_x = (int)((frames[0].shape[1] - text_size[0]) / 2)
    text_y = (int)((frames[0].shape[0] + text_size[1]) / 2)
    ```

- 不要用 `pip install stereovision` ，因为这样调用的库函数和从github上下载的不一样，里面有问题。可以 `pip uninstall stereovision` 之后将 `bin` 文件夹之中的文件移动到根目录中运行，这样调用的库函数来自本地的`stereovison`文件夹。

- 在 `stereovision\calibration` 文件中的函数 `calibrate_cameras` 调换参数顺序due to opencv版本。
  ref: `https://github.com/erget/StereoVision/pull/16`

- `tune_blockmatcher` 报错 `module 'cv2' has no attribute 'STEREO_BM_NARROW_PRESET'`
  从(https://github.com/sdlouhy/StereoVision)下载新库存到 `stereovision_new` 文件夹，`tune_blockmatcher` 与 `images_to_pointcloud` 也改用新的。

## Ref

- Building a stereo rig (https://github.com/erget/StereoVision#:~:text=Building%20a%20stereo,Producing%20point%20clouds)
- Stereo calibration (https://erget.wordpress.com/2014/02/28/calibrating-a-stereo-pair-with-python/)
- Tuning the block matcher (https://erget.wordpress.com/2014/05/02/producing-3d-point-clouds-from-stereo-photos-tuning-the-block-matcher-for-best-results/)
- Producing point clouds (https://erget.wordpress.com/2014/04/27/producing-3d-point-clouds-with-a-stereo-camera-in-opencv)
- opencv教程 (http://web.archive.org/web/20190203045746/https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_depthmap/py_depthmap.html)
- opencv官网 (https://opencv.org/releases/page/7/)
- 支持opencv3的库？ (https://github.com/sdlouhy/StereoVision)