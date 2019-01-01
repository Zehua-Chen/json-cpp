#pragma once

#include <iostream>
#include <string>
#include <string_view>

namespace json
{
enum class TokenType
{
    beginObject,
    endObject,
    beginArray,
    endArray,
    key,
    value,
};

template<typename CharT>
struct Token
{
    Token();
    Token(std::basic_string<CharT> data, TokenType type);

    void append(CharT letter);

    bool operator==(const Token<CharT> &other) const;
    bool operator!=(const Token<CharT> &other) const;

    std::basic_string<CharT> data;
    TokenType type;
};

template<typename CharT>
std::basic_ostream<CharT> &
operator<<(std::basic_ostream<CharT> &out, const Token<CharT> &token)
{
    using std::string_view;

    const auto print = [&](string_view text) {
        for (const auto letter : text)
        {
            out << out.widen(letter);
        }
    };

    switch (token.type)
    {
    case TokenType::key:
        print("key=");
        out << token.data;
        break;
    case TokenType::value:
        print("value=");
        out << token.data;
        break;
    case TokenType::beginObject:
        print("beginObject");
        break;
    case TokenType::endObject:
        print("endObject");
        break;
    case TokenType::beginArray:
        print("beginArray");
        break;
    case TokenType::endArray:
        print("endArray");
        break;
    }

    return out;
}
} // namespace json

// Implementation

namespace json
{
template<typename CharT>
Token<CharT>::Token()
{
}

template<typename CharT>
Token<CharT>::Token(std::basic_string<CharT> data, TokenType type)
    : data(data)
    , type(type)
{
}

template<typename CharT>
void Token<CharT>::append(CharT letter)
{
    data.push_back(letter);
}

template<typename CharT>
bool Token<CharT>::operator==(const Token<CharT> &other) const
{
    if (other.type != type)
    {
        return false;
    }

    if (other.data != data)
    {
        return false;
    }

    return true;
}

template<typename CharT>
bool Token<CharT>::operator!=(const Token<CharT> &other) const
{
    if (other.type != type)
    {
        return true;
    }

    if (other.data != data)
    {
        return true;
    }

    return false;
}
} // namespace json