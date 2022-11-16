Original Author: `Daniel Lee <Lee.Daniel.1986@gmail.com>`_

## Bug list

- 在函数 `enforce_delay`里, `text_x` 和 `text_y` 必须是整数，修改为
```
text_x = (int)((frames[0].shape[1] - text_size[0]) / 2)
text_y = (int)((frames[0].shape[0] + text_size[1]) / 2)
```
- 不要用`pip install stereovision`，因为这样调用的库函数和从github上下载的不一样，里面有问题。可以`pip uninstall stereovision`之后将`bin`文件夹之中的文件移动到根目录中运行，这样调用的库函数来自根目录中`stereovison`文件夹。