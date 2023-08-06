
set(TOOL_INCLUDES math base sim play cpython)
list(TRANSFORM TOOL_INCLUDES PREPEND "${PROJECT_SOURCE_DIR}/src/")
find_package(Python 3.7 COMPONENTS Interpreter Development)
find_package(pybind11 CONFIG)


set(TOOL_LIBS
    "${SIM_LIBRARY}"
    "${MATH_LIBRARY}"
    "${BASE_LIBRARY}"
    "${LAPACK_BLAS}"
    Threads::Threads
)

set(TOOL_LIST
    "frametool"
    "sieve"
    "report"
    "reportF"
    "reader"
)

#add_library(pybind11_headers INTERFACE)

# Build the Tools
foreach(TOOL ${TOOL_LIST})
    add_executable("${TOOL}" "${PROJECT_SOURCE_DIR}/src/tools/${TOOL}.cc")
    set_source_files_properties(
        PROPERTIES
        EXTERNAL_OBJECT true
        GENERATED true
    )
    target_link_libraries(${TOOL} PUBLIC "${TOOL_LIBS}")
    target_include_directories(${TOOL} PUBLIC ${TOOL_INCLUDES})
endforeach()


set(PYCY_SOURCES
    "${PROJECT_SOURCE_DIR}/src/tools/pycytosim.cc"
)
set_source_files_properties(
        PROPERTIES
        EXTERNAL_OBJECT true
        GENERATED true
    )
pybind11_add_module(cytosim  ${PYCY_SOURCES})
add_compile_options(-fPIC -shared -Wl,undefined,dynamic)
target_link_libraries(cytosim PUBLIC "${TOOL_LIBS}")
target_include_directories(cytosim PUBLIC ${TOOL_INCLUDES})
