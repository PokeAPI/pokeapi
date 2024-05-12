with import <nixpkgs> { };
pkgs.mkShell {
  name = "onix-shellder";
  venvDir = "./.venv";
  buildInputs = [
    python310Packages.python
    python310Packages.venvShellHook

    # Required dependancies 
    black
    taglib
    openssl
    git
    libxml2
    libxslt
    libzip
    zlib
  ];

  # Run this command, only after creating the virtual environment
  postVenvCreation = ''
    unset SOURCE_DATE_EPOCH
    pip install -r requirements.txt
  '';

  postShellHook = ''
    # allow pip to install wheels
    unset SOURCE_DATE_EPOCH
    zsh -l
  '';

}
