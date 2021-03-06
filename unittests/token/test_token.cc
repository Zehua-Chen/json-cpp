//
//  TokenTest.cpp
//  CPP
//
//  Created by Zehua Chen on 12/31/18.
//  Copyright © 2018 Zehua Chen. All rights reserved.
//

#include <string>
#include "gtest/gtest.h"
#include "json/token/token.h"

using std::get;
using std::string;

using namespace std::string_literals;

using namespace json::token;

TEST(TokenTest, CopyConstructor) {
  Token<char> token1{"something"};
  Token<char> token2 = token1;

  EXPECT_EQ(token2.string(), token1.string());
}

TEST(TokenTest, PerfectForwarding) {
  string data = "aaa";
  Token<char> copy{Token<char>::Type::kString, data};
  Token<char> moved{Token<char>::Type::kString, std::move(data)};

  ASSERT_EQ(copy.string(), "aaa");
  ASSERT_EQ(moved.string(), "aaa");
  ASSERT_EQ(data.empty(), true);
}

TEST(TokenTest, MoveConstructor) {
  Token<char> token1{"something"};
  Token<char> token2 = std::move(token1);

  EXPECT_TRUE(token1.string().empty());
  EXPECT_EQ(token2.string(), "something");
}

TEST(TokenTest, CompareSame) {
  // Begin Object
  {
    Token<char> token1 = {Token<char>::Type::kBeginObject};
    Token<char> token2 = {Token<char>::Type::kBeginObject};

    EXPECT_EQ(token1, token2);
  }

  // Begin Array
  {
    Token<char> token1 = {Token<char>::Type::kBeginArray};
    Token<char> token2 = {Token<char>::Type::kBeginArray};

    EXPECT_EQ(token1, token2);
  }

  // Strings
  {
    Token<char> token1 = {"a"};
    Token<char> token2 = {"a"};

    EXPECT_EQ(token1, token2);
    EXPECT_EQ(token1.string(), token2.string());
  }

  // Numbers
  {
    Token<char> token1 = {12.0f};
    Token<char> token2 = {12.0f};

    EXPECT_EQ(token1, token2);
    EXPECT_EQ(token1.number(), token2.number());
  }
}

TEST(TokenTest, CompareDifferent) {
  // Object
  {
    Token<char> token1 = {Token<char>::Type::kBeginObject};
    Token<char> token2 = {Token<char>::Type::kEndObject};

    EXPECT_NE(token1, token2);
  }

  // Array
  {
    Token<char> token1{Token<char>::Type::kBeginArray};
    Token<char> token2{Token<char>::Type::kEndArray};

    EXPECT_NE(token1, token2);
  }

  // String and null
  {
    Token<char> token1{"a"};
    Token<char> token2{Token<char>::Type::kNull};

    EXPECT_NE(token1, token2);
  }

  // Different Buffer - string
  {
    Token<char> token1{"a"};
    Token<char> token2{"b"};

    EXPECT_NE(token1, token2);
  }

  // Different Buffer - Value
  {
    Token<char> token1{"a"};
    Token<char> token2{"b"};

    EXPECT_NE(token1, token2);
  }
}