##FAQ1: git: Permission denied(publickey). fatal:Could not read from remote repository.

#产生原因是没有生成ssh key，按照以下步骤即可使用

git生成ssh的命令
##进入目录 cd ~/.ssh
##ssh-keygen -t rsa -C "your email"
如果不设置密码的话，一路回车，使用默认值即可。 
但是我敲完这条命令，按回车 

Generating public/private rsa key pair.
Enter file in which to save the key (/c/Users/Administrator/.ssh/id_rsa):
/c/Users/Administrator/.ssh/id_rsa already exists.
Overwrite (y/n)? y
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /c/Users/Administrator/.ssh/id_rsa.
Your public key has been saved in /c/Users/Administrator/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:keUBxTM+1WzLMIAirI/1HMDbF4oKSJAWHe2q1bNaZCs ahworld07@gmail.com
The key's randomart image is:
+---[RSA 2048]----+
|ooo+o   .==. o   |
|.o .=.. o++.+ +  |
|+  ..* ooo.+ = . |
|o . +.+ ..o   o  |
| . =o= oS  .     |
|  oo+o+          |
|  oE oo          |
| .  o.           |
|   ..            |
+----[SHA256]-----+
##cat id_rsa.pub 得到ssh key，复制ssh key
##在github setting 找到SSH and GPG keys, 粘贴在ssh key, 然后 “Add SSH Key”
##接着就可以操作   git remote add origin https://github.com/seqyuan/programs.git
##git push -u origin master 


