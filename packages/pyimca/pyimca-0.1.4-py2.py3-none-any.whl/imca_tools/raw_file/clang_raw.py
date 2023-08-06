clang_raw = """
CompileFlags:                             
    Add: 
      [
        -std=c++17,
        -Wno-documentation,
        -Wno-missing-prototypes,
      ]
    CompilationDatabase: vs-build
Diagnostics:
  ClangTidy:
    Add:
    [
        performance-*,
        bugprone-*,
        modernize-*,
        clang-analyzer-*,
        readability-identifier*,
    ]
    CheckOptions:
      readability-identifier-naming.VariableCase: camelCase

"""
