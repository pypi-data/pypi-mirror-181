CMAKE_MINIMUM_REQUIRED(VERSION 3.10)
PROJECT(test_project Fortran)

# Директория для исполняемых файлов
SET(BIN_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
# Директория для статических библиотек
SET(ARC_DIRECTORY ${CMAKE_BINARY_DIR}/slib)
# Директория для модулей Fortran
SET(MOD_DIRECTORY ${CMAKE_BINARY_DIR}/mods)

IF(WIN32)
    # В windows динамические библиотеки должны находится в одной папке с exe
    SET(LIB_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
ELSE()
    # Данная опция включает относительный путь для динамических библиотек.
    # Директорию bin с вложенной директорией lib может быть перемещена, 
    # и программа будет успешно запускаться, даже если директория
    # сборки удалена
    SET(CMAKE_BUILD_RPATH_USE_ORIGIN TRUE)
    SET(LIB_DIRECTORY ${BIN_DIRECTORY}/lib)
ENDIF()

SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${BIN_DIRECTORY})
SET(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${LIB_DIRECTORY})
SET(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${ARC_DIRECTORY})
SET(CMAKE_Fortran_MODULE_DIRECTORY ${MOD_DIRECTORY})

ADD_SUBDIRECTORY(mcdrag) # Исходный код исполняемого файла
ADD_SUBDIRECTORY(internal_ballistics) # Исходный код динамической библиотеки
ADD_SUBDIRECTORY(external_ballistics) # Исходный код статической библиотеки
ADD_SUBDIRECTORY(al_tate_model) # Исходный код модуля 
