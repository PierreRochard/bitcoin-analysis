from clang.cindex import Index, Config, TranslationUnit, CursorKind


def list_includes(translation_unit):
    """ Find all includes within the given TranslationUnit
    """
    cursor = translation_unit.cursor

    includes = []

    for child in cursor.get_children():
        # We're only interested in preprocessor #include directives
        #
        if child.kind == CursorKind.INCLUSION_DIRECTIVE:
            # We don't want Cursors from files other than the one belonging to
            # translation_unit otherwise we get #includes for every file found
            # when clang parsed the input file.
            #
            if (child.location.file is not None) and (
                    child.location.file.name == cursor.displayname):
                includes.append(child.displayname)

    return includes


Config.set_library_path("/usr/local/Cellar/llvm/6.0.1/lib/")
index = Index.create()
translation_unit: TranslationUnit = index.parse(
    path=None,
    args=[
        '/Users/pierre/src/bitcoin/src/wallet/wallet.h',
        '/Users/pierre/src/bitcoin/src/wallet/wallet.cpp'
    ]
)

for child in translation_unit.cursor.get_children():
    # print(child.kind, child.spelling)
    if child.spelling == 'COutput':
        print('here')
