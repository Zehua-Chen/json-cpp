# Json Library

## Features

- Full Json standard compatibilty;
- Works with
  - `char`;
  - `char16_t`;
  - `char32_t`;
  - `wchar_t`;
- `char16_t` and `char32_t` are **only theoratically supported. Being able
  to successfully compile with these character types requires the respective
  C++ STL having support for these character types**.
- STL-like design
  - Inputs string are passed as iterators
  - Char type support implemented through template, like `basic_string<CharT>`;

## Requirements

- C++17 compatible compilers

## Usage

You are welcome to add the build system you use! Just open a pull request!

### CMake

- Download the repository (ex. `FetchContent`)
- Link the `json` library target to your targets

```cmake
include(FetchContent)

# declare json
FetchContent_Declare(
    json
    GIT_REPOSITORY https://github.com/Zehua-Chen/cpp-json.git
    GIT_TAG version)

# see if json has been downloaded
FetchContent_GetProperties(json)

if(NOT jsoncpp_POPULATED)
    # download json cpp if not
    FetchContent_Populate(json)
    # add json's CMakeLists as a sub directory
    add_subdirectory(${jsoncpp_SOURCE_DIR} ${jsoncpp_BINARY_DIR})
endif()

target_link_libraries(
    your_target
    PRIVATE
        json)
```

### Other Build Systems

- Download the repository
- Add "./include" to your include path
- Include the umbrella header `json.hpp` and start parsing json!

## Quick Start

```cpp

#include "json/json.hpp"
#include <string>
#include <iostream>

using namespace json;

int main() {
  string json = "{ 'key': 'value' }";
  Value value = parse(json.begin(), json.end());

  std::cout << value["key"].string() << std::endl;

  return 0;
}
```

## Known Limitations

- No error resporting
- Only string to json, and not the other way around;
- `BasicValue<CharT>` does not have iterators
- `BasicValue<CharT>` only have basic data access methods;

## Development

### Setup

- When generating build files using cmake, define `JSONCPP_DEV` to be 1

```
cmake .. -G Ninja -DJSONCPP_DEV=1
```

#### Windows

`ParseTest.cpp` may not work as expected on Windows, as the file path used to
access the json file follows Linux/Unix format.
