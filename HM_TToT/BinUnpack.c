/*
- BinUnpack
- Unpack *.bin archive files from (DS, 3DS) HM Series
- Support Grand Bazzar, The Tale of Two Towns
----------------How To Use
- Just Drag And Drop Bin File To Binunpack.c
-
*/

#include <stdio.h>
#include <stdlib.h>  // exit()
#include <direct.h>
#include <string.h>
#include <windows.h>
#include <shlwapi.h>
#pragma comment(lib, "shlwapi.lib")
#define _CRT_SECURE_NO_WARNINGS
#define EXIT(text) { printf(text); exit(EXIT_FAILURE); }
//#define MAX_PATH 256

void Usage(void);
void Unpack(char *filename);
void Extract(int k, char* filename);
int* SubFilePointerArray;
int* SubFileSizeArray;
char* locfilename;
char* ptr = NULL;
int size;
int main(int argc, char** argv[])
{
	if (argc == 2) Unpack(argv[1]);
	else Usage();

	printf("\nDone\n");
	return 0;
}



void Unpack(char *filename)
{
	FILE *fp;
	int SubFilePointer;
	int SubFileSize;

	locfilename = malloc(sizeof(char) * (strlen(filename)*2)); // 파일 생성 위해서 만듬
	

	strcpy(locfilename, filename);
	PathRemoveExtensionA(locfilename);

	if (_mkdir(locfilename) > 0) EXIT("Create Folder Error\n"); //dir만들기
	if (_chdir(locfilename) != 0) EXIT("Select Folder Error\n");
	printf("%s\n", filename);
	fp = fopen(filename, "rb, ccs=UTF-16LE"); //파일 읽어오기
	if (fp == NULL)
	{
		EXIT("Error");
	}
	else
	{
		fread(&size, sizeof(int), 1, fp); //파일 사이즈 구하기
	}
	SubFilePointerArray = (int*)malloc(sizeof(int) * (size + 2)); SubFilePointerArray[size + 1] = 0; //배열 크기 size갯수로 늘리기
	SubFileSizeArray = (int*)malloc(sizeof(int) * (size + 2)); SubFileSizeArray[size + 1] = 0; //배열 크기 size갯수로 늘리기
	for (int i = 0; i < size; i++)
	{
		fread(&SubFilePointer, sizeof(int), 1, fp);
		fread(&SubFileSize, sizeof(int), 1, fp);
		
		SubFilePointerArray[i] = SubFilePointer;
		SubFileSizeArray[i] = SubFileSize;

	}
	fclose(fp);
	for (int i = 0; i < size; i++)
	{
		Extract(i, filename);
	}

	free(locfilename);
	free(SubFilePointerArray);
	free(SubFileSizeArray);
	return;
}
void Extract(int k, char *filename)
{
	
	FILE* fp;
	FILE* out;
	unsigned int FileAddress;
	unsigned int *FileStream=(int *)malloc(sizeof(int)* SubFileSizeArray[k]);
	char CopyText[MAX_PATH];
	printf("Index %d Extracting..   ", k);
	FileAddress = 4 + (8 * size) + SubFilePointerArray[k];
	sprintf(CopyText, "%s", filename);
	PathStripPathA(CopyText);
	PathRemoveExtensionA(CopyText);
	sprintf(CopyText, "%s_%d", CopyText,k); 
	printf("%s AND SIZE %x\n", CopyText,SubFileSizeArray[k]);
	fp = fopen(filename, "rb"); //파일 읽어오기
	out = fopen(CopyText, "wb");


	fseek(fp, FileAddress, SEEK_SET); //오프셋 이동
	fread(FileStream, SubFileSizeArray[k], 1, fp);
	fwrite(FileStream, SubFileSizeArray[k], 1, out);

	free(FileStream);
	fclose(fp);
	fclose(out);
	return;
}
void Usage(void)
{
	EXIT(
		"Usage: BinUnpack [FILE_NAME] \n"
	);
	return;
}