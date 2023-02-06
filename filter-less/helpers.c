#include "helpers.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int i,j;
    for( i = 0; i<=height-1;i++)
    {
      for(j=0;j<=width-1;j++)
        {
            int red=image[i][j].rgbtRed;
            int blue=image[i][j].rgbtBlue;
            int green=image[i][j].rgbtGreen;
            int avg=(round((red+green+blue)/3));
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
        }
    }
    return;
}
// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int i , j ;
    for( i = 0; i <= height-1 ; i++)
    {
            // int average= round(( image[i][width].rgbtRed + image[i][width].rgbtBlue + image[i][width].rgbtGreen)/3);
        // apply( &x , i , image[i]);
      for(j=0;j<=width-1;j++)
        {
            int red = image[i][j].rgbtRed;
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;
            float SepiaRed = round(0.393 * red + 0.769*green + 0.189 * blue);
            float SepiaBlue = round(0.349 * red + 0.686 * green + 0.168 * blue);
            float SepiaGreen = round(0.272 * red +0.534*green + 0.131 * blue);
            if(SepiaRed >255)
            {
                SepiaRed=255;
            }
            if(SepiaGreen>255)
            {
                SepiaGreen=255;
            }
            if(SepiaBlue >255)
            {
                SepiaBlue=255;
            }

            image[i][j].rgbtRed = SepiaRed;
            image[i][j].rgbtBlue = SepiaBlue;
            image[i][j].rgbtGreen = SepiaGreen;
        }
            // printf("%i\n", average);
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int i,j,k;
    for( i = 0; i<=height-1;i++)
    {
      for(j=0,k=width-1; j<=width-1 && k>=0;j++,k--)
        {
            if(j==k || j>k)
            {
                return;
            }
            else
            {
                image[i][j]=image[i][k];
            }
        }
    }
    return;
}
// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create temp array
    RGBTRIPLE temp[height][width];
    for (int i = 0; i <=height-1; i++)
    {
        for (int j = 0; j <= width-1; j++)
        {
            temp[i][j] = image[i][j];
        }
    }
    for (int i = 0; i <= height-1; i++)
    {
        for (int j = 0; j <= width-1; j++)
        {
            int k,l;
            int red;
            int blue;
            int green;
            int count;
            red = blue = green = count = 0;
            for (k = -1; k < 2; k++)
            //initialize all the values
            {
                for (l = -1; l < 2; l++)//check if they are within bounds
                {
                    if (i + k < 0 || i + k >= height)
                    {
                        continue;
                    }
                    //checking the rows boundary
                    if (j + l < 0 || j + l >= width)
                    {
                        continue;
                    }
                    // now we increase the summation value stored in rgb variables.
                    red += temp[i + k][j + l].rgbtRed;
                    blue += temp[i + k][j + l].rgbtBlue;
                    green += temp[i + k][j + l].rgbtGreen;
                    count++;
                }
            }
            // Get average and blur image
            image[i][j].rgbtRed = round(red / count);
            image[i][j].rgbtGreen = round(green / count);
            image[i][j].rgbtBlue = round(blue / count);
        }
    }
    return;
}