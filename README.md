<<<<<<< HEAD
好的，以下是关于这个软件的说明文档：

# 多机器人路径规划GUI程序说明文档

## 简介

此软件是一个基于蚁群算法的GUI程序，可以帮助用户在自定义的环境中找到最短路径，支持多机器人在同一环境中的路径规划。并将结果保存为.jpg和.gif格式。
该软件具有清晰的用户界面，可以轻松重置起点和终点，可自定义蚁群算法相关参数。拥有全新原创算法“Dead-Cell”算法大幅提高搜索效率。

## 安装

在使用本软件之前，请确保您已经若你已配置好相关环境，并将所有文件下载到同一目录下。可以通过运行Ant GUI.py文件启动程序。若没有配置相关环境，也可以直接运行Ant GUI.exe程序。

## 使用方法

### 创建环境

在程序界面中，您可以选择使用自己创建的环境，或者在界面右上方从预设的环境中选择一个进行测试。如果您选择创建自己的环境，可以通过在界面中点击“CREATE NOW！！”来直接绘制障碍物和起点终点等来创建环境。若您只是想创建一个临时环境，你可以在接下来的弹窗中选择“Don’t Save”。您也可以单击右侧的“Randomize！！”和“Randomize a Maze!”来随机生成环境或迷宫。

### 寻找最短路径

一旦您选择好了环境，首先可以通过点击“Reset Start and End”按钮来部署机器人的起点和终点（左键改变障碍状态，右键设置起点或者终点），设置完起点和终点后，您可以通过单击“Run”按钮来启动蚁群算法，寻找最短路径。您可以通过单击“Set Parameters”按钮来调整蚁群算法的相关参数，如迭代次数、蚂蚁数量、信息素蒸发系数等，以便获得更好的结果。界面左边的四个选择分别代表是否使用“Dead-Cell”算法、是否将本次结果保存为动图、是否画出蚁群算法的中间过程、是否选择四向行动（适合求解迷宫）。

### 保存结果

当蚁群算法完成寻路任务后，会有一个弹窗，询问你是否要将本次寻路的环境应用到下次寻路中。此设定的存在是为了适应“Dead-Cell”算法。因为此算法的功能是在蚂蚁寻路过程中不断排除环境中的无效点。于是，若在弹窗中选择“yes”，则表明您不满意此次的寻路结果，您可以再次更改蚂蚁迭代次数和蚂蚁只数等相关参数，在已经被排除大部分环境中无效点的新环境中再次进行寻路，直到用户满意为止。因此，比较推荐的做法是先运行“20次迭代，100只蚂蚁”，排除掉环境中大部分无效点，然后再运行“80次迭代，100只蚂蚁”以获得更好的结果。
若在弹窗中选择“No”，那么软件会认为用户接受此次的寻路结果，并将保存此次的结果。您可以在images文件夹中找到你的结果。你也可以在主界面的Setting中更改你的保存路径。

## 其他功能

除了上述主要功能外，该程序还具有以下功能：

- “Dead-cell”算法：一种新的算法，可以有效减少迭代次数，提高算法效率。

- 多机器人路径规划：支持在同一环境中同时规划多个机器人的最短路径。在得到数个机器人的最短路径后，单击“Multiplayer plan”按钮即可得到多个机器人之间实现完美的避碰处理后的路径规划，并得到保存在Robots下的gif结果动图

## 注意事项

- 请确保parameter.pkl和save_path.pkl文件与Ant GUI.exe或Ant GUI.py文件在同一目录下。

- 若出现更改保存路径后软件无法运行的情况，可将最初的两个pkl备份文件覆盖此时的两个pkl文件即可。

- 规划多机器人的路径时，其优先级是按照结果次序来的。例如：从Solutuion-1到Solutuion-9，优先级依次递减。

- 在删除已有的规划好的机器人路径时，只能从最后一个机器人往前删除，因此在规划机器人寻路次序时务必小心。


## 结束语

多机器人路径规划GUI程序是一个功能丰富的路径规划软件，可以帮助用户快速在自定义的环境中找到最短路径。如果您在使用过程中遇到任何问题或有任何建议，请随时联系我们。


Multi-robot Path Planning GUI Program User Guide
Introduction
This software is a GUI program based on the ant colony algorithm, which helps users find the shortest path in a customized environment and supports multi-robot path planning in the same environment. The results can be saved as .jpg and .gif formats. The software has a clear user interface, which allows users to easily reset the start and end points and customize the ant colony algorithm-related parameters. It also has a brand new original algorithm "Dead-Cell" algorithm which significantly improves search efficiency.

Installation
Before using this software, please make sure you have configured the relevant environment and downloaded all files into the same directory. You can start the program by running the Ant GUI.py file. If you haven't configured the relevant environment, you can also run the Ant GUI.exe program directly.

Usage
Creating an Environment
In the program interface, you can choose to use your own created environment, or select one from the preset environments in the upper right corner of the interface to test. If you choose to create your own environment, you can directly draw obstacles, starting points, and ending points by clicking "CREATE NOW!!" in the interface to create the environment. If you only want to create a temporary environment, you can select "Don't Save" in the following pop-up window. You can also click "Randomize!!" and "Randomize a Maze!" on the right to randomly generate an environment or maze.

Finding the Shortest Path
Once you have selected the environment, you can first deploy the starting and ending points of the robots by clicking the "Reset Start and End" button (left-click to change the obstacle status, right-click to set the starting or ending point). After setting the starting and ending points, you can click the "Run" button to start the ant colony algorithm and find the shortest path. You can adjust the relevant parameters of the ant colony algorithm, such as the number of iterations, the number of ants, and the pheromone evaporation coefficient, by clicking the "Set Parameters" button to obtain better results. The four choices on the left of the interface respectively represent whether to use the "Dead-Cell" algorithm, whether to save this result as an animation, whether to draw the intermediate process of the ant colony algorithm, and whether to choose four-way action (suitable for solving mazes).

Saving the Result
When the ant colony algorithm completes the pathfinding task, a pop-up window will appear asking whether you want to apply this pathfinding environment to the next pathfinding. This setting is designed to adapt to the "Dead-Cell" algorithm. Because the function of this algorithm is to constantly exclude invalid points in the environment during ant pathfinding. Therefore, if you select "Yes" in the pop-up window, it means that you are not satisfied with the pathfinding result this time. You can change the relevant parameters of ant iterations and ants, and perform pathfinding again in a new environment where most invalid points have been excluded until you are satisfied. Therefore, the recommended method is to first run "20 iterations, 100 ants" to eliminate most of the invalid points in the environment, and then run "80 iterations, 100 ants" to get better results. If you select "No" in the pop-up window, the software will assume that you accept the pathfinding result of this time and save the result. You can find your results in the images folder. You can also change your save path in the Setting of the main interface.

Here's the translation of your software documentation into English:

## Other Features

In addition to the main features mentioned above, this program also has the following features:

- "Dead-cell" algorithm: a new algorithm that can effectively reduce the number of iterations and improve algorithm efficiency.

- Multi-robot path planning: supports simultaneous planning of the shortest path for multiple robots in the same environment. After obtaining the shortest path for several robots, click the "Multiplayer plan" button to obtain the path planning between multiple robots with perfect collision avoidance, and save the resulting gif animation under the "Robots" directory.

## Notes

- Please ensure that the "parameter.pkl" and "save_path.pkl" files are in the same directory as the "Ant GUI.exe" or "Ant GUI.py" file.

- If the software fails to run after changing the save path, you can overwrite the current "pkl" files with the original backup files.

- When planning paths for multiple robots, the priority is based on the order of the results. For example, from "Solutuion-1" to "Solutuion-9", the priority decreases in order.

- When deleting planned paths for existing robots, you can only delete them starting from the last robot, so be careful when planning the order of robot pathfinding.

## Conclusion

The Multi-Robot Path Planning GUI program is a feature-rich path planning software that can help users quickly find the shortest path in a custom environment. If you encounter any problems or have any suggestions during use, please feel free to contact us.
=======
# Ant-Colony-Algorithm
-An Ant Colony Algorithm GUI program

WHAT DOSE THIS PROJECT DO???

- Create your own Environment  (There is few of initial Environments which I created for you to test and play)

- Find the shortest path

- Save result as .jpg and .gif like this:

![image](https://github.com/LiarGs/Ant-Colony-Algorithm-GUI/blob/master/images/Shortest%20Path%20Map%20(without%20dead-cell)%20th.gif)

![image](https://github.com/LiarGs/Ant-Colony-Algorithm-GUI/blob/master/images/Shortest%20Path%20Map%20(with%20dead-cell).jpg)

WHAT FEATURES DOES IT HAVE?

- Clear visual interface

- New "Dead-cell" algorithm which greatly reduces the number of iterations(Of course you can choose not to use it)

- You Can see how ants works on figure

- Reset  Start and End easily

- Adjustable parameters

- Randomize a Graph of course

- Choose result save path

CAN I USE IT TO SLOVE A MAZE???

- YES!! Design your maze and solve  it with ants. You will get a solution

HOW I USE THIS PROJECT???

- Make sure you download all files in the same file

- You can just run Ant GUI.exe without a python
 
- !! parameter.pkl and save_path.pkl must be in the same file with .exe !!

- Set new result save path in 'Settings'

- Click 'Start' to start and explore yourself

- It is recommended to run '20 Iterations, 100 Ant-numbers' first and run '80 Iterations 100 Ant-numbers' after. It will be better than '100 Iterations, 100 Ant-numbers' at first

WHAT LANGUAGE DOSE THIS PROJET USE??

- Python of course

- Based on Ant Colony Algorithm and My original "Dead-cell" algorithm

CAN IT BE USED FOR COMMERCIAL PURPOSES???

- NO!!! I design it as my Graduation Project and I have not pass it

LAST 
- Randomize a Maze (to do)

- Have FUN!!! and Enjoy it!!
>>>>>>> 4e751c2c9ef9be627d1269d2871e6a4b281f945f
