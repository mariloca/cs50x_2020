#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float value;
    int avg;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            value = (float)(image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3;
            avg = round(value);
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtRed = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaRed, sepiaGreen, sepiaBlue;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Calculate new RBG value
            sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            //Cap new RGB value
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++) //image[0][first] = image[0][last], set middle point, flip both sides
        {
            RGBTRIPLE tmp; //swap first and last item
            tmp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copyimage[height][width];  //create a image[] copy, prevent change original value of image[];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float newred = 0.0, newgreen = 0.0, newblue = 0.0;
            int cnt = 0;
            for (int dr = -1; dr <= 1; dr++)  //dr=[-1,0,1], dc=[-1,0,1]
            {

                for (int dc = -1; dc <= 1; dc++)
                {
                    int nr, nc;
                    nr = i + dr; //adding dr and dc --> new i and new j
                    nc = j + dc;
                    if (nr >= 0 && nr < height && nc >= 0 && nc < width) //check if new i and new j are valid -->within 0~height and 0~width
                    {
                        newred += image[nr][nc].rgbtRed; //red  value from all neighbors
                        newgreen += image[nr][nc].rgbtGreen;
                        newblue += image[nr][nc].rgbtBlue;
                        cnt ++; //how many neighbors have been added
                    }
                }

            }
            copyimage[i][j].rgbtRed = round((float)newred / cnt); //set current cell's red to avg of all neighbors
            copyimage[i][j].rgbtGreen = round((float)newgreen / cnt);
            copyimage[i][j].rgbtBlue = round((float)newblue / cnt);
        }
    }

    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width; c++)
        {
            image[r][c] = copyimage[r][c]; //set copyimage[] value back to original image[];
        }
    }
    return;
}
