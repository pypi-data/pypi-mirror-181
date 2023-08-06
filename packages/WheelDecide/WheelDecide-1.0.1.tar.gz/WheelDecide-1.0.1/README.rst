WheelDecide \_ 转盘决定命运
==================================

|License| |Pypi| |Author| |Github|

安装方法
--------

通过 pip 安装

::

   pip install WheelDecide

更新

::

   pip install WheelDecide --upgrade

使用方法
--------

导入

::

   import WheelDecide

使用

::

   w = WheelDecide.wheel()

   w.setinterval(1) <- 一个int类型，代表时间间隔

   w.setUnseletedBgcolor("white") <- 一个str类型，代表未选中的元素背景颜色

   w.setSeletedBgcolor("red") <- 一个str类型，代表已选中的元素背景颜色

   w.setupwheel(["1","2","3","4","a","b","c","d","!","?","#","%"]) <- 十二个str类型组成的list，代表转盘的元素


**!注意事项!**

*导入*
::

   import WheelDecide #√

   import wheeldecide #×

*使用*

::

   #setinterval值默认为1

   #setUnseletedBgcolor值默认为"white"

   #setSeletedBgcolor值默认为"red"

   ### setupwheel永远是最后一条指令！！！ ###
   
关于作者
--------
Author

*Jason4zh*

Email

*13640817984@163.com*

Package

*https://pypi.org/project/WheelDecide/*

Github

*https://github.com/Jason4zh/WheelDecide/*

::

   print("Thank you for using!")



本次更新修改v1.0.1
------------------

1. 添加了转盘元素背景颜色的自定义

.. |License| image:: https://img.shields.io/badge/License-BSD-yellow
   :target: https://github.com/Jason4zh/WheelDecide/blob/main/LICENSE
.. |Pypi| image:: https://img.shields.io/badge/Pypi-v1.0-blue
   :target: https://pypi.org/project/WheelDecide
.. |Author| image:: https://img.shields.io/badge/Author-Jason4zh-green
   :target: https://pypi.org/user/Jason4zh
.. |Github| image:: https://img.shields.io/badge/Github-Jason4zh-red
   :target: https://github.com/Jason4zh/WheelDecide
