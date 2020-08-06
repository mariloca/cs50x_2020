#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    //typedef uint8_t BYTE;
    if (argc == 2)
    {
        //Open memory card
        FILE *rawfile = fopen(argv[1], "r");
        if (!rawfile)
        {
            return 1;
        }
        unsigned char bytes[512];  //Read 512 bytes into a buffer
        FILE *img;
        //char *filename;
        int cnt = -1; //filename count
        char *filename = malloc(sizeof(char) * 15);
        //Repeat until end of card.Return value of fread is number of blocks read, if is not equal to number parameter, then error occurs or EOF
        while (fread(bytes, 512, 1, rawfile))
        {
            //Read data from memory card  size: size of the block; number:number of blocks
            if (bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff
                && (bytes[3] & 0xf0) == 0xe0) //Check first four bytes, start of new JPEG
            {
                //If first JPEG, open a new file to write the data
                if (cnt == -1)
                {
                    sprintf(filename, "%03i.jpg", ++cnt);
                    img = fopen(filename, "w"); //filename is '001.jpg'
                    fwrite(bytes, 512, 1, img);
                    printf("First JPEG: %s\n", filename);
                }
                else
                {
                    //Close current file
                    //sprintf(filename, "%03i.jpg", cnt);
                    fclose(img);
                    //Open new file
                    sprintf(filename, "%03i.jpg", ++cnt);
                    img = fopen(filename, "w");
                    fwrite(bytes, 512, 1, img);
                    printf("Next JPEG: %s\n", filename);
                }
            }
            else //Not the new jpg start
            {
                //Write the data continuously into the current file
                fwrite(bytes, 512, 1, img);
            }
        }
        free(filename);
        fclose(img); //Close any remaining files
        return 0;
    }
    else
    {
        //Empty input or more than 2 arguments
        printf("Usage: %s image\n", argv[0]);
        return 1;
    }

}
