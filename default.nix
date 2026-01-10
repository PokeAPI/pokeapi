with import <nixpkgs> { };
pkgs.mkShell {
  name = "onix-shellder";
  venvDir = "./.venv";
  buildInputs = [
    python313Packages.python
    python313Packages.venvShellHook

    # Required dependencies

    # Python
    python313Packages.black

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
