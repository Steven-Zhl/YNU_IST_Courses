#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Windows.h>
#define LEN_LIMIT 18  //用户名、密码的长度不得超过18位
char filePath[] = "Account.txt";//本地文件的路径
enum function { Login, Register, Exit, ChangeUsername, ChangePassword, Cancellation, Error };
enum contentType { userName, account, password };
struct user {
	char* userName;
	char* account;
	char* password;
	char* content;//用于导出的数据
	void initial(char* getContent) {//为各个参数分配空间并初始化内容
		userName = (char*)malloc(LEN_LIMIT + 1);
		account = (char*)malloc(LEN_LIMIT + 1);
		password = (char*)malloc(LEN_LIMIT + 1);
		strcpy(userName, strtok(getContent, "-"));
		strcpy(account, strtok(NULL, "-"));
		strcpy(password, strtok(NULL, "-"));
	}
	char* getContent() {//将各个数据组合成放在Account.txt中的数据
		content = (char*)malloc(strlen(userName) + strlen(account) + strlen(password) + 3);
		strcpy(content, userName);
		strcat(content, "-");
		strcat(content, account);
		strcat(content, "-");
		strcat(content, password);
		return content;
	}
};
user* allUser;//user类型的数组，用于存放所有用户信息
user* thisUser;//当前用户指针
void main() {
	void LoginPanel();
	void RegisterPanel();
	void showWelcome(function & operater);
	function choice;//选择的功能
	showWelcome(choice);
	switch (choice) {
	case Login: {
		LoginPanel();
		break;
	}case Register: {
		RegisterPanel();
		break;
	}case Exit: {
		printf("即将退出，感谢使用");
		exit(0);
	}default: {
		printf("您的输入有误，请稍后再试");
		system("pause");
		system("cls");
		main();
	}
	}
}

//登录的功能面板
void LoginPanel() {
	void MenuPanel();
	int file_lineNum();
	char* file_content(int lineNum);
	void showLogin(char*& account, char*& password);
	int checkLogin(char* account, char* password, user * allUser);

	char* account = (char*)malloc(LEN_LIMIT + 1);//暂存当前用户的信息
	char* password = (char*)malloc(LEN_LIMIT + 1);
	int index;//当前用户在数组中的index，用于为thisUser指针定位

	allUser = (user*)malloc(sizeof(user) * file_lineNum());
	for (int i = 0; i < file_lineNum(); i++) {
		char* getContent = (char*)malloc(3 * LEN_LIMIT + 3);
		strcpy(getContent, file_content(i + 1));
		allUser[i].initial(getContent);
	}
	showLogin(account, password);//显示登录界面，并获取输入
	index = checkLogin(account, password, allUser);//检查是否可以登录（即输入是否正确）
	if (index != -1) {
		thisUser = &allUser[index];
		printf("欢迎使用\n");
		system("pause");
		system("cls");
		free(account);
		free(password);
		MenuPanel();
	}
	else {
		puts("您的账号或密码输入有误，请重试");
		system("pause");
		system("cls");
		main();
	}
}

//注册的功能面板
void RegisterPanel() {
	int file_lineNum();
	char* file_content(int lineNum);
	bool showRegister(char* account, char* userName, char* password, char* beforeAccount);
	void file_InContent(user & user);

	user newUser;//存放新用户
	user lastUser;//获取到新用户前的最后一个用户
	newUser.account = (char*)malloc(LEN_LIMIT);
	newUser.userName = (char*)malloc(LEN_LIMIT);
	newUser.password = (char*)malloc(LEN_LIMIT);
	char* getContent = (char*)malloc(LEN_LIMIT);
	strcpy(getContent, file_content(file_lineNum()));
	lastUser.initial(getContent);//获取到最后一个用户的信息
	//获取到注册状态
	bool state = showRegister(newUser.account, newUser.userName, newUser.password, lastUser.account);
	if (state) {
		file_InContent(newUser);
		puts("注册完成");
		printf("账号：%s\n", newUser.account);
		printf("用户名：%s\n", newUser.userName);
		printf("密码：%s\n", newUser.password);
		puts("请重新登录");
		system("pause");
		system("cls");
		free(lastUser.account);
		free(lastUser.userName);
		free(lastUser.password);
	}
	main();
}

//主菜单面板
void MenuPanel() {
	void ResetUserNamePanel();
	void ResetPasswordPanel();
	void CancellationPanel();
	void showMenu(function & operater);

	function operater;
	showMenu(operater);
	switch (operater) {
	case ChangeUsername: {ResetUserNamePanel(); break; }
	case ChangePassword: {ResetPasswordPanel(); break; }
	case Cancellation: { CancellationPanel(); break; }
	case Exit: {printf("即将退出，感谢使用"); exit(0); }
	default: {
		printf("您的输入有误，请重试\n");
		system("pause");
		system("cls");
		MenuPanel();
	}
	}
}

//修改用户名
void ResetUserNamePanel() {
	void showResetUserName(char* origin, char* newName, bool& state);
	int file_lineNum();
	void file_InContent(user * users, int userNum);

	char* newName = (char*)malloc(LEN_LIMIT + 1);
	bool changeState;
	showResetUserName(thisUser->userName, newName, changeState);
	if (changeState) {
		strcpy(thisUser->userName, newName);
		file_InContent(allUser, file_lineNum());//文件写入
		puts("修改完成，请重新登录");
		system("pause");
		system("cls");
		free(newName);
		main();
	}
	else { MenuPanel(); }
}

//修改密码
void ResetPasswordPanel() {
	void showResetPassword(char* origin, char* newPassword);
	int file_lineNum();
	void file_InContent(user * users, int userNum);

	char* newPassword = (char*)malloc(LEN_LIMIT + 1);
	showResetPassword(thisUser->password, newPassword);
	if (newPassword) {
		strcpy(thisUser->password, newPassword);
		file_InContent(allUser, file_lineNum());//文件写入
		puts("修改完成，请重新登录");
		system("pause");
		system("cls");
		free(newPassword);
		main();
	}
	else { MenuPanel(); }
}

//注销用户
void CancellationPanel() {
	bool showCancellation();
	int file_lineNum();
	void removeUser(user * allUser, int userNum, user * thisUser);
	void file_InContent(user * users, int userNum);

	bool choice = showCancellation();
	if (choice) {
		removeUser(allUser, file_lineNum(), thisUser);//执行删除当前角色
		file_InContent(allUser, file_lineNum() - 1);//将更改写入文件
		puts("修改完成，请重新登录");
		system("pause");
		system("cls");
		main();
	}
	else { MenuPanel(); }
}

//以下定义的函数用于运算
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
void removeUser(user* allUser, int userNum, user* thisUser) {
	for (int i = 0; i < userNum; i++) {
		if (&allUser[i] == thisUser) {
			for (int j = i; j < userNum - 1; j++) {
				strcpy(allUser[j].account, allUser[j + 1].account);
				strcpy(allUser[j].userName, allUser[j + 1].userName);
				strcpy(allUser[j].password, allUser[j + 1].password);
			}
			allUser = (user*)realloc(allUser, sizeof(user) * (userNum - 1));
			break;
		}
	}
}


//以下定义的函数用于显示界面

//展示主菜单界面
void showWelcome(function& operater) {
	int choice;
	puts("┌───────────────────────────────────────────────────────────────────┐");
	puts("│                                                                   │");
	puts("│                            QQ账户管理                             │");
	puts("│                                                                   │");
	puts("│                             1.登录                                │");
	puts("│                                                                   │");
	puts("│                             2.注册                                │");
	puts("│                                                                   │");
	puts("│                             3.退出                                │");
	puts("│                                                                   │");
	puts("└───────────────────────────────────────────────────────────────────┘");
	printf("欢迎使用！请输入相应操作的代号：");
	scanf("%d", &choice);
	system("cls");
	switch (choice) {
	case 1: {
		operater = Login;
		break; }
	case 2: {
		operater = Register;
		break; }
	case 3: {
		operater = Exit;
		break;
	}
	default: {
		operater = Error;
		break; }
	}

}

//获取到输入的账户和密码
void showLogin(char*& account, char*& password) {
	system("cls");
	printf("身份认证\n");
	printf("账号：__________________\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b");
	scanf("%s", account);
	system("cls");//清屏，以更新界面
	printf("身份认证\n");
	printf("账号：%s\n", account);
	printf("密码：__________________\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b");
	scanf("%s", password);
	system("cls");
}

//注册账户的相关界面
bool showRegister(char* account, char* userName, char* password, char* beforeAccount) {
	char* getContent = (char*)malloc(LEN_LIMIT + 1);//暂存输入的内容
	printf("请输入用户名：");
	scanf("%s", getContent);
	if (strlen(getContent) > LEN_LIMIT) {
		puts("您的用户名长度不正确，请稍后再试");
		system("pause");
		system("cls");
		return false;
	}
	strcpy(userName, getContent);
	printf("请输入密码：");
	scanf("%s", getContent);
	if (strlen(getContent) > LEN_LIMIT) {
		puts("您的密码格式不正确，请稍后再试");
		system("pause");
		system("cls");
		return false;
	}
	strcpy(password, getContent);
	int lastval = atoi(beforeAccount);//获取到上一位的账号
	itoa(lastval + 1, account, 10);//分配账号
	free(getContent);
	return true;
}

//展示功能菜单
void showMenu(function& operater) {
	int choice;
	puts("┌───────────────────────────────────────────────────────────────────┐");
	puts("│                                                                   │");
	puts("│                            功能菜单                               │");
	puts("│                                                                   │");
	puts("│                           1.修改用户名                            │");
	puts("│                                                                   │");
	puts("│                           2.修改密码                              │");
	puts("│                                                                   │");
	puts("│                           3.注销账号                              │");
	puts("│                                                                   │");
	puts("│                           4.退出                                  │");
	puts("└───────────────────────────────────────────────────────────────────┘");
	printf("请输入相应操作的代号：");
	scanf("%d", &choice);
	system("cls");
	switch (choice) {
	case 1: {operater = ChangeUsername; break; }
	case 2: {operater = ChangePassword; break; }
	case 3: {operater = Cancellation; break; }
	case 4: {operater = Exit; break; }
	default: {operater = Error; break; }
	}
}

//修改用户名的相关显示
void showResetUserName(char* origin, char* newName, bool& state) {
	int choice;
	printf("您的原用户名为:%s\n", origin);
	printf("请输入您的新用户名：");
	scanf("%s", newName);
	system("cls");
	printf("您的用户名即将由 %s 修改为 %s\n", origin, newName);
	puts("是否确定？");
	puts("1. 确定    2. 取消");
	scanf("%d", &choice);
	if (choice == 1) { printf("已修改完毕\n"); state = true; }
	else {
		printf("已取消操作\n");
		state = false;//避免意外传参
	}
	system("pause");
	system("cls");
}

//修改密码的展示
void showResetPassword(char* origin, char* newPassword) {
	int choice;
	char* input = (char*)malloc(LEN_LIMIT + 1);
	printf("请输入您的原密码：");
	scanf("%s", input);
	if (strcmp(input, origin)) {
		puts("密码输入错误，请稍后再试");
		newPassword = NULL;
		return;
	}
	free(input);
	printf("请输入您的新密码：");
	scanf("%s", newPassword);
	system("cls");
	printf("您的密码即将由 %s 修改为 %s\n", origin, newPassword);
	puts("是否确定？");
	puts("1. 确定    2. 取消");
	scanf("%d", &choice);
	if (choice == 1) { printf("已修改完毕\n"); }
	else {
		printf("已取消操作\n");
		newPassword = NULL;
	}
	system("pause");
	system("cls");
}

//注销账号的展示
bool showCancellation() {
	int choice;
	printf("您即将注销该账号");
	puts("是否确定？");
	puts("1. 确定    2. 取消");
	scanf("%d", &choice);
	if (choice == 1) {
		printf("已修改完毕\n");
		return true;
	}
	else {
		printf("已取消操作\n");
		return false;
	}
}