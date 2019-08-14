/*
- BinPack
- Pack *.bin archive files from (DS, 3DS) HM Series
- Support Grand Bazzar, The Tale of Two Towns
----------------How To Use
- Just Drag And Drop Directory To BinPack.exe
- Directory Must Be Made From BinUnpack.exe
-
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>
#include <io.h>
#include <conio.h>
#include <shlwapi.h>
#include "tinydir.h"
#define _CRT_SECURE_NO_WARNINGS
#pragma comment(lib, "shlwapi.lib")
#define EXIT(text) { printf(text); exit(EXIT_FAILURE); }
void Pack(char* filename);
void Usage(void);
char* Mid(char txt[], int start, int count);
void BubbleSort(int *list[], int Count)
{
	for (int i = 0; i < Count - 1; i++)
	{
		for (int j = 0; j < Count - 1 - i; j++)
		{
			if (list[j] > list[j + 1])
			{

				int temp = list[j];
				list[j] = list[j + 1];
				list[j + 1] = temp;
			}
		}
	}
	return;
}
int* SubFilePointerArray;
int* SubFileSizeArray;
int** FileArray;



int main(int argc, char** argv[])
{
	if (argc == 2) Pack(argv[1]);
	else Usage();

	printf("\nDone\n");


	return 0;
}



void Pack(char* Dirname)
{
	/*
		Dirname 디렉토리명
		FileName 만들어질 파일 명(=디렉토리 명)
	*/
	tinydir_dir dir;
	FILE* SaveFile;
	int FileCount = 0;
	int k = 0;
	int *FileList;
	int TempBinary = 0;
	long StartAdd;
	long SubStartAdd;
	long SubEndAdd; //파일 기록을 위한 변수
	long RealSubEndAdd; //실제 파일 기록을 위한 변수(실제 파일은 4의 배수로 저장되어야함.
	char* RealFileOrd[10] = { 0, };
	char* TempDir = (char*)malloc(sizeof(char) * strlen(Dirname));
	char* FileName[MAX_PATH];
	char* SaveFileName[MAX_PATH];
	strcpy(TempDir, Dirname);
	strcpy(FileName, Dirname);
	PathStripPathA(FileName);
	printf("File Name : %s\n", FileName);
	
	//----------------파일 갯수 얻기
	tinydir_open(&dir, TempDir);
	while (dir.has_next)
	{
		tinydir_file file;
		tinydir_readfile(&dir, &file);
		if (!file.is_dir) FileCount++;
		tinydir_next(&dir);
	}
	tinydir_close(&dir);
	printf("File Count : %d\n\n\n\n", FileCount);

	//----------------파일 갯수로 배열 만들어 저장하기
	FileList = malloc(sizeof(int) * FileCount);
	tinydir_open(&dir, TempDir);
	while (dir.has_next)
	{
		tinydir_file file;
		tinydir_readfile(&dir, &file);
		if (!file.is_dir)
		{
			strncpy(RealFileOrd, (file.name) + strlen(FileName)+1, strlen(file.name) - (strlen(FileName))); //숫자 부분만 추출
			FileList[k] = atoi(RealFileOrd); //배열에 숫자부분만 추출
			k++;
		}
		
		tinydir_next(&dir);
	}
	tinydir_close(&dir);

	BubbleSort(FileList, FileCount); //오름차순 정렬
	strcpy(SaveFileName, FileName);
	strcat(SaveFileName, ".bin");

	//------------------ 바이너리에 빈공간 미리 넣기--------
	SaveFile = fopen(SaveFileName, "wb+, ccs=UTF-16LE"); //파일 읽어오기

	fwrite(&FileCount, sizeof(int), 1, SaveFile);
	for (int i = 0; i < FileCount*2; i++)
	{
		fwrite(&TempBinary , sizeof(int), 1, SaveFile); // 맨 처음 기록될 스트림을 위해 빈공간으로 다 씀
	}
	StartAdd = ftell(SaveFile); //StartAdd에 SaveFile 주소값 저장
	SubEndAdd = ftell(SaveFile); //0번째 인덱스를 Seek하기위해서 저장
	fclose(SaveFile);



	for (int i = 0; i < FileCount; i++)
	{
		FILE* ReadFile;
		int SubFileSize;
		long Write1;
		long Write2;
		char* OpenDir = (char*)malloc(sizeof(char) * (strlen(Dirname) + strlen(FileName) + 10));
		unsigned int* FileStream;


		SaveFile = fopen(SaveFileName, "rb+");
		fseek(SaveFile, 0, SEEK_END); //파일 맨 끝에 기록하기위해 파일 포인터 이동
		SubStartAdd = ftell(SaveFile);
		sprintf(OpenDir, "%s\\%s_%d", Dirname, FileName,FileList[i]);
		//printf("%s\n", OpenDir);
		ReadFile = fopen(OpenDir, "rb"); //파일 읽어오기


		fseek(ReadFile, 0, SEEK_END);    // 파일 포인터를 파일의 끝으로 이동시킴
		SubFileSize = ftell(ReadFile);          // 파일 포인터의 현재 위치를 얻음
		
		//--------------파일 사이즈 측정 및 파일 기록-------------
		
		//printf("FileSize : %x\n", SubFileSize);
		FileStream = (int*)malloc(SubFileSize);
		fseek(ReadFile, 0, SEEK_SET);
		fread(FileStream, SubFileSize, 1, ReadFile);
		fwrite(FileStream, SubFileSize, 1, SaveFile);
		SubEndAdd = ftell(SaveFile);
		RealSubEndAdd = ftell(ReadFile);
		
		while (RealSubEndAdd % 4 != 0) // 실제론 4바이트의 배수로 저장되어야하므로 추가적으로 0 붙여줌
		{
			fwrite(&TempBinary, 1, 1, SaveFile);
			RealSubEndAdd = ftell(SaveFile);
		}
		
		fclose(SaveFile);

		//---------------오프셋 쓰기--------------
		SaveFile = fopen(SaveFileName, "rb+, ccs=UTF-16LE"); //파일 읽어오기
		fseek(SaveFile, 4 + (8 * i), SEEK_SET);
		Write1 = SubStartAdd - StartAdd;
		Write2 = SubEndAdd - SubStartAdd;
		fwrite(&Write1, sizeof(long), 1, SaveFile);
		fwrite(&Write2, sizeof(long), 1, SaveFile); //포인터 2개 기록

		fclose(SaveFile);
		fclose(ReadFile);


		//Sleep(10000);
	}

	
}
void Usage(void)
{
	EXIT(
		"Usage: BinPack [DIR_NAME] \n"
	);
	return;
}

