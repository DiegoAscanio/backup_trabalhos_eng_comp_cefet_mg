#include<stdio.h>
#include "msg.h"

int * printmessage_1(char **msg, struct svc_req *req) {
	static int result;			/* must be static! */
	FILE *f;
 
	f = fopen("/dev/stdout", "w");
	if (f == (FILE *)NULL) {
		result = 0;
		return (&result);
	}
	fprintf(f, "%s\n", *msg);
	fclose(f);
	result = 1;
	return (&result);
}
