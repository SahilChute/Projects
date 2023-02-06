#include <stdio.h>
#include <stdlib.h>
#include<stdint.h>
#include<stdbool.h>
int main(int argc, char *argv[])
{
    typedef uint8_t BYTE;
    BYTE buffer[512];
    char filename[8];//000.jpg=7chars 8th for \0
    int count = 0;//we initialize a counter to count which image
    int bytes;//bytes read by fread
    FILE *image = NULL;//initialize the image
    FILE *f = fopen(argv[1], "r");
    if(argc!=2)//to check for valid argument
    {
        printf("Usage format: ./recover image.raw");
        return false;
    }
    if(f==NULL)
    {
        printf("cannot open the file");//incase there is an empty folder
        return false;
    }
    while(true)
    {
        bytes = fread(buffer, sizeof(BYTE), 512, f);//read 512 bytes into buffer
        if(buffer[0]==0xff && buffer[1]== 0xd8 && buffer[2]== 0xff && (buffer[3] & 0xff)==0xe0)//checks for start of jpeg
        {
            if(count==0)//if first jpeg
            {
                sprintf(filename, "%03i.jpg", count);//if start of new jpeg
                image=fopen(filename, "w");
                fwrite(buffer, sizeof(BYTE), bytes, image);
                count++;
            }
            else
            {
                fclose(image);//if not first jpeg then close the previous image
                sprintf(filename, "%03i.jpg", count);
                image=fopen(filename, "w");
                fwrite(buffer, sizeof(BYTE), bytes, image);
                count++;
            }
        }
        else if (count!=0 && bytes!=0)//incase there is no jpg present in that memory we just write over it
        {
            fwrite(buffer, sizeof(BYTE), bytes, image);
        }
        else if (bytes == 0)//for the end of the loop
        {
                fclose(image);
                fclose(f);
                return false;
        }
    }
    fclose(image);
    fclose(f);
    // return false;
}

