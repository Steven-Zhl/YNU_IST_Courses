#ifndef __MANAGE_H__
#define __MANAGE_H__
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "display.h"
#include "manage.h"



//获取文件行数，即学生个数
int file_lineNum() {
	FILE* accountFile = fopen(filePath, "r");
	fseek(accountFile, 0, SEEK_SET);
	char sep = fgetc(accountFile);
	int lineNum = sep == EOF ? 0 : 1;//若第一行就为EOF则说明行数为0，若第一行不为EOF则至少有1行
	while (sep != EOF)
	{
		if (sep == '\n')
		{
			lineNum++;
		}
		sep = fgetc(accountFile);
	}
	fclose(accountFile);
	return lineNum;
}

//获取特定行的用户信息
char* file_content(int lineNum) {
	FILE* accountFile = fopen(filePath, "r");//文件指针
	char line[3 * LEN_LIMIT + 3];//每行的原数据
	fseek(accountFile, 0, SEEK_SET);//将光标定位到文件开头
	//只有目标行数小于等于总行数的时候才能进行读取
	if (lineNum <= file_lineNum()) {
		for (int i = 0; i < lineNum; i++) {
			fscanf(accountFile, "%s", line);
			fgetc(accountFile);//换行
		}
	}
	fclose(accountFile);
	return line;
}

//用于写入文件的函数，两种重载，第一个是覆写，适用于修改内容；第二个追加，适用于注册
void file_InContent(user* users, int userNum) {
	FILE* accountFile = fopen(filePath, "w");
	fseek(accountFile, 0, SEEK_SET);
	for (int i = 0; i < userNum; i++) {
		fputs(users[i].getContent(), accountFile);
		if (i != userNum - 1) { fprintf(accountFile, "\n"); }
	}
	fclose(accountFile);
}
void file_InContent(user& user) {
	FILE* accountFile = fopen(filePath, "a");
	fseek(accountFile, 0, SEEK_END);
	fputs("\n", accountFile);
	fputs(user.getContent(), accountFile);
	fclose(accountFile);
}

//判断登录是否成功，即账号密码是否能够查到
int checkLogin(char* account, char* password, user* allUser) {
	for (int i = 0; i < file_lineNum(); i++) {
		if (!strcmp(allUser[i].account, account) && !strcmp(allUser[i].password, password)) {
			return i;
		}
	}
	return -1;
}

//删除allUser中的thisUser
void removeUser(user* allUser, int userNum,user* thisUser) {
	for (int i = 0; i < userNum; i++) {
		if (&allUser[i] == thisUser) {
			for (int j = i; j < userNum-1; j++) {
				strcpy(allUser[j].account, allUser[j + 1].account);
				strcpy(allUser[j].userName, allUser[j + 1].userName);
				strcpy(allUser[j].password, allUser[j + 1].password);
			}
			allUser = (user*)realloc(allUser, sizeof(user) * (userNum - 1));
			break;
		}
	}
}
#endif