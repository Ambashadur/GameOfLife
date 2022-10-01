#define LIFE 0b00000111

void calculate_next_generation(char* cells, int width, int height)
{
    char sum = 0;
    
    int left_bottom = (height - 1) * width;
    int right_bottom = width * height - 1;

    // left-up corner
    sum += cells[right_bottom] & LIFE;
    sum += cells[left_bottom] & LIFE;
    sum += cells[left_bottom + 1] & LIFE;
    sum += cells[width - 1] & LIFE;
    sum += cells[1] & LIFE;
    sum += cells[width + width - 1] & LIFE;
    sum += cells[width] & LIFE;
    sum += cells[width + 1] & LIFE;
    cells[0] += sum << 4;

    // right-up corner
    sum = 0;
    sum += cells[width * height - 2] & LIFE;
    sum += cells[right_bottom] & LIFE;
    sum += cells[left_bottom] & LIFE;
    sum += cells[width - 2] & LIFE;
    sum += cells[0] & LIFE;
    sum += cells[width + width - 2] & LIFE;
    sum += cells[width + width - 1] & LIFE;
    sum += cells[width] & LIFE;
    cells[width - 1] += sum << 4;

    // left-bottom corner
    sum = 0;
    sum += cells[left_bottom - 1] & LIFE;
    sum += cells[(height - 2) * width] & LIFE;
    sum += cells[(height - 2) * width + 1] & LIFE;
    sum += cells[right_bottom] & LIFE;     
    sum += cells[left_bottom + 1] & LIFE;
    sum += cells[width - 1] & LIFE;
    sum += cells[0] & LIFE;
    sum += cells[1] & LIFE;
    cells[left_bottom] += sum << 4;

    // right-bottom corner
    sum = 0;
    sum += cells[left_bottom - 2] & LIFE;
    sum += cells[left_bottom - 1] & LIFE;
    sum += cells[(height - 2) * width] & LIFE;
    sum += cells[width * height - 2] & LIFE;
    sum += cells[left_bottom] & LIFE;
    sum += cells[width - 2] & LIFE;
    sum += cells[width - 1] & LIFE;
    sum += cells[0] & LIFE;
    cells[right_bottom] += sum << 4;

    int i;
    int j;

    // top and botom lines
    for (i = 1; i < width - 1; i++)
    {
        j = i + left_bottom;

        sum = 0;
        sum += cells[j - 1] & LIFE;
        sum += cells[j] & LIFE;
        sum += cells[j + 1] & LIFE;
        sum += cells[i - 1] & LIFE;
        sum += cells[i + 1] & LIFE;
        sum += cells[i + width] & LIFE;
        sum += cells[i + width - 1] & LIFE;
        sum += cells[i + width + 1] & LIFE;
        cells[i] += sum << 4;

        sum = 0;
        sum += cells[j - width - 1] & LIFE;
        sum += cells[j - width] & LIFE;
        sum += cells[j - width + 1] & LIFE;
        sum += cells[j - 1] & LIFE;
        sum += cells[j + 1] & LIFE;
        sum += cells[i - 1] & LIFE;
        sum += cells[i] & LIFE;
        sum += cells[i + 1] & LIFE;
        cells[j] += sum << 4;
    }

    // left and right lines
    for(i = width; i <= left_bottom - width; i += width)
    {
        j = i + width - 1;

        sum = 0;
        sum += cells[i - 1] & LIFE;
        sum += cells[i - width] & LIFE;
        sum += cells[i - width + 1] & LIFE;
        sum += cells[j] & LIFE;
        sum += cells[i + 1] & LIFE;
        sum += cells[j + width] & LIFE;
        sum += cells[i + width] & LIFE;
        sum += cells[i + width + 1] & LIFE;
        cells[i] += sum << 4;

        sum = 0;
        sum += cells[j - width - 1] & LIFE;
        sum += cells[j - width] & LIFE;
        sum += cells[i - width] & LIFE;
        sum += cells[j - 1] & LIFE;
        sum += cells[i] & LIFE;
        sum += cells[j + width - 1] & LIFE;
        sum += cells[j + width] & LIFE;
        sum += cells[j + 1] & LIFE;
        cells[j] += sum << 4;
    }

    for (i = width + 1; i < left_bottom - 1;)
    {
        int i_height = i / width;
        int i_width = i - i_height * width;

        sum = 0;
        sum += cells[i - 1] & LIFE;
        sum += cells[i + 1] & LIFE;
        sum += cells[i - width] & LIFE;
        sum += cells[i - width - 1] & LIFE;
        sum += cells[i - width + 1] & LIFE;
        sum += cells[i + width] & LIFE;
        sum += cells[i + width - 1] & LIFE;
        sum += cells[i + width + 1] & LIFE;
        cells[i] += sum << 4;

        i++;

        if (i_width == width - 1)
            i += 2;
    }

    char x_1, x_2, x_3, x_4 = 0;
    char previous_cell = 0;

    // calculating alive or not
    for (i = 0; i < width * height; i++)
    {
        x_1 = (~cells[i] & 0b01000000) >> 6;
        x_2 = (cells[i] & 0b00100000) >> 5;
        x_3 = (cells[i] & 0b00010000) >> 4;
        x_4 = cells[i] & 0b000000001;

        previous_cell = cells[i] & LIFE;
        cells[i] = (x_1 & x_2 & x_3) | (x_1 & x_2 & x_4);

        if (previous_cell ^ cells[i])
            cells[i] += 0b10000000;
    }
}