/*
 * Copyright 2012 Giorgio Vazzana
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/* Compile: gcc -Wall -O make_bitmap2.c -o make_bitmap2 */

#include <stdio.h>
#include <stdlib.h>

struct pgm {
	unsigned int width;
	unsigned int height;
	unsigned int max;
	unsigned char *data;
};

int write_pgm(const char *filename, const struct pgm *frame)
{
	FILE *fp;

	fp = fopen(filename, "w");
	if (!fp) {
		printf("Error while opening %s\n", filename);
		return 1;
	}

	fprintf(fp, "P5\n%d %d\n%d\n", frame->width, frame->height, frame->max);
	fwrite(frame->data, (size_t) frame->width, (size_t) frame->height, fp);
	fclose(fp);

	return 0;
}


int main(int argc, char *argv[])
{
	int i, c;
	unsigned char byte;
	struct pgm frame;

	if (argc < 3) {
		printf("Usage: cat sequence | make_bitmap width height\n");
		return 1;
	}

	frame.width = atoi(argv[1]);
	frame.height = atoi(argv[2]);
	if (frame.width > 4096 || frame.height > 4096) {
		printf("Error: one dimension is > 4096\n");
		return 1;
	}
	frame.max = 255;
	frame.data = malloc(frame.width * frame.height);
	if (!frame.data) {
		printf("Error: malloc() failed\n");
		return 1;
	}

	for (i = 0; i < frame.width * frame.height; i++) {
		c = fgetc(stdin);
		if (c == EOF) {
			/* printf("Error: unexpected EOF\n"); */
			/* return 1; */
		}
		byte = (c == '0') ? 0 : 255;
		frame.data[i] = byte;
	}

	write_pgm("bitmap.pgm", &frame);

	return 0;
}
