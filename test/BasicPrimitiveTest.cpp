#include "Json/Json.hpp"
#include "gtest/gtest.h"
#include <string>
#include <iostream>

using std::string;
using std::string_view;

using std::cout;
using std::endl;

using namespace json;

TEST(BasicPrimitiveTest, Construction)
{
    auto primitive = makePrimitive();
    EXPECT_EQ(primitive.type(), Type::primitive);
    EXPECT_TRUE(primitive.isPrimitive());
}

TEST(BasicPrimitiveTest, ReadWrite)
{
    auto primitive = makePrimitive();
    primitive.string("aaa");
    EXPECT_EQ(primitive.string(), "aaa");
    
    auto &value = primitive.string();
    value = "a";
    
    EXPECT_EQ(primitive.string(), "a");
}