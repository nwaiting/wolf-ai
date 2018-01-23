#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <limits.h>
#include <time.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>

#ifdef WIN32
#include <Windows.h>
typedef unsigned __int64 SNC_UI64;
typedef __int64 SNC_I64;
typedef short bool;
#define true 1
#define false 0
#define UINT64_MAX ((SNC_UI64)(-1))
#else
#include <stdint.h>
#include <stdbool.h>
#include <fcntl.h>
#include <unistd.h>
typedef uint64_t SNC_UI64;
typedef int64_t SNC_I64;
#endif

#ifndef MAX_PATH
#define MAX_PATH 1024
#endif

#ifndef WIN32
#include <pthread.h>
#define ngx_stdcall
/*
typedef pid_t  ngx_tid_t;
typedef unsigned int ngx_thread_value_t;
*/
#ifdef __SNC_NGX__
//typedef ngx_thread_value_t (ngx_stdcall *ngx_thread_func_pt)(void* arg);
#endif // __SNC_NGX__
typedef int64_t msec_t;
#else
typedef __int64 msec_t;
#endif

typedef unsigned int SNC_UI32;
typedef int SNC_I32;

static const size_t ENCRYPT_ROUNDS = 32; // at least 32
static const u_int DELTA = 0x9E3779B9;
static const u_int FINAL_SUM = 0xC6EF3720;
static const size_t BLOCK_SIZE = (sizeof(unsigned int) << 1);
static const size_t BLOCK_SIZE_TWICE = ((sizeof(unsigned int) << 1) << 1);
static const size_t BLOCK_SIZE_HALF = ((sizeof(unsigned int) << 1) >> 1);

#ifndef PROTOTYPES
#define PROTOTYPES 0
#endif

/* POINTER defines a generic pointer type */
typedef unsigned char *POINTER;

/* UINT2 defines a two byte word */
typedef unsigned short int UINT2;

/* UINT4 defines a four byte word */
typedef unsigned long int UINT4;

#if PROTOTYPES
#define PROTO_LIST(list) list
#else
#define PROTO_LIST(list) ()
#endif

/************************************************************
*  interface
************************************************************/

#define SEGMENT_SIZE 20971520 // 20MB
#define BLOCK_SIZE 2097152 // 2MB
#define MAX_TRACKS 2
#define ATOM_PREAMBLE_SIZE 8
#define DRAG_TIME_SCALE 15 // 15sec
#define MAX_MP4_NAME_LENGTH 512

#ifdef WIN32
#pragma pack(1)
#endif

#ifndef WIN32
__attribute__ ((packed))
#endif
SYNACAST_GUID;
#ifdef WIN32
#pragma pack()
#endif

enum VideoBlockType
{
	BLOCK_ERR		= 0,
	BLOCK_BIG		= 1,
	BLOCK_SEG		= 2,
};

u_int GetTimeFromStr(char* str,int len)
{
	int i=0;
	union tagkey{char ch[4];u_int key;} tmp_key;
	memset(&tmp_key,0,sizeof(tmp_key));

	for(i=0;i<len && i < 4;i++)
	{
       		tmp_key.ch[i%4]=tmp_key.ch[i%4]^str[i];
	}
	return tmp_key.key;
}
void Time2Str(u_int timet, char* str,int len)
{
	int i=0;
	union tagkey
	{
		char ch[4];
		unsigned int key;
	} tmp_key;

	char char_index[] = "0123456789abcdef";

	memset(str,0,len);
	memset(&tmp_key,0,sizeof(tmp_key));
	tmp_key.key = timet;

	for(i=0;i<len && i < 4;i++)
	{
		str[2*i] = char_index[tmp_key.ch[i]&0xF];
		str[2*i+1] = char_index[(tmp_key.ch[i]>>0x4)&0x0F];
	}
}

void TGetKey(const unsigned int *k0, unsigned int *sn, unsigned int *start, unsigned int *k3 )
{
	*sn = *k0<<8|*k0>>24;
	*start = *k0<<16|*k0>>16;
	*k3 = *k0<<24|*k0>>8;
}

int Str2Hex(unsigned char *buffer, unsigned int buf_size, char *hexstr, unsigned int hs_size)
{
	char char_index[] = "0123456789abcdef";
	size_t i;

	if (hs_size < 2*buf_size+1) return 0;

	for (i = 0; i < buf_size; i++)
	{
		hexstr[2*i] = char_index[buffer[i]&0xF];
		hexstr[2*i+1] = char_index[(buffer[i]>>0x4)&0x0F];
	}
	hexstr[2*buf_size] = '\0';
	return 1;
}

unsigned int GetkeyFromstr(char* str, size_t len)
{
	size_t i=0;
	union tagkey
	{
		char ch[4];
		unsigned int key;
	}tmp_key;
	memset(&tmp_key,0,sizeof(tmp_key));

	for(i=0;i<len;i++)
	{
		tmp_key.ch[i%4] ^= str[i];
	}
	return tmp_key.key;
}
unsigned int _GetkeyFromstr(char* str, int len) {
	unsigned int key = 0;
	int i;
	for (i = 0; i < len; i++) {
		key ^= (unsigned int) (str[i]) << (i % 4 * 8);
	}
	return key;
}
void TEncrypt(unsigned char *buffer, unsigned int buf_size, char* key, size_t len)
	/*¼ÓÃÜbuffer´óÐ¡²»ÄÜÐ¡ÓÚ16×Ö½Ú,32Î»Ê±¼ä´Áºó²¹ÈÎÒâ×Ö·û´ÕÆëºó¼ÓÃÜ*/
{
	size_t i;
	unsigned int k0 = GetkeyFromstr(key, len), sn=0, start=0, k3=0;
	TGetKey(&k0, &sn, &start, &k3);
	for (i = 0; i + BLOCK_SIZE_TWICE <= buf_size; i += BLOCK_SIZE_TWICE)
	{
		unsigned int *v = (unsigned int*) (buffer + i);
		unsigned int v0 = v[0], v1 = v[1], sum = 0;
		size_t j;
		for (j = 0; j < ENCRYPT_ROUNDS; j++)
		{
			sum += DELTA;
			v0 += ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + sn);
			v1 += ((v0<<4) + start) ^ (v0 + sum) ^ ((v0>>5) + k3);
		}
		v[0] = v0; v[1] = v1;
	}
}
void _TEncrypt(char* buffer, int buf_size, char* key, int len) {
                int i;
				u_int k0 = _GetkeyFromstr(key, len);
                u_int k1 = 0;
                u_int k2 = 0;
                u_int k3 = 0;
                k1 = k0 << 8 | k0 >> 24;
                k2 = k0 << 16 | k0 >> 16;
                k3 = k0 << 24 | k0 >> 8;
				
                for (i = 0; i + BLOCK_SIZE_TWICE <= buf_size; i += BLOCK_SIZE_TWICE) {
                        u_int v0 = 0, v1 = 0, sum = 0;
						int j,k;
                        for ( k = 0; k < 4; k++) {
                                v0 |= (u_int) (buffer[i + k] & 0xff) << (k * 8);
                                v1 |= (u_int) (buffer[i + k + 4] & 0xff) << (k * 8);
                        }

                        for (j = 0; j < ENCRYPT_ROUNDS; j++) {
                                sum += DELTA;
				v0 += (((v1 << 4) + k0)
					^ (v1 + sum))
					^ ((v1 >> 5) + k1);
				v1 += (((v0 << 4) + k2)
					^ (v0 + sum))
					^ ((v0 >> 5) + k3);
                        }

                        for (k = 0; k < 4; k++) {
                                buffer[i + k] = (char) ((v0 >> (k * 8)) & 0xFF);
                                buffer[i + k + 4] = (char) ((v1 >> (k * 8)) & 0xFF);
                        }
                }
 }

unsigned int TDecrypt(char *hexstr, char* key)
{
	size_t i = 0;
	unsigned int k0 = GetkeyFromstr(key, strlen(key)), sn, start, k3;
	unsigned int buf_size = 256;
	unsigned char buffer[256];
	unsigned int timet = 0;

	memset(buffer,0,buf_size);

	if (2*buf_size < strlen(hexstr)) return -1;

	for (i = 0; i < strlen(hexstr)/2; i++)
	{
		buffer[i] = (hexstr[2*i]-(hexstr[2*i]>'9'?'a'-10:'0')) | ((hexstr[2*i+1]-(hexstr[2*i+1]>'9'?'a'-10:'0'))<<4);
	}

	TGetKey(&k0, &sn, &start, &k3);
	for (i = 0; i + BLOCK_SIZE_TWICE <= buf_size; i += BLOCK_SIZE_TWICE)
	{
		unsigned int *v = (unsigned int*) (buffer + i);
		unsigned int v0 = v[0], v1 = v[1], sum = FINAL_SUM;
		size_t j;
		for (j = 0; j < ENCRYPT_ROUNDS; j++)
		{
			v1 -= ((v0<<4) + start) ^ (v0 + sum) ^ ((v0>>5) + k3);
			v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + sn);
			sum -= DELTA;
		}
		v[0] = v0; v[1] = v1;
	}

	for(i=0;i<buf_size && i < 8;i++)
	{
		timet |= (unsigned int)(buffer[i]-(buffer[i]>'9'?'a'-10:'0'))<<(28-i%8*4);
	}
	return timet;
}

void _Time2Str(u_int timet, char* str, int len) {
      int i;
      for (i = 0; i < len && i < 8; i++) {
          str[i] = (char) ((timet >> (28 - i % 8 * 4)) & 0xF);
          str[i] += (char) (str[i] > 9 ? 'a' - (char) 10 : '0');
      }
}

void getKey(char* pkey , time_t t)
{
	char bytes[16] ={0};
	char key[16]  ={0};
	char result[33]  ={0};
	char* keystr = "qqqqqww";
	unsigned int timet = t;
	int i;
	for ( i = 0; i < 16; i++) {
			key[i] = i < strlen(keystr) ? keystr[i] :  0;
	}
	
//	timet-=100;
	_Time2Str( timet, bytes , 16);
	for (i = 0; i < 16; i++) {
			if (bytes[i] == 0) {
					bytes[i] =  rand()%256+1;
			}
	}

	_TEncrypt(bytes, 16, key, 16);
	Str2Hex(bytes, 16, result, 33);
	strcpy(pkey,result);
}

