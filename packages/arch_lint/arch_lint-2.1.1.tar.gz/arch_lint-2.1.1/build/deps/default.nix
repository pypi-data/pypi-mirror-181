{
  nixpkgs,
  python_version,
}: let
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    buildPythonPackage = nixpkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = nixpkgs.python3Packages.fetchPypi;
  };
  python_pkgs =
    nixpkgs."${python_version}Packages"
    // {
      grimp = import ./grimp {
        inherit lib python_pkgs;
      };
      types-deprecated = import ./deprecated/stubs.nix lib;
    };
in {
  inherit lib python_pkgs;
}
