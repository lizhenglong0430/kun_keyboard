编译方法
执行`pyi-makespec -F -i .\imgs\kun_keyboard.ico -w .\main.py`以生成spec文件  
修改spec文件中`datas=[('audios','audios'),('imgs','imgs')],`一行，audios，imgs为主函数所在文件同级目录  
修改完之后执行`pyinstaller .\main.spec`就可以生成可执行文件  
