Original Author: `Daniel Lee <Lee.Daniel.1986@gmail.com>`_

## 操作流程
0. 配置环境
   ```
   python
   opencv
   simplejson
   progressbar
   open3d==0.10.0.0
   ```
   均可通过 `pip install` 安装，其中前四个应该对版本要求不大，最后一个需要 `pip install opend3d==0.10.0.0`。
1. 运行 `show_webcams`
   - 在cmd输入 `python show_webcams -h` 查看帮助；
   - 在cmd输入`python show_webcams 1 2` 运行程序，`1`和`2`是摄像头编号，不同设备可能不同；
   - 运行成功则能看到两个摄像头拍摄画面。
2. 运行 `capture_chessboards`
   - 在cmd输入`capture_chessboards 1 2 n tmp\` 运行程序，`1`和`2`是摄像头编号，`n`是指定拍摄棋盘格数量， `tmp\`是保存棋盘格图像的路径，自行创建；
   - 生成的图像是 `.ppm` 格式的，可以下载 `Honeyview` 查看；
   - 我自己测试的存在`chessboard_output\`里了；
   - 理论上越多越好。
   
3. 运行 `calibrate_cameras`
   - 在cmd输入`calibrate_cameras tmp_1\ tmp_2\` 运行程序，`tmp_1\`是上面保存棋盘格图像的路径，`tmp_2\`是要保存标定数据的；
   - 我自己测试的存在`calibrare_output\`里了，输出为
      ```
      Reading input files...
      [========================================================================] 100%
      Calibrating cameras. This can take a while.
      The average error between chessboard points and their epipolar lines is 
      2.5703303146362306 pixels. This should be as small as possible.
      ```  
   - 运行结束后会返回像素值误差，越小越好。
4. 运行 `tune_blockmatcher`
   - 在cmd输入`python tune_blockmatcher tmp_1\ tmp_2\`运行程序，`tmp_1\`是保存标定数据的的路径，`tmp_2\`是双目相机拍到的两待测距图片；
   - 我自己测试的文件夹是`test_img\`
   - 不太懂，可以再看看教程，应该是调参的。

5. 运行 `images_to_pointcloud`
   - `python images_to_pointcloud calibrate_output\ test_img\left_1.ppm test_img\right_1.ppm cloud_2.ply`

6. 显示云图，可以直接vscode调试运行`show_cloud_point.py`（是我自己写的不用命令行了）

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