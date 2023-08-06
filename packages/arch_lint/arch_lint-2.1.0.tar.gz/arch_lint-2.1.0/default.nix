{
  src,
  nixpkgs,
}: let
  supported = ["python38" "python39" "python310"];
  version = let
    file_str = builtins.readFile "${src}/arch_lint/__init__.py";
    match = builtins.match ".*__version__ *= *\"(.+?)\"\n.*" file_str;
  in
    builtins.elemAt match 0;
  metadata = (builtins.fromTOML (builtins.readFile ./pyproject.toml)).project // {inherit version;};
  publish = import ./build/publish {
    inherit nixpkgs;
  };

  build_for = python_version: let
    deps = import ./build/deps {
      inherit nixpkgs python_version;
    };
    self_pkgs = import ./build/pkg {
      inherit src metadata;
      lib = deps.lib;
      python_pkgs = deps.python_pkgs;
    };
    checks = import ./ci/check.nix {self_pkg = self_pkgs.pkg;};
  in {
    check = checks;
    env = self_pkgs.env;
    pkg = self_pkgs.pkg;
  };

  pkgs = builtins.listToAttrs (map
    (name: {
      inherit name;
      value = build_for name;
    })
    supported);
in
  pkgs
  // {
    inherit publish;
  }
