import os

from clang.cindex import Index, Config, TranslationUnit, CursorKind


class BitcoinCodeExplorer(object):
    def __init__(self):
        homebrew_lib_path = '/usr/local/Cellar/llvm/6.0.1/lib/'
        xcode_lib_path = '/Applications/Xcode.app/Contents/Developer/Toolchains' \
                         '/XcodeDefault.xctoolchain/usr/lib/'

        if os.path.exists(homebrew_lib_path):
            Config.set_library_path(homebrew_lib_path)
        elif os.path.exists(xcode_lib_path):
            Config.set_library_path(xcode_lib_path)
        else:
            raise Exception('Path for libclang lib not found')

        self.index: Index = Index.create()

        self.translation_unit: TranslationUnit = self.index.parse(
            path=None,
            args=[
                '/Users/pierre/src/bitcoin/src/wallet/wallet.h',
                '/Users/pierre/src/bitcoin/src/wallet/wallet.cpp'
            ]
        )

    def iterate_nodes(self):
        for child in self.translation_unit.cursor.get_children():
            # print(child.kind, child.spelling)
            if child.spelling == 'COutput':
                print('here')

    def list_includes(self, translation_unit):
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
