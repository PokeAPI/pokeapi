with import <nixpkgs> { };

mkShell {
  packages = [
    uv

    # non-Python system libraries your project needs
    taglib
    openssl
    git
    libxml2
    libxslt
    libzip
    zlib
  ];

  shellHook = ''
    unset SOURCE_DATE_EPOCH
    uv sync --locked --all-extras --dev
  '';
}