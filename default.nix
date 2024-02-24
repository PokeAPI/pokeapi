with import <nixpkgs> { };

let
  pythonPackages = python3Packages;
in pkgs.mkShell rec {
  name = "impurePythonEnv";
  venvDir = "./.venv";
  buildInputs = [
    python310Packages.python
    python310Packages.venvShellHook

    # python310Packages.coverage
    # python310Packages.python-mimeparse
    # python310Packages.python-dateutil
    # python310Packages.drf-spectacular
    # python310Packages.djangorestframework
    # python310Packages.django-redis
    # python310Packages.django-cors-headers

    # Required dependancies 
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
  '';

}
