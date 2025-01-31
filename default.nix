with import <nixpkgs> { };
pkgs.mkShell {
  name = "onix-shellder";
  venvDir = "./.venv";
  buildInputs = [
    python312Packages.python
    python312Packages.venvShellHook

    # Required dependencies

    # Python
    python312Packages.black

    # misc
    taglib
    openssl
    git
    libxml2
    libxslt
    libzip
    zlib
  ];

  # Runs after creating the virtual environment
  postVenvCreation = ''
    unset SOURCE_DATE_EPOCH
    pip install -r requirements.txt
  '';

  postShellHook = ''
    unset SOURCE_DATE_EPOCH
    # use z shell, run exit to get back to default bash
    zsh -l
  '';

}
