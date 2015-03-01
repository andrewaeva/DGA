#include <windows.h>
#include <stdio.h>
#include <math.h>

typedef double(__cdecl *_sin)(_In_ double _X);
_sin psin = sin;
typedef double(__cdecl *_log)(_In_ double _X);
_log plog = log;

__int64 mykey = 0;
double dbl = 6.26454564e-1;
char *tld_list[] = { ".cc", ".cn", ".ws", ".com", ".net", ".org", ".info", ".biz" };

void seed_prng()
{
	LARGE_INTEGER PerformanceCount;
	DWORD tid = GetCurrentThreadId();
	DWORD pid = GetCurrentProcessId();
	BOOL  res = QueryPerformanceCounter(&PerformanceCount);
	if (!res)
	{
		PerformanceCount.HighPart &= res;
		PerformanceCount.LowPart = 1130540720;
	}
	srand(tid ^ pid ^ PerformanceCount.LowPart ^ GetTickCount());
}

__declspec(naked) void naked_func2(void)
{
	__asm{
		push ebx
			push esi
			mov     eax, [esp + 24]
			or      eax, eax
			jnz     short loc_3C7062
			mov     ecx, [esp + 20]
			mov     eax, [esp + 16]
			xor     edx, edx
			div     ecx
			mov     ebx, eax
			mov     eax, [esp + 12]
			div     ecx
			mov     edx, ebx
			jmp     short loc_3C70A3
		loc_3C7062 :
		mov     ecx, eax
			mov     ebx, [esp + 20]
			mov     edx, [esp + 16]
			mov     eax, [esp + 12]
		loc_3C7070 :
				   shr     ecx, 1
				   rcr     ebx, 1
				   shr     edx, 1
				   rcr     eax, 1
				   or      ecx, ecx
				   jnz     short loc_3C7070
				   div     ebx
				   mov     esi, eax
				   mul     dword ptr[esp + 24]
				   mov     ecx, eax
				   mov     eax, [esp + 20]
				   mul     esi
				   add     edx, ecx
				   jb      short loc_3C709E
				   cmp     edx, [esp + 16]
				   ja      short loc_3C709E
				   jb      short loc_3C709F
				   cmp     eax, [esp + 12]
				   jbe     short loc_3C709F
			   loc_3C709E :
		dec     esi
		loc_3C709F :
		xor     edx, edx
			mov     eax, esi
		loc_3C70A3 :
		pop esi
			pop ebx
			ret 10h
	};

}

__declspec(naked) void naked_func(void)
{
	__asm{
		mov     eax, [esp + 8]
			mov     ecx, [esp + 16]
			or      ecx, eax
			mov     ecx, [esp + 12]
			jnz     short loc_3C70C9
			mov     eax, [esp + 4]
			mul     ecx
			retn    10h
		loc_3C70C9:
		push    ebx
			mul     ecx
			mov     ebx, eax
			mov     eax, [esp + 8]
			mul     dword ptr[esp + 20]
			add     ebx, eax
			mov     eax, [esp + 8]
			mul     ecx
			add     edx, ebx
			pop     ebx
			retn    10h
	};
}

int Rand()
{
	int ret = 0;

	double var_8 = 0;
	double var_10 = 0;
	double var_18 = 0;
	double var_30 = 0;
	double var_20 = 0;

	__asm{
		pushad
			mov     ecx, dword ptr[mykey + 4]
			mov     eax, dword ptr[mykey]
			and     dword ptr[var_8], 0
			push    esi
			mov     edx, ecx
			push    edi
			mov     dword ptr[var_8 + 4], edx
			mov     edi, 7FFFFFFFh
			and     edx, edi
			mov     dword ptr[var_10], eax
			mov     dword ptr[var_10 + 4], edx
			fild[var_10]
			mov     esi, 80000000h
			and     dword ptr[var_8 + 4], esi
			fild[var_8]
			and     dword ptr[var_8], 0
			mov     dword ptr[var_8 + 4], ecx
			and     dword ptr[var_8 + 4], esi
			fchs
			and     ecx, edi
			faddp   st(1), st
			mov     dword ptr[var_18], eax
			mov     dword ptr[var_18 + 4], ecx
			push    ecx
			fstp[var_10]
			push    ecx
			fild[var_18]
			fild[var_8]
			fchs
			faddp   st(1), st
			fstp    qword ptr[esp]
			call    psin
			add     esp, 8
			fstp[var_20]
			push    0
			push    53125624h
			push    dword ptr[mykey + 4]
			push    dword ptr[mykey]
			call    naked_func
			and     dword ptr[var_8], 0
			mov     dword ptr[var_8 + 4], edx
			and     dword ptr[var_8 + 4], esi
			and     edx, edi
			mov     dword ptr[var_18], eax
			mov     dword ptr[var_18 + 4], edx
			fild[var_18]
			push    ecx
			fild[var_8]
			push    ecx
			fchs
			faddp   st(1), st
			fadd[var_20]
			fmul[var_10]
			fadd    dbl
			fmul[var_10]
			fstp[var_20]
			fld[var_10]
			fstp    qword ptr[esp]
			call    plog
			fadd[var_20]
			pop     ecx
			pop     ecx
			pop     edi
			fstp    qword ptr mykey
			mov     eax, dword ptr[mykey]
			mov		ret, eax
			pop     esi
			popad
	};

	return ret;
}

void print_domains(char * datestr)
{
	SYSTEMTIME time;
	FILETIME filetime;
	char domain[32];

	memset(&time, 0, sizeof(SYSTEMTIME));
	memset(&filetime, 0, sizeof(FILETIME));

	if (datestr == NULL)
	{
		GetSystemTime(&time);
		time.wDayOfWeek = 0;
		time.wHour = 0;
		time.wMilliseconds = 0;
		time.wMinute = 0;
		time.wSecond = 0;
	}
	else
	{
		sscanf(datestr, "%4d%2d%2d", &time.wYear, &time.wMonth, &time.wDay);
	}

	printf("Generating domains for %d-%d-%d:\n\n", time.wYear, time.wMonth, time.wDay);

	seed_prng();

	SystemTimeToFileTime(&time, &filetime);

	__asm
	{
		push eax
			push edx
			push 0x3
			push 0x52C94565
			push filetime.dwHighDateTime
			push filetime.dwLowDateTime
			call naked_func
			push 0x580
			push 0x28E44000
			push edx
			push eax
			call naked_func2
			add eax, 0x0A3596526
			adc edx, 0
			mov dword ptr[mykey], eax
			mov dword ptr[mykey + 4], edx
			pop edx
			pop eax
	};

	int max = 100000;
	FILE *fp;
	if ((fp = fopen("conficker.txt", "at")) == NULL) {
		exit(1);
	}
	while (max--)
	{
		int len = (Rand() % 4) + 8;
		int i = 0;

		memset(domain, 0, sizeof(domain));

		while (i < len)
		{
			domain[i++] = (unsigned char)(labs(Rand()) % 26) + 97;
		}

		domain[i] = '\0';
		strcat(domain, tld_list[Rand() & 7]);

		fprintf(fp,"%s\n", domain);
	}
	fclose(fp);
	ExitProcess(0);
}


int main() {
	print_domains(NULL);
	return 0;
}
