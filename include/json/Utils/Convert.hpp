#pragma once

#include <stdint.h>

namespace json::utils::convert::number
{
template<typename IntT, typename CharT>
IntT fromHex(CharT letter);

template<typename IntT, typename CharT>
IntT fromDec(CharT letter);
}

// Implementations

namespace json::utils::convert::number
{
template<typename IntT, typename CharT>
IntT fromHex(CharT letter)
{
    switch (letter)
    {
    case '0':
    case '1':
    case '2':
    case '3':
    case '4':
    case '5':
    case '6':
    case '7':
    case '8':
    case '9':
        return letter - 48;
    case 'a':
    case 'b':
    case 'c':
    case 'd':
    case 'e':
    case 'f':
        return letter - 87;
    case 'A':
    case 'B':
    case 'C':
    case 'D':
    case 'E':
    case 'F':
        return letter - 55;
    default:
        return -1;
    }
}

template<typename IntT, typename CharT>
IntT fromDec(CharT letter)
{
    switch (letter)
    {
    case '0':
    case '1':
    case '2':
    case '3':
    case '4':
    case '5':
    case '6':
    case '7':
    case '8':
    case '9':
        return letter - 48;
    default:
        return -1;
    }
}
}