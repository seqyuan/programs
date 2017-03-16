# applyProject

此程序为方便每周下单申请使用

这是一个golang程序，需要安装golang，并且配置环境变量

需要安以下go包
```
"github.com/dgiagio/getpass"
"github.com/mattn/go-sqlite3"
"github.com/tealeg/xlsx"
```


## install

使用以下命令下载applyProject程序

`git clone git@github.com:seqyuan/programs.git`

使用以下命令进行程序编译和初始化

```
cd programs/applyProject/src
make install
make init
/abspath/applyProject/bin/applyProject -creatdb
/abspath/applyProject/bin/applyProject -creatusrdb
```
## 使用applyProject

### 第一次使用applyProject

执行以下命令查看使用说明

`/abspath/applyProject/bin/applyProject`

第一次运行此程序，会自动提示你输入你的用户信息（姓名，组别，邮箱），如下：

```
$apply
你的需要输入 姓名组别邮箱 等信息才能使用这个程序！

>>> 请输入你的姓名:
苑赞

>>> 请输入你的组别:
转录调控组 [0]
生物学DNA组 [1]
医口DNA组 [2]
分析组 [3]

如果你的组不在列表里请直接输入组名
0

>>> 请输入你的邮箱:
zanyuan@genome.cn
```
填写完成你的用户信息后，再次运行

`/abspath/applyProject/bin/applyProject`

会出现程序使用说明，如下：

```
$apply

Program: applyProject (Tools for apply project)
Version: 0.1.1-20170214
注意输入不能有中文标点符号!
Xshell删除字符时请按住Ctrl键

Usage:  applyProject <command> [options]

Command:
    a|apply                 Apply a project
    q|query                 Query the apply projects of your groups
    e|edit [id]             ReEdit the apply project
    d|delete [id]           Delete the apply project

   eu|editusr               ReEdit usr information
    o|outDir [dir]          Dir to export apply projects excel file(then you can send it by email)
    m|mail [out.xlsx]       Send the Excel to taoliu@genome.cn

    -flagplus               This week last week flag change
    -creatdb                Reset applyProject DB only for admin
    -creatusrdb             Reset usr DB only for admin
    -importOldxls [xlsFile] Import old projects from excel only for admin
```
### 确认或者修改用户信息

由于输入法等一些原因可能导致输入的用户信息有误，想要检查或者更改可以*eu*参数进行修改或者确认，如下：
```
$apply eu

>>> 请输入你的姓名:苑赞


>>> 请输入你的组别 转录调控组
:
转录调控组 [0]
生物学DNA组 [1]
医口DNA组 [2]
分析组 [3]

如果你的组不在列表里请直接输入组名


>>> 请输入你的邮箱:zanyuan@genome.cn
```
运行`applyProject eu`命令，会提示已输入的用户信息，如果某一项填写有问题可直接输入进行修改，如果不需要做修改，请直接按回车键

### 申请任务

`applyProject a`


### 查询所在组已申请任务单

`applyProject q`  或者 `applyProject q|less -S`

### 修改某任务单

如果想修改 id（第一列）为108的任务，执行以下命令：

`applyProject e 108`

会提示已输入的信息，如果某一项填写有问题可直接输入进行修改，如果不需要做修改，请直接按回车键


### 删除某个任务单

如果想删除 id（第一列）为108的任务，执行以下命令：

`applyProject d 108`


### 连续第二周使用此程序

如果上周用此程序申请了任务单，本周再次使用，会首先提示输入上周申请任务的（子项目编号和项目完成情况），如下：
```
$apply

流程bug提交程序设计-bug提交到流程负责人，而不是主管，减少冗余沟通

此项目为上周项目有两项内容需要填写
>>> 请输入此项目的子项目编号:
```
填写完成后就可以进行本周的项目申请了


### 导出本周申请项和上周项目完成情况

如果确认组内申请任务已经完成需要运行以下命令导出到 excel，运行以下命令就会到出到当前路径

`applyProject o ./`

### 发送邮件

检查确认excel无误后，执行以下命令会发送给涛哥，并且抄送给组内所有人

`applyProject m yourExcelFile`

### 把本周项目改变为上周项目

各组组长确认涛哥对本周任务都下单后，运行以下命令，以把本周申请的任务做一个标记，使下周申请时能够跳出，使组员填写项目完成情况

`applyProject -flagplus`

如果有任务单不符要求，请组长先行联系组员进行项目修改/或者删除项目，导出excel并且发送邮件后，再执行以上命令

### 从excel文件导入任务

如果你是组长，请*确保组员*都使用本程序进行过用户信息的填写，然后运行以下命令，以导入上周申请的任务单

`applyProject -importOldxls`