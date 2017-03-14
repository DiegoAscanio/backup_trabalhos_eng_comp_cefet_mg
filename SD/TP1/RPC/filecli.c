#include <stdio.h>
#include <rpc/rpc.h>        /* always needed */
#include "file.h"            /* file.h wil be generated by rpcgen */

int main (int argc, char *argv[]) {
	CLIENT *cl;
	char **content;
	char *server;
	char *server_file;
	char *destination_file;

	if (argc != 4) {
		fprintf(stderr, "usage %s host server_file destination_file\n", argv[0]);
		exit(1);
	}

	server = argv[1];
	server_file = argv[2];
	destination_file = argv[3];

	cl = clnt_create(server, FILE_PROG, FILE_VERS, "tcp");
	if (cl == NULL) {
		clnt_pcreateerror(server);
		exit(1);
	}

	content = servefile_1(&server_file, cl);

	if (content == NULL) {
		clnt_perror(cl, server);
		exit(1);
	}

	FILE *fp;
	fp = fopen(destination_file, "w");
	while (*content != '\0') {
		fwrite(*content, sizeof(char), 1, fp);
		*content ++;
	}
	printf("Sucessfull Download!\n");
	fclose(fp);
	return 0;
}