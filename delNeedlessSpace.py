#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 08:50:54 2018

@author: sdc
"""

import sys
import os
import pprint
import chardet

FILENAMEFILTERS = ('.c', '.h')  #文件过滤器，只需要.c和.h文件

#获取文件的编码格式
def get_file_encoding(file):
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']

#处理过滤出来的文件
def handleCertainFiles(filenames):
    for filename in filenames:
        os.system("dos2unix "+filename)
        print('del %s space...' %(filename))
        #使用with 方式，不用调用close()函数
        with open(filename, 'r+') as fileHandle:#不能以'a+'的方式打开
            fileContents = fileHandle.readlines()
            if len(fileContents) == 0:
                print('%s file is empty' % filename)
                continue
            #确保最后一行有换行符
            finalLineContent = fileContents[-1]
            if finalLineContent[-1] != '\n':
                finalLineContent = finalLineContent + '\n'
                fileContents[-1] = finalLineContent
                #print(fileContents)
            
            newFileContents = []	#存储修改后的内容，最终将其写入文件中
            for lineContent in fileContents:
                newLineContent = lineContent[:-1] #去除 \n
                if newLineContent.strip() != '': #如果去除首尾的空格后不为空，那么只应该去掉行尾的空格
                    newLineContent = newLineContent.rstrip() + '\n'
                else:
                    newLineContent = newLineContent.strip() + '\n'
                        
                newFileContents.append(newLineContent)
            fileHandle.seek(0, 0)	#将文件指针放在文件开头
            fileHandle.truncate()	#清空文件
            #print(newFileContents)
            fileHandle.writelines(newFileContents)	#写入修改后的内容

#查找符合要求的文件
#返回符合要求的文件列表,和编码错误的文件列表
def findCertainFiles(filenames):
    
    right_files = []
    wrong_files = []
    
    print('Checking file encoding...')
    for filename in filenames:
        filenamePrefix, filenameSuffix = os.path.splitext(filename) #分离文件名和文件后缀
        if filenameSuffix in FILENAMEFILTERS:
            file_encoding = get_file_encoding(filename)
            if((file_encoding != 'ascii') and (file_encoding != 'utf-8')):
                #print('Please change file(%s) encoding to \'utf-8\'' %(filename))
                wrong_files.append(filename)
                continue;
            else:            
                right_files.append(filename)
    return right_files, wrong_files

#在目录中找到所有文件
#返回所有的文件，包含文件的路径
def findFilesInDir(dir):
    
    result = []
    
    if not os.path.exists(dir):
        print('Wrong dir name')
        return result
    for mainDir, subDir, files in os.walk(dir):
        for file in files:
            filename = os.path.join(mainDir, file)
            result.append(filename)
    return result

def main():
    
    all_files = []
    right_files = []
    error_files = []
    
    if len(sys.argv) < 2:
        print('Usage: delNeedlessSpace.py dirname')
        return
    all_files = findFilesInDir(sys.argv[1])
    #pprint.pprint(tuple(allFiles))
    right_files, error_files = findCertainFiles(all_files)
    #pprint.pprint(tuple(allFiles))
    handleCertainFiles(right_files)
    if len(error_files) != 0:
        print('The encoding of those files shown below should be converted to \'utf-8\':')
        pprint.pprint(tuple(error_files))
    
if __name__ == '__main__':
    main()
